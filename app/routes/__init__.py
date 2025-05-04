from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app import db
from app.models import CanonicalProduct, ProductVariant, VendorPrice, ScrapeJob, Alert
from app.scrapers.ebay_scraper import EbayScraper
# Import but don't instantiate yet
from app.services.alert_service import DiscordAlertService
from app.forms import CanonicalProductForm, ProductVariantForm
from datetime import datetime, timedelta
import os
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get counts for dashboard stats
    product_count = CanonicalProduct.query.count()
    deals_count = VendorPrice.query.filter(VendorPrice.price_vs_threshold > 0).count()
    recent_scrapes_count = ScrapeJob.query.filter(ScrapeJob.created_at > datetime.utcnow() - timedelta(days=1)).count()
    alerts_count = Alert.query.count()
    
    # Get data for dashboard widgets
    best_deals = VendorPrice.query.filter(VendorPrice.price_vs_threshold > 0).order_by(VendorPrice.price_vs_threshold.desc()).limit(5).all()
    recent_scrapes = ScrapeJob.query.order_by(ScrapeJob.created_at.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                           product_count=product_count,
                           deals_count=deals_count,
                           recent_scrapes_count=recent_scrapes_count,
                           alerts_count=alerts_count,
                           best_deals=best_deals,
                           recent_scrapes=recent_scrapes)

@main_bp.route('/products')
def products():
    products = CanonicalProduct.query.all()
    return render_template('products.html', products=products)

@main_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    form = CanonicalProductForm()
    
    if form.validate_on_submit():
        product = CanonicalProduct(
            brand=form.brand.data,
            name=form.name.data,
            category=form.category.data
        )
        db.session.add(product)
        db.session.commit()
        
        flash(f"Product '{product.brand} {product.name}' added successfully. Now add variants.", "success")
        return redirect(url_for('main.edit_product', product_id=product.id))
    
    return render_template('product_form.html', form=form)

@main_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = CanonicalProduct.query.get_or_404(product_id)
    form = CanonicalProductForm(obj=product)
    variant_form = ProductVariantForm()
    
    if form.validate_on_submit():
        product.brand = form.brand.data
        product.name = form.name.data
        product.category = form.category.data
        db.session.commit()
        
        flash(f"Product '{product.brand} {product.name}' updated successfully.", "success")
        return redirect(url_for('main.edit_product', product_id=product.id))
    
    return render_template('product_form.html', form=form, variant_form=variant_form, product=product)

@main_bp.route('/products/<int:product_id>/variants/add', methods=['POST'])
def add_variant(product_id):
    product = CanonicalProduct.query.get_or_404(product_id)
    form = ProductVariantForm()
    
    if form.validate_on_submit():
        variant = ProductVariant(
            canonical_product_id=product.id,
            flavor=form.flavor.data,
            unit_size_oz=form.unit_size_oz.data,
            units_per_pack=form.units_per_pack.data,
            upc=form.upc.data,
            threshold_price_per_unit=form.threshold_price_per_unit.data,
            target_price_per_unit=form.target_price_per_unit.data
        )
        db.session.add(variant)
        db.session.commit()
        
        flash(f"Variant {variant.unit_size_oz}oz {variant.units_per_pack}-pack added successfully.", "success")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "danger")
    
    return redirect(url_for('main.edit_product', product_id=product.id))

@main_bp.route('/deals')
def deals():
    deals = VendorPrice.query.filter(VendorPrice.price_vs_threshold > 0).order_by(VendorPrice.price_vs_threshold.desc()).all()
    return render_template('deals.html', deals=deals)

@main_bp.route('/scrape/<int:variant_id>')
def scrape_product(variant_id):
    variant = ProductVariant.query.get_or_404(variant_id)
    scraper = EbayScraper()
    
    try:
        prices = scraper.scrape_product(variant)
        flash(f"Successfully scraped {len(prices)} prices for {variant.product.brand} {variant.product.name}", "success")
        return redirect(url_for('main.edit_product', product_id=variant.canonical_product_id))
    except Exception as e:
        flash(f"Error scraping: {str(e)}", "danger")
        return redirect(url_for('main.edit_product', product_id=variant.canonical_product_id))