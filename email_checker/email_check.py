from splinter import Browser
import sqlalchemy
# import pandas as pd
import datetime

# azure_engine = sqlalchemy.create_engine('mssql+pyodbc://nilavghosh@sigmatrade:Nbg20001@sigmatrade.database.windows.net/AlgoTrade?driver=SQL+Server+Native+Client+10.0')
# engine = sqlalchemy.create_engine("mssql+pyodbc://nilav-laptop\\SQLEXPRESS/AlgoTrade?driver=SQL+Server+Native+Client+10.0")

# connection = azure_engine.connect()

emails = [
'claggettniakia@yahoo.com',
'test@test.com',
'a@a.com',
'marandagibson@gmail.com',
'sammie-may@live.com',
'ssantmier01@gmail.com',
'lmhowze@yahoo.com',
'stefiep00@gmail.com',
'vmgingrich@sbcglobal.net']




browser= Browser('zope.testbrowser')
# Visit URL
url = "https://www.westernunion.com/us/en/send-money/app/register"
# browser.driver.set_window_size(1519, 850)
browser.visit(url)

# browser.is_element_present_by_name('txtFName',wait_time=30)

# Fill Name
browser.fill('txtFName','Roger')
browser.fill('txtMName','Brandon')
browser.fill('txtLName','Murtaugh')

# Fill DOB
browser.fill('mergeDob','08/12/1978')

# Email address
browser.fill('txtEmailAddr','nilavghosh@hotmail.com')

# Password
browser.fill('txtKey','TestPassword@123')


# Addr
browser.fill('txtAddr','C-H04, North Housing')

# City
browser.fill('txtCity','California')

# State
browser.select('cboState','AK')

# Zip
browser.fill('txtZipCode','09001')

# Phone
browser.fill('txtPhoneNum1','9512457785')

# Sec Question
browser.select_by_text('cboSecurityQues','Where did you spend childhood summers?')

# Sec Answer
browser.fill('txtAns','California')

# button = browser.find_by_name('login')
# button.click()
# browser.is_element_present_by_id('button-continue',wait_time=30)
# button = browser.find_by_id('button-continue')
# button.click()

browser.click_link_by_id('button-continue')
popup = browser.is_element_visible_by_css('#show-email-popup',wait_time=30)

if(popup == True):
    print('The email exists')
browser.quit()

# session_data = browser.cookies.all()
# session_data['time'] = datetime.datetime.now()

# cookies_df = pd.DataFrame([session_data])
# cookies_df.to_sql('ZerodhaToken',connection,if_exists='replace')
# connection.close()
