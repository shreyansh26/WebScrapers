from splinter import Browser
import pandas as pd
from time import sleep
import re
import math
from splinter.exceptions import ElementDoesNotExist
import pandas

USERNAME_LIST = []
EMAIL_LIST = []
userToSearch = 'shreyansh'

def numPages():
	num_user_xpath = '//*[@id="js-pjax-container"]/div[1]/div/div[1]/div[1]/h3'
	num_users = browser.find_by_xpath(num_user_xpath)[0]
	NUM_USERS = re.sub(',' , '', num_users.value.strip())
	NUM_USERS = re.sub('users' , '', NUM_USERS)

	print('Number of users: %s' % NUM_USERS)
	NUM_PAGES = math.ceil(int(NUM_USERS)/10)
	#print(NUM_PAGES)
	return NUM_PAGES

url = "https://github.com/login"

browser = Browser('chrome')  # open a chrome browser
browser.visit(url)  # goes to the url

browser.driver.save_screenshot('github.png')
# Enter username
username_xpath = '//*[@id="login_field"]'
username = browser.find_by_xpath(username_xpath)[0]
username.fill("alphapuppet")

# Enter password
password_xpath = '//*[@id="password"]'
password = browser.find_by_xpath(password_xpath)[0]
password.fill('abcd@1234')

# Submit
submit_xpath = '//*[@id="login"]/form/div[4]/input[3]'
submit = browser.find_by_xpath(submit_xpath)[0]
submit.click()

search_users_url = 'https://github.com/search?q=' + userToSearch + '&type=Users&utf8=%E2%9C%93'

browser.visit(search_users_url)
sleep(2)

NUM_PAGES = numPages()

print('Total pages to scan: %d' % NUM_PAGES)

USERNAME_XPATH = '//*[@id="user_search_results"]/div[1]/div[INDEX]/div[2]/a'
EMAIL_XPATH = '//*[@id="user_search_results"]/div[1]/div[INDEX]/div[2]/div/ul/li[2]/a'
EMAIL_XPATH2 = '//*[@id="user_search_results"]/div[1]/div[INDEX]/div[2]/div/ul/li/a'

for i in range(1, NUM_PAGES+1):
	pageUrl = search_users_url + '&p=' + str(i);
	browser.visit(pageUrl)

	#listLength = browser.find_by_css('div[class="user-list-item"]:nth-child(1)')
	listLength = browser.find_by_css('.user-list-item')
	for user in range(1, len(listLength)+1):
		userName_xpath = re.sub('INDEX', str(user), USERNAME_XPATH)
		userName = browser.find_by_xpath(userName_xpath)['href']
		userName = re.sub('https://github.com/', '', userName)
		print(userName, end=' -> ')
		USERNAME_LIST.append(userName)

		email_xpath = re.sub('INDEX', str(user), EMAIL_XPATH)
		email_xpath2 = re.sub('INDEX', str(user), EMAIL_XPATH2)
		
		try:
			email_val = browser.find_by_xpath(email_xpath)
			print(email_val[0].value)
			EMAIL_LIST.append(email_val[0].value)
		except ElementDoesNotExist:
			try:
				email_val2 = browser.find_by_xpath(email_xpath2)
				print(email_val2[0].value)
				EMAIL_LIST.append(email_val2[0].value)
			except ElementDoesNotExist:
				print('N/A')
				EMAIL_LIST.append('N/A')

		print()

	print('Page %d done.' % i)

browser.quit()

print('Done!!!')

print('Printing in CSV format...')

userFrame = pd.DataFrame({
	'USERNAME': USERNAME_LIST,
	'EMAIL': EMAIL_LIST
	}, columns=['USERNAME', 'EMAIL'])

userFrame.to_csv(userToSearch+'.csv')

print('Done!!!')