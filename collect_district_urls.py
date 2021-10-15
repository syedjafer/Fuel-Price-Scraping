import os
import json
import requests
from bs4 import BeautifulSoup


SRC_URL = 'https://www.mypetrolprice.com/petrol-price-in-india.aspx'


def collect_district_urls():
	state_to_districts = {}
	place_url = {}
	try:
		req = requests.get(SRC_URL)
		soup = BeautifulSoup(req.text, 'html.parser')
		all_states = soup.find_all("div",{"class":"sixteen columns row"})
		state_obj = all_states[3]
		states = state_obj.find_all("h2")
		for elem in states:
			try:
				temp = []
				tctx = elem.find_next("div",{"class":"txtC"})
				districts = tctx.find_all("div",{"class":"SF"}) if tctx else []
				for district in districts:
					try:
						ch = district.find("div",{"class":"CH"}) if district else []
						a_link = ch.find_all("a")
						if a_link:
							url = a_link[-1]["href"]
							num = url.split("/")[-2]
							ap_text = "?FuelType=0&LocationId="+num
							url += ap_text
							temp.append([url,a_link[-1].text])
							_name = a_link[-1].text
							place_url[_name] = url
							print(f"# {_name} - {url}")
					except Exception as ex:
						raise ex
				state_to_districts[elem.text] = temp
			except Exception as ex:
				raise ex
	except Exception as ex:
		raise ex

	# Writing District Urls to file for future usage
	if not os.path.isdir(os.path.join(os.getcwd(), 'data')):
		os.mkdir(os.path.join(os.getcwd(), 'data'))
	data_file = open(os.path.join(os.getcwd(), "data","districts.json"),"w")
	data_file.write(json.dumps(place_url))
	data_file.close()
	return place_url
