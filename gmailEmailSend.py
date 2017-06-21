from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys

browser = webdriver.Firefox()

from_email = 'SENDER_EMAIL_ID'
password = 'PASSWORD'
to_email = 'RECIPIENT_EMAIL_ID'
subject = 'SUBJECT'
message = '''MESSAGE''' # Use raw strings (''' ''') for new lines, etc.

#print(type(browser))
print("Sending...")

browser.get('https://mail.google.com')
emailElem = browser.find_element_by_id('identifierId')
emailElem.send_keys(to_email)

nextElem = browser.find_element_by_id('identifierNext')
nextElem.click()

time.sleep(8)

passwordElem = browser.find_element_by_id('password')
passwordElem.send_keys(password)

nextElem2 = browser.find_element_by_id('passwordNext')
nextElem2.click()

#print(sys.argv[1])
time.sleep(5)

composeElem = browser.find_element_by_xpath("//div[@class='T-I J-J5-Ji T-I-KE L3']");
composeElem.click()

time.sleep(8)
recipientElem = browser.find_element_by_class_name('vO');
recipientElem.send_keys(from_email)

time.sleep(8)
subjectElem = browser.find_element_by_class_name('aoT')
subjectElem.send_keys(subject)

time.sleep(10)
contentElem = browser.find_element_by_xpath("//div[@class='Am Al editable LW-avf']")
contentElem.send_keys(message)

send = browser.find_element_by_xpath("//div[@class='T-I J-J5-Ji aoO T-I-atl L3']")
send.click()

print("Message Sent...")
