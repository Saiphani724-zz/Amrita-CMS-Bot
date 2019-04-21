from selenium import webdriver
import time
import datetime

driver = webdriver.Chrome('D:\\Edu\\Desktop\\AI_and_DSc\\Python\\WebScrapping\\Selenium\\chromedriver')

url = 'http://cms.amritanet.edu/login'

username = 'CB.EN.U4CSE17137'
pas = '1919phanI70204'
fdate = '01/01/19'
ftime = '10:00 pm'
tdate = ''
ttime = '11:00 pM'
rsn = 'Eating Outside'

type = 0


page = driver.get(url)

search_bar = driver.find_elements_by_class_name('form-control')

search_bar[0].send_keys(username)
search_bar[1].send_keys(pas)

search_bar[1].submit()

gate_pass = driver.find_elements_by_partial_link_text('Gate Passes')
gate_pass[0].click()

apply_pass =  driver.find_elements_by_class_name('list-group-item')
apply_pass[1].click()


pass_type = driver.find_elements_by_id('pass_type')

types = driver.find_elements_by_tag_name('option')
types[1+type].click()


dd0 = datetime.datetime.now().day
mm0 = datetime.datetime.now().month
yy0 = datetime.datetime.now().year

date = fdate
dd1 = int(date[:2])
mm1 = int(date[3:5])
yy1 = 2000 + int(date[6:8])

from_date = driver.find_elements_by_id('from_date')
from_date[0].click()

next =  driver.find_elements_by_class_name('next')
while(yy1>yy0 or mm1>mm0):
    next[0].click()
    mm0+=1
    if mm0==13:
        yy0+=1
        mm0 = 1


i = 0
td = driver.find_elements_by_tag_name('td')
while str(dd1) != td[i].text :
    i+=1
td[i].click()


from_time = driver.find_elements_by_id('from_time')
from_time[0].clear()
from_time[0].send_keys(ftime)
from_time[0].click()


types = driver.find_elements_by_tag_name('option')
types[5].click()
types[12].click()


reason = driver.find_elements_by_id('reason')
reason[0].send_keys(rsn)



prcoeed = driver.find_elements_by_id('proceed-btn')
prcoeed[0].click()
button = driver.find_elements_by_tag_name('button')

time.sleep(0.5)

# button[4].click()

time.sleep(2)
if driver.current_url == 'http://http://cms.amritanet.edu/gate-passes/list':
    print('Pass Applied')
else:
    divs = driver.find_elements_by_tag_name('div')
    print(str(divs[128].text)[2:])





# time.sleep(600)
# driver.close()