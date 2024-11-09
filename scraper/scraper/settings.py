from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from shutil import which

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

DOWNLOAD_TIMEOUT = 120
RETRY_TIMES = 2
DOWNLOAD_FAIL_ON_DATALOSS = False

# AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 10

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = 'httpcache'

# Selenium configuration with GPU acceleration
SELENIUM_DRIVER_EXECUTABLE_PATH = which("C:/Webdriver/chromedriver.exe")
SELENIUM_DRIVER_SERVICE = Service(executable_path=SELENIUM_DRIVER_EXECUTABLE_PATH)
# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--enable-webgl')
chrome_options.add_argument('--disable-software-rasterizer')

# Set up Selenium driver kwargs
SELENIUM_DRIVER_KWARGS = {
    'service': SELENIUM_DRIVER_SERVICE,
    'options': chrome_options
}