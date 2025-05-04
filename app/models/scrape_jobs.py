 
from app import db

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
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    vendor_prices = db.relationship('VendorPrice', backref='variant', lazy=True)
    
    def __repr__(self):
        return f'<ProductVariant {self.id}: {self.unit_size_oz}oz {self.units_per_pack}-pack>'