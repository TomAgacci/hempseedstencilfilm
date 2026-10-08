#!/usr/bin/env python3
"""
hemp_stencil_laser_helper.py

Simple helper to suggest starting laser-cutting parameters
for thin hemp-based stencil films, based on thickness and laser type.
"""

def suggest_settings(laser_type: str, power_watts: float, thickness_mm: float):
    """
    Suggest starting settings for cutting hemp-based stencil film.

    Parameters
    ----------
    laser_type : str
        "CO2" or "diode"
    power_watts : float
        Nominal laser power in watts.
    thickness_mm : float
        Film thickness in millimeters (e.g., 0.08).
    """
    laser_type = laser_type.upper().strip()

    if thickness_mm <= 0:
        raise ValueError("Thickness must be positive.")

    # Base scaling factor: thicker film → slower speed and/or higher power
    # This is a simple heuristic, not a physical model.
    thickness_factor = max(0.5, min(2.0, thickness_mm / 0.08))

    if laser_type == "CO2":
        # Assume typical hobby CO2 laser (e.g., 40–60 W)
        base_power_pct = 20.0  # %
        base_speed_mm_s = 280.0

        power_pct = base_power_pct * thickness_factor
        speed_mm_s = base_speed_mm_s / thickness_factor
        passes = 1 if thickness_mm <= 0.1 else 2

    elif laser_type == "DIODE":
        # Assume typical diode laser (e.g., 10–20 W)
        base_power_pct = 70.0  # %
        base_speed_mm_s = 150.0

        power_pct = base_power_pct * thickness_factor
        speed_mm_s = base_speed_mm_s / thickness_factor
        passes = 1 if thickness_mm <= 0.08 else 2

    else:
        raise ValueError("Unsupported laser_type. Use 'CO2' or 'diode'.")

    # Clamp values to reasonable ranges
    power_pct = max(5.0, min(100.0, power_pct))
    speed_mm_s = max(50.0, min(500.0, speed_mm_s))

    return {
        "laser_type": laser_type,
        "power_watts": power_watts,
        "thickness_mm": thickness_mm,
        "power_percent": round(power_pct, 1),
        "speed_mm_s": round(speed_mm_s, 1),
        "passes": passes,
    }


def print_test_plan(settings: dict):
    """
    Print a simple test plan based on suggested settings.
    """
    print("=== Hemp Stencil Film Laser Test Plan ===")
    print(f"Laser type      : {settings['laser_type']}")
    print(f"Laser power     : {settings['power_watts']} W (nominal)")
    print(f"Film thickness  : {settings['thickness_mm']} mm")
    print()
    print("Suggested starting settings:")
    print(f"  Power         : {settings['power_percent']} %")
    print(f"  Speed         : {settings['speed_mm_s']} mm/s")
    print(f"  Passes        : {settings['passes']}")
    print()
    print("Test procedure:")
    print("  1. Place a small piece of film on the bed (use light hold-down).")
    print("  2. Focus the laser at the film surface.")
    print("  3. Cut a 5 x 5 mm square using the suggested settings.")
    print("  4. Inspect edges for melt, charring, and incomplete cut.")
    print("  5. Adjust power/speed slightly and repeat until edges are clean.")
    print("  6. Once satisfied, apply settings to full stencil designs.")
    print("==========================================")


if __name__ == "__main__":
    # Example usage: CO2 laser, 50 W, 0.08 mm film
    laser_type = "CO2"
    power_watts = 50.0
    thickness_mm = 0.08

    settings = suggest_settings(laser_type, power_watts, thickness_mm)
    print_test_plan(settings)
