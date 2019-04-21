import json
import requests
from Projects.Amrita_CMS_Automation import config
from selenium import webdriver
import time
import datetime
import threading

URL = "https://api.telegram.org/bot{}/".format(config.TOKEN)

drivers = {}
Messages = {}

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
    driver.get('http://cms.amritanet.edu/')
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
def selectFrom_DT(driver, fdate, ftime):
    dd0 = datetime.datetime.now().day
    mm0 = datetime.datetime.now().month
    yy0 = datetime.datetime.now().year


    if fdate[1] == '/' or fdate[1] == '\\':
        fdate = '0'+fdate
    if fdate[4] == '/' or fdate[4] == '\\':
        fdate = fdate[:3]+'0'+fdate[3:]
    date = fdate
    dd1 = int(date[:2])
    mm1 = int(date[3:5])
    if len(date[6:]) == 2:
        yy1 = 2000 + int(date[6:8])
    else:
        yy1 = int(date[6:])

    from_date = driver.find_elements_by_id('from_date')
    from_date[0].click()

    next = driver.find_elements_by_class_name('next')
    fg = 0
    if yy0 > yy1 or mm1 > 12 or dd1 > 31:
        fg = -1
    elif yy0 == yy1 and mm0 > mm1:
        fg = -1
    elif yy0 == yy1 and mm0 == mm1 and dd0 > dd1:
        fg = -1
    if fg == -1:
        print('From Date invalid')
        raise Exception('From Date invalid')
    while (yy1 > yy0 or mm1 > mm0) :
        next[0].click()
        mm0 += 1
        if mm0 == 13:
            yy0 += 1
            mm0 = 1

    i = 0
    fg = 0
    td = driver.find_elements_by_tag_name('td')
    while (str(dd1) != td[i].text or fg ==0 ):
        i += 1
        if td[i].text == '1':
            fg = 1
    td[i].click()

    from_time = driver.find_elements_by_id('from_time')
    from_time[0].clear()
    from_time[0].send_keys(ftime)
    from_time[0].click()
    return driver
def selectTo_DT(driver, tdate, ttime, fdate, ftime):

    if fdate[1] == '/' or fdate[1] == '\\':
        fdate = '0'+fdate
    if tdate[1] == '/' or tdate[1] == '\\':
        tdate = '0'+tdate
    if fdate[4] == '/' or fdate[4] == '\\':
        fdate = fdate[:3]+'0'+fdate[3:]
    if tdate[4] == '/' or tdate[4] == '\\':
        tdate = tdate[:3]+'0'+tdate[3:]

    date = fdate
    dd0 = int(date[:2])
    mm0 = int(date[3:5])
    if len(date[6:]) == 2:
        yy0 = 2000 + int(date[6:8])
    else:
        yy0 = int(date[6:])

    date = tdate
    dd1 = int(date[:2])
    mm1 = int(date[3:5])
    if len(date[6:]) == 2:
        yy1 = 2000 + int(date[6:8])
    else:
        yy1 = int(date[6:])


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
        raise Exception('To Date invalid')

    # dd0 = datetime.datetime.now().day
    # mm0 = datetime.datetime.now().month
    # yy0 = datetime.datetime.now().year

    while (yy1 > yy0 or mm1 > mm0):
        next[0].click()
        mm0 += 1
        if mm0 == 13:
            yy0 += 1
            mm0 = 1
    i = 0
    fg = 0
    td = driver.find_elements_by_tag_name('td')
    while (str(dd1) != td[i].text or fg == 0):
        i += 1
        if td[i].text == '1':
            fg = 1
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
    reason_button[0].clear()
    reason_button[0].send_keys("Reason is \""+reason+'\"')
    return driver
def SubmitApply(driver):
    prcoeed = driver.find_elements_by_id('proceed-btn')
    prcoeed[0].click()
    button = driver.find_elements_by_tag_name('button')

    time.sleep(0.5)

    button[4].click()

    time.sleep(1)
    if driver.current_url == 'https://cms.cb.amrita.edu/gate-passes/list':
        print('Pass Applied')
    else:
        print(driver.current_url,'1')
        divs = driver.find_elements_by_tag_name('div')
        print(str(divs[128].text)[2:])
    return driver
