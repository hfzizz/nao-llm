import scrapy
from scrapy_selenium import SeleniumRequest
from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime

class UBDTextSpider(scrapy.Spider):
    name = "website_scraper"

    start_urls = [
        'https://sds.ubd.edu.bn/',
        'https://ubd.edu.bn/',
        'https://expert.ubd.edu.bn/'
        'https://borneobulletin.com.bn/'
        'https://www.bruneitourism.com/'
        'https://en.wikipedia.org/wiki/Brunei'
    ]
    

    allowed_domains = ['sds.ubd.edu.bn', 'ubd.edu.bn', 'expert.ubd.edu.bn' ,'borneobulletin.com.bn', 'bruneitourism.com','wikipedia.org']
    
    # Set to store visited URLs
    visited_urls = set()

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # Extract text content from the page
        page_text = " ".join(response.xpath('//body//text()').getall()).strip()

        yield {
            'url': response.url,
            'text': page_text
        }

        # Track visited URL
        self.visited_urls.add(response.url)

        # Recursively follow internal links within the same domain
        links = response.css('a::attr(href)').getall()
        for link in links:
            full_url = response.urljoin(link)
            # Check if URL is internal, not visited, and within date range if applicable
            if self.is_internal_link(full_url) and full_url not in self.visited_urls:
                if not self.has_unwanted_params(full_url) and self.is_valid_date(full_url):
                    self.visited_urls.add(full_url)
                    yield SeleniumRequest(url=full_url, callback=self.parse)

    def is_internal_link(self, url):
        """Check if the link is within the allowed domains."""
        parsed_url = urlparse(url)
        return parsed_url.netloc in self.allowed_domains

    def has_unwanted_params(self, url):
        """Check if URL contains unwanted query parameters (e.g., 'tribe-bar-date')."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        # Filter out URLs with 'tribe-bar-date' or other unwanted parameters
        return 'tribe-bar-date' in query_params

    def is_valid_date(self, url):
        """Check if the URL contains a valid date between 2020 and 2024."""
        # Regular expression to match URLs with date format (YYYY-MM-DD)
        date_pattern = re.compile(r'/(\d{4})-(\d{2})-(\d{2})/')
        match = date_pattern.search(url)

        if match:
            year = int(match.group(1))
            if 2020 <= year <= 2024:
                return True
            return False  # Exclude URLs outside the date range
        return True  # URLs without a date pattern are allowed