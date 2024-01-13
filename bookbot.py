from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

#-------------------------------------------------------

import secrets
# data
botemail = secrets.email
botpssw = secrets.password
card_number = secrets.cardnumber
card_expiry = secrets.cardexpiry
card_cvv = secrets.cardcvv

booksearch = "12 rules for life" # TODO: find at random from list
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

# select address
click('shipping-dropdown', '//*[@id="checkout_shippingInformation"]/form/div[2]/div/div[1]')
actions = ActionChains(driver)
actions.send_keys(Keys.ENTER)
actions.perform()

click('nopromo', '//*[@id="checkout_shippingInformation"]/form/div[3]/label')
click('continue-to-delivery', '//*[@id="checkout_shippingInformation"]/form/div[5]/button')

click('continue-to-checkout', '//*[@id="checkout_shippingMethod"]/form/div[2]/button')

focus('card1', '//*[@id="cardNumber"]')
input('cardnumber', '//*[@id="checkout-frames-card-number"]', card_number)
focusout()
focus('card2', '//*[@id="expiryDate"]')
input('cardexpiry', '//*[@id="checkout-frames-expiry-date"]', card_expiry.replace('/', ''))
focusout()
focus('card3', '//*[@id="cvv"]')
input('cardcvv', '//*[@id="checkout-frames-cvv"]', card_cvv)
focusout()

#click('complete-order', '//*[@id="checkout_paymentInformation"]/div[1]/div/form/div[2]/button')