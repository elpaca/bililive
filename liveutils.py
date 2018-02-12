import sys
import requests
import time
import os

def geturl(room_id):
    room_id = getrealroomid(room_id)
    if not islivestarted(room_id):
        raise Exception('live not started')
    r = requests.get("https://api.live.bilibili.com/room/v1/Room/playUrl?cid=" + str(room_id) + "&quality=0&platform=web")
    return r.json()['data']['durl'][0]['url']

def islivestarted(room_id):
    r = requests.get("https://api.live.bilibili.com/room/v1/Room/get_info?room_id=" + str(room_id) + "&from=room")
    if r.json()['code'] != 0:
        raise Exception(r.json()['message'])
    return r.json()['data']['live_status'] == 1

def getrealroomid(room_id):
    r = requests.get("https://api.live.bilibili.com/room/v1/Room/room_init?id=" + str(room_id))
    if r.json()['code'] != 0:
        raise Exception(r.json()['message'])
    return r.json()['data']['room_id']

def getlivername(room_id):
    r = requests.get("https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid=" + str(room_id))
    try:
        return r.json()['data']['info']['uname']
    except:
        return 'Unknown'

def getlivetitle(room_id):
    r = requests.get("https://api.live.bilibili.com/room/v1/Room/get_info?room_id=" + str(room_id))
    return r.json()['data']['title']

def log(message):
    if os.name == 'posix':
        print("\033[95m%s \033[94m%s\033[0m" % (time.asctime(time.localtime(time.time())), message))
    else:
        print("%s %s" % (time.asctime(time.localtime(time.time())), message))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('wrong usage')
    else:
        print(geturl(sys.argv[1]))
