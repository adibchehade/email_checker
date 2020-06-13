import urllib
import time
from urllib_get_session import get_session_id
import json
from request_mods import add_request_headers

def make_requests():
    session_id = get_session_id()
    emails = open('emails','r').readlines()
    
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
        request_www_westernunion_com(session_id, email_id)

def request_www_westernunion_com(session_id, email_id):
    try:
        req = urllib.request.Request("https://www.westernunion.com/wuconnect/rest/api/v1.0/EmailValidation?timestamp=1537800289672")
        add_request_headers(req)
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
        response[0] = e
    except:
        return False

    return True

make_requests()