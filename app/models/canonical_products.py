from app import db

class CanonicalProduct(db.Model):
    __tablename__ = 'canonical_products'
    
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<CanonicalProduct {self.brand} {self.name}>'