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

xpathmap = {
    'accept-cookies':       '//*[@id="onetrust-accept-btn-handler"]',
    'close-localechange':   '//*[@id="__BVID__297___BV_modal_body_"]/div[2]/div[1]/div[2]/div',
    'search':               '//*[@id="__layout"]/div/section/div[3]/div[1]/div/input',
    'prodlist':             '//*[@id="atcssearch-undefined"]',
    'cart':                 '//*[@id="__layout"]/div/section/div[3]/div[2]/span',
    'checkout':             '//*[@id="__BVID__282___BV_modal_body_"]/div/div[1]/div[1]/a',
    
    'checkout2':            '//*[@id="__layout"]/div/div/section/div/div[3]/div[2]/div[2]/div[1]/a',
    
    'email':                '//*[@id="checkoutMethod_email"]',
    'already-registered':   '//*[@id="checkout_checkoutMethod"]/form/div[2]/button[2]',
    'password':             '//*[@id="checkoutMethod_password"]',
    'login':                '//*[@id="checkout_checkoutMethod"]/form/div[3]/button',
    
    'shipping-dropdown':    '//*[@id="checkout_shippingInformation"]/form/div[2]/div/div[1]',
    
    'nopromo':              '//*[@id="checkout_shippingInformation"]/form/div[3]/label',
    'continue-to-delivery': '//*[@id="checkout_shippingInformation"]/form/div[5]/button',
    
    'continue-to-checkout': '//*[@id="checkout_shippingMethod"]/form/div[2]/button',
    
    'card1':                '//*[@id="cardNumber"]',
    'cardnumber':           '//*[@id="checkout-frames-card-number"]',
    'card2':                '//*[@id="expiryDate"]',
    'cardexpiry':           '//*[@id="checkout-frames-expiry-date"]',
    'card3':                '//*[@id="cvv"]',
    'cardcvv':              '//*[@id="checkout-frames-cvv"]',
    
    'complete-order':       '//*[@id="checkout_paymentInformation"]/div[1]/div/form/div[2]/button',
    'confirm-payment':      '//*[@id="Use the Wise app"]',

    'prodprice':            '//*[@id="__layout"]/div/div/div/div[2]/div[2]/div/div[3]/div[1]/div[1]',
    'prod-addcart':         '//*[@id="stickyStart"]/div/div[1]/button',
}

#-------------------------------------------------------

timeout = 10

def click(name):
    #driver.find_element(By.XPATH, xpath).click()
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpathmap[name]))
        ).click()
    except:
        pass

def get(name):
    try:
        #elem = driver.find_element(By.XPATH, xpathmap[name])
        elem = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpathmap[name]))
        )
        return elem
    except:
        return None

def input(name, value, enter = False):
    elem = get(name)
    #elem.clear()
    for i in range(100):
        elem.send_keys(Keys.BACK_SPACE)
    elem.send_keys(value)
    if enter:
        elem.send_keys(Keys.RETURN)

def gettext(name):
    elem = get(name)
    return elem.text if elem else ''

def wait(seconds):
    time.sleep(seconds)

def focus(name):
    iframe = get(name)
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

click('accept-cookies')
click('close-localechange')

def tryBuyBook():
    book_search = random_file_line(books_wishlist).rstrip() # removes trailing whitespaces/newlines
    if book_search[0] == '#':
        log(f"invalid book: starts with # ({book_search})")
        return False

    target_title, target_author = book_search.split(' - ') # TODO: handle different format
    log(f'searching "{book_search}"')
    input('search', book_search, True)

    wait(1) # otherwise we look at the url too soon
    isOnSearchPage = "?search=" in driver.current_url
    if isOnSearchPage:
        # TODO: Handle if a single book is found and we're already on that page
        # TODO: Handle if we error out 404
        prodlist = get('prodlist')
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
            return False

        log("filtered books:")
        sorted_books = sorted(filtered_books, key=lambda x: x[2])
        for book in sorted_books:
            log(f"\t{book}")

        best_book = find_best_priced_book(filtered_books)
        if not best_book:
            log(f'no best book found, all prices too high')
            return False
        log(f"decided for {best_book}")

        best_index = books.index(best_book)
        bookelems[best_index].find_element(By.CLASS_NAME, 'btn-yellow').click() # add to cart
    else:
        # is on product page:
        log('im on prod page')
        price = extract_price(gettext('prodprice'))
        if price > max_price:
            log(f'book is too expensive: {price}')
            return False
        click('prod-addcart')

    click('cart')
    click('checkout')

    click('checkout2')

    input('email', login_email)
    click('already-registered')
    input('password', login_password)
    click('login')

    # select address
    click('shipping-dropdown')
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    click('nopromo')
    click('continue-to-delivery')

    click('continue-to-checkout')

    focus('card1')
    input('cardnumber', card_number)
    defocus()
    focus('card2')
    input('cardexpiry', card_expiry.replace('/', ''))
    defocus()
    focus('card3')
    input('cardcvv', card_cvv)
    defocus()

    if do_purchase:
        click('complete-order')
        click('confirm-payment')
        log('Success. Book purchased')
    log('done')
    return True

#-------------------------------------------------------

for i in range(5):
    try:
        success = tryBuyBook()
        if success:
            break
    except Exception as e:
        log(f"Exception: {e}. Retrying...")