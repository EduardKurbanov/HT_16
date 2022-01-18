# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# from news_about_events.settings import FEED_EXPORT_FIELDS

from scrapy import signals
import sqlite3

DEFAULT_NAME = "default_table"


class NewsAboutEventsPipeline:
    def __init__(self):
        self.filename: str = None

    def create_table(self, db_name: str):
        self.cur.execute(f"""DROP TABLE IF EXISTS {DEFAULT_NAME}""")
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {DEFAULT_NAME}(
            header TEXT,
            text_news TEXT,
            tag TEXT,
            link TEXT
        )""")

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    #
    def spider_opened(self, spider):
        self.con = sqlite3.connect("vikka_news_db.db")
        self.cur = self.con.cursor()
        self.create_table(self.filename)

    def spider_closed(self, spider):
        self.cur.execute(f"""ALTER TABLE {DEFAULT_NAME} RENAME TO DATE_{self.filename}""")
        self.con.close()

    def process_item(self, item, spider):
        self.filename = item["date"]
        self.cur.execute(f"""INSERT INTO {DEFAULT_NAME} VALUES(?,?,?,?)""",
                         (
                             str(item["header"]).encode("utf-8"),
                             str(item["text"]).encode("utf-8"),
                             str(item["tag"]).encode("utf-8"),
                             str(item["link"]).encode("utf-8")
                         ))
        self.con.commit()
        return item
