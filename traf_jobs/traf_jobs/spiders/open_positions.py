import scrapy
from scrapy_playwright.page import PageMethod


class OpenPositionsSpider(scrapy.Spider):
    name = "open_positions"
    allowed_domains = ["trafigura.com"]
    start_urls = ["https://careers.trafigura.com/TrafiguraCareerSite/search"]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright = True,
                playwright_page_methods = [
                    PageMethod("wait_for_selector", "section#results div[role='list']"),
                    PageMethod("evaluate", """
                               
                        const interval_id = setInterval(function(){
                            const button = document.querySelector('div.py-3.ng-star-inserted > button');

                            if (button) {
                                button.scrollIntoView();
                                button.click();
                            } else {
                                clearInterval(interval_id);
                            }
                        }, 1000);
                        """),
                    PageMethod("wait_for_selector", "div.py-3.ng-star-inserted > button", state="detached"),
                    
                ]
            )
        )
            
        #button_selector: str = div.py-3.ng-star-inserted > button
        

    async def parse(self, response):
        for job in response.css('div[role="list"] div[role="listitem"]'):
            yield {
                'title': job.css('a::text').get()
            }
        
