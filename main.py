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
  exit(ImportError())

page_to_scrape = webdriver.Firefox()
page_to_scrape.get("http://quotes.toscrape.com")

page_to_scrape.find_element(By.LINK_TEXT, "Login").click()

time.sleep(2)
page_to_scrape.find_element(By.ID, "username").send_keys("admin")
page_to_scrape.find_element(By.ID, "password").send_keys("test")

page_to_scrape.find_element(By.CSS_SELECTOR, "input.btn-primary").click()

data_frame = pd.DataFrame(columns=["QUOTES", "AUTHORS"])
page = 1

while True:

	print(f"Page: {page} scraping...", )

	quotes = page_to_scrape.find_elements(By.CLASS_NAME, "text")
	authors = page_to_scrape.find_elements(By.CLASS_NAME, "author")

	for quote, author in zip(quotes, authors) :
		data_frame_lengh = len(data_frame)
		q = quote.text.strip("“").strip("”").strip('"')
		q = f"{q}"
		data_frame.loc[data_frame_lengh] = [q, author.text]

	print("done.\n")
	try:
		page_to_scrape.find_element(By.PARTIAL_LINK_TEXT, "Next").click()
		page += 1

	except NoSuchElementException:
		print("End of site")
		break
data_frame.index += 1

data_frame.to_csv(r'out.csv')
