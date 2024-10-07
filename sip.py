"""Scrapy crawler to test the performance of CrawlSpider"""
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

class SipSpider(CrawlSpider):
    """Spider to scrape Whiskey data from sipwhiskey.com"""
    name = 'sip'
    allowed_domains = ['sipwhiskey.com']
    start_urls = ['https://sipwhiskey.com/']

    # Main page # https://sipwhiskey.com/collections/alcohol
    # Product (Item) # https://sipwhiskey.com/collections/alcohol/products/blantons-single-barrel-bourbon-700ml

    rules=(
        Rule(LinkExtractor(allow='collections/alcohol',deny=['products'])),
        Rule(LinkExtractor(allow='products'), callback='parse_items')
    )

    def parse_items(self, response):
        """Parse product details"""
        # Extract product details and yield item
        yield {
            'product_title': response.css('h1.title::text').get(),
            'brand': response.css('div.vendor a::text').get(),
            'product_price': response.css('span.price::text').get(),
        }

# Create a CrawlerProcess and start the spider
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "output.json": {"format": "json"},
        },
        "LOG_LEVEL": "INFO",  # Optional: Set logging level to "INFO" to reduce verbosity
    })
    process.crawl(SipSpider)
    process.start()  # Start the crawling process