def coords_to_glcoords(coords: tuple[float, float], screen_size: tuple[float, float]) -> tuple[float, float]:
    """
    Convert screen coordinates to OpenGL coordinates.

    :param coords: A tuple containing the x and y coordinates on the screen.
    :param screen_size: A tuple containing the width and height of the screen.
    :return: A tuple containing the x and y coordinates in OpenGL format.
    """
    center_x, center_y = screen_size[0] // 2, screen_size[1] // 2
    x, y = coords
    x_result = (x - center_x) / center_x
    y_result = (center_y - y) / center_y
    return x_result, y_result