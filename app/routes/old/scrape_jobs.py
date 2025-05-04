 
from flask import Blueprint, render_template, request, redirect, url_for, flash

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
def index():
    return render_template('products/index.html')