#coding=utf8
from google_play_spider.items import GooglePlaySpiderItem
import scrapy

class PttSpider(scrapy.Spider):
      name = "playspider"      
      start_urls = ["https://play.google.com/store/apps/collection/topselling_free",
                    "https://play.google.com/store/apps/collection/topselling_paid",
                    "https://play.google.com/store/apps/collection/topgrossing",
                    "https://play.google.com/store/apps/category/GAME/collection/topselling_free",
                    "https://play.google.com/store/apps/category/GAME/collection/topselling_paid",
                    "https://play.google.com/store/apps/category/GAME/collection/topgrossing",
                    "https://play.google.com/store/apps/collection/topselling_new_free",
                    "https://play.google.com/store/apps/collection/topselling_new_paid",
                    "https://play.google.com/store/apps/category/GAME/collection/topselling_new_free",
                    "https://play.google.com/store/apps/category/GAME/collection/topselling_new_paid"] 

      def parse(self, response):  
          #取得 顯示更多內容 URL

          table_title = response.xpath('//div[@class="cluster-heading"]/h2/text()')[0].extract().strip()
          total = 0
          for url in response.xpath('//div[@class="card no-rationale square-cover apps small"]/div[@class="card-content id-track-click id-track-impression"]'):
              total += 1

              title = url.xpath('div[@class="details"]/a[@class="title"]/text()')[0].extract()
              imgURL = 'https:' + url.xpath('div[@class="cover"]/div/div/div/img/@data-cover-large')[0].extract()
              description_list = url.xpath('div[@class="details"]/div[@class="description"]/text()')[0].extract()
              description = ''.join(description_list)
              autor = url.xpath('div[@class="details"]/div[@class="subtitle-container"]/a/text()')[0].extract()
              targetURL = 'https://play.google.com' + url.xpath('div[@class="details"]/a/@href')[0].extract()
              autor_URL = 'https://play.google.com' + url.xpath('div[@class="details"]/div[@class="subtitle-container"]/a/@href')[0].extract()
              try:
                star = url.xpath('div[@class="reason-set"]/span/a/div/div/@aria-label')[0].extract()
              except:
                star = 'no star_rate'
              star_rates = star

              #使用POST , 抓資料 100 筆
              request = scrapy.FormRequest(               
                     targetURL,
                     formdata = {'start':'0',
                                 'num':'1',
                                 'numChildren':'0',
                                 'cctcss':'square-cover',
                                 'cllayout':'NORMAL',
                                 'ipf':'1',
                                 'xhr':'1',
                                 'token':'zNTXc17yBEzmbkMlpt4eKj14YOo:1458833715345'},
                    callback = self.parse_data,
                    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'},
                    cookies = {'cookie-key': '_ga=GA1.2.259790884.1552095104; __qca=P0-52365157-1552095104157; __gads=ID=2c4091f81a0034fa:T=1552184369:S=ALNI_MbjxZVq-WfZ8xsrvjXMKBhCeCh_tg; notice-ctt=4%3B1552860610439; _gid=GA1.2.1799586118.1553292208'}
                 )
              request.meta['table_title'] = table_title.strip()
              request.meta['title'] = title.strip()
              request.meta['imgURL'] = imgURL.strip()
              request.meta['description'] = description.strip()
              request.meta['autor'] = autor.strip()
              request.meta['autor_URL'] = autor_URL.strip()
              request.meta['star_rates'] = star_rates.strip()
              yield  request

              if total == 200:
                break


      def parse_data(self, response):  
          #抓取各項資料 使用xpath時,如要抓取一層內的一層,請一層一層往下抓,不要用跳的,不然會抓不到
          playitem = GooglePlaySpiderItem()
          
          playitem['title'] = response.meta['title']
          playitem['imgURL'] = response.meta['imgURL']
          playitem['description'] = response.meta['description']
          playitem['autor'] = response.meta['autor']
          playitem['autor_URL'] = response.meta['autor_URL']
          playitem['star_rates'] = response.meta['star_rates']
          playitem['table_title']= response.meta['table_title']

          cat = []
          for label in response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div/div[1]/div[1]/span[@class="T32cc UAO9ie"]'):
            label_name = label.xpath('a/text()')[0].extract()
            if label_name != playitem['autor']:
              cat.append(label_name.strip()[:5000])
          playitem['category'] = "".join(cat)

          price = response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/c-wiz/c-wiz/div/span/button')[0].extract()
          details = response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[3]/div/div[1]/meta/@content')[0].extract()
          five_ratings = response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/c-wiz/div[2]/div[1]/span[2]/@style')[0].extract()
          four_ratings = response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/c-wiz/div[2]/div[2]/span[2]/@style')[0].extract()
          three_ratings = response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/c-wiz/div[2]/div[3]/span[2]/@style')[0].extract()
          two_ratings = response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/c-wiz/div[2]/div[4]/span[2]/@style')[0].extract()
          one_ratings = response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/c-wiz/div[2]/div[5]/span[2]/@style')[0].extract()
          
          rev = []
          for review in response.xpath('//div[@class="zc7KVe"]/div[@class="d15Mdf bAhLNe"/div[@class="UD7Dzf"]'):
            rev.append(review.xpath('span[1]/text()')[0].extract())
          playitem['reviews'] = "".join(rev)

          size = response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[3]/div[1]/div[2]/div/div[3]/span/div/span/text()')[0].extract()
          installs = response.xpath('//div[@class="QKtxw"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[3]/div[1]/div[2]/div/div[4]/span/div/span/text()')[0].extract()

          playitem['price'] = price.strip()[:-4]
          playitem['details'] = details.strip()[:100000]
          playitem['five_ratings'] = five_ratings.strip()[7:]
          playitem['four_ratings'] = four_ratings.strip()[7:]
          playitem['three_ratings'] = three_ratings.strip()[7:]
          playitem['two_ratings'] = two_ratings.strip()[7:]
          playitem['one_ratings'] = one_ratings.strip()[7:]
          playitem['size'] = size.strip()
          playitem['installs'] = installs.strip()[:-1]

          yield playitem
            

