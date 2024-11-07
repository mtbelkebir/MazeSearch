def coords_to_glcoords(coords: tuple[float, float], screen_size: tuple[float, float]) -> tuple[float, float]:
    """
    :param coords:
    :param screen_size:
    :return:
    """
    center_x, center_y = screen_size[0] // 2, screen_size[1] // 2
    x, y = coords
    x_result = (x - center_x) / center_x
    y_result = (center_y - y) / center_y
    return x_result, y_result