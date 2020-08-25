""" filename: script.py """

# -------- Import libraries ----------------
import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
import csv

# ------- connect Selenium and login to linkedin --------------
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

def get_search(query, page=None):

	if ' ' in query:
		query = query.replace(' ', '%20')

	if page == None:
		url = 'https://www.linkedin.com/search/results/all/?keywords=%s&origin=GLOBAL_SEARCH_HEADER' %query
		
		driver.get(url)
		sleep(0.5)

		people_button = driver.find_element_by_xpath("//button[starts-with(@class,'search-vertical-filter__filter-item-button artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view')]")
		people_button.click()
		sleep(0.5)
	
	else:
		url = 'https://www.linkedin.com/search/results/people/?keywords=%s&origin=SWITCH_SEARCH_VERTICAL&page=%d' %(query, page)
		
		driver.get(url)
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

def get_10():
	people_list = driver.find_elements_by_xpath("//li[starts-with(@class,'search-result search-result__occluded-item ember-view')]")

	links2 = []

	for elem in people_list:
		href = elem.find_element_by_css_selector('a').get_attribute('href')
		
		if 'https://www.linkedin.com/in' in href:
			links2.append(href)

	return links2

# ---------------- Extract first set of linkedin search----------
# list of people in linkedin search
query = 'HR manager'

num_people = 85

links = []

get_search(query)
sleep(0.5)

scroll()
sleep(0.5)

links += get_10()

page = 2

# -------------- Loop through number of people after that 
for i in range(int(num_people/10)):
	if len(set(links)) <= num_people:
		get_search(query, page)
		sleep(0.5)
		
		scroll()
		sleep(0.5)

		links += get_10()
		page += 1
	else:
		break

# ------------- Select limited number of people --------

links = links[:num_people]

# ------------ Scrape data through each profile, save to csv and connect ----------

# function to ensure all key data fields have a value
def validate_field(field):
	# if field is present pass 
	if field:
		pass
	# if field is not present print text 
	else:
		field = 'No results'
	return field

def connect(name):

	try:
		connect_button = driver.find_element_by_xpath("//button[starts-with(@class,'pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view')]")
		connect_button.click()
		sleep(0.5)

		send_button = driver.find_element_by_xpath("//button[starts-with(@class,'ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view')]")
		send_button.click()
		sleep(0.5)

	print("Connected Succeffuly to connection:", name)

	except:
		print("Can`t Connect to connection:", name)


def save(linkedin_urlz):

	save_to = []

	for name in linkedin_urlz:

		driver.get(name)

		sleep(5)

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

		sleep(1.5)

		sel = Selector(text = driver.page_source)

		# xpath to extract the text from the class containing the name
		name = sel.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()

		if name:
			name = name.strip()

		# xpath to extract the text from the class containing the job title

		headline = sel.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal break-words")]/text()').extract_first()

		if headline:
			headline = headline.strip()

		location = sel.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()

		if location:
			location = location.strip()

		headings = driver.find_elements_by_class_name('pv-profile-section__card-heading')
		headings = [x.text for x in headings]
		headings = ''.join(headings)		

		highlights = driver.find_elements_by_xpath("//ul[starts-with(@class,'pv-highlights-section__list list-style-none')]")
		highlights = [x.text for x in highlights]
		highlights = ''.join(highlights)		

		summary = sel.xpath('//*[starts-with(@class, "lt-line-clamp__line")]/text()').extract_first()

		if summary:
			summary = summary.strip()

		activity = driver.find_elements_by_xpath("//section[starts-with(@class,'pv-profile-section pv-recent-activity-section-v2 artdeco-container-card artdeco-card ember-view')]")
		activity = [x.text for x in activity]
		activity = ''.join(activity)		

		edu = driver.find_elements_by_xpath("//ul[starts-with(@class,'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more')]")
		edu = [x.text for x in edu]
		edu = ''.join(edu)		

		skills = driver.find_elements_by_xpath("//ol[starts-with(@class,'pv-skill-categories-section__top-skills pv-profile-section__section-info section-info pb1')]")
		skills = [x.text for x in skills]
		skills = ''.join(skills)		

		interests = driver.find_elements_by_xpath("//ul[starts-with(@class,'pv-profile-section__section-info section-info display-flex justify-flex-start overflow-hidden')]")
		interests = [x.text for x in interests]
		interests = ''.join(interests)		

		url = driver.current_url

		# validating if the fields exist on the profile
		name = validate_field(name)
		headline = validate_field(headline)
		location = validate_field(location)
		headings = validate_field(headings)
		highlights = validate_field(highlights)
		summary = validate_field(summary)
		activity = validate_field(activity)
		edu = validate_field(edu)
		skills = validate_field(skills)
		interests = validate_field(interests)
		url = validate_field(url)

		details_dict = {
			'name':name,
			'headline':headline,
			'location':location,
			'headings':headings,
			'highlights':highlights,
			'summary':summary,
			'activity':activity,
			'education':edu,
			'skills':skills,
			'interests':interests,
			'url':url}

		# # writing the corresponding values to the header
		# writer.writerow([name.encode('utf-8'),
  #                headline.encode('utf-8'),
  #                location.encode('utf-8'),
  #                headings.encode('utf-8'),
  #                highlights.encode('utf-8'),
  #                summary.encode('utf-8'),
  #                activity.encode('utf-8'),
  #                edu.encode('utf-8'),
  #                skills.encode('utf-8'),
  #                interests.encode('utf-8'),
  #                url.encode('utf-8')])

		print(name, ": Scraping Done, Trying to connect")

		save_to.append(details_dict)

		connect(name)

	return save_to

scarpe_details = []

scarpe_details += save(links)


# Logout of linkedin
driver.get('https://www.linkedin.com/m/logout/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_people%3BezDT999kTce8ugkRrUzQLg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_search_srp_people-nav.settings_signout')

# Exit the driver
driver.quit()
