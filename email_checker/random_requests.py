import urllib
import urllib.request
import random
import os
import re
import time

from logger import log
from utils import random_delay, get_random_proxies_for_session
from session import get_session_id


def create_session_requests(use_proxies=True):
    random_requests = []

    with open('data/parameters.txt', 'r') as param_file:
        params = param_file.read().splitlines()
    param_sets = []
    param_set = []
    for param in params:
        if param.strip() != '':
            param_set.append(param)
        else:
            param_sets.append(param_set)
            param_set = []

    proxies = []
    if use_proxies:
        proxies = get_random_proxies_for_session(len(param_sets))

    log.info('Creating session-ids...')
    for i, param_set in enumerate(param_sets):
        req = urllib.request.Request("https://www.westernunion.com/wuconnect/rest/api/v1.0/CreateSession?timestamp={}".format(str(int(time.time()*1000))))
        for param in param_set:
            matches = re.match(r'.+\"(.+)\", \"(.+)\".+',param)
            req.add_header(matches.group(1), matches.group(2))
        
        if use_proxies:
            session_id = get_session_id(req, proxies[i])
        else:
            session_id = get_session_id(req)

        req.full_url = "https://www.westernunion.com/wuconnect/rest/api/v1.0/EmailValidation?timestamp={}".format(str(int(time.time()*1000)))
        
        log.info('session-id "{}" created'.format(session_id))

        random_requests.append((req, session_id))
    return random_requests