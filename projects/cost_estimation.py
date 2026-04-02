def estimate_cost(room_type, room_size_sqft, material_quality, design_style):
    base_rates = {
        'living_room': 800,
        'bedroom': 700,
        'kitchen': 1200,
        'office': 900,
        'bathroom': 1000,
    }

    material_multiplier = {
        'basic': 1.0,
        'standard': 1.5,
        'premium': 2.0,
    }

    style_multiplier = {
        'minimalist': 1.0,
        'modern': 1.3,
        'classic': 1.5,
        'bohemian': 1.2,
        'industrial': 1.4,
    }

    base_rate = base_rates.get(room_type, 800)
    mat_mult = material_multiplier.get(material_quality, 1.0)
    style_mult = style_multiplier.get(design_style, 1.0)

    estimated_cost = base_rate * room_size_sqft * mat_mult * style_mult
    return round(estimated_cost, 2)