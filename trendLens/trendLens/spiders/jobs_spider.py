import scrapy


class JobsSpiderSpider(scrapy.Spider):
    name = "jobs_spider"
    allowed_domains = ["indeed.com"]
    start_urls = ["https://www.indeed.com/jobs?q=software+developer&l=Remote&from=searchOnHP&vjk=723db8b2ccb25505"]

    def parse(self, response):
        pass
