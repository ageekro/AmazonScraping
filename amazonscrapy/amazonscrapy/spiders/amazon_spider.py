# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonscrapyItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_number = 2
    start_urls = [
        'https://www.amazon.com/s?k=apple+laptop&i=computers&rh=p_n_condition-type%3A2224371011&dc&crid=1X9IZHPHOQXLM'
        '&qid=1563256213&rnid=2224369011&sprefix=apple%2Caps%2C400&ref=sr_nr_p_n_condition-type_1 '
    ]

    def parse(self, response):
        items = AmazonscrapyItem()

        product_name = response.css(".a-color-base.a-text-normal::text").extract()
        product_like = response.css(".a-size-small .a-size-base").css("::text").extract()
        product_price = response.css(".a-spacing-top-mini:nth-child(1) .a-color-base , .a-price:nth-child(1) "
                                     ".a-price-whole").css("::text").extract()
        product_imagelink = response.css(".s-image-fixed-height .s-image").css("::attr(src)").extract()

        items["name"] = product_name
        items["like"] = product_like
        items["price"] = product_price
        items["imagelink"] = product_imagelink

        yield items

        next_page = "https://www.amazon.com/s?k=apple+laptop&i=computers&rh=p_n_condition-type%3A2224371011&dc&page=" + str(AmazonSpiderSpider.page_number) + "&crid=1X9IZHPHOQXLM&qid=1563275332&rnid=2224369011&sprefix=apple%2Caps%2C400&ref=sr_pg_3 "

        if AmazonSpiderSpider.page_number <= 3:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
