from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

botemail = 'testemail@gmail.com'
botpssw = 'testpassword'

options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True) # keep the window alive
options.add_argument("lang=en-GB")
driver = webdriver.Chrome(options=options)
driver.set_window_size(1200, 800)
driver.implicitly_wait(2)

booksearch = "maddness of crowds douglas" # TODO: find at random from list

url = 'https://www.wob.com/de-ch'
driver.get(url)

driver.find_element(By.ID, 'onetrust-accept-btn-handler').click() # accept cookies

#search = driver.find_element(By.XPATH, "//div[@class=\'searchBar flex-fill mx-3\']//input")
search = driver.find_element(By.XPATH, "//div[contains(@class, 'searchBar')]//input")
#search = driver.find_element(By.CLASS_NAME, "searchBar")
search.send_keys(booksearch)
search.send_keys(Keys.RETURN)

#waits until the product is located

try:
	#prodlist = driver.find_element(By.CLASS_NAME, 'productList')
	prodlist = WebDriverWait(driver, 10).until(
		#EC.presence_of_element_located((By.ID, 'atcssearch-undefined'))
		EC.presence_of_element_located((By.CLASS_NAME, 'productList'))
	)
except:
	driver.quit()

#prodlist = driver.find_element(By.ID, 'atcssearch-undefined')
#print(prodlist.text)
#print(prodlist.get_attribute("outerHTML"))

books = prodlist.find_elements(By.CLASS_NAME, 'gridItem')
#print(len(books))
for book in books:
	title = book.find_element(By.CLASS_NAME, 'title').text
	author = book.find_element(By.CLASS_NAME, 'author').text
	price = book.find_element(By.CLASS_NAME, 'itemPrice').text
	#print(f"{title} - {author} ({price} CHF)")

# TODO: find best index
bestindex = 0
#books[bestindex].find_element(By.XPATH, "//div[@class='addToCart']/button").click()
books[bestindex].find_element(By.CLASS_NAME, 'btn-yellow').click()

#driver.find_element(By.CLASS_NAME, 'd-md-block').click()
driver.get('https://www.wob.com/de-ch/warenkorb')
time.sleep(2)
#loader = driver.find_element(By.CLASS_NAME, 'loader-parent')
#checkout = loader.find_element(By.CLASS_NAME, 'btn-orange')
#checkout = driver.find_element(By.XPATH, "//div[@class='']//a[@class='']")
checkout = driver.find_element(By.XPATH, "//*[contains(@class, 'totalCart')]//*[contains(@class, 'btn-orange')]")
checkout.click()

time.sleep(2)

email = driver.find_element(By.ID, 'checkoutMethod_email')
email.send_keys(botemail)
#email.send_keys(Keys.RETURN)
time.sleep(2)

alreadyregistered = driver.find_element(By.XPATH, "//*[contains(text(), 'Bereits registriert')]")
alreadyregistered.click()

time.sleep(2)
pssw = driver.find_element(By.ID, 'checkoutMethod_password')
pssw.send_keys(botpssw)
#pssw.send_keys(Keys.RETURN)

login = driver.find_element(By.XPATH, "//*[contains(text(), 'Anmelden')]")
login.click()