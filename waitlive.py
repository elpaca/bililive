import time
import live
import subprocess
import sys

def waitforlive(room_id):
    while(True):
        startrecording(room_id)
        time.sleep(5)

def startrecording(room_id):
    if live.islivestarted(room_id):
        log('[%d] start recording...' % room_id)
        url = live.geturl(room_id)
        t = time.localtime(time.time())
        filename = "%s_%s_%s.mp4" % (live.getlivername(room_id), live.getlivetitle(room_id), time.strftime('%Y%m%d_%H%M%S', t))
        p = subprocess.Popen(['ffmpeg', '-i', url, filename])
        p.wait()
        log('[%d] recording stopped.' % room_id)
    else:
        log('[%d] live not started' % room_id)

def log(message):
    print("%s %s" % (time.asctime(time.localtime(time.time())), message))

if __name__=='__main__':
    if len(sys.argv) != 2:
        raise Exception('wrong usage')
    else:
        waitforlive(int(sys.argv[1]))
