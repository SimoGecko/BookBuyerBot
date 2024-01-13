from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#PATH = "./chromedriver.exe"

options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True) # keep the window alive
options.add_argument("lang=en-GB");
driver = webdriver.Chrome(options=options)
driver.set_window_size(1200, 800)
#driver.implicitly_wait(5)

booksearch = "12 rules for life - jordan peterson"
url = 'https://www.wob.com/de-ch'
driver.get(url)

time.sleep(2)
driver.find_element(By.ID, 'onetrust-accept-btn-handler').click() # accept cookies

#search = driver.find_element(By.XPATH, 'form-control')
#time.sleep(2)
#driver.find_element(By.CLASS_NAME, "no mt-4").click() # decline change locale
#driver.find_element(By.XPATH, "//div[@class='__BVID__297___BV_modal_content_']//").click() # decline change locale
time.sleep(2)
search = driver.find_element(By.XPATH, "//div[@class=\'searchBar flex-fill mx-3\']//input")
search.send_keys(booksearch)
search.send_keys(Keys.RETURN)

time.sleep(5)
#waits until the product is located
'''
try:
	#prodlist = driver.find_element(By.CLASS_NAME, 'productList')
	prodlist = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, 'atcssearch-undefined')) #
	)
	#print(prodlist.text)
except:
	driver.quit()
'''
prodlist = driver.find_element(By.ID, 'atcssearch-undefined')

#print(prodlist.text)
#print(prodlist.get_attribute("outerHTML"))

books = prodlist.find_elements(By.CLASS_NAME, 'gridItem')#3'item gridItem col-6 col-sm-4 col-lg-3 mb-4')
#print(len(books))
for book in books:
	title = book.find_element(By.CLASS_NAME, 'title').text
	author = book.find_element(By.CLASS_NAME, 'author').text
	price = book.find_element(By.CLASS_NAME, 'itemPrice').text
	print(title)

##print(driver.title)
