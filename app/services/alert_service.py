import requests
import json

class DiscordAlertService:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        
    def send_price_alert(self, product_variant, vendor_price, vendor_name, product_url):
        """Send price alert to Discord webhook"""
        embed = {
            "title": f"Price Alert: {product_variant.brand} {product_variant.name}",
            "description": f"Price dropped below threshold!",
            "color": 5814783,  # Green color
            "fields": [
                {"name": "Product", "value": f"{product_variant.brand} {product_variant.name}", "inline": True},
                {"name": "Variant", "value": f"{product_variant.unit_size_oz}oz {product_variant.units_per_pack}-pack", "inline": True},
                {"name": "Vendor", "value": vendor_name, "inline": True},
                {"name": "Price Per Unit", "value": f"${vendor_price.price_per_unit:.2f}", "inline": True},
                {"name": "Total Price", "value": f"${vendor_price.total_cost:.2f}", "inline": True},
                {"name": "Threshold", "value": f"${product_variant.threshold_price_per_unit:.2f}", "inline": True},
                {"name": "Savings vs Threshold", "value": f"${vendor_price.price_vs_threshold:.2f} per unit", "inline": False}
            ],
            "url": product_url
        }
        
        payload = {
            "embeds": [embed],
            "username": "Snaxa Price Alerts"
        }
        
        response = requests.post(
            self.webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        
        return response.status_code == 204