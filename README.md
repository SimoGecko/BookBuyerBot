# Book Buyer Bot 📚🤖

## What is this?
This is a bot that periodically buys a random book from your book wishlist and ships it directly to you.
It started as an effort for me to read more, by having a new book that interests me arrive at my doorstep each month, without me having to do anything (other than pay). Plus, the surprise of not knowing what's going to arrive makes it more interesting.

## How does this work?
The bot selects a book at random from your book wishlist inside `books.txt`, then uses [Selenium](https://www.selenium.dev/) to navigate to [wob.com](https://www.wob.com/en-gb) - a book shop - to find and purchase the book.
The bot automatically filters for books that closely match the book title and author, and picks one of the cheapest books available.
It's possible to configure the bot with a maximum price, e.g. $15, to make sure it won't purchase anything too expensive. It's also possible to specify a "budget surplus", which allows the bot to spend it to select a better edition rather than the cheapest one.
For example, if there are 3 books, costing $9, $10, $12, and $20 and you you allow a budget surplus of $3, it will pick the book of $12, since it's likely that it's a better version of the book.

## How to run this?
- Fill out `books.txt` with your book wishlist. Books should be in the format `Book Title - Author`. Lines starting with `#` will be ignored.
- Create an account on [wob.com](https://www.wob.com/en-gb). Navigate to `My Account`, then add a default billing + shipping address. The bot will use this.
- In the script `bookbot.py`, fill out your login email + password and card information for payment, as well as the max allowed price and budget surplus.
- Run this manually by calling `run.bat` or `py bookbot.py`. Alternatively, schedule this to run monthly or whenever you want using `cron` (Unix) or Task Scheduler (Windows).
- Done!

When the bot tries to buy something, you might be prompted to confirm the purchase, depending on your payment method.
