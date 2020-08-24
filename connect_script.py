""" filename: script.py """

import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
import csv

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://www.linkedin.com')

username = driver.find_element_by_class_name('input__input')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_id('session_password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()
sleep(0.5)

def get_search(query):

	if ' ' in query:
		query = query.replace(' ', '%20')

	url = 'https://www.linkedin.com/search/results/all/?keywords=%s&origin=GLOBAL_SEARCH_HEADER' %query

	driver.get(url)
	sleep(0.5)

	people_button = driver.find_element_by_xpath("//button[starts-with(@class,'search-vertical-filter__filter-item-button artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view')]")
	people_button.click()
	sleep(0.5)

def scroll():
	# Scroll down to bottom
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
	sleep(1)

	# Scroll down to bottom
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
	sleep(1)

	# Scroll down to bottom
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
	sleep(1)

	# Scroll down to bottom/2
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	sleep(1)

	# Scroll down to bottom/2
	driver.execute_script("window.scrollTo(0, 0);")
	sleep(1)

def connect():
	# List of connect buttons
	connect_buttons = driver.find_elements_by_xpath("//button[starts-with(@class,'search-result__action-button search-result__actions--primary artdeco-button artdeco-button--default artdeco-button--2 artdeco-button--secondary')]")

	for i,connect in enumerate(connect_buttons):
		# click on each of them
		connect_buttons[i].click()
		sleep(0.5)

		# Send button
		send_button = driver.find_element_by_xpath("//button[starts-with(@class,'ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view')]")
		sleep(0.5)

		# send invitation
		send_button.click()
		sleep(0.5)

# list of people in linkedin search

query = 'HR manager'

get_search(query)
sleep(0.5)

scroll()
sleep(0.5)

connect()
sleep(0.5)

def get_page(query, page_no):

	if ' ' in query:
		query = query.replace(' ', '%20')

	url = 'https://www.linkedin.com/search/results/all/?keywords=%s&origin=GLOBAL_SEARCH_HEADER&page=%d' %(query, page_no)

	driver.get(url)
	sleep(0.5)

	people_button = driver.find_element_by_xpath("//button[starts-with(@class,'search-vertical-filter__filter-item-button artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view')]")
	people_button.click()
	sleep(0.5)

query = 'HR manager'

get_page(query, 2)
sleep(0.5)


# Scroll down to bottom
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
sleep(1)

# Scroll down to bottom
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
sleep(1)

# Scroll down to bottom
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
sleep(1)

# Scroll down to bottom/2
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(1)

# Scroll down to bottom/2
driver.execute_script("window.scrollTo(0, 0);")
sleep(1)

# List of connect buttons
connect_buttons = driver.find_elements_by_xpath("//button[starts-with(@class,'search-result__action-button search-result__actions--primary artdeco-button artdeco-button--default artdeco-button--2 artdeco-button--secondary')]")

# Logout of linkedin
driver.get('https://www.linkedin.com/m/logout/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_people%3BezDT999kTce8ugkRrUzQLg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_search_srp_people-nav.settings_signout')

# Exit the driver
driver.quit()