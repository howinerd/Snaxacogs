from app import db
from datetime import datetime
class CanonicalProduct(db.Model):
    __tablename__ = 'canonical_products'
    
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    variants = db.relationship('ProductVariant', backref='product', lazy=True)
    
    def get_best_price(self):
        """Get the best price per unit across all variants"""
        best_price = None
        for variant in self.variants:
            for price in variant.vendor_prices:
                if price.in_stock and (best_price is None or price.price_per_unit < best_price):
                    best_price = price.price_per_unit
        return best_price
    def has_deal(self):
        """Check if any variant has a price below threshold"""
        for variant in self.variants:
            for price in variant.vendor_prices:
                if price.in_stock and price.price_vs_threshold > 0:
                    return True
        return False
    
    def __repr__(self):
        return f'<CanonicalProduct {self.brand} {self.name}>'

class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    
    id = db.Column(db.Integer, primary_key=True)
    canonical_product_id = db.Column(db.Integer, db.ForeignKey('canonical_products.id'), nullable=False)
    flavor = db.Column(db.String(100))
    unit_size_oz = db.Column(db.Float, nullable=False)
    units_per_pack = db.Column(db.Integer, nullable=False)
    upc = db.Column(db.String(50))
    threshold_price_per_unit = db.Column(db.Float, nullable=False)
    target_price_per_unit = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    vendor_prices = db.relationship('VendorPrice', backref='variant', lazy=True)
    
    def __repr__(self):
        return f'<ProductVariant {self.id}: {self.unit_size_oz}oz {self.units_per_pack}-pack>'

class VendorPrice(db.Model):
    __tablename__ = 'vendor_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'), nullable=False)
    vendor_name = db.Column(db.String(100), nullable=False)
    vendor_item_id = db.Column(db.String(100))
    vendor_url = db.Column(db.String(500))
    package_price = db.Column(db.Float, nullable=False)
    shipping_cost = db.Column(db.Float, default=0.0)
    total_cost = db.Column(db.Float, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    price_per_oz = db.Column(db.Float, nullable=False)
    price_vs_threshold = db.Column(db.Float, nullable=False)
    price_vs_target = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    scrape_job_id = db.Column(db.Integer, db.ForeignKey('scrape_jobs.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<VendorPrice {self.vendor_name}: ${self.price_per_unit:.2f} per unit>'

class ScrapeJob(db.Model):
    __tablename__ = 'scrape_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'))
    vendor_name = db.Column(db.String(100))
    status = db.Column(db.String(20), default='queued')  # queued, in_progress, completed, failed
    error_message = db.Column(db.Text)
    response_code = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    vendor_prices = db.relationship('VendorPrice', backref='scrape_job', lazy=True)
    
    def __repr__(self):
        return f'<ScrapeJob {self.id}: {self.status}>'

class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'), nullable=False)
    vendor_price_id = db.Column(db.Integer, db.ForeignKey('vendor_prices.id'), nullable=False)
    vendor_name = db.Column(db.String(100), nullable=False)
    threshold_price = db.Column(db.Float, nullable=False)
    alert_price = db.Column(db.Float, nullable=False)
    alert_channel = db.Column(db.String(50), default='discord')
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_status = db.Column(db.String(20), default='sent')  # sent, failed
    
    product_variant = db.relationship('ProductVariant', backref='alerts', lazy=True)
    vendor_price = db.relationship('VendorPrice', backref='alerts', lazy=True)
    
    def __repr__(self):
        return f'<Alert for {self.product_variant_id} at ${self.alert_price:.2f}>'