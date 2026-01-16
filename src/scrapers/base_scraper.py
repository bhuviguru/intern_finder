from abc import ABC, abstractmethod
import logging

class BaseScraper(ABC):
    def __init__(self, browser_instance=None):
        self.browser = browser_instance
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def scrape(self, keywords):
        """
        Scrape jobs based on keywords.
        Should return a list of job dictionaries.
        """
        pass
    
    def set_browser(self, browser):
        self.browser = browser
