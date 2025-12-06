import requests
from bs4 import BeautifulSoup

def fn_realTimePrice():
	url = 'https://www.investing.com/currencies/xau-usd'
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0'
	}

	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.content, 'html.parser')

	realTimeXAU_price = soup.find('div', class_='text-5xl/9')

	return realTimeXAU_price.string