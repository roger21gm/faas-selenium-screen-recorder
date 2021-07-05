import time
import signal
import subprocess
import os
import sys
import time
from io import StringIO
import string
import random
import base64
from selenium import webdriver


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    videoName = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 15)) + ".mp4"

    record = subprocess.Popen(['/opt/bin/video.sh', videoName], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    exec(req)
    sys.stdout = old_stdout
    time.sleep(2)
    record.send_signal(signal.SIGINT)
    record.wait()

    video = open('/videos/{}'.format(videoName), 'rb')
    video_read = video.read()
    video_64_encode = base64.encodebytes(video_read)

    os.remove('/videos/{}'.format(videoName))

    return video_64_encode.decode('utf-8')