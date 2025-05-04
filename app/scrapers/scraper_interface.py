from abc import ABC, abstractmethod

class ScraperInterface(ABC):
    """Base interface for all vendor scrapers"""
    
    @abstractmethod
    def scrape_product(self, product_variant, **kwargs):
        """
        Scrape pricing information for a product variant
        Returns a list of vendor_price objects
        """
        pass
        
    @abstractmethod
    def is_in_stock(self, listing_data):
        """
        Determine if a product listing is in stock
        Returns boolean
        """
        pass