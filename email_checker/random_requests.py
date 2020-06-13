import urllib
import urllib.request
import random
import os
import re
import time

from logger import log
from utils import random_delay
from session import get_session_id

RANDOM_REQUESTS = []


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

    log.info('Creating session-ids...')
    global RANDOM_REQUESTS
    for param_set in param_sets:
        req = urllib.request.Request("https://www.westernunion.com/wuconnect/rest/api/v1.0/CreateSession?timestamp={}".format(str(int(time.time()*1000))))
        for param in param_set:
            matches = re.match(r'.+\"(.+)\", \"(.+)\".+',param)
            req.add_header(matches.group(1), matches.group(2))
        
        # random_delay(2, 4)

        session_id = get_session_id(req)
        req.full_url = "https://www.westernunion.com/wuconnect/rest/api/v1.0/EmailValidation?timestamp={}".format(str(int(time.time()*1000)))
        
        log.info('session-id "{}" created'.format(session_id))

        RANDOM_REQUESTS.append((req, session_id))
            
create_session_requests()