import requests
import re
import sys
import sqlite3
from bs4 import BeautifulSoup
import json
import time
import random
fileName = 'applestore.json'

from lxml import etree

class spider(object):

	def getsource(self, url):
		#time.sleep(random.randint(0,3))
		headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "User-Agent":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; TencentTraveler 4.0; .NET CLR 2.0.50727" }
		sourceHtml = requests.get(url, headers = headers, timeout=20)
		#print ('new url')
		#print (url)
		return sourceHtml.text

	def getNeedInfo(self,sourceHtml):
		soup = BeautifulSoup(sourceHtml, features='html5lib')
		playitem = {}

		table_title = 'free-apps'

		div = soup.find('div', {'class': 'animation-wrapper is-visible ember-view'})
		#print ('div')
		#print (div)
		try:
			section = div.find_all('div', {'class': 'ember-view'})[1].find('section', {'class': 'l-content-width section section--hero product-hero ember-view'})
		except:
			print ('sourceHtml')
			print (div)

		age_rating = section.find('header').find('h1').find('span').string

		try:
			subtitle = section.find('header').find_all('h2')[0].string
			autor = section.find('header').find_all('h2')[1].find('a').string
			autor_URL = section.find('header').find_all('h2')[1].find('a').get('href')
		except:
			autor = section.find('header').find_all('h2')[0].find('a').string
			autor_URL = section.find('header').find_all('h2')[0].find('a').get('href')
			subtitle = 'N/A'

		#print ('section')
		#print (section.find('header'))

		sub_rank = section.find('header').find_all('ul', {'class': 'product-header__list app-header__list'})[0].find('li', {'class': 'inline-list__item'}).string
		if sub_rank == None:
			sub_rank="N/A"
		star = section.find('figcaption').string

		section = div.find_all('div', {'class': 'ember-view'})[1].find_all('section', {'class': 'l-content-width section section--bordered'})[1]

		description = ""
		for des in section.find_all('p'):
			description += str(des).replace('<p>', '').replace('<p/>', '').replace('<br>', '').replace('<br/>','')

		section = div.find_all('div', {'class': 'ember-view'})[1].find_all('section', {'class': 'l-content-width section section--bordered'})[2]

		five_star = section.find('figure').find_all('div', {'class': 'we-star-bar-graph__bar__foreground-bar'})[0].get('style')
		four_star = section.find('figure').find_all('div', {'class': 'we-star-bar-graph__bar__foreground-bar'})[1].get('style')
		three_star = section.find('figure').find_all('div', {'class': 'we-star-bar-graph__bar__foreground-bar'})[2].get('style')
		two_star = section.find('figure').find_all('div', {'class': 'we-star-bar-graph__bar__foreground-bar'})[3].get('style')
		one_star = section.find('figure').find_all('div', {'class': 'we-star-bar-graph__bar__foreground-bar'})[4].get('style')

		reviews = ['']
		try:
			for rv in section.find_all('div', {'class': 'we-customer-review lockup ember-view'}):
				reviews.append(str(rv.find("p")).replace('<p>', '').replace('<p/>', '').replace('<br>', '').replace('<br/>',''))
		except:
			pass

		section = div.find_all('div', {'class': 'ember-view'})[1].find_all('section', {'class': 'l-content-width section section--bordered'})[3]

		inapp_purchase = "N/A"
		try:
			size = section.find_all('dd')[1].string
			category = section.find_all('dd')[2].find('a').string
			price = section.find_all('dd')[7].string
		except:
			try:
				inapp_purchase = []
				section = div.find_all('div', {'class': 'ember-view'})[1].find_all('section', {'class': 'l-content-width section section--bordered'})[4]
				size = section.find_all('dd')[1].string
				category = section.find_all('dd')[2].find('a').string
				price = section.find_all('dd')[7].string
				for sml in section.find_all('dd')[-1].find_all('li'):
					inapp_purchase.append(sml.find_all('span')[-1].string)
			except:
				inapp_purchase = []
				section = div.find_all('div', {'class': 'ember-view'})[1].find_all('section', {'class': 'l-content-width section section--bordered'})[5]
				size = section.find_all('dd')[1].string
				category = section.find_all('dd')[2].find('a').string
				price = section.find_all('dd')[7].string
				for sml in section.find_all('dd')[-1].find_all('li'):
					inapp_purchase.append(sml.find_all('span')[-1].string)

		similar = []
		section = div.find_all('div', {'class': 'ember-view'})[1].find_all('section', {'class': 'l-content-width section section--bordered'})[-1]
		for sml in section.find_all('a')[1:]:
			similar.append(sml.find('div', {'class': 'we-lockup__title'}).find('div').string)

		#if "free" in price:
			#inapp_purchase = []
			#for inapp in response.xpath('//*[@id="ember-app"]/div/main/div/div/div/div/div/div[2]/section[7]/div/div[1]/dl/div[11]/dd/ol/div/li'):
				#inapp_purchase.append(inapp.xpath('span[2]/text()')[0].extract() 
		playitem['table_title'] = table_title.strip()
		playitem['age_rating'] = age_rating.strip()
		playitem['subtitle'] = subtitle.strip()
		playitem['autor'] = autor.strip()
		playitem['autor_URL'] = autor_URL.strip()
		playitem['sub_rank'] = sub_rank.strip()
		playitem['star']= star.strip()
		playitem['description'] = description.strip()
		playitem['five_star'] = five_star.strip()
		playitem['four_star'] = four_star.strip()
		playitem['three_star'] = three_star.strip()
		playitem['two_star'] = two_star.strip()
		playitem['one_star'] = one_star.strip()
		playitem['reviews'] = "|".join(reviews)
		playitem['size']= size.strip()
		playitem['category'] = category.strip()
		playitem['price'] = price.strip()
		playitem['inapp_purchase'] = ",".join(inapp_purchase)
		playitem['similar'] = ",".join(similar)

		return playitem

