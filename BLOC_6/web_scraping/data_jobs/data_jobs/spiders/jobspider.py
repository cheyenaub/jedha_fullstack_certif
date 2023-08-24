import scrapy
from scrapy import FormRequest


class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["www.hellowork.com"]
    start_urls = ["https://www.hellowork.com/fr-fr/emploi/recherche.html?k=data&l=France&p={}".format(page+1) for page in range(601)]


    def parse(self, response):
        jobs_links = response.css('a.md\:tw-text-xlOld::attr(href)').getall()
        for link in jobs_links:
            absolute_url = response.urljoin(link)
            yield scrapy.Request(absolute_url, callback=self.parse_job_details)
            
    def parse_job_details(self, response):
        
        try:
            yield {
                'job_title' : response.xpath('/html/body/section[2]/h1/span/text()').get(),
                'job_location' : response.xpath('/html/body/main/section[1]/section[3]/ul[1]/li[1]').get(),
                'job_company' : response.xpath('/html/body/section[2]/h1/text()').get(),
                'job_description' : ''.join(response.css('p.tw-typo-long-m::text').getall()),
                'profile' : ''.join(response.xpath('/html/body/main/section[1]/section[5]/p/text()').getall()),
                'type' : response.xpath('/html/body/main/section[1]/section[7]/ul[1]/li[2]/text()').get(),
                'salary' : response.xpath('/html/body/main/section[1]/section[4]/ul[1]/li[4]/text()').get()
            }
            
        except Exception as e:
            yield {
                'title': None,
                'company': None,
                'description': None,
                'research': None,
                'type': None,
                'salary': None,
                'error': str(e)
            }
