import requests
import time
import pandas as pd
from pathlib import Path

districts = {
	"8162" : "CENTRAL",
	"8176" : "DWARKA",
	"8168" : "EAST",
	"8956" : "EOW",
	"8169" : "IGI AIRPORT",
	"8160" : "METRO",
	"8165" : "NEW DELHI",
	"8166" : "NORTH",
	"8173" : "NORTH EAST",
	"8175" : "CRIME BRANCH",
	"8172" : "NORTH WEST",
	"8174" : "OUTER DISTRICT",
	"8991" : "OUTER NORTH",
	"8164" : "RAILWAYS",
	"8959" : "ROHINI",
	"8957" : "SHAHDARA",
	"8167" : "SOUTH",
	"8171" : "SOUTH WEST",
	"8955" : "SOUTH-EAST",
	"8954" : "SPECIAL CELL",
	"8953" : "SPECIAL POLICE UNIT FOR WOMEN & CHILDREN",
	"8161" : "VIGILANCE",
	"8170" : "WEST"
}

police_stations_get_url = "https://cctns.delhipolice.gov.in/citizen/getfirsearchpolicestations.htm"
pdf_get_url = "https://cctns.delhipolice.gov.in/citizen/gefirprint.htm?"

for year in range(15,16):
	for district in districts.keys():
		post_data = {
			"districtCd": district,
			"time": str(int(time.time()))
		}

		police_stations_json = (requests.post(police_stations_get_url, data = post_data)).json()

		for station in police_stations_json["rows"]:
			code = station[0]
			name = station[1] 
			# print(code, name)

			year = str(year)
			break_count =0

			for number in range(1,10000):

				if break_count > 4:
					break

				number = "{:04d}".format(number)
				req_string = pdf_get_url+"firRegNo="+code+year+number
				# print(req_string)

				try:
					pdf_resp = requests.get(req_string, timeout=5)
				except:
					try:
						pdf_resp = requests.get(req_string, timeout=5)
					except:
						break_count+=1
						continue

				pdf_data = pdf_resp.content
				
				if not pdf_data:
					break_count+=1
					continue
				
				path = Path.cwd().joinpath("data", "20"+year, districts[district], name)
				path.mkdir(parents=True, exist_ok=True)
				filename = path.joinpath(code + year + number + ".pdf")
				filename.write_bytes(pdf_data)
				print(filename)
				break_count = 0