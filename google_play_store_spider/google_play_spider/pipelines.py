# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
 
import sqlite3

db = 'googleplay.db'

class GooglePlaySpiderPipeline(object):
    def __init__(self):  
        pass
    
    def open_spider(self, spider):
        #sqlite
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute('DROP TABLE IF EXISTS googleplay')
        self.cur.execute('create table if not exists googleplay(table_title varchar(20),title varchar(50), title_URL varchar(100), imgURL varchar(100), description varchar(250), autor varchar(30),      autor_URL varchar(100), star_rates varchar(20))')

    def close_spider(self, spider):  
        #sqlite
        self.con.commit()
        self.con.close()           
     
    def process_item(self, item, spider):  
        #sqlite
        col = ','.join(item.keys())
        placeholders = ','.join(len(item) * '?')
        sql = 'INSERT INTO googleplay({}) values({})'          
        self.cur.execute( sql.format(col,placeholders), tuple(item.values()) )        

        return item  
    
