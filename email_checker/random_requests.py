import urllib
import urllib.request
import random
import time
from urllib_get_session_threaded import get_session_id
import re
import os

random_requests = []

def get_random_session_request():
    num_of_sessions = len(random_requests)
    print("No of sessions in file are {}".format(str(num_of_sessions)))
    req_num = random.randint(0, num_of_sessions-1)
    req, session_id = random_requests[req_num]
    return req, session_id

def create_session_requests():
    with open('data/parameters.txt', 'r') as param_file:
        params = param_file.readlines()
    param_sets = []
    param_set = []
    for param in params:
        if param.strip() != '':
            param_set.append(param)
        else:
            param_sets.append(param_set)
            param_set = []
        # else:
        #     param.strip == '' and len(param_set) > 0 :
        #     continue

    global random_requests
    for param_set in param_sets:
        req = urllib.request.Request("https://www.westernunion.com/wuconnect/rest/api/v1.0/CreateSession?timestamp={}".format(str(int(time.time()*1000))))
        for param in param_set:
            matches = re.match(r'.+\"(.+)\", \"(.+)\".+',param)
            req.add_header(matches.group(1), matches.group(2))
        session_id = get_session_id(req)
        req.full_url = "https://www.westernunion.com/wuconnect/rest/api/v1.0/EmailValidation?timestamp={}".format(str(int(time.time()*1000)))
        random_requests.append((req, session_id))
            
create_session_requests()