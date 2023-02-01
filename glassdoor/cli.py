import os

import click
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from glassdoor import glassdoor_spider


@click.command()
def main():
    os.environ["SCRAPY_SETTINGS_MODULE"] = "glassdoor.settings"
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(glassdoor_spider.GlassdoorSpider)
    process.start()


if __name__ == "__main__":  # pragma: no cover
    main()  # pylint: disable=no-value-for-parameter
