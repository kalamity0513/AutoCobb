import numpy as np 
import math 

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

# Function to calculate the perpendicular line passing through the centers of the medial and lateral circles
def perpendicular_line_through_centers(data):
    # Extract lateral and medial points
    lateral_points = [
        data.get('anterolateral pt', None),
        data.get('posterolateral pt', None),
        data.get('pt 1 (L)', None),
        data.get('pt 2 (L)', None),
        data.get('pt 3 (L)', None),
        data.get('pt 4 (L)', None),
        data.get('pt 5 (L)', None),
        data.get('pt 6 (L)', None),
        data.get('pt 7 (L)', None),
        data.get('pt 8 (L)', None),
        data.get('pt 9 (L)', None)
    ]

    medial_points = [
        data.get('anteromedial pt', None),
        data.get('posteromedial pt', None),
        data.get('pt 10 (M)', None),
        data.get('pt 11 (M)', None),
        data.get('pt 12 (M)', None),
        data.get('pt 13 (M)', None),
        data.get('pt 14 (M)', None),
        data.get('pt 15 (M)', None),
        data.get('pt 16 (M)', None),
        data.get('pt 17 (M)', None),
        data.get('pt 18 (M)', None)
    ]

    # Calculate centers of circles for lateral and medial points
    lateral_center = ls_circle([point[0] for point in lateral_points if point is not None], [point[1] for point in lateral_points if point is not None])
    medial_center = ls_circle([point[0] for point in medial_points if point is not None], [point[1] for point in medial_points if point is not None])

    # Calculate equation of the line passing through the centers
    x1, y1 = lateral_center[:2]
    x2, y2 = medial_center[:2]
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    # Calculate the slope of the perpendicular line
    m_perpendicular = -1 / m if m != 0 else float('inf')

    # The perpendicular line passes through the midpoint of the original line
    x_mid = (x1 + x2) / 2
    y_mid = (y1 + y2) / 2
    b_perpendicular = y_mid - m_perpendicular * x_mid

    return m_perpendicular, b_perpendicular

def line_from_two_points(point1, point2):
    """
    Construct a line equation given two points.

    Args:
    point1 (tuple): Coordinates of the first point (x1, y1).
    point2 (tuple): Coordinates of the second point (x2, y2).

    Returns:
    tuple: Slope (m) and y-intercept (b) of the line equation.
    """
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the slope (m)
    if x2 - x1 != 0:  # Avoid division by zero
        m = (y2 - y1) / (x2 - x1)
    else:
        m = float('inf')  # If the line is vertical, slope is infinity

    # Calculate the y-intercept (b)
    b = y1 - m * x1

    return m, b

def angle_between_lines(m1, m2):
    # Calculate the angles using the slopes of the lines
    angle_radians = math.atan(abs((m2 - m1) / (1 + m1 * m2)))
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def extract_data(data):
    """
    Extracts specified data from a given dictionary and returns them.

    Args:
    data (dict): Dictionary containing the data.

    Returns:
    tuple: A tuple containing slice number, medial rad, lateral rad, LatAng, MedAng,
           lateral values, medial values, MTT pt, and PCL insertion pt in the specified format.
    """
    slice_number = data.get('Slice', None)
    medial_rad = data.get('medial rad', None)
    lateral_rad = data.get('lateral rad', None)
    LatAng = data.get('LatAng', None)
    MedAng = data.get('MedAng', None)

    lateral_values = [
        data.get('anterolateral pt', None),
        data.get('posterolateral pt', None),
        data.get('pt 1 (L)', None),
        data.get('pt 2 (L)', None),
        data.get('pt 3 (L)', None),
        data.get('pt 4 (L)', None),
        data.get('pt 5 (L)', None),
        data.get('pt 6 (L)', None),
        data.get('pt 7 (L)', None),
        data.get('pt 8 (L)', None),
        data.get('pt 9 (L)', None)
    ]

    medial_values = [
        data.get('anteromedial pt', None),
        data.get('posteromedial pt', None),
        data.get('pt 10 (M)', None),
        data.get('pt 11 (M)', None),
        data.get('pt 12 (M)', None),
        data.get('pt 13 (M)', None),
        data.get('pt 14 (M)', None),
        data.get('pt 15 (M)', None),
        data.get('pt 16 (M)', None),
        data.get('pt 17 (M)', None),
        data.get('pt 18 (M)', None)
    ]
    
    mtt_pt = data.get('MTT pt', None)
    pcl_insertion_pt = data.get('PCL insertion pt', None)

    return slice_number, medial_rad, lateral_rad, LatAng, MedAng, lateral_values, medial_values, mtt_pt, pcl_insertion_pt
