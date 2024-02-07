import numpy as np 

def ls_circle(xx, yy):
    asize = np.size(xx) # number of coordinate points given, atleast 30 minimum for the Cobb's Method
    J = np.zeros((asize, 3)) # Jacobian matrix
    K = np.zeros(asize)

    for ix in range(0, asize):
        x = xx[ix]
        y = yy[ix]

        J[ix, 0] = x*x + y*y
        J[ix, 1] = x
        J[ix, 2] = y
        K[ix] = 1.0

    K = K.transpose()
    JT = J.transpose()
    JTJ = np.dot(JT, J)
    InvJTJ = np.linalg.inv(JTJ)

    # Determining the coefficients
    ABC = np.dot(InvJTJ, np.dot(JT, K))
    A = ABC[0]
    B = ABC[1]
    C = ABC[2]

    xofs = -B / (2 * A) # x-coordinate of the centre
    yofs = -C / (2 * A) # y-coordinate of the centre
    R = np.sqrt(4 * A + B*B + C*C) / (2 * A) # radius of the best fit circle
    if R < 0.0: #can't have a negative radius
        R = -R

    return xofs, yofs, R

def draw_line_between_centers(data):
    # Extract lateral and medial points
    lateral_points = data[5]
    medial_points = data[6]

    # Calculate centers of circles for lateral and medial points
    lateral_center = ls_circle([point[0] for point in lateral_points], [point[1] for point in lateral_points])
    medial_center = ls_circle([point[0] for point in medial_points], [point[1] for point in medial_points])

    # Calculate equation of the line passing through the centers
    x1, y1 = lateral_center[:2]
    x2, y2 = medial_center[:2]
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    return m, b

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

