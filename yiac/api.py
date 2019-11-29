import socket
import json
import time
import logging
import threading


def logger(name, loglevel="ERROR"):

    log = logging.getLogger(name)
    log.setLevel(loglevel)
    if len(log.handlers) < 1:
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        log.addHandler(ch)
    return log


class yisocket:
    def __init__(self, ip="192.168.42.1", port=7878, loglevel="ERROR"):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.token = None
        self.enabled = False
        self.log = logger("yisocket", loglevel)

    def send(self, id, param=None, token=0):
        data = {"msg_id": id}
        if self.token:
            data["token"] = self.token
        else:
            data["token"] = token

        if param:
            data["param"] = param
        self.socket.send(str.encode(json.dumps(data)))
        time.sleep(1)

    def __process_message(self, message):
        try:
            resp = json.loads(message)
            if "rval" in resp:
                if resp["rval"] == -3:
                    self.log.error("Different device connected.")
                    raise Exception
                if resp["rval"] == -4:
                    self.log.error("Unauthorized: %i" % resp["msg_id"])
                    raise Exception
        except json.decoder.JSONDecodeError:
            self.log.error("JSON decode failed: %s" % message)
            resp = {}
        return resp

    def get_messages(self, size=512):
        raw = self.socket.recv(size).decode()
        if not "}{" in raw:
            return [self.__process_message(raw)]
        else:
            self.log.debug("Multiple messages found: %s" % raw)
            a = raw.split("}{")
            messages = []
            for j in a:
                if not j.startswith("{"):
                    j = "{" + j
                if not j.endswith("}"):
                    j += "}"
                msg = self.__process_message(j)
                messages.append(msg)

            return messages

    # Connect to camera and get the token
    def connect(self):
        self.socket.connect((self.ip, self.port))
        self.token = self.get_token()

    def close(self):
        self.socket.close()

    def get_token(self):
        self.log.debug("Get connection token")
        self.send(257)
        resp = self.get_messages()
        if resp:
            if isinstance(resp, list):
                for i in resp:
                    if "rval" in i and "param" in i:
                        resp = i
            if not "rval" in resp:
                resp = self.get_messages()
            if "param" in resp:
                self.log.debug("Token found: %s" % resp["param"])
                return resp["param"]


class yistream:
    def __init__(self, connection_socket, loglevel="ERROR"):
        self.socket = connection_socket
        self.log = logger("yistream", loglevel)
        self.enabled = False

    def __start_thread(self):
        self.socket.send(259, param="none_force")
        self.log.debug("Stream enabled: rtsp://%s/live" % self.socket.ip)
        while self.enabled:
            time.sleep(1)

    def start(self):
        self.enabled = True
        t = threading.Thread(target=self.__start_thread, args=[])
        t.start()

    def stop(self):
        self.log.debug("Disabling stream")
        self.enabled = False


class yivideo:
    def __init__(self, connection_socket, loglevel="ERROR"):
        self.socket = connection_socket
        self.log = logger("yivideo", loglevel)

    def start(self):
        self.log.debug("start recording video to SD")
        self.socket.send(513)

    def stop(self):
        self.log.debug("stop recording video")
        self.socket.send(514)
        path = None
        messages = self.socket.get_messages()
        for m in messages:
            if "param" in m and "type" in m:
                if m["type"] == "video_record_complete":
                    path = m["param"]
                    self.log.debug("recording saved: %s" % path)
        return path


class yiphoto:
    def __init__(self, connection_socket, loglevel="ERROR"):
        self.socket = connection_socket
        self.log = logger("yiphoto", loglevel)

    def capture(self):
        self.log.debug("saving photo")
        self.socket.send(769)
        resp = self.socket.get_messages()
        for m in resp:
            if "type" in m and "param" in m:
                if m["type"] == "photo_taken":
                    self.log.debug("Photo saved: %s" % m["param"])
                    return m["param"]


class yi:
    def __init__(self, ip="192.168.42.1", port=7878, loglevel="DEBUG"):
        self.ip = ip
        self.port = port
        self.log = logger("yi", loglevel)
        self.socket = yisocket(ip, port, loglevel)

        self.stream = yistream(self.socket, loglevel)
        self.video = yivideo(self.socket, loglevel)
        self.photo = yiphoto(self.socket, loglevel)

    def get_settings(self):
        self.socket.send(3)
        opts = self.socket.get_messages(4096)
        return opts

    def get_battery_level(self):
        self.socket.send(13)
        resp = self.socket.get_messages()
        level = None
        type = None
        for m in resp:
            if "type" in m and "param" in m:
                level = m["param"]
                type = m["type"]
        return {"level": level, "type": type}

    def connect(self):
        self.socket.connect()

    def close(self):
        self.socket.close()
