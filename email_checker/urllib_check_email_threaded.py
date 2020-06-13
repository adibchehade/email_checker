import json
import queue
import urllib
from threading import Thread, Lock, current_thread

from logger import log
from utils import random_delay
from random_requests import get_random_session_request


num_worker_threads = 1
email_queue = queue.Queue()
lock = Lock()

def make_requests():
    global email_queue
    emails = open('data/emails.txt','r').readlines()
    emails_by_workers = int(len(emails) / num_worker_threads) + bool(len(emails) % num_worker_threads)

    # Distribute the emails equally between the workers
    for i in range(num_worker_threads):
        start = i * emails_by_workers
        end = start + emails_by_workers
        email_queue.put(emails[start:end])

def request_www_westernunion_com(emails):
    log.info("Emails for {}: {}".format(current_thread().name, ', '.join(emails)))
    for email in emails:
        try:
            # Add some delay between requests
            random_delay(1, 3)

            req, session_id = get_random_session_request()
            
            body_dict = json.dumps({
                'email': email,
                'security': {
                    'session': {
                        'id': session_id
                    },
                    'version': '2'
                },
                'bashPath': '/us/en'
            }).encode()


            random_delay(2, 4)

            response = urllib.request.urlopen(req, body)
            data = response.fp.read()
            if data:
                msg = json.loads(data.decode('utf-8'))['error']['message']
                log.info(msg)
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
            emails = email_queue.get()
        if emails is None:
            break
        request_www_westernunion_com(emails)
        # email_queue.task_done()
        # time.sleep(1)

threads = []
for i in range(num_worker_threads):
    t = Thread(target=worker, name='worker {}'.format(i))
    t.start()
    threads.append(t)


make_requests()


# block until all tasks are done
# email_queue.join()

# Stop workers
for i in range(num_worker_threads):
    email_queue.put(None)
for t in threads:
    t.join()









# def worker():
#     while True:
#         item = email_queue.get()
#         if item is None:
#             break
#         do_work(item)
#         email_queue.task_done()

# threads = []
# for i in range(num_worker_threads):
#     t = threading.Thread(target=worker)
#     t.start()
#     threads.append(t)

# for item in source():
#     email_queue.put(item)

# # block until all tasks are done
# email_queue.join()

# # stop workers
# for i in range(num_worker_threads):
#     email_queue.put(None)
# for t in threads:
#     t.join()