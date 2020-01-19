class AmazonSetSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = ['https://www.amazon.in/s?i=amazon-devices&ref=nb_sb_noss']

    def parse(self, response):
        SET_SELECTOR = '.set'
        for AmazonSet in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h1 ::text'
            PRICE_SELECTOR = './/dl[dt/text() = "Price"]/dd/a/text()'
            RATINGS_SELECTOR = './/dl[dt/text() = "Ratings"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': AmazonSet.css(NAME_SELECTOR).extract_first(),
                'price': AmazonSet.xpath(PRICE_SELECTOR).extract_first(),
                'ratings': AmazonSet.xpath(RATINGS_SELECTOR).extract_first(),
                'image': AmazonSet.css(IMAGE_SELECTOR).extract_first(),
            }

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
