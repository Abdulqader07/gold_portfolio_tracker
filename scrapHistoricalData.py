import json
import sqlite3
import requests
from datetime import datetime

def histScraper():
	connection = sqlite3.connect('./database/database.db')
	cursor = connection.cursor()

	url = 'https://www.macrotrends.net/economic-data/2627/10YD'

	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0'
	}

	response = requests.get(url, headers=headers)

	jsonResponse = response.json()
	data = jsonResponse['data']

	appendData = list()

	for i in range(len(data)):
		price = float(data[i][1])
		date = str(data[i][0])
		readableDate = datetime.fromtimestamp(int(date[:-3])).strftime("%Y-%m-%d")

		cursor.execute("INSERT INTO historicalData (dateXAU, priceXAU) VALUES (?, ?)",
			(readableDate, price))

	connection.commit()
	connection.close()

	return None