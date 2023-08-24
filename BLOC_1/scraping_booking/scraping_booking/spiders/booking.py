import scrapy


class BookingSpider(scrapy.Spider):
    name = "booking"
    # offset parameter to get hotels from all pages
    offsets = range(0, 125, 25)
    allowed_domains = ['booking.com']
    # url of the top 5 cities 
    start_urls = [
        "https://www.booking.com/searchresults.fr.html?ss=Les+Saintes-Maries-de-la-Mer&ssne=Les+Saintes-Maries-de-la-Mer&ssne_untouched=Les+Saintes-Maries-de-la-Mer&nflt=ht_id%3D204&offset={}".format(offset) for offset in offsets
    ] + [
    "https://www.booking.com/searchresults.fr.html?ss=Marseille&ssne=Marseille&ssne_untouched=Marseille&nflt=ht_id%3D204&offset={}".format(offset) for offset in offsets
    ] + [
    "https://www.booking.com/searchresults.fr.html?ss=Lille%2C+Nord-Pas-de-Calais%2C+France&ssne=Lille%2C+Nord-Pas-de-Calais%2C+France&ssne_untouched=Lille%2C+Nord-Pas-de-Calais%2C+France&nflt=ht_id%3D204&offset={}".format(offset) for offset in offsets
    ] + [
    "https://www.booking.com/searchresults.fr.html?ss=Aigues-Mortes%2C+Languedoc-Roussillon%2C+France&ssne=Aigues-Mortes%2C+Languedoc-Roussillon%2C+France&ssne_untouched=Aigues-Mortes%2C+Languedoc-Roussillon%2C+France&nflt=ht_id%3D204&offset={}".format(offset) for offset in offsets
    ] + [
    "https://www.booking.com/searchresults.fr.html?ss=La+Rochelle%2C+Poitou-Charentes%2C+France&ssne=La+Rochelle%2C+Poitou-Charentes%2C+France&ssne_untouched=La+Rochelle%2C+Poitou-Charentes%2C+France&nflt=ht_id%3D204&offset={}".format(offset) for offset in offsets
]
    # Function to get the links of all hotels 
    def parse(self, response):
        hotel_links = response.css('a.e13098a59f::attr(href)').getall()
        for link in hotel_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_job_details)

    # Function to be applied for each hotel link retrieve
    def parse_job_details(self, response):
        
        try:
            yield {
                'hotel_name' : response.xpath('//*[@id="hp_hotel_name"]/div/h2/text()').get(),
                'url' : response.css('a.bui_breadcrumb__link_masked::attr(href)').get(),
                'coordinates' : response.css('a#hotel_header::attr(data-atlas-latlng)').get(),
                'score' : response.xpath('//div[@class="a3b8729ab1 d86cee9b25"]/text()').get(),
                'description' : response.xpath('//*[@id="property_description_content"]/div/p/text()').get(),
                'city' : response.xpath('//*[@id="showMap2"]/span[1]/text()').get()
            }
            
        except Exception as e:
            yield {
                'hotel_name': None,
                'url': None,
                'coordinates': None,
                'score': None,
                'description': None,
                'city' : None,
                'error': str(e)
            }
