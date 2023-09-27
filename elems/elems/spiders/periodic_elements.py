import scrapy
from elems.items import PeriodicElemsItem
from scrapy.loader import ItemLoader
from scrapy_playwright.page import PageMethod



class PeriodicElementsSpider(scrapy.Spider):
    name = "periodic_elements"
    
    def start_requests(self):
        yield scrapy.Request(url='https://pubchem.ncbi.nlm.nih.gov/ptable', meta=dict(
            playwright=True,
            playwright_page_methods  = [
                PageMethod('wait_for_selector', 'div.ptable')
            ]
        ))

    async def parse(self, response):
        for element in response.css("div.ptable div.element"):
            i = ItemLoader(item=PeriodicElemsItem(), selector=element)
            i.add_css('name', '[data-tooltip = "Name"]')
            i.add_css('symbol', '[data-tooltip = "Symbol"]')
            i.add_css('atomic_number', '[data-tooltip = "Atomic Number"]')#exact
            i.add_css('atomic_mass', '[data-tooltip *= "Atomic Mass"]')#contains
            i.add_css('chemical_group', '[data-tooltip = "Chemical Group Block"]')

            yield i.load_item()
            
