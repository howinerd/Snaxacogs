def normalize_price(package_price, shipping_cost, units_per_pack, unit_size_oz, 
                    threshold_price_per_unit, target_price_per_unit):
    """
    Normalize pricing data according to our standard calculations
    """
    total_cost = package_price + shipping_cost
    price_per_unit = total_cost / units_per_pack
    price_per_oz = total_cost / (units_per_pack * unit_size_oz)
    price_vs_threshold = threshold_price_per_unit - price_per_unit
    price_vs_target = target_price_per_unit - price_per_unit
    
    return {
        'total_cost': total_cost,
        'price_per_unit': price_per_unit,
        'price_per_oz': price_per_oz,
        'price_vs_threshold': price_vs_threshold,
        'price_vs_target': price_vs_target
    }