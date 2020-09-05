import scrapy
import os
import sqlite3


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://javpop.com/tag/%e3%83%a1%e3%83%ad%e3%83%87%e3%82%a3%e3%83%bc%e3%83%bb%e9%9b%9b%e3%83%bb%e3%83%9e%e3%83%bc%e3%82%af%e3%82%b9',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        tarent_name = response.xpath('/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/h2[1]').get()

        art_links = response.xpath('/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/ul[1]/li[9]/a').getall()

# ここから違うページ
        name = response.xpath('/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/h1[1]').get()
        image = response.xpath('/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/p[1]/img[1]').get()

        download_links = response.xpath('/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/blockquote[5]/p/a').getall()

        art_num = response.url.split("/")[-1].split('.')[0]
        
        connection = sqlite3.connect(os.environ['SQLITEPATH'])

        cursor = connection.cursor()
        try:
            cursor.execute(
'''
// ステージ名が存在しなければ挿入する。
INSERT INTO tarent select where NOT EXISTS (SELECT * FROM WHERE stage_name = :id);
INSERT INTO javpop VALUES ((SELECT id FROM WHERE stage_name = :id),:art_title,:art_img);
INSERT INTO javpoplink VALUES (:id,:art_title,:art_img);
'''
            ,[1])
            cursor.commit()

        except sqlite3.Error as e:
            cursor.rollback()
            print(e)

        finally:
            cursor.close()
