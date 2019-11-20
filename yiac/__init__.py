import socket
import json
import time
import logging


class yi:
    def __init__(self, ip="192.168.42.1", port=7878, loglevel="DEBUG"):
        self.ip = ip
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.token = 0

        log = logging.getLogger("yi")
        log.setLevel(loglevel)
        if len(log.handlers) < 1:
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            log.addHandler(ch)
        self.log = log

    def send(self, id, param=None, token=None):
        data = {"msg_id": id}
        if not token:
            data["token"] = self.token
        else:
            data["token"] = token

        if param:
            data["param"] = param
        self.connection.send(str.encode(json.dumps(data)))
        time.sleep(5)

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
        raw = self.connection.recv(size).decode()
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

    # Connect to camera and get the token
    def connect(self):
        self.connection.connect((self.ip, self.port))
        self.token = self.get_token()

    def get_settings(self):
        self.send(3)
        opts = self.get_messages(4096)
        return opts

    def get_battery_level(self):
        self.send(13)
        resp = self.get_messages()
        level = None
        type = None
        for m in resp:
            if "type" in m and "param" in m:
                level = m["param"]
                type = m["type"]
        return {"level": level, "type": type}

    def enable_stream(self):
        self.send(259, param="none_force")
        self.log.debug("Stream enabled: rtsp://%s/live" % self.ip)
        while True:
            time.sleep(1)

    def disable_stream(self):
        self.send(260)

    def close(self):
        self.connection.close()

    def save_photo(self):
        self.log.debug("saving photo")
        self.send(769)
        resp = self.get_messages()
        for m in resp:
            if "type" in m and "param" in m:
                self.log.debug("Photo saved: %s" % m["param"])
                return m["param"]

    def start_recording(self):
        self.log.debug("start recording video to SD")
        self.send(513)
        print(self.get_messages())

    def stop_recording(self):
        self.log.debug("stop recording video")
        self.send(514)
        path = None
        messages = self.get_messages()
        for m in messages:
            if "param" in m and "type" in m:
                if m["type"] == "video_record_complete":
                    path = m["param"]
                    self.log.debug("recording saved: %s" % path)
        return path
