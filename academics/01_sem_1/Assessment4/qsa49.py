#Write a function called calculate_slope which return the slope of a linear equation.
def calculate_slope(x1, y1, x2, y2):
    if x2 - x1 == 0:
        raise ValueError("Slope is undefined for vertical lines (x1 cannot be equal to x2).")
    slope = (y2 - y1) / (x2 - x1)
    return slope
print("slope",calculate_slope(8, 9, 7, 6))