"""
TODO: Impliment a web scraping tool with Beautiful Soup or Scrapy and output them to json or csv
site : quotes.toscrape.com
site : books.toscrape.com
"""

try: # try to see if all the needed libraries are installed
	from selenium import webdriver
	from selenium.webdriver.common.by import By
	import time
	from selenium.common.exceptions import NoSuchElementException
	import pandas as pd
except ImportError:
  print("Error: Some or one library is not installed. Please install them using pip:\n pip install -r requirements.txt")
  exit()

driver_gbp_to_euro = webdriver.Firefox()
driver_gbp_to_euro.get("https://www.exchange-rates.org/converter/gbp-eur")  # Replace with the path to your local HTML file

time.sleep(2)

gbp_euro = driver_gbp_to_euro.find_element(By.CSS_SELECTOR, '.to-rate').text

driver_gbp_to_euro.quit()

driver_quotes = webdriver.Firefox()
driver_quotes.get("http://quotes.toscrape.com")

driver_books = webdriver.Firefox()
driver_books.get("https://books.toscrape.com/index.html")

driver_quotes.find_element(By.LINK_TEXT, "Login").click()

time.sleep(2)
driver_quotes.find_element(By.ID, "username").send_keys("admin")
driver_quotes.find_element(By.ID, "password").send_keys("test")

driver_quotes.find_element(By.CSS_SELECTOR, "input.btn-primary").click()

data_frame_quotes = pd.DataFrame(columns=["QUOTES", "AUTHORS"])
page_quotes_to_scrape = 1


data_frame_books = pd.DataFrame(columns=["Title", "Star rating", "Price", "Stock availability"])
page_books_to_scrape = 1

while True:

	print(f"Page: {page_quotes_to_scrape} scraping...", )

	quotes = driver_quotes.find_elements(By.CLASS_NAME, "text")
	authors = driver_quotes.find_elements(By.CLASS_NAME, "author")

	for quote, author in zip(quotes, authors) :
		data_frame_lengh_quotes = len(data_frame_quotes)
		q = quote.text.strip("“").strip("”").strip('"')
		q = f"{q}"
		data_frame_quotes.loc[data_frame_lengh_quotes] = [q, author.text]

	print("done.\n")

	try:
		driver_quotes.find_element(By.PARTIAL_LINK_TEXT, "Next").click()
		page_quotes_to_scrape += 1

	except NoSuchElementException:
		print("End of site quotes to scrape")
		break

while True:
  products = driver_books.find_elements(By.CSS_SELECTOR, 'article.product_pod')
  print(f"Page: {page_books_to_scrape} scraping...", )

  for product in products:
    data_frame_books_lengh = len(data_frame_books)

    title = product.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_property('title')
    star_rating = product.find_element(By.CSS_SELECTOR, 'p.star-rating').get_dom_attribute('class').replace('star-rating ', '')
    price = product.find_element(By.CSS_SELECTOR, 'p.price_color').text
    in_stock = driver_books.find_element(By.CSS_SELECTOR, 'div.product_price').find_element(By.CSS_SELECTOR,'p.instock.availability').text

    _, value_in_gbp = price.split("£")
    price = str(float(value_in_gbp) * float(gbp_euro))  + "€"

    data_frame_books.loc[data_frame_books_lengh] = [title, star_rating, price, in_stock]

  
  print("done.\n")
  
  try:
    next_click = driver_books.find_element(By.PARTIAL_LINK_TEXT, "next").click()
    page_books_to_scrape += 1

  except NoSuchElementException:
    print("End of site books to scrape")
    break

driver_quotes.quit()
driver_books.quit()

data_frame_quotes.index += 1
print(data_frame_quotes)
data_frame_quotes.to_csv(r'out.csv')

# Print the results
data_frame_books.index += 1
print(data_frame_books)
data_frame_books.to_csv(r'out2.csv')
