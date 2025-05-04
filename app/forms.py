from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class CanonicalProductForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('energy_drinks', 'Energy Drinks'),
        ('snacks', 'Snacks'),
        ('beverages', 'Beverages'),
        ('candy', 'Candy'),
        ('chips', 'Chips'),
        ('cookies', 'Cookies'),
        ('other', 'Other')
    ])
    submit = SubmitField('Save Product')

class ProductVariantForm(FlaskForm):
    flavor = StringField('Flavor', validators=[Optional()])
    unit_size_oz = FloatField('Size (oz)', validators=[DataRequired(), NumberRange(min=0.1)])
    units_per_pack = IntegerField('Units Per Pack', validators=[DataRequired(), NumberRange(min=1)])
    upc = StringField('UPC', validators=[Optional()])
    threshold_price_per_unit = FloatField('Threshold Price (per unit)', validators=[DataRequired(), NumberRange(min=0.01)])
    target_price_per_unit = FloatField('Target Price (per unit)', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Add Variant')