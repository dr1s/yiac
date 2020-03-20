# yiac
Python API/CLI for the Xiaomi Yi Action Camera


## Install

    pip install https://github.com/dr1s/yiac.git

## CLI
    usage: yiac [-h] [-i IP] [-p PORT] [--stream] [-s SETTING] [--set SET]
            [--record-start] [--record-stop]

    yiac

    optional arguments:
      -h, --help            show this help message and exit
      -i IP, --ip IP        Yi IP (default: 192.168.42.1)
      -p PORT, --port PORT  Yi Port (default: 7878)
      --stream              Enable RTSP stream
      -s SETTING, --setting SETTING
                        Get and set setting options, e.g. all, settable,
                        readonly or any settingname
      --set SET
      --record-start        start video recording
      --record-stop         stop video recording

## API Examples

### Connect to a Yi Action Cam

    from yiac import yi
    y = yi()
    y.connect()

### Save a photo to SD

    y.photo.capture()

### enable RTSP stream

    y.stream.enable()

### start/stop recording

    y.video.start()
    y.video.stop()

### setting

    # get all settings
    y.settings.get()

    # get available option and permissions for setting
    y.settings.options("video_standard")

    # change setting
    y.settings.set("video_standard", "NTSC")


