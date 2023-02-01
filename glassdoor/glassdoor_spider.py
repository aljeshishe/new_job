import logging

import scrapy
# v.platformTrust = lambda: None
from glassdoor.request import GetCsrfRequest

from glassdoor.state import State

log = logging.getLogger(__name__)


class GlassdoorSpider(scrapy.Spider):
    name = 'airbnb'
    url = "https://www.glassdoor.com/graph"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = State()

    def start_requests(self):
        yield GetCsrfRequest(state=self.state)
