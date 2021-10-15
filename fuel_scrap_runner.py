import os
import re
import time

import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from collect_district_urls import collect_district_urls
from constant import fuel as con_fuel
from constant import driver as con_driver

class FuelPrice:
        def __init__(self, stop_date, out_location, place_urls):
                self.stop_date = stop_date
                self.out_location = out_location
                self.place_urls = place_urls
                self.data = {con_fuel.CITY: [], con_fuel.DATE: [], con_fuel.RATE: []}

        def collect_tabular_data(self, browser, name):
                try:
                        table = browser.find_element_by_id("BC_GV")
                        rows = table.find_elements_by_tag_name("td")
                        for index in range(0, (len(rows) - 1)):
                                # Price
                                _price = rows[index].find_element_by_class_name("GVPrice").text.replace("₹ ", "")
                                self.data[con_fuel.RATE].append(float(_price))

                                # Date
                                _date = re.sub("\n", "-", rows[index].find_element_by_class_name("DateDiv").text)
                                _date = pd.to_datetime(_date).strftime(con_fuel.DATE_FORMAT)
                                self.data[con_fuel.DATE].append(_date)

                                # City
                                self.data[con_fuel.CITY].append(name)
                                print(name, _price)

                except Exception as ex:
                        print(ex)

        def collect_data_from_single_url(self, browser, url, name):
                try:
                        # Navigate to the Url
                        browser.get(url)
                        time.sleep(5)
                        # total_pages = int(self.browser.find_element(By.XPATH, con_fuel.LABEL_TAG_XPATH).text)
                        total_pages = int(
                            browser.find_element_by_xpath(
                                '//*[@id="BC_GV_CustomGridPager_LabelNumberOfPages"]'
                            ).text
                        )
                        for page in range(1, total_pages-1):
                                try:
                                        NEXT_BUTTON_XPATH = '//input[@type="submit" and @name="ctl00$BC$GV$ctl07$CustomGridPager$NextButton" and  @value=">"]'
                                        next_btn = browser.find_element_by_xpath(NEXT_BUTTON_XPATH)
                                        next_btn.send_keys(Keys.DOWN)
                                        try:
                                                self.collect_tabular_data( browser=browser, name=name)
                                                print(self.stop_date, self.data[con_fuel.DATE])
                                                if self.stop_date in self.data[con_fuel.DATE]:
                                                        break
                                                else:
                                                        # next_btn.click()
                                                        time.sleep(10)
                                        except:
                                                browser.close()
                                except:
                                        browser.close()
                except:
                        browser.close()

        def collect_historical_data(self):
                for name, url in self.place_urls.items():
                        options = Options()
                        options.headless = True
                        browser = webdriver.Chrome(con_driver.CHROMEDRIVER_LOC, chrome_options=options)
                        print("#"*30, name)
                        self.collect_data_from_single_url(browser=browser, url=url, name=name)
                        browser.close()
                        print(name, url)

                # Creating DataFrame for Operations
                try:
                        df = pd.DataFrame(self.data)
                        # df = df.query(f'date >= "{self.stop_date}"')
                        df = df.sort_values(by=[con_fuel.CITY, con_fuel.DATE], ascending=True).reset_index(  drop=True  )
                        df.to_csv(self.out_location, index=False)
                except Exception as ex:
                        print(ex)

_stop_date = '2021-10-10'
_out_location = os.path.join(os.getcwd(), "data", "petrol_price.csv")
_place_urls = collect_district_urls()
fp = FuelPrice(stop_date=_stop_date,
          out_location=_out_location,
          place_urls=_place_urls )
fp.collect_historical_data()
