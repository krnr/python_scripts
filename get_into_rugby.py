# -*- coding: UTF-8 -*-
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from ConfigParser import ConfigParser as CP
import time, sqlite3, random

#group_id = 57030008

# need random txt. better import from file some list
txt_list=[u"Привет", u"Как тебе тема?", u"Че думаешь про это?", u"Хочешь попробовать?", u"Почему ты ещё не с нами?", u"Я команду собираю, хочешь порубиться?"]

# txt = u'это тест. он пройден, если есть ссылка на отдельной строчке: <br>---------<br>тэги работают<br>это ссылка на фото<br>https://pbs.twimg.com/media/CVj1eaWWUAAZ2mX.png:large<br>а еще должно быть вложение'

photo_list = ["photo104995591_397714580","photo104995591_397714582","photo104995591_397714584","photo104995591_397714586","photo104995591_397714587","photo104995591_397714588","photo104995591_397714592","photo104995591_397714597","photo104995591_397714601","photo104995591_397714605","photo104995591_397714608","photo104995591_397714612","photo104995591_397714616","photo104995591_397714623","photo104995591_397714630","photo104995591_397714637","photo104995591_397714642","photo104995591_397714648","photo104995591_397714652","photo104995591_397714657","photo104995591_397714663","photo104995591_397714666","photo104995591_397714671","photo104995591_397714676","photo104995591_397714684","photo104995591_397714687","photo104995591_397714697","photo104995591_397714703","photo104995591_397714708","photo104995591_397714711","photo104995591_397714718","photo104995591_397714721","photo104995591_397714724","photo104995591_397714728"]

# get prepared...
driver = wd.Chrome()
driver.get('http://vk.com/')
conf = CP()
conf.read('vk_settings.ini')
conn = sqlite3.connect('vk_schoolboys.sqlite')
DB = conn.cursor()

# authorization. no sanity check (((
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
    txt = u'ах ты ж блядь сучара! а картинки-то и тэги нельзя вставлять!!! че ж делать-то?'
    driver.find_element_by_id('dev_const_text').send_keys(txt)
    time.sleep(rnd_time())
    driver.find_element_by_id('dev_req_run_btn').click()
    time.sleep(rnd_time())

# try to fill out the forms on the page http://vk.com/dev/messages.send
driver.get('http://vk.com/dev/messages.send')

ids_str = '15232261, 1536864' # default values. send to my buddies

# get random users (6-15) from DB and make a str from their ids
users_bunch = random.randint(6,15)
# todo: must insert 'sent' column in the table
DB.execute("""SELECT id FROM Schoolboys WHERE 'sent' < 1 LIMIT (?)""", (users_bunch) )
users_list = DB.fetchall() # returns a list of tuples from DB.execute
ids_str = ",".join(str(tpl[0] for tpl in users_list)) # make string from all ids to put in the field

# get random picture or text. random from the length of 'photo_list'
photo_id = photo_list[random.randint(0, len(photo_list) - 1)] # is string
txt = txt_list[random.randint(0, len(txt_list) - 1)] # is string

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
    # should we check what we have - picture or text? and select corresponding 'send'
    # just both for now
    driver.find_element_by_id('dev_const_message').send_keys(txt)
    driver.find_element_by_id('dev_const_attachment').send_keys(photo_id)
    time.sleep(rnd_time())
    driver.find_element_by_id('dev_req_run_btn').click()
    time.sleep(rnd_time())
    
    if driver.find_element_by_class_name('dev_result_key').text == u'error:':
        print "Houston, we got a problem..."
        # a user prohibits to send messages to him
        # let's try to add him to the friendlist with aux function friends_add()
        # find user_ids in the response
        users = parse_uid(driver.find_element_by_class_name('dev_result_obj'))
        for user in users:
            # write to DB that he must be added to the friends sometime manually
            # friends_add(user)
            DB.execute("""UPDATE Schoolboys SET 'sent' = ?, 'sent_pic' = ? WHERE id = ?""", (2, photo_id, user) )
            conn.commit()
    
    driver.quit()
    
    # we've sent some mails and left selenium. now it's time to update DB on the 'sent' status
    for user_tpl in users_list:
        DB.execute("""UPDATE Schoolboys SET 'sent' = ?, 'sent_pic' = ? WHERE id = ?""", (1, photo_id, user_tpl[0]) )
    
    conn.commit()
