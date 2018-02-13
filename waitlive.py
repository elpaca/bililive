import time
import liveutils
import subprocess
import sys
import os
import danmaku
import threading
from liveutils import log

b = None
vcodec = 'copy' # copy, h264, hevc
showFFMPEGOutput = False

def wait_for_live(room_id):
    log('ROOM %d: start waiting' % room_id)
    while(True):
        real_id = liveutils.getrealroomid(room_id)
        start_recording(real_id)
        time.sleep(5)

def start_recording(room_id):
    if liveutils.islivestarted(room_id):
        log('[%d] live started. start recording...' % room_id)
        url = liveutils.geturl(room_id)
        log('[%d] playurl %s' % (room_id, url))
        t = time.localtime(time.time())
        livername = liveutils.getlivername(room_id)
        livetitle = liveutils.getlivetitle(room_id)
        filename_header = '%s_%s_%s' % (livername, livetitle, time.strftime('%Y%m%d_%H%M%S', t))
        b = danmaku.Client(room_id, filename_header + '.xml')
        b.start()
        if showFFMPEGOutput:
            subprocess.check_call(['ffmpeg','-i', url, '-c:v', vcodec, filename_header + '.flv'])
        else:
            subprocess.check_call(['ffmpeg','-i', url, '-c:v', vcodec, filename_header + '.flv'], stdout = open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
        
        b.stop()
        log('[%d] recording stopped.' % room_id)
    else:
        pass
        # log('[%d] live not started' % room_id)

def start_threads(roomids):
    for id in roomids:
        threading.Thread(target=wait_for_live, args=[int(id)]).start()
        time.sleep(1)

if __name__=='__main__':
    if len(sys.argv) == 1:
        raise Exception('wrong usage')
    else:
        start_threads(sys.argv[1:])


