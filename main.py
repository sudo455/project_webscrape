try: # try to see if all the needed libraries are installed
	from selenium import webdriver
	from selenium.webdriver.common.by import By
	import time
	from selenium.common.exceptions import NoSuchElementException
	import pandas as pd
except ImportError:
  print("Error: Some or one library is not installed. Please install them using pip:\n pip install -r requirements.txt")
  exit()

#initialise web drivers
driver_gbp_to_euro = webdriver.Firefox()
driver_quotes = webdriver.Firefox()
driver_books = webdriver.Firefox()

driver_gbp_to_euro.get("https://www.exchange-rates.org/converter/gbp-eur")  # live british pount to euro convertion website

time.sleep(2)

gbp_euro = driver_gbp_to_euro.find_element(By.CSS_SELECTOR, '.to-rate').text # get the value of euros per 1 British Pound(gbp)

driver_gbp_to_euro.quit()# exit web driver because is not needed

driver_quotes.get("http://quotes.toscrape.com") # scrape quotes pre loader
driver_books.get("https://books.toscrape.com/index.html") # scrape books pre loader 

##########################################################################
# block to login to quotes to scrape
driver_quotes.find_element(By.LINK_TEXT, "Login").click()
time.sleep(2)

driver_quotes.find_element(By.ID, "username").send_keys("admin")
driver_quotes.find_element(By.ID, "password").send_keys("test")

driver_quotes.find_element(By.CSS_SELECTOR, "input.btn-primary").click()
##########################################################################

data_frame_quotes = pd.DataFrame(columns=["QUOTES", "AUTHORS"]) # dataframe for quotes
page_quotes_to_scrape = 1 # for user output 


data_frame_books = pd.DataFrame(columns=["Title", "Star rating", "Price", "Stock availability"]) # dataframe for the books
page_books_to_scrape = 1 # for user output 
############################################################
# block to scrape the site: http://quotes.toscrape.com
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
############################################################


############################################################
# block to scrape the site: https://books.toscrape.com

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
############################################################

driver_quotes.quit() 
driver_books.quit() # safe exit of the drivers

data_frame_quotes.index += 1
data_frame_books.index += 1 # fix index of dataframes because the dataframe starts with 0 and not 1

# Print the results
print(data_frame_quotes)
print(data_frame_books)

# write the output to 2 .csv files
data_frame_quotes.to_csv(r'out.csv')
data_frame_books.to_csv(r'out2.csv')
