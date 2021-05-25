import numpy as np
import cv2

# define parameters/cordinates for images 
def order_points(pts):
    rect =	rect = np.zeros((4, 2), dtype = "float32")

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect



# load img and find fix cordinate for transformation
def four_point_transform(image, pts):
    rect = order_points(pts)
    (t1, tr, br, b1) = rect

    widthA = np.sqrt(((br[0] - b1[0]) ** 2) + ((br[1] - br[1]) ** 2))
    widthB = np.sqrt(((tr[0] - t1[0]) ** 2) + ((tr[1] - t1[1]) ** 2))
    maxwidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((t1[0] -b1[0] ) ** 2) + ((t1[1] - b1[1]) ** 2))
    maxheight = max(int(heightA), int(heightB))

    dest = np.array([
        [0, 0],
        [maxwidth - 1, 0],
        [maxwidth - 1, maxheight - 1],
        [0, maxheight - 1]], dtype = "float32")



# transform cordinate in matrix form and stored in dest
    Mt = cv2.getPerspectiveTransform(rect, dest)
    warped = cv2.warpPerspective(image, Mt, (maxwidth, maxheight))

    return warped
    #print (warped)