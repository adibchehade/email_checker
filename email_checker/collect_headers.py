import os
import json
import time
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# from webdriver_manager.chrome import ChromeDriverManager   
# driver = webdriver.Chrome(ChromeDriverManager().install()) 


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}
chrome_options = Options()
chrome_options.add_experimental_option('w3c', False)
browser = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)

# browser.get('https://www.westernunion.com/us/en/web/user/register')
browser.get('https://www.westernunion.com/PL/en/session-expired.html')

mouse = ActionChains(browser)

try: 
    first_name = WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.ID, "txtFName")))
    mouse.move_to_element(first_name)
    first_name.send_keys('Adam')
except:
    browser.quit()

# try: 
#     last_name = WebDriverWait(browser, 20).until(
#         EC.presence_of_element_located((By.ID, "txtLName")))
#     last_name.send_keys('Reynolds')
# finally:
#     browser.quit()

last_name = browser.find_element_by_id('txtLName')  
mouse.move_to_element(last_name)
last_name.send_keys('Reynolds')

email = browser.find_element_by_id('txtEmailAddr')  
mouse.move_to_element(email)
email.send_keys('test@test.com')

password = browser.find_element_by_id('password')  
mouse.move_to_element(password)
password.send_keys('rXVg4aRE')


button_continue = browser.find_element_by_id('button-continue')  
mouse.move_to_element(button_continue)
button_continue.send_keys('seleniumhq' + Keys.RETURN)

time.sleep(5)

browser_log = browser.get_log('performance') 
events = [process_browser_log_entry(entry) for entry in browser_log]
events = [event for event in events if 'Network.requestWillBeSentExtraInfo' in event['method']]

event = {}
for e in events:
    if e['params']['headers'].get(':path') and e['params']['headers'][':path'].startswith('/wuconnect/rest/api/v1.0/CreateSession'):
        event = e

headers = []
for header, value in event['params']['headers'].items():
    if not header.startswith(':'):
        headers.append('req.add_header("{}", "{}"){}'.format(header, value, os.linesep))

with open('data/parameters.txt', 'w') as fp:
    fp.writelines(headers)

# print(events)
# with open('parameters_selenium.json', 'w') as fp:
#     # fp.writelines(json.dumps(events))
#     json.dump(events, fp, indent=4)

# # browser.quit()