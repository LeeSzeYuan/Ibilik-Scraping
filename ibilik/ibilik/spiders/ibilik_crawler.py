import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import IbilikItem

class IbilikCrawlerSpider(scrapy.Spider):
    name = 'ibilik_crawler'
    page_number = 2
    start_urls = [
        'https://www.ibilik.my/rooms/malaysia'
    ]

    def parse(self, response):
        # open_in_browser(response)

        items = IbilikItem()

        home_list_div = response.css('div.home-list-pop')

        for home in home_list_div:
            name = home.css('h3').css('::text').extract()
            price = home.css('.room_price span').css('::text').extract()
            location = home.css('.lightblue a').css('::text').extract()[0].strip()
            
            view = home.css('.home-list-pop-rat').css('::text').extract()

            try:
                type = home.css('p:nth-child(3)').css('::text').extract()[1].strip()
                ammenity = home.css('p:nth-child(4)').css('::text').extract()[1].strip()
            except:
                try :
                    type = home.css('p:nth-child(2)').css('::text').extract()[1].strip()
                    ammenity = home.css('p:nth-child(3)').css('::text').extract()[1].strip()
                except:
                    ammenity = ""

            items["name"] = name
            items["price"] = price
            items["location"] = location
            items["type"] = type
            items["view"] = view
            items["ammenity"] = ammenity

            yield items

        

        next_page = f'https://www.ibilik.my/rooms/malaysia?page={IbilikCrawlerSpider.page_number}'

        if IbilikCrawlerSpider.page_number < 501:
            IbilikCrawlerSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)
