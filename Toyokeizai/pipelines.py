# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import datetime


class UnwrapPipeline:
    def process_item(self, item, spider):
        # ItemLoader gets all items as lists; set the property to the first value to remove them from the lists

        item['title'] = item.get('title')[0]
        item['subtitle'] = item.get('subtitle')[0]
        item['author'] = item.get('author')[0]
        item['date'] = item.get('date')[0]
        item['text'] = item.get('text')[0]

        return item


class PrintPipeline:
    def process_item(self, item, spider):
        # Prints all items; For testing purposes

        print(item.get('title'))
        print(item.get('subtitle'))
        print(item.get('author'))
        print(item.get('date'))
        print("--------------------------------------")
        print(item.get('text'))
        print("--------------------------------------")
        return item


class DatabasePipeline:
    # Database setup
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute(""" CREATE TABLE IF NOT EXISTS articles 
        (title text, subtitle text, author text, date text, content text) """)

        self.conn.commit()

    def process_item(self, item, spider):
        # Insert values

        self.c.execute("SELECT title FROM articles")
        titles = self.c.fetchall()
        titles = [title[0] for title in titles]
        if item.get('title') in titles:
            return item

        self.c.execute("INSERT INTO articles (title, subtitle, author, date, content) VALUES (?,?,?,?,?)", (
            item.get('title'), item.get('subtitle'), item.get('author'), item.get('date'), item.get('text')))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # Save and close database
        self.conn.close()