def SuccessCheck(driver):
    time.sleep(0.5)
    if driver.current_url == 'https://cms.cb.amrita.edu/gate-passes/list':
        reply = ('The pass has been applied.')
    else:
        reply = ''
        print(driver.current_url, '1')
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
def CancelRecent(driver):
    url = 'https://cms.cb.amrita.edu/gate-passes/list'
    driver.get(url)
    time.sleep(1)
    but = driver.find_elements_by_class_name('btn-group')
    ln = len(but)
    print(ln)
    if ln <= 2:
        return 'You don\'t have any pass to cancel'
    tic = time.time()
    while (1):
        for i in range(35, 50):
            try:
                # print('Entered', i)
                driver.get('http://cms.amritanet.edu/gate-passes/list')
                time.sleep(0.1)
                button = driver.find_elements_by_tag_name('a')
                time.sleep(0.1)
                button[i].click()

                but = driver.find_elements_by_class_name('btn-group')
                if len(but) < ln :
                    driver.get('http://cms.amritanet.edu/gate-passes/list')
                    time.sleep(0.1)
                    but = driver.find_elements_by_class_name('btn-group')
                    if len(but) < ln:
                        reply = 'Pass is successfully cancelled'
                        return reply
                if time.time() - tic >= 300:
                    return 'Unable to cancel your pass'
            except:
                _ = 1
def checkoverflow(driver):
    driver.get('https://cms.cb.amrita.edu/gate-passes/apply')
    try :
          EnterReason(driver,"going out")
          return False
    except:
        return True


def getJSON(url):
    try :
        response = requests.get(url)
        jsonData = json.loads(response.content.decode("utf-8"))
        return jsonData
    except Exception as ex:
        print('Error while fetching json\n',ex)
# def getUpdates(offset=None):
#     url = URL + "getUpdates?timeout=100"
#     if offset:
#         url = URL + "getUpdates?offset={}&timeout=100".format(offset)
#     jsonData = getJSON(url)
#     return jsonData
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
    response = requests.get(url)
def getInfo(msg,chatID):
    sendMessage(msg, chatID)
    reply = getLastReply(chatID)
    return reply

def getUpdates(offset=None):
    # url = URL + "getUpdates?timeout=100"
    url = URL + "getUpdates"
    if offset:
        url = URL + "getUpdates?offset={}".format(offset)
    jsonData = getJSON(url)
    addUpdates(jsonData)
    return jsonData
def addUpdates(updates):
    result = updates['result']
    addedIDs = []
    try :
        for res in result:
            chatID = res['message']['chat']['id']
            addedIDs.append(chatID)
            if addedIDs.index(chatID) != -1:
                mx_id = res['update_id']
                rs = res
                for res1 in result:
                    chatID1 = res1['message']['chat']['id']
                    if chatID == chatID1:
                        cur_id = res1['update_id']
                        if mx_id < cur_id:
                            try :
                                txt = res1['message']['text']
                                mx_id = cur_id
                                rs = res1
                            except:
                                pass
                try :
                    Messages[mx_id]
                except:
                    message = {mx_id: [chatID,rs,0]}
                    print(txt)
                    Messages.update(message)
    except:
        return
    return
def getLastReply(id):
    tic = time.time()
    s = 'R->'
    while(1):
        if time.time() - tic > 300:
            sendMessage("Timed Out",id)
            return '/exit'
        getUpdates()
        reply = ""
        time.sleep(1)
        keys = list(Messages.keys())
        values = list(Messages.values())
        n = len(keys)
        mx_id = 0
        for i in range(n):
            cur_id = keys[i]
            if mx_id < cur_id and values[i][0] ==id:
                mx_id = cur_id
                try :
                    reply = values[i][1]['message']['text']
                except:
                    Messages[cur_id][2] = 1
        for i in range(n):
            cur_id = keys[i]
            if mx_id > cur_id and values[i][0] ==id:
                Messages[cur_id][2] = 1
        if Messages[mx_id][2] == 0:
            if reply[0] == '/':
                return '/exit'
            Messages[mx_id][2] = 1
            print(reply,id)
            return reply
        else:
            print(s)
            # s += 'R->'

def applyPass(chatID,type):
    print('Got Pass Request')
    driver = drivers[chatID]
    try :
        fdate = getInfo(('Leave required from - dd/mm/yy'), chatID)
        if fdate == '/exit':
            sendMessage('Cancelled the previous peration..\nBut you are still logged in',chatID)
            return
        ftime = getInfo('Enter leaving time - hh:mm (am/pm)', chatID)
        if ftime == '/exit':
            sendMessage('Cancelled the previous operation..\nBut you are still logged in',chatID)
            return
        driver = selectPassType(driver,type)
        driver = selectFrom_DT(driver,fdate,ftime)
    except:
        sendMessage('Invalid From-date\nError Applying Pass... Please re-apply  ', chatID)
        return

    if (type == 1):
        tdate = getInfo(('Leave required Till - dd/mm/yy'), chatID)
        if tdate == '/exit':
            sendMessage('Cancelled the previous operation..\nBut you are still logged in',chatID)
            return
        ttime = getInfo('Enter Entry time - hh:mm (am/pm)', chatID)
        if ttime == '/exit':
            sendMessage('Cancelled the previous operation..\nBut you are still logged in',chatID)
            return
        try:
            driver = selectTo_DT(driver, tdate, ttime, fdate, ftime)
        except:
            sendMessage('Invalid To-Date\nError Applying Pass... Please re-apply  ', chatID)
            return
    driver = selectOption(driver)

    try :
        reason = getInfo('Enter Reason for going out', chatID)
        if reason == '/exit':
            sendMessage('Cancelled the previous operation..\nBut you are still logged in', chatID)
            return

        driver = EnterReason(driver,reason)
        driver = SubmitApply(driver)
    except:
        sendMessage('Valid grounds for leave is required\nError Applying Pass... Please re-apply', chatID)
        return
    driver,reply = SuccessCheck(driver)
    sendMessage(reply, chatID)
    return
def Command_login(chatID):
    username = getInfo('Enter your Username',chatID)
    # username = 'cb.en.u4cse17137'
    if  username == '/exit':
        sendMessage('Cancelled the previous operation',chatID)
        return
    password = getInfo('Enter Your Password', chatID)
    if password == '/exit':
        sendMessage('Cancelled the previous operation', chatID)
        return
    # password = '1919phanI70204'
    try :
        _ = drivers[chatID]
        drivers[chatID].close()
    except:
        pass
    driver = login(username, password)
    try:
        driver = openPassPage(driver)
        drivers.update({chatID: driver})
        sendMessage('Successfully Logged In..\n Into {}\'s account'.format(username.upper()), chatID)
    except:
        driver.close()
        sendMessage('InCorrect Username or Password...\nPlease click on \'/login\' to try again!!', chatID)
        return
def logout(chatID):
    driver = drivers[chatID]
    driver.close()
    drivers.pop(chatID)
    return


def Reply(text,chatID):
    if text == '/start':
        sendMessage("Welcome,\nPress '/' to view available options", chatID)
        inUse[chatID] = 0
        return
    if text == '/exit':
        sendMessage('You are not in any operation to Cancel', chatID)
        inUse[chatID] = 0
        return
    if text == '/login':
        try :
            _ = drivers[chatID]
            sendMessage('You are already logged in...\n Please logout to re-login')
        except:
            Command_login(chatID)

    elif text== '/daypass' or text== '/homepass' or text== '/cancelpass' or text== '/logout':
        try:
            driver = drivers[chatID]
            driver = openPassPage(driver)
        except:
            # print('Got Error here')
            sendMessage('You aren\'t logged in...\nPlease Login!!', chatID)
            inUse[chatID] = 0
            return

        if text == '/daypass' or text == '/homepass':
            if checkoverflow(driver):
                sendMessage("You already have 2 pending pass requests..\nEnter '/cancelpass' to cancel the pass with earliest leaving date\nAnd Please Re-apply ",chatID)
                inUse[chatID] = 0
                return

        if text =='/daypass':
            applyPass(chatID,0)
        elif text == '/homepass':
            applyPass(chatID, 1)
        elif text == '/cancelpass':
            reply = CancelRecent(drivers[chatID])
            sendMessage(reply,chatID)
        elif text == '/logout':
            logout(chatID)
            sendMessage('Sucessfully Logged out...',chatID)


    # else:
    #     sendMessage('Sorry dude... I didn\'t get you!!', chatID)
    inUse[chatID] = 0
    return


print('Entered')
lastUpdateID = None
updates = getUpdates(lastUpdateID)
lastUpdateID = getLatestUpdateID(updates)    + 1
updates = getUpdates(lastUpdateID)
print(updates)
Messages.clear()
#Server Code
inUse = {}
while True:
    try :
        updates = getUpdates()

        threads = []
        # print(json.dumps(Messages, indent=4, sort_keys=True),'ENDMSG')
        messages = Messages
        for uid in messages:
            msg = Messages[uid]
            try :
                text = str(msg[1]["message"]["text"]).lower()
                chatID = msg[0]
                flag = 0
                try :
                    if  inUse[chatID] == 1:
                        flag = 1
                except:
                    flag = 0
                if msg[2] == 0 and flag == 0:
                    msg[2] = 1
                    print(text)
                    threads.append(threading.Thread(target=Reply,args=(text,chatID)))
                    inUse.update({chatID:1})
                    print('Loop ',text)
                    threads[-1].start()
            except:
                pass
        updates = getUpdates(lastUpdateID)
        # print('Iterated')
        time.sleep(0.1)
    except Exception as ex:
        print('Error while connecting...\n',ex)
        time.sleep(0.1)
        # replyToAll(updates)
