def extract_data(data):
    """
    Extracts specified data from a given dictionary and returns them.

    Args:
    data (dict): Dictionary containing the data.

    Returns:
    tuple: A tuple containing slice number, medial rad, lateral rad, LatAng, MedAng,
           lateral values, and medial values in the specified format.
    """
    slice_number = data.get('Slice', None)
    medial_rad = data.get('medial rad', None)
    lateral_rad = data.get('lateral rad', None)
    LatAng = data.get('LatAng', None)
    MedAng = data.get('MedAng', None)

    lateral_values = [
        data.get('anterolateral pt', None),
        data.get('posterolateral pt', None),
        data.get('pt 11 (L)', None),
        data.get('pt 12 (L)', None),
        data.get('pt 13 (L)', None),
        data.get('pt 14 (L)', None),
        data.get('pt 15 (L)', None),
        data.get('pt 16 (L)', None),
        data.get('pt 17 (L)', None),
        data.get('pt 18 (L)', None),
        data.get('pt 19 (L)', None)
    ]

    medial_values = [
        data.get('anteromedial pt', None),
        data.get('posteroemdial pt', None),
        data.get('pt 20 (M)', None),
        data.get('pt 21 (M)', None),
        data.get('pt 22 (M)', None),
        data.get('pt 23 (M)', None),
        data.get('pt 24 (M)', None),
        data.get('pt 25 (M)', None),
        data.get('pt 26 (M)', None),
        data.get('pt 27 (M)', None),
        data.get('pt 28 (M)', None)
    ]

    return slice_number, medial_rad, lateral_rad, LatAng, MedAng, lateral_values, medial_values

