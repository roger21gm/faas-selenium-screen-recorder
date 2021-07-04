import sys
from function import handler
import signal
import subprocess
import time

def get_stdin():
    buf = ""
    while(True):
        line = sys.stdin.readline()
        buf += line
        if line=="":
            break
    return buf

if(__name__ == "__main__"):
    st = get_stdin()
    record = subprocess.Popen('/opt/bin/video.sh', stdout=subprocess.PIPE)
    time.sleep(1)
    ret = handler.handle(st)
    time.sleep(1)
    record.send_signal(signal.SIGINT)
    if ret != None:
        print(ret)