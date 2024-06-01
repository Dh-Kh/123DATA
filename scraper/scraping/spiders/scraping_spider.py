import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from ..items import ScrapingItem
from selenium.common.exceptions import TimeoutException


class ScrapingSpiderSpider(scrapy.Spider):

    name = "scraping_spider"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/legkovie/?page=%d" % i for i in range(1, 2)]
    handle_httpstatus_list = [404,403]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                errback=self.errback_httpbin,
                dont_filter=True
            )
            

    def parse(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        item = ScrapingItem()
        driver = response.request.meta["driver"]
        wait = WebDriverWait(driver, 3)
        action = ActionChains(driver)
        urls = response.xpath('//div[@class="item ticket-title"]/a/@href').getall()
        for i in range(len(urls)):
            driver.get(urls[i])
            item["url"] = urls[i]
            title = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//div[@class="heading"]/h1[@class="head"]'
            )))
            item["title"] = title.text
            price_usd = wait.until(EC.visibility_of_element_located((
                 By.XPATH, '//div[@class="price_value"]/strong'   
            )))
            item["price_usd"] = price_usd.text
            try:
                odometer = wait.until(EC.visibility_of_element_located((
                    By.XPATH, '//div[@class="base-information bold"]/span[@class="size18"]'
                )))
                item["odometer"] = odometer.text
            except TimeoutException:
                item["car_mileage"] = 0
            try:
                username = wait.until(EC.visibility_of_element_located((
                    By.XPATH, '//div[@class="seller_info_name bold"]'
                )))
            except TimeoutException:
                username = wait.until(EC.visibility_of_element_located((
                    By.XPATH, '//h4[@class="seller_info_name"]/a'
                )))
            item["username"] = username.text
            hidden_phone_numbers = wait.until(EC.presence_of_all_elements_located((
                 By.XPATH, '//div[@class="phones_item "]/span[@class="phone bold"]'   
            )))
            driver.execute_script("arguments[0].click();", hidden_phone_numbers[0])
            phone_number = wait.until(EC.presence_of_all_elements_located((
                By.XPATH, '//div[@class="item-field list-phone"]/a'
            )))
            phone_stack = []
            for y in range(len(phone_number)):
                data_value = phone_number[y].get_attribute("data-value")
                phone_stack.append(data_value)
            action.move_by_offset(10, 10).click().perform()
            item["phone_number"] = phone_stack
            try:
                car_vin = wait.until(EC.visibility_of_element_located((
                    By.XPATH, '//span[@class="label-vin"]'    
                )))
                item["car_vin"] = car_vin.text
            except TimeoutException:
                item["car_vin"] = "No vin"
            try:
                car_number = wait.until(EC.visibility_of_element_located((
                     By.XPATH, '//span[@class="state-num ua"]'   
                )))
                item["car_number"] = car_number.text
            except TimeoutException:
                item["car_number"] = "No number"
            image_url = wait.until(EC.presence_of_all_elements_located((
                By.XPATH, '//div[@class="wrapper"]/a/picture/img'    
            )))
            images_stack = []  
            for y in range(len(image_url)):
                src_value = image_url[y].get_attribute("src")
                images_stack.append(src_value)
            item["image_url"] = images_stack
            item["images_count"] = len(images_stack)
            yield item
            
    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
