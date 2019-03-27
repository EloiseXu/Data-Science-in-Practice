# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json  
import sqlite3

#fileName = 'googleplay.json'
db = 'googleplay.db'

class GooglePlaySpiderPipeline(object):
    def __init__(self):  
        #json
        #with open(fileName, 'w') as f:
             #f.write('[\n')
        pass
    
    def open_spider(self, spider):
        #sqlite
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute('DROP TABLE IF EXISTS googleplay')
        self.cur.execute('create table if not exists googleplay(table_title varchar(20),title varchar(50), title_URL varchar(100), imgURL varchar(100), description varchar(250), autor varchar(30), autor_URL varchar(100), star_rates varchar(20), price varchar(20), details varchar(10000), five_ratings varchar(20), four_ratings varchar(20), three_ratings varchar(20), two_ratings varchar(20), one_ratings varchar(20), category varchar(20), reviews varchar(5000), size varchar(20), installs varchar(20))')

    def close_spider(self, spider):  
        #sqlite
        self.con.commit()
        self.con.close()     

        #json
        #with open(fileName, 'r') as f:
            #content = f.read()
        #with open(fileName, 'w') as f:
            #f.write( content[:-1] + "\n]" )        
     
    def process_item(self, item, spider):  
        #sqlite
        col = ','.join(item.keys())
        placeholders = ','.join(len(item) * '?')
        sql = 'INSERT INTO googleplay({}) values({})'          
        self.cur.execute( sql.format(col,placeholders), tuple(item.values()) )        

        #json
        #line = json.dumps(dict(item), ensure_ascii = False, indent = 4 ) + ','  
        #with open(fileName, 'wb') as f:
             #f.write( line.encode('utf8') ) 
        return item  
    
