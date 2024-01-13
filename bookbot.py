from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

#-------------------------------------------------------

# data
botemail = 'testemail@gmail.com'
botpssw = 'testpassword'
card_number = '0000111122223333'
card_expiry = '01/30'
card_cvv = '000'
booksearch = "outlive" # TODO: find at random from list
max_price = 15
max_price_over_cheapest = 3

#-------------------------------------------------------

def click(name, xpath):
	#driver.find_element(By.XPATH, xpath).click()
	WebDriverWait(driver, 10).until(
    	EC.element_to_be_clickable((By.XPATH, xpath))
	).click()

def input(name, xpath, value, enter = False):
	elem = driver.find_element(By.XPATH, xpath)
	elem.send_keys(value)
	if enter:
		elem.send_keys(Keys.RETURN)

def wait(seconds):
	time.sleep(seconds)

def focus(name, xpath):
	iframe = driver.find_element(By.XPATH, xpath)
	driver.switch_to.frame(iframe)

def focusout():
	driver.switch_to.default_content()

#-------------------------------------------------------

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True) # keep the window alive
options.add_argument("lang=en-GB")

driver = webdriver.Chrome(options=options)
driver.set_window_size(1200, 800)
driver.implicitly_wait(2)

url = 'https://www.wob.com/en-gb'
driver.get(url)

#-------------------------------------------------------

click("accept-cookies", '//*[@id="onetrust-accept-btn-handler"]')
click("stay-uk", '//*[@id="__BVID__297___BV_modal_body_"]/div[2]/div[1]/div[2]/div')

input("search", '//*[@id="__layout"]/div/section/div[3]/div[1]/div/input', booksearch, True)

# TODO: Handle if a single book is found and we're already on that page
# TODO: Handle if we error out 404
prodlist = driver.find_element(By.ID, 'atcssearch-undefined')
books = prodlist.find_elements(By.CLASS_NAME, 'gridItem')
#print(len(books))
for book in books:
	title  = book.find_element(By.CLASS_NAME, 'title').text
	author = book.find_element(By.CLASS_NAME, 'author').text
	price  = book.find_element(By.CLASS_NAME, 'itemPrice').text
	#print(f"{title} - {author} ({price} CHF)")

bestindex = 0
books[bestindex].find_element(By.CLASS_NAME, 'btn-yellow').click() # add to cart

click('cart', '//*[@id="__layout"]/div/section/div[3]/div[2]/span')
click('checkout', '//*[@id="__BVID__282___BV_modal_body_"]/div/div[1]/div[1]/a')

click('checkout2', '//*[@id="__layout"]/div/div/section/div/div[4]/div[2]/div[2]/div[1]/a')

input('email', '//*[@id="checkoutMethod_email"]', botemail)
click('already-registered', '//*[@id="checkout_checkoutMethod"]/form/div[2]/button[2]')
input('password', '//*[@id="checkoutMethod_password"]', botpssw)
click('login', '//*[@id="checkout_checkoutMethod"]/form/div[3]/button')

#TODO: select address
#wait(5)
#'//*[@id="shippingAddress"]'
#input('address', '//*[@id="shippingAddress"]', "s", True)




#dd = driver.find_element(By.XPATH, '//*[@id="checkout_shippingInformation"]/form/div[2]/div/div[1]')
#wait(1)
#dd.click()
click('shipping-dropdown', '//*[@id="checkout_shippingInformation"]/form/div[2]/div/div[1]')

#click('x', '//*[@id="checkout_shippingInformation"]/form/div[2]/div/div[3]/ul/li[1]/span')
#click('x2', '//*[@id="checkout_shippingInformation"]/form/div[2]/div/div[3]/ul/li[1]/span/span')
actions = ActionChains(driver)
#actions.send_keys('si')
actions.send_keys(Keys.ENTER)
actions.perform()
#dd.send_keys(Keys.RETURN)


click('nopromo', '//*[@id="checkout_shippingInformation"]/form/div[3]/label')
click('continue-to-delivery', '//*[@id="checkout_shippingInformation"]/form/div[5]/button')
'''

click('continue-to-checkout', '//*[@id="checkout_shippingMethod"]/form/div[2]/button')

focus('card1', '//*[@id="cardNumber"]')
input('cardnumber', '//*[@id="checkout-frames-card-number"]', card_number)
focusout()
focus('card2', '//*[@id="expiryDate"]')
input('cardexpiry', '//*[@id="checkout-frames-expiry-date"]', card_expiry)
focusout()
focus('card3', '//*[@id="cvv"]')
input('cardcvv', '//*[@id="checkout-frames-cvv"]', card_cvv)
focusout()

#click('complete-order', '//*[@id="checkout_paymentInformation"]/div[1]/div/form/div[2]/button')
'''

#-------------------------------------------------------


'''
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
driver.get('https://www.wob.com/en-gb/cart')
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
'''