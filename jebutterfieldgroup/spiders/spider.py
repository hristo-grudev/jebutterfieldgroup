import scrapy

from scrapy.loader import ItemLoader

from ..items import JebutterfieldgroupItem
from itemloaders.processors import TakeFirst


class JebutterfieldgroupSpider(scrapy.Spider):
	name = 'jebutterfieldgroup'
	start_urls = ['https://www.je.butterfieldgroup.com/News/Pages/default.aspx?Year=2021']

	def parse(self, response):
		post_links = response.xpath('//tr[@class="default"]')
		for post in post_links:
			url = post.xpath('.//div[@class="item link-item bullet"]/a/@href').get()
			date = post.xpath('.//td[@class="default bottomBorderdot padL7"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

		next_page = response.xpath('//td[contains(@class, "newsYear")]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//*[(@id = "WebPartWPQ2")]//td//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=JebutterfieldgroupItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
