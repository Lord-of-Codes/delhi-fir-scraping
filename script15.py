import requests
import time
from pathlib import Path
import os

districts = {
	"8160": "METRO",
	"8161": "VIGILANCE",
	"8162": "CENTRAL",
	"8164": "RAILWAYS",
	"8165": "NEW DELHI",
	"8166": "NORTH",
	"8167": "SOUTH",
	"8168": "EAST",
	"8169": "IGI AIRPORT",
	"8170": "WEST",
	"8171": "SOUTH WEST",
	"8172": "NORTH WEST",
	"8173": "NORTH EAST",
	"8174": "OUTER DISTRICT",
	"8175": "CRIME BRANCH",
	"8176": "DWARKA",
	"8953": "SPECIAL POLICE UNIT FOR WOMEN & CHILDREN",
	"8954": "SPECIAL CELL",
	"8955": "SOUTH-EAST",
	"8956": "EOW",
	"8957": "SHAHDARA",
	"8959": "ROHINI",
	"8991": "OUTER NORTH"
}

police_stations_get_url = "https://cctns.delhipolice.gov.in/citizen/getfirsearchpolicestations.htm"
pdf_get_url = "https://cctns.delhipolice.gov.in/citizen/gefirprint.htm?"

skip_flag = True

for year in range(15,16):
	for district in districts.keys():
		post_data = {
			"districtCd": district,
			"time": str(int(time.time()))
		}

		try:
			police_stations_json = (requests.post(police_stations_get_url, data = post_data)).json()
		except:
			while(True):
				try:
					police_stations_json = (requests.post(police_stations_get_url, data = post_data)).json()
					if police_stations_json:
						break
				except:
					print(str(int(time.time())) + " fetching police stations")
					time.sleep(60)


		for station in police_stations_json["rows"]:
			code = station[0]
			name = station[1] 
			# print(code, name)

			# if skip_flag and name != 'PATEL NAGAR':
			# 	continue
			# else:
			# 	skip_flag = False
				

			year = str(year)
			break_count =0

			for number in range(1,10000):

				if break_count > 4 and number > 1000:
					break

				number = "{:04d}".format(number)

				path = Path.cwd().joinpath("data", "20"+year, districts[district], name)
				filename = path.joinpath(code + year + number + ".pdf")

				if os.path.exists(filename):
					print(str(filename) + "\tfile already present")
					continue
				
				req_string = pdf_get_url+"firRegNo="+code+year+number
				try:
					pdf_resp = requests.get(req_string, timeout=3)
				except:
					# try:
					# 	pdf_resp = requests.get(req_string, timeout=5)
					# except:
					break_count+=1
					continue

				if pdf_resp.status_code == 404:
					break_count+=1
					continue
				
				pdf_data = pdf_resp.content
				
				if not pdf_data:
					break_count+=1
					continue
				
				path.mkdir(parents=True, exist_ok=True)
				filename.write_bytes(pdf_data)
				print(filename)
				break_count = 0