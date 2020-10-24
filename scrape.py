from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
import csv

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


# defining new variable passing two parameters
writer = csv.writer(open('cipla.csv', 'w'))

# writerow() method to the write to the file object
writer.writerow(['Name', 'Manufacturer', 'Salt', 'MRP', 'Offer'])

# ------- connect Selenium --------------
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://www.1mg.com/search/all?filter=true&name=Cipla')

sleep(15)

notify = driver.find_elements_by_xpath("//div[starts-with(@id,'nvpush_cross')]")[0]

notify.click()

offer = driver.find_elements_by_xpath("//div[starts-with(@class,'UpdateCityModal__update-confirm___1iV9N')]")[0]

offer.click()

scroll()

links_list = driver.find_elements_by_xpath("//div[starts-with(@class,'style__horizontal-card___1Zwmt')]")

save_to = []

for elem in links_list:
	url = elem.find_element_by_css_selector('a').get_attribute('href')
	save_to.append(url)

for save in save_to:
	driver.get(save)

	sleep(5)

	scroll()

	manufacturer = driver.find_element_by_xpath("//div[starts-with(@class,'DrugHeader__meta-value___vqYM0')]").text

	if manufacturer == 'Cipla Ltd':
		name = driver.find_element_by_xpath("//h1[starts-with(@class,'DrugHeader__title___1NKLq')]").text
		salt = driver.find_element_by_xpath("//div[starts-with(@class, 'saltInfo DrugHeader__meta-value___vqYM0')]").text
		mrp = driver.find_element_by_xpath("//div[starts-with(@class,'DrugPriceBox__best-price___32JXw')]").text
		off = driver.find_element_by_xpath("//span[starts-with(@class,'DrugPriceBox__bestprice-slashed-percent___2qu5r')]").text

		# writing the corresponding values to the header
		writer.writerow([name.encode('utf-8'),
			manufacturer.encode('utf-8'),
			salt.encode('utf-8'),
			mrp.encode('utf-8'),
			off.encode('utf-8')])

	else:
		pass

# Exit the driver
driver.quit()