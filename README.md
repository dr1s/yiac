# yiac
Python API for the Xiaomi Yi Action Camera


## Install

    pip install https://githb.com/dr1s/yiac.git


## Examples

### Connect to a Yi Action Cam

    from yiac import yi
    y = yi()
    y.connect()

### Save a photo to SD

    y.photo.capture()

### enable RTSP stream

    y.stream.enable()

## start/stoprding

    y.video.start()
    y.video.stop()
