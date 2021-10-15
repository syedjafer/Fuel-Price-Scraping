# Scraping Fuel Price

# Installation

```
pip install -r requirements.txt
```

# Usage

Update the stop_date value in <b> fuel_scrap_runner.py </b> Make sure stop_date is the past date. 
This script will scrape all the data from today till the stop_date.

Then run,

```
python fuel_scrap_runner.py
```

After completion all the data will be available inside the dataset folder. 


Here, we have used Chrome for selenium scraping, so you need to choose the corresponding chromedriver .

Checkout for chromedriver which supports your chrome version from here https://sites.google.com/a/chromium.org/chromedriver/downloads


# Credits

This data is been scraped from mypetrolprice.  https://mypetrolprice.com/petrol-price-in-india.aspx . 
