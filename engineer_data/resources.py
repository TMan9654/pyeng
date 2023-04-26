
# Structural Data
HSS_PROFILES = {  # (Height [in], Width [in], Thickness [in])
    "HSS 10X4X3/16": (10, 4, 0.1875),
    "HSS 10X4X0.1875": (10, 4, 0.1875),
    "HSS 10X4X1/4": (10, 4, 0.25),
    "HSS 10X4X0.25": (10, 4, 0.25),
    "HSS 10X4X3/8": (10, 4, 0.375),
    "HSS 10X4X0.375": (10, 4, 0.375)
}
STRUCTURAL_MATERIALS = {  # (Tensile Strength [psi], Yield Strength [psi], Density [lb/in³], Elastic Modulus [psi])
    "PLAIN CARBON STEEL": (57989.8585, 31994.4547, 0.2817927981, 30457924.91),
    "POLYCARBONATE 30CF": (47891.42849, 18857.14296, 0.0517000013, 5059999.881)
}
STRUCTURAL_SUPPORTS = {
    "PIN": (0, 0, 1),
    "FIX": (0, 0, 0),
    "ROLLER": (1, 0, 1),
    "SPRING": (0, 0, 0)
}

# Unit Systems
# (length, mass, force, strength, u_length, u_area, u_volume, u_inertia, u_mass, u_strength, u_PLoad, u_PLoad, u_QLoad)
UNIT_SYSTEMS = {
    "IMPERIAL [IN]": ("in", "in²", "in³", "in⁴", "lb", "psi", "lbf", "lbf/in"),
    "IMPERIAL [FT]": ("ft", "ft²", "ft³", "ft⁴", "lb", "psi", "lbf", "lbf/ft"),
    "METRIC [MM]": ("mm", "mm²", "mm³", "mm⁴", "kg", "kPa", "N", "N/m"),
    "METRIC [M]": ("m", "m²", "m³", "m⁴", "kg", "MPa", "kN", "kN/m")
}

# Fluids Data
FLUID_MATERIALS = {  # (Density [slugs/ft³], )
    "WATER": (1.94,)
}
