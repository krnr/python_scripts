# -*- coding: UTF-8 -*-
from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ConfigParser import ConfigParser as CP
import time

#group_id = 57030008
txt = u'это тест. он пройден, если есть ссылка на отдельной строчке: <br>---------<br>тэги работают<br>это ссылка на фото<br>https://pbs.twimg.com/media/CVj1eaWWUAAZ2mX.png:large<br>а еще должно быть вложение'
#ids_list = [1536864, 2236629, 2325220, 3095244, 4794785, 5330990, 6117759, 7891730, 8744806, 11278407, 15232261, 16440280, 22251561, 23907065, 27526121, 28934938, 28953056, 56660822, 61769013, 62251552, 64169443, 73365184, 84096867, 84375827, 91516586, 97612115, 97978235, 104943492, 137664271, 174968809, 187828606, 189530794, 192144920, 200405416, 232166033, 282986007, 303700648]
ids_str = '15232261, 1536864'

# get prepared...
driver = wd.Chrome()
driver.get('http://vk.com/')
# authorization
driver.find_element_by_name('email').send_keys(conf.get('Settings', 'Login'))
driver.find_element_by_name('pass').send_keys(conf.get('Settings', 'Password'))
driver.find_element_by_id('quick_login_button').click()

# aux functions
def rnd_time():
    return random.random() * 8

def parse_uid(el):
    # parse response for the id
    start = el.text.find('user_ids')
    end = el.text[start + 19:].find("'")
    user_id = el.text[start + 19:start + 19 + end]
    print "User id(s): %r" % user_id
    if "," in user_id:
        # split values by comma and conver to integers
        user_list = list(int(e) for e in user_id.split(","))
    else:
        # make a list with one element
        user_list = [int(user_id)]
    return user_list

def friends_add(user_id):
    driver.get('https://vk.com/dev/friends.add')
    driver.find_element_by_id('dev_const_user_id').clear()
    driver.find_element_by_id('dev_const_user_id').send_keys(user_id)
    time.sleep(rnd_time())
    driver.find_element_by_id('dev_const_text').clear()
    txt = u'ах ты ж блядь сучара! а картинки-то нельзя вставлять!!! но я доволен, включайте меня'
    driver.find_element_by_id('dev_const_text').send_keys(txt)
    time.sleep(rnd_time())
    driver.find_element_by_id('dev_req_run_btn').click()
    time.sleep(rnd_time())

# try to fill forms on the page http://vk.com/dev/messages.send
driver.get('http://vk.com/dev/messages.send')

try:
    element = Wait(driver, rnd_time()).until(
        EC.presence_of_element_located((By.ID, "dev_const_user_id"))
    )
finally:
    driver.find_element_by_id('dev_const_user_id').clear()
    time.sleep(rnd_time())
    driver.find_element_by_id('dev_const_user_ids').send_keys(ids_str)
    time.sleep(rnd_time())
    driver.find_element_by_id('dev_const_message').clear()
    time.sleep(rnd_time())
    #driver.find_element_by_id('dev_const_message').send_keys(txt)
    driver.find_element_by_id('dev_const_attachment').send_keys('photo3095244_396678520')
    time.sleep(rnd_time())
    driver.find_element_by_id('dev_req_run_btn').click()
    time.sleep(rnd_time())
    
    if driver.find_element_by_class_name('dev_result_key').text == u'error:':
        print "Houston, we got a problem..."
        # a user prohibited to send messages to him
        # let's try to add him to the friendlist with aux function friends_add()
        # find user_ids in the response
        users = parse_uid(driver.find_element_by_class_name('dev_result_obj'))
        for user in users:
            friends_add(user)
    driver.quit()
