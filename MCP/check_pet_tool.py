def check_temperature(temp_c: float | None) -> str:
    if temp_c is None:
        return "Temperature data not provided"
    if temp_c < 37.5:
        return "Low temperature, possible hypothermia risk"
    elif 37.5 <= temp_c <= 39.5:
        return "Normal temperature"
    else:
        return "High temperature, possible fever or infection risk"


def check_heart_rate(hr: int | None, species: str = "dog") -> str:
    if hr is None:
        return "Heart rate data not provided"
    ranges = {
        "dog": (60, 140),
        "cat": (140, 220)
    }
    low, high = ranges.get(species, (60, 140))
    
    if hr < low:
        return f"Low heart rate ({hr} bpm), possible cardiac issues"
    elif low <= hr <= high:
        return f"Normal heart rate ({hr} bpm)"
    else:
        return f"High heart rate ({hr} bpm), possible stress or illness"


def check_activity_level(steps: int | None) -> str:
    if steps is None:
        return "Activity data not provided"
    if steps < 1000:
        return "Low activity, may indicate laziness or illness"
    elif 1000 <= steps <= 5000:
        return "Normal activity level"
    else:
        return "High activity, may indicate over-exercise or stress"


def check_food_intake(intake_g: float | None, species: str = "dog") -> str:
    if intake_g is None:
        return "Food intake data not provided"
    ref = {
        "dog": (200, 500),
        "cat": (50, 200)
    }
    low, high = ref.get(species, (100, 300))
    
    if intake_g < low:
        return f"Low food intake ({intake_g} g), possible loss of appetite"
    elif low <= intake_g <= high:
        return f"Normal food intake ({intake_g} g)"
    else:
        return f"Excessive food intake ({intake_g} g), potential obesity risk"


def health_summary(temp_c: float | None, hr: int | None, steps: int | None, intake_g: float | None, species: str = "dog") -> dict:
    return {
        "Temperature": check_temperature(temp_c),
        "Heart Rate": check_heart_rate(hr, species),
        "Activity": check_activity_level(steps),
        "Food Intake": check_food_intake(intake_g, species)
    }
