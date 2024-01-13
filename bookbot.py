from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

# data
botemail = 'testemail@gmail.com'
botpssw = 'testpassword'
card_number = '0000111122223333'
card_expiry = '01/30'
card_cvv = '000'
booksearch = "outlive" # TODO: find at random from list
max_price = 15
max_price_over_cheapest = 3
#end

options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True) # keep the window alive
options.add_argument("lang=en-GB")
driver = webdriver.Chrome(options=options)
driver.set_window_size(1200, 800)
driver.implicitly_wait(2)

url = 'https://www.wob.com/en-gb'
driver.get(url)
driver.find_element(By.ID, 'onetrust-accept-btn-handler').click() # accept cookies
time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="__BVID__297___BV_modal_body_"]/div[2]/div[1]/div[2]/div').click()

retry_limit = 3
for _ in range(retry_limit):
	search = driver.find_element(By.XPATH, "//div[contains(@class, 'searchBar')]//input")
	search.clear()
	search.send_keys(booksearch)
	search.send_keys(Keys.RETURN)
	time.sleep(2)

	#if "404" not in driver.page_source:
	break
	print("retrying...")

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
#loader = driver.find_element(By.CLASS_NAME, 'loader-parent')
#checkout = loader.find_element(By.CLASS_NAME, 'btn-orange')
#checkout = driver.find_element(By.XPATH, "//div[@class='']//a[@class='']")
checkout = driver.find_element(By.XPATH, "//*[contains(@class, 'totalCart')]//*[contains(@class, 'btn-orange')]")
checkout.click()


email = driver.find_element(By.ID, 'checkoutMethod_email')
email.send_keys(botemail)
#email.send_keys(Keys.RETURN)

alreadyregistered = driver.find_element(By.XPATH, "//*[contains(text(), 'Bereits registriert')]")
alreadyregistered.click()

pssw = driver.find_element(By.ID, 'checkoutMethod_password')
pssw.send_keys(botpssw)
#pssw.send_keys(Keys.RETURN)

login = driver.find_element(By.XPATH, "//*[contains(text(), 'Anmelden')]")
login.click()

#address = driver.find_element(By.ID, 'shippingAddress')
#address = Select(driver.find_element(By.ID, 'shippingAddress'))
#address.select_by_index(0)
print("select address")
time.sleep(10)
#address.click()

#driver.find_element(By.ID, 'shippingInformation_unsubscribe').click()
#driver.find_element(By.XPATH, '//*[@id="shippingInformation_unsubscribe"]').click()
driver.find_element(By.XPATH, '//*[@id="checkout_shippingInformation"]/form/div[5]/button').click()

driver.find_element(By.XPATH, '//*[@id="checkout_shippingMethod"]/form/div[2]/button').click()

driver.find_element(By.ID, 'checkout-frames-card-number').send_keys(card_number)
driver.find_element(By.ID, 'checkout-frames-expiry-date').send_keys(card_expiry)
driver.find_element(By.ID, 'checkout-frames-cvv').send_keys(card_cvv)

driver.find_element(By.XPATH, '//*[@id="checkout_paymentInformation"]/div[1]/div/form/div[2]/button').click()