if __name__ == '__main__':
	spider = spider()

	start_url='https://www.apple.com/itunes/charts/top-grossing-apps/'
	start_sourceHtml = spider.getsource(start_url)
	selector = etree.HTML(start_sourceHtml)
	line = []
	exc = []
	#exp_free = ['Merge Plane - Best Idle Game', 'Google Photos', 'OfferUp - Buy. Sell. Simple.', 'Color Road!', u'Piano Tiles 2\u2122', 'Slices']
	#exp_paid = ['NBA 2K18', "My Baby's Beat", 'FaceOscar', 'Flipagram.', 'The Amazing Spider-Man 2', 'HappyCow Find Vegan Food', 'My Macros+ | Diet & Calories', 'Zombieville USA 2']
	#exp_grossing = ['Final Fantasy XV: A New Empire', 'HOOKED', 'Micromon Adventures']
	#exp= ['NBA 2K18', "My Baby's Beat", 'FaceOscar', 'Flipagram.', 'The Amazing Spider-Man 2', 'HappyCow Find Vegan Food', 'My Macros+ | Diet & Calories', 'Zombieville USA 2']

	for url in selector.xpath('//*[@id="main"]/section/div/ul/li'):
		targetURL = url.xpath('a/@href')[0]
		pos = targetURL.find('?')
		targetURL = targetURL[:pos+5]
		title = url.xpath('h3/a/text()')[0]
		sourceHtml = spider.getsource(targetURL)
		singleinfo = {}
		#if not title in exp:
			#continue
		try:
			singleinfo = spider.getNeedInfo('')
		except:
			try:
				time.sleep(5)
				sourceHtml = spider.getsource(targetURL)
				singleinfo = {}
				singleinfo = spider.getNeedInfo(sourceHtml)
			except:
				print (title)
				exc.append(title)
				continue
		line.append(singleinfo)
		singleinfo['title']=title

		#print (singleinfo)
		#break

	print ('len')
	print (len(line))
	print ('exc')
	print (exc)
	with open(fileName, 'w') as f:
		json.dump(line,f)
        