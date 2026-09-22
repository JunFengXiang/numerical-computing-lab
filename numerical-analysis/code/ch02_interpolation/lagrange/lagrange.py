def linear_interpolation(x,x0,x1,y0,y1):
    l0 = (x-x1)/(x0-x1)
    l1 = (x-x0)/(x1-x0)
    return y0 * l0 +y1 *l1