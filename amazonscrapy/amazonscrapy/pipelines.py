# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Scraped data -> Item Containers -> Json/csv Files # scrapy crawl example -o name.json/csv/xml
# Scraped data -> Item Containers -> pipeline -> SQL/Mongo database
import sqlite3

class AmazonscrapyPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("products.db")
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS products_tb""")
        self.cursor.execute("""CREATE TABLE products_tb(
                            name TEXT,
                            like INT,
                            price INT,
                            imagelink TEXT
                            )""")

    def store_db(self, item):
        self.cursor.execute("""INSERT INTO products_tb VALUES (?,?,?,?)""",
                            (item["name"][0], item["like"][0], item["price"][0],item["imagelink"][0]))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item