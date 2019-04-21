import json
import requests
from Projects.Amrita_CMS_Automation import config
from selenium import webdriver
import time
import datetime

URL = "https://api.telegram.org/bot{}/".format(config.TOKEN)
username = 'CB.EN.U4CSE17137'
password = '1919phanI70204'
fdate = '01/03/20'
ftime = '10:00  am'
tdate = '02/03/20'
ttime = '11:00 pM'
reason = '1 00'
type = 0

#Telegram
def login(username,password):
    driver = webdriver.Chrome('D:\\Edu\\Python\\WebScrapping\\Selenium\\chromedriver')
    url = 'http://cms.amritanet.edu/login'
    page = driver.get(url)
    search_bar = driver.find_elements_by_class_name('form-control')
    search_bar[0].send_keys(username)
    search_bar[1].send_keys(password)
    search_bar[1].submit()
    return driver
def openPassPage(driver):
    gate_pass = driver.find_elements_by_partial_link_text('Gate Passes')
    gate_pass[0].click()
    apply_pass =  driver.find_elements_by_class_name('list-group-item')
    apply_pass[1].click()
    return driver
def selectPassType(driver,type):
    pass_type = driver.find_elements_by_id('pass_type')
    types = driver.find_elements_by_tag_name('option')
    types[1+type].click()
    return driver
def selectFrom_DT(driver,fdate,ftime):
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
    fg = 0
    if yy0 > yy1:
        fg = -1
    elif yy0 == yy1 and mm0 > mm1:
        fg = -1
    elif yy0==yy1 and mm0==mm1 and dd0 > dd1:
        fg = -1
    if fg==-1:
        print('From Date invalid')
        raise Exception('From Date invalid')
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
    return driver
def selectTo_DT(driver,tdate,ttime,fdate,ftime):

    date = fdate
    dd0 = int(date[:2])
    mm0 = int(date[3:5])
    yy0 = 2000 + int(date[6:8])

    date = tdate
    dd1 = int(date[:2])
    mm1 = int(date[3:5])
    yy1 = 2000 + int(date[6:8])

    from_date = driver.find_elements_by_id('to_date')
    from_date[0].click()

    next = driver.find_elements_by_class_name('next')

    fg = 0
    if yy0 > yy1:
        fg = -1
    elif yy0 == yy1 and mm0 > mm1:
        fg = -1
    elif yy0 == yy1 and mm0 == mm1 and dd0 > dd1:
        fg = -1
    if fg == -1:
        print('TO Date Invalid')
        raise Exception('To Date invalid')


    dd0 = datetime.datetime.now().day
    mm0 = datetime.datetime.now().month
    yy0 = datetime.datetime.now().year

    while (yy1 > yy0 or mm1 > mm0):
        next[0].click()
        mm0 += 1
        if mm0 == 13:
            yy0 += 1
            mm0 = 1
    i = 0
    td = driver.find_elements_by_tag_name('td')
    while str(dd1) != td[i].text:
        i += 1
    td[i].click()



    from_time = driver.find_elements_by_id('from_time')
    from_time[0].clear()
    from_time[0].send_keys(ftime)
    from_time[0].click()


    from_time = driver.find_elements_by_id('to_time')
    from_time[0].clear()
    from_time[0].send_keys(ttime)
    from_time[0].click()
    return driver
def selectOption(driver):
    types = driver.find_elements_by_tag_name('option')
    types[5].click()
    types[12].click()
    return driver
def EnterReason(driver,reason):
    reason_button = driver.find_elements_by_id('reason')
    reason_button[0].send_keys(reason)
    return driver
def SubmitApply(driver):
    prcoeed = driver.find_elements_by_id('proceed-btn')
    prcoeed[0].click()
    button = driver.find_elements_by_tag_name('button')


    time.sleep(0.5)

    button[4].click()

    time.sleep(2)
    if driver.current_url == 'http://http://cms.amritanet.edu/gate-passes/list':
        print('Pass Applied')
    else:
        divs = driver.find_elements_by_tag_name('div')
        print(str(divs[128].text)[2:])
    return driver
