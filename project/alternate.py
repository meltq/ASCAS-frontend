from typing import List, Dict


def generate_orbital_variations(base_a: float, base_e: float, variations: int = 4) -> List[Dict]:
    """
    Generate different possible orbital equations by varying parameters

    Args:
        base_a: Base semi-major axis (km)
        base_e: Base eccentricity
        variations: Number of variations to generate

    Returns:
        List of dictionaries containing orbital equations and their parameters
    """
    MIN_ALTITUDE = 200
    EARTH_RADIUS = 6378
    MAX_E = 0.9

    min_a = EARTH_RADIUS + MIN_ALTITUDE

    equations = []

    equations.append({
        'name': 'Base Orbit',
        'parameters': {
            'semi_major_axis': base_a,
            'eccentricity': base_e
        },
        'equation': f'r = {base_a}(1 - {base_e}²)/(1 + {base_e}cos(θ))',
        'periapsis': base_a * (1 - base_e),
        'apoapsis': base_a * (1 + base_e)
    })

    higher_a = base_a * 1.5
    equations.append({
        'name': 'Higher Circular Orbit',
        'parameters': {
            'semi_major_axis': higher_a,
            'eccentricity': 0
        },
        'equation': f'r = {higher_a}',
        'periapsis': higher_a,
        'apoapsis': higher_a
    })

    new_e = min(base_e + 0.2, MAX_E)
    equations.append({
        'name': 'More Eccentric Orbit',
        'parameters': {
            'semi_major_axis': base_a,
            'eccentricity': new_e
        },
        'equation': f'r = {base_a}(1 - {new_e}²)/(1 + {new_e}cos(θ))',
        'periapsis': base_a * (1 - new_e),
        'apoapsis': base_a * (1 + new_e)
    })

    lower_a = max(base_a * 0.7, min_a)
    lower_e = max(base_e - 0.1, 0)
    equations.append({
        'name': 'Lower Orbit',
        'parameters': {
            'semi_major_axis': lower_a,
            'eccentricity': lower_e
        },
        'equation': f'r = {lower_a}(1 - {lower_e}²)/(1 + {lower_e}cos(θ))',
        'periapsis': lower_a * (1 - lower_e),
        'apoapsis': lower_a * (1 + lower_e)
    })

    valid_equations = [
        eq for eq in equations
        if eq['periapsis'] > EARTH_RADIUS + MIN_ALTITUDE
    ]

    return valid_equations


base_semi_major = 42165  # km
base_eccentricity = 0.0002945

variations = generate_orbital_variations(base_semi_major, base_eccentricity)

for orbit in variations:
    print(f"\n{orbit['name']}:")
    print(f"Equation: {orbit['equation']}")
    print(f"Semi-major axis: {orbit['parameters']['semi_major_axis']} km")
    print(f"Eccentricity: {orbit['parameters']['eccentricity']}")
    print(f"Periapsis: {orbit['periapsis']:.1f} km")
    print(f"Apoapsis: {orbit['apoapsis']:.1f} km")
