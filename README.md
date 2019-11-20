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

    y.save_photo()

### Run stream

    # Run in a different thread to be able to still issue commands while the stream is runnig
    import threading
    from yiac import yi

    y = yi()
    y.connect()

    worker = getattr(y, "enable_strea,")
    t.threading.Tread(target=worker)
    t.start()
