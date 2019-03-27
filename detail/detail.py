import requests
import re
import sys
import sqlite3
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
db = 'googleplay.db'
fileName = 'googleplay.json'

from lxml import etree

class spider(object):

	def getsource(self, url):
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
		sourceHtml = requests.get(url, headers = headers)
		return sourceHtml.text

	def getNeedInfo(self,sourceHtml):
		currentAllInfo = []
		selector = etree.HTML(sourceHtml)
		soup = BeautifulSoup(sourceHtml, features='lxml')
		singlePageInfo = {}

		labels = soup.find_all('span', {'class': 'T32cc UAO9ie'})
		cat = '['
		for label in labels:
			label_name = label.find('a').string.strip()[:20]
			cat = cat+label_name+','
		singlePageInfo['category'] = cat[:-1] + ']'
		price = selector.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/c-wiz/c-wiz/div/span/button/@aria-label')[0]
		details = selector.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[3]/div/div[1]/meta/@content')[0]
		div = soup.find_all('div', {'class': 'mMF0fd'})
		ratings = []
		for i, ele in enumerate(div):
			ratings.append(ele.find_all('span')[1].get('style').strip()[7:])

		div = soup.find_all('div', {'class': 'hAyfc'})
		size = div[1].find('span').find('div').find('span').string
		
		age = selector.xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div/div[1]/div[2]/div/text()')[0]
		
		installs = div[2].find('span').find('div').find('span').string
		singlePageInfo['price'] = price
		singlePageInfo['details'] = details.strip()[:100000]
		if len(ratings) == 0:
			singlePageInfo['ratings_1'] = "N/A"
			singlePageInfo['ratings_2'] = "N/A"
			singlePageInfo['ratings_3'] = "N/A"
			singlePageInfo['ratings_4'] = "N/A"
			singlePageInfo['ratings_4'] = "N/A"
		else:
			singlePageInfo['ratings_1'] = ratings[4]
			singlePageInfo['ratings_2'] = ratings[3]
			singlePageInfo['ratings_3'] = ratings[2]
			singlePageInfo['ratings_4'] = ratings[1]
			singlePageInfo['ratings_5'] = ratings[0]
		singlePageInfo['size'] = size.strip()
		singlePageInfo['installs'] = installs.strip()[:-1]
		singlePageInfo['age'] = age.strip()

		return singlePageInfo

if __name__ == '__main__':
	spider = spider()

	con = sqlite3.connect(db)
	cur = con.cursor()

	cursor = cur.execute("SELECT * from googleplay")
	line = []
	for row in cursor:

		url = row[2]
		#url = 'https://play.google.com/store/apps/details?id=com.wEirCode1_8657018'

		o = urlparse(url)
		ids = o.query[3:]

		sourceHtml = spider.getsource(url)
		singleinfo = {}
		singleinfo = spider.getNeedInfo(sourceHtml)

		singleinfo['table_title'] = row[0]
		singleinfo['title'] = row[1]
		singleinfo['imgURL'] = row[3]
		singleinfo['description'] = row[4]
		singleinfo['autor'] = row[5]
		singleinfo['autor_URL'] = row[6]
		singleinfo['star_rates'] = row[7]
		singleinfo['app_id'] = ids

		line.append(singleinfo)

		#print (singleinfo)
		#break

	print ('len')
	print (len(line))
	with open(fileName, 'w') as f:
		json.dump(line,f)

	con.commit()
	con.close() 
        