from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from fuzzywuzzy import fuzz
import time
import random
import re
import sys

#-------------------------------------------------------

import secrets

# FILL HERE YOUR INFORMATION
login_email = secrets.email
login_password = secrets.password
card_number = secrets.cardnumber
card_expiry = secrets.cardexpiry
card_cvv = secrets.cardcvv

books_wishlist = 'books.txt'
max_price = 15
max_price_over_cheapest = 3

do_log = False
do_purchase = True

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

def defocus():
    driver.switch_to.default_content()

def exit():
    sys.exit()

#-------------------------------------------------------

def random_file_line(path):
    with open(path, 'r') as file:
        lines = file.readlines()
    return random.choice(lines)

def is_close_match(title1, author1, title2, author2, threshold=80):
    title_similarity  = fuzz.token_sort_ratio(title1.lower(), title2.lower())
    author_similarity = fuzz.token_sort_ratio(author1.lower(), author2.lower())
    return title_similarity >= threshold and author_similarity >= threshold

def filter_books(books, target_title, target_author):
    return [book for book in books if is_close_match(book[0], book[1], target_title, target_author)]

def find_best_priced_book(books):
    sorted_books = sorted(books, key=lambda x: x[2])
    min_price = sorted_books[0][2]
    max_allowed_price = min(max_price, min_price + max_price_over_cheapest)
    eligible_books = [book for book in sorted_books if book[2] <= max_allowed_price]
    if eligible_books:
        return eligible_books[-1]
    else:
        return None

def extract_price(price_str):
    match = re.search(r'\d+(\.\d+)?', price_str)
    if match:
        return float(match.group())
    else:
        return None

def log(msg):
    if do_log:
        print(msg)

#-------------------------------------------------------

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True) # keeps the window alive
options.add_argument("lang=en-GB")

driver = webdriver.Chrome(options=options)
driver.set_window_size(1200, 800)
driver.implicitly_wait(2)

url = 'https://www.wob.com/en-gb'
driver.get(url)

#-------------------------------------------------------

click('accept-cookies', '//*[@id="onetrust-accept-btn-handler"]')
click('close-localechange', '//*[@id="__BVID__297___BV_modal_body_"]/div[2]/div[1]/div[2]/div')

book_search = random_file_line(books_wishlist)
if book_search[0] == '#':
    log("invalid book: starts with #")
    exit()

target_title, target_author = book_search.split(' - ') # TODO: handle different format
log(f'searching "{book_search}"')
input('search', '//*[@id="__layout"]/div/section/div[3]/div[1]/div/input', book_search, True)

# TODO: Handle if a single book is found and we're already on that page
# TODO: Handle if we error out 404
prodlist = driver.find_element(By.ID, 'atcssearch-undefined')
bookelems = prodlist.find_elements(By.CLASS_NAME, 'gridItem')
books = []
for bookelem in bookelems:
    title  = bookelem.find_element(By.CLASS_NAME, 'title').text
    author = bookelem.find_element(By.CLASS_NAME, 'author').text[3:] # trim initial 'by '
    price  = extract_price(bookelem.find_element(By.CLASS_NAME, 'itemPrice').text)
    book = (title, author, price)
    books.append(book)

log(f'found {len(books)} books')
for book in books:
    log(f"\t{book}")

filtered_books = filter_books(books, target_title, target_author)
if not filtered_books:
    log('no book matched the filter')
    exit()

log("filtered books:")
sorted_books = sorted(filtered_books, key=lambda x: x[2])
for book in sorted_books:
    log(f"\t{book}")

best_book = find_best_priced_book(filtered_books)
if not best_book:
    log('no best book found')
    exit()
log(f"decided for {best_book}")

best_index = books.index(best_book)
bookelems[best_index].find_element(By.CLASS_NAME, 'btn-yellow').click() # add to cart

click('cart', '//*[@id="__layout"]/div/section/div[3]/div[2]/span')
click('checkout', '//*[@id="__BVID__282___BV_modal_body_"]/div/div[1]/div[1]/a')

click('checkout2', '//*[@id="__layout"]/div/div/section/div/div[3]/div[2]/div[2]/div[1]/a')

input('email', '//*[@id="checkoutMethod_email"]', login_email)
click('already-registered', '//*[@id="checkout_checkoutMethod"]/form/div[2]/button[2]')
input('password', '//*[@id="checkoutMethod_password"]', login_password)
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
defocus()
focus('card2', '//*[@id="expiryDate"]')
input('cardexpiry', '//*[@id="checkout-frames-expiry-date"]', card_expiry.replace('/', ''))
defocus()
focus('card3', '//*[@id="cvv"]')
input('cardcvv', '//*[@id="checkout-frames-cvv"]', card_cvv)
defocus()

if do_purchase:
    click('complete-order', '//*[@id="checkout_paymentInformation"]/div[1]/div/form/div[2]/button')
    click('confirm-payment', '//*[@id="Use the Wise app"]')
    log('Success. Book purchased')

log('done')