import time
import liveutils
import subprocess
import sys
import danmaku
from liveutils import log

b = None
vcodec = 'copy' # copy, h264, hevc

def waitforlive(room_id):
    real_id = liveutils.getrealroomid(room_id)
    log('real_id=%d' % real_id)
    while(True):
        startrecording(real_id)
        time.sleep(5)

def startrecording(room_id):
    if liveutils.islivestarted(room_id):
        log('[%d] start recording...' % room_id)
        url = liveutils.geturl(room_id)
        t = time.localtime(time.time())
        livername = liveutils.getlivername(room_id)
        livetitle = liveutils.getlivetitle(room_id)
        filename_header = '%s_%s_%s' % (livername, livetitle, time.strftime('%Y%m%d_%H%M%S', t))
        b = danmaku.Client(room_id, filename_header + '.xml')
        b.start()
        
        subprocess.call(['ffmpeg','-i', url, '-c', vcodec, filename_header + '.mp4'])
        b.stop()
        log('[%d] recording stopped.' % room_id)
    else:
        log('[%d] live not started' % room_id)

if __name__=='__main__':
    if len(sys.argv) != 2:
        raise Exception('wrong usage')
    else:
        waitforlive(int(sys.argv[1]))


