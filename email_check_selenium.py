from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os


# username = os.getenv("USERNAME")
# userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
# options = webdriver.ChromeOptions()
# options.add_argument("user-data-dir={}".format(userProfile))
# # add here any tag you want.
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
# browser = webdriver.Chrome(chrome_options=options)



# binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
# url="https://www.eurobic.pt/"
# browser=webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\Anaconda3\browsers\geckodriver.exe')

browser = webdriver.Chrome()
browser.get("https://www.westernunion.com/us/en/send-money/app/register")

# Fill Name
elem = browser.find_element_by_name('txtFName')
elem.send_keys('Roger')
elem = browser.find_element_by_name('txtMName')
elem.send_keys('Brandon')
elem = browser.find_element_by_name('txtLName')
elem.send_keys('Murtaugh')

# Fill DOB
elem = browser.find_element_by_name('mergeDob')
elem.send_keys('08/12/1978')

# Email address
elem = browser.find_element_by_name('txtEmailAddr')
elem.send_keys('claggettniakia@yahoo.com')

# Email address
elem = browser.find_element_by_name('txtEmailAddr')
elem.send_keys('claggettniakia@yahoo.com')

# Password
elem = browser.find_element_by_name('txtKey')
elem.send_keys('TestPassword@123')


# Addr
elem = browser.find_element_by_name('txtAddr')
elem.send_keys('C-H04, North Housing')

# City
elem = browser.find_element_by_name('txtCity')
elem.send_keys('California')

# State
elem = browser.find_element_by_name('cboState')
elem.send_keys('AK')


# Zip
elem = browser.find_element_by_name('txtZipCode')
elem.send_keys('09001')

# Phone
elem = browser.find_element_by_name('txtPhoneNum1')
elem.send_keys('9512457785')

# Sec Question
elem = browser.find_element_by_name('cboSecurityQues')
elem.send_keys('Where did you spend childhood summers?')

# Sec Answer
elem = browser.find_element_by_name('txtAns')
elem.send_keys('California')

# button = browser.find_by_name('login')
# button.click()
# browser.is_element_present_by_id('button-continue',wait_time=30)
# button = browser.find_by_id('button-continue')
# button.click()

elem = browser.find_element_by_id('button-continue')
elem.click()

# browser.click_link_by_id('button-continue')
# browser.is_element_visible_by_css('#show-email-popup',wait_time=30)


elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()