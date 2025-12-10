import os
import json
import sqlite3
import requests
from datetime import datetime
from database.tables import fn_createDataBaseTables

PATH = './database/database.db'

def fn_historicalData():
	url = 'https://www.macrotrends.net/economic-data/2627/10YD'

	headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0'
	}

	response = requests.get(url, headers=headers)

	jsonResponse = response.json()
	data = jsonResponse['data']

	if not os.path.exists(PATH):

		fn_createDataBaseTables()

		connection = sqlite3.connect(PATH)
		cursor = connection.cursor()

		dataLength = len(data)

		for i in range(dataLength):
			price = float(data[i][1])
			date = str(data[i][0])
			readableDate = datetime.fromtimestamp(int(date[:-3])).strftime("%Y-%m-%d")

			cursor.execute("INSERT INTO historicalData (dateXAU, priceXAU) VALUES (?, ?);",
				(readableDate, price))

		connection.commit()
		connection.close()

		return 'DataBase Created With XAU Data.'

	connection = sqlite3.connect(PATH)
	cursor = connection.cursor()

	cursor.execute('''
		SELECT dateXAU FROM historicalData 
		ORDER BY dateXAU DESC LIMIT 1;
		''')

	lastDateXAU = cursor.fetchone()

	lastJsonDateStr = str(data[-1][0])
	lastJsonDate = datetime.fromtimestamp(int(lastJsonDateStr[:-3])).strftime('%Y-%m-%d')

	if lastJsonDate == lastDateXAU[0]:
		connection.commit()
		cursor.close()

		return 'No New Changes.'

	datesList = list()

	while lastJsonDate > lastDateXAU[0]:
		priceJson = float(data[-1][1])
		datesList.append((lastJsonDate, priceJson))
		data.pop()
		
		if not data:
			break

		lastJsonDateStr = str(data[-1][0])
		lastJsonDate = datetime.fromtimestamp(int(lastJsonDateStr[:-3])).strftime('%Y-%m-%d')

	datesList.reverse()

	for (date, price) in datesList:
		cursor.execute('''
			INSERT INTO historicalData (dateXAU, priceXAU) 
			VALUES (?, ?);''', (date, price))

	connection.commit()
	cursor.close()

	return 'DataBase Updated, (New Data Found).'

print(fn_historicalData())