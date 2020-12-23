import scrapy
from scrapy.loader import ItemLoader
from Toyokeizai.items import Article


class ToyoSpider(scrapy.Spider):
    name = 'toyo'
    allowed_domains = ['toyokeizai.net']
    handle_httpstatus_list = [301]
    start_urls = ['https://toyokeizai.net/list/ranking', 'https://toyokeizai.net/list/ranking-24hour',
                  'https://toyokeizai.net/list/ranking-weekly', 'https://toyokeizai.net/list/ranking-monthly', ]

    def parse(self, response):
        links = response.xpath(
            "//div[@class='article-list ranking']/ul/li/div[@class='ttl small']/a/@href").getall()
        yield from response.follow_all(links, callback=self.parse_article)

    def parse_article(self, response):
        article = ItemLoader(item=Article(), response=response)

        # Fill in all properties via XPath
        article.add_xpath('title', '//h1/text()')
        article.add_xpath('subtitle', "//h2/text()")
        article.add_xpath('author', "(//div[@class='author']//a)[1]//text()")
        article.add_xpath('date', "//div[@id='article-body']//div[@class='date']/descendant-or-self::*/text()")
        text = response.xpath("//div[@id='article-body-inner']/descendant-or-self::*/text()").getall()
        text = ' '.join(text).strip()
        text = ' '.join(text.split())
        article.add_value('text', text)
        return article.load_item()
