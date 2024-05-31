# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
import psycopg2


class ScrapingPipeline:
    def process_item(self, item, spider):
        try:
            price_usd = int(item["price_usd"].replace(" ", "").replace("$", "").replace(",", "."))
            item["price_usd"] = price_usd
        except:
            item["price_usd"] = 0
        try:    
            item["odometer"] = int(item["odometer"]) * 1000
        except:
            item["odometer"] = 0
        return item

class DatabasePipiline:
    
    def open_spider(self, spider):
        settings = get_project_settings()
        hostname = settings.get("DB_HOST")
        username = settings.get("DB_USER")
        database = settings.get("DB_NAME")
        password = settings.get("DB_PASSWORD")
        
        self.connection = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database,
        )
        self.cursor = self.connection.cursor()
        
    def process_item(self, item, spider):
        
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Autoria (
                    id serial PRIMARY KEY,
                    url VARCHAR(2038),
                    title VARCHAR(255),
                    price_usd int,
                    odometer int,
                    username VARCHAR(255),
                    phone_number TEXT [],
                    image_url TEXT [],
                    images_count int,
                    car_number VARCHAR(255),
                    car_vin VARCHAR(255),
                    datetime_found timestamp default current_timestamp
                    )
                """
                
                )
            self.cursor.execute(
                """
                INSERT INTO Autoria (
                    url,
                    title,
                    price_usd,
                    odometer,
                    username,
                    phone_number,
                    image_url,
                    images_count,
                    car_number,
                    car_vin
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                """, (
                    item["url"],
                    item["title"],
                    item["price_usd"],
                    item["odometer"],
                    item["username"],
                    item["phone_number"],
                    item["image_url"],
                    item["images_count"],
                    item["car_number"],
                    item["car_vin"]
                ))
            self.connection.commit()
        except psycopg2.Error:
            self.connection.rollback()
        
        return item
        
    
    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()