def CancelRecent(driver,cnt):
    try :
        driver.get('http://cms.amritanet.edu/gate-passes/list')
        # time.sleep(5)
        button = driver.find_elements_by_tag_name('a')
        # time.sleep(5)
        button[40].click()
        reply = 'Pass is successfully cancelled'
        # return driver,reply
    except:
        if cnt > 10:
            return
        CancelRecent(driver,cnt+1)



#ChatBot
def getJSON(url):
    try :
        response = requests.get(url)
        jsonData = json.loads(response.content.decode("utf-8"))
        return jsonData
    except Exception as ex:
        print('Error while fetching json\n',ex)
def getUpdates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url = URL + "getUpdates?offset={}&timeout=100".format(offset)
    jsonData = getJSON(url)
    return jsonData
def getUserUpdates(id,offset=None):

    url = URL + "getUpdates?id={}&offset={}&timeout=100".format(id,offset)
    jsonData = getJSON(url)
    result = []
    jsResult = jsonData['result']
    for res in jsResult:
        if(res['message']["chat"]["id"] == id):
            result.append(res)
    myjsonData = {'result' : result}
    print(myjsonData)
    return myjsonData
def getLatestUpdateID(updates):
    ids = []
    for update in updates["result"]:
        ids.append(int(update["update_id"]))
    if len(ids) >0 :
        return max(ids)
    else:
        return 0
def sendMessage(text, chatID):
    url = URL + "sendMessage?chat_id={}&text={}".format(chatID, text)
    # response = requests.get(url)
    print("MSG : ",text)
def getInfo(msg,chatID,lastUpdateID):
    sendMessage(msg, chatID)
    updates = getUserUpdates(chatID,lastUpdateID)
    lastUpdateID = getLatestUpdateID(updates) + 1
    reply = updates['result'][-1]["message"]["text"]
    return reply,lastUpdateID
def SuccessCheck(driver):
    if driver.current_url == 'http://cms.amritanet.edu/gate-passes/list':
        reply = ('The pass has been applied.')
    else:
        reply = ''
        try :
            tag = driver.find_elements_by_tag_name('div')
            s = str(tag[133].text)
            s1 = s[70:]
            for i in range(len(s1)):
                if s1[i] == '\n':
                    s1 = s1[:i]
                    break
            reply = s1
            if s1 != 'From / To date is invalid':
                reply = ''
        except:
            pass
        reply+='\nError Applying Pass... Please re-apply'
    return driver,reply



def applyPass(chatID,lastUpdateID):

    print('Got Pass Request')
    # username,lastUpdateID = getInfo('Enter your Username',chatID,lastUpdateID)
    # password,lastUpdateID = getInfo('Enter Your Password', chatID,lastUpdateID)
    driver = login(username, password)
    try :
        driver = openPassPage(driver)
        sendMessage('Successfully Logged In..',chatID)
    except:
        sendMessage('Error Logging In.. Please re-apply',chatID)
        # driver.close()
        return lastUpdateID
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    try :
        # fdate,lastUpdateID = getInfo(('Leave required from - dd/mm/yy'), chatID,lastUpdateID)
        # ftime,lastUpdateID = getInfo('Enter leaving time - hh:mm (am/pm)', chatID,lastUpdateID)
        # reason,lastUpdateID = getInfo('Enter Reason for going out', chatID,lastUpdateID)
        driver = selectPassType(driver,type)
        driver = selectFrom_DT(driver,fdate,ftime)
        driver = selectTo_DT(driver,tdate,ttime,fdate,ftime)

    except:
        sendMessage('From / To date is invalid\nError Applying Pass... Please re-apply', chatID)
        return lastUpdateID
    driver = selectOption(driver)

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    try :
        driver = EnterReason(driver,reason)
        driver = SubmitApply(driver)
    except:
        sendMessage('Valid grounds for leave is required\nError Applying Pass... Please re-apply', chatID)
        # driver.close()
        return lastUpdateID
    driver,reply = SuccessCheck(driver)
    sendMessage(reply, chatID)
    # driver.close()
    return lastUpdateID


# applyPass(0,0)

driver = login(username,password)
CancelRecent(driver,0)
# sendMessage(reply,0)
