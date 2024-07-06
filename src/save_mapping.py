import math
from math import sqrt
import cv2
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
from statistics import mean
import imutils
from skimage import exposure
import argparse
import random
import json
import time

def random_color():
  """
  Generate a random color
  """
  color = list(np.random.choice(range(256), size=3))
  return (int(color[0]), int(color[1]), int(color[2]))

def order_points_clockwise(pts):
  # sort the points based on their x-coordinates
  xSorted = pts[np.argsort(pts[:, 0]), :]

  # grab the left-most and right-most points from the sorted
  # x-roodinate points
  leftMost = xSorted[:2, :]
  rightMost = xSorted[2:, :]

  # now, sort the left-most coordinates according to their
  # y-coordinates so we can grab the top-left and bottom-left
  # points, respectively
  leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
  (tl, bl) = leftMost

  # now, sort the right-most coordinates according to their
  # y-coordinates so we can grab the top-right and bottom-right
  # points, respectively
  rightMost = rightMost[np.argsort(rightMost[:, 1]), :]
  (tr, br) = rightMost

  # return the coordinates in top-left, top-right,
  # bottom-right, and bottom-left order
  return np.array([tl, tr, br, bl], dtype="int32")

def perspective_transform(image, corners):
  def order_corner_points(corners):
    # Separate corners into individual points
    # Index 0 - top-right
    #       1 - top-left
    #       2 - bottom-left
    #       3 - bottom-right
    corners = [(corner[0][0], corner[0][1]) for corner in corners]
    top_r, top_l, bottom_l, bottom_r = corners[0], corners[1], corners[2], corners[3]
    return (top_l, top_r, bottom_r, bottom_l)

  # Order points in clockwise order
  ordered_corners = order_corner_points(corners)
  top_l, top_r, bottom_r, bottom_l = ordered_corners

  # Determine width of new image which is the max distance between
  # (bottom right and bottom left) or (top right and top left) x-coordinates
  width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
  width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
  width = max(int(width_A), int(width_B))

  # Determine height of new image which is the max distance between
  # (top right and bottom right) or (top left and bottom left) y-coordinates
  height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
  height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
  height = max(int(height_A), int(height_B))

  # Construct new points to obtain top-down view of image in
  # top_r, top_l, bottom_l, bottom_r order
  dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                  [0, height - 1]], dtype = "float32")

  # Convert to Numpy format
  ordered_corners = np.array(ordered_corners, dtype="float32")

  # Find perspective transform matrix
  matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)

  # Return the transformed image
  return cv2.warpPerspective(image, matrix, (width, height))

def draw_chessboard_corner(img, matrix):
  mapping_img = img.copy()
  colors = [(140,0,236), (145,45,102), (166,84,0), (239,174,0), (81,166,0), (63,198,141), (0,242,255), (29,148,247), (36,28,237)]
  for (idx, points) in enumerate(matrix):
    # draw horizontal line
    cv2.line(mapping_img, points[0], points[-1], colors[idx], 2)

    # draw diagonal line
    if idx > 0:
      cv2.line(mapping_img, matrix[idx - 1][-1], points[0], colors[idx], 1)

    # draw points
    for point in points:
      cv2.circle(mapping_img, point, 5, colors[idx], -1)

  return mapping_img

def distance(p, q):
  return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

# Canny edge detection
def canny_edge(img, sigma=0.33):
  v = np.median(img)
  lower = int(max(0, (1.0 - sigma) * v))
  upper = int(min(255, (1.0 + sigma) * v))
  edges = cv2.Canny(img, lower, upper)
  return edges


# Hough line detection
def hough_line(edges, min_line_length=100, max_line_gap=10):
  lines = cv2.HoughLines(edges, 1, np.pi / 180, 125, min_line_length, max_line_gap)
  lines = np.reshape(lines, (-1, 2))
  return lines

# Separate line into horizontal and vertical
def h_v_lines(lines):
  h_lines, v_lines = [], []
  for rho, theta in lines:
    if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
      v_lines.append([rho, theta])
    else:
      h_lines.append([rho, theta])
  return h_lines, v_lines


# Find the intersections of the lines
def line_intersections(h_lines, v_lines):
  points = []
  for r_h, t_h in h_lines:
    for r_v, t_v in v_lines:
      a = np.array([[np.cos(t_h), np.sin(t_h)], [np.cos(t_v), np.sin(t_v)]])
      b = np.array([r_h, r_v])
      inter_point = np.linalg.solve(a, b)
      points.append(inter_point)
  return np.array(points)


# Hierarchical cluster (by euclidean distance) intersection points
def cluster_points(points):
  dists = spatial.distance.pdist(points)
  single_linkage = cluster.hierarchy.single(dists)
  flat_clusters = cluster.hierarchy.fcluster(single_linkage, 15, 'distance')
  cluster_dict = defaultdict(list)
  for i in range(len(flat_clusters)):
    cluster_dict[flat_clusters[i]].append(points[i])
  cluster_values = cluster_dict.values()
  clusters = map(lambda arr: (np.mean(np.array(arr)[:, 0]), np.mean(np.array(arr)[:, 1])), cluster_values)
  return sorted(list(clusters), key=lambda k: [k[1], k[0]])

def convertCorners2Matrix(corners, thresh_val=10.0):
    """
    Convert chess board squares corners into 9x9 matrix of points.

    matrix:

    [
      [coord0_0, coord0_1, ...., coord0_N]
      [coord1_0, coord1_1, ...., coord1_N]
      [coord2_0, coord2_1, ...., coord2_N]
    ]
    """
    # we will start with first corner
    target_corner = corners[0]

    chess_matrix = []
    while len(corners) != 0:
      # get all corners where axis y between min_thresh and max_thresh
      min_thresh = target_corner[1] - thresh_val
      max_thresh = target_corner[1] + thresh_val
      line_corners = [p for p in corners if p[1] >= min_thresh and p[1] <= max_thresh]
      line_corners.sort(key=lambda p: p[0])

      # add corners of the line into matrix
      if len(line_corners) > 0:
        chess_matrix.append(line_corners)

      # remove finded corners of the main array
      corners = [p for p in corners if p not in line_corners]

      # define a new target corner
      if len(corners) != 0:
        target_corner = corners[0]

    return chess_matrix


def parseMatrix(matrix):
    """
    Parse matrix 9x9 of points into a matrix 8x8 of `Square` object

    matrix:
    
    [
      [Square0_0, Square0_1, ...., Square0_N]
      [Square1_0, Square1_1, ...., Square1_N]
      [Square2_0, Square2_1, ...., Square2_N]
    ]
    """
    if len(matrix) != 9:
      print("[ERROR] No 9x9 dimension matrix found")
      return

    new_matrix = []
    for (row_idx, points) in enumerate(matrix[:len(matrix) - 1]):
      squares = []
      for (col_idx, pt1) in enumerate(points[:len(points) - 1]):
        pt2 = matrix[row_idx + 1][col_idx + 1]

        x1 = round(pt1[0])
        y1 = round(pt1[1])
        x2 = round(pt2[0])
        y2 = round(pt2[1])

        squares.append((x1, y1, x2, y2))
      new_matrix.append(squares)
    return new_matrix

def rotate_image(image, angle):
  # Grab the dimensions of the image and then determine the center
  (h, w) = image.shape[:2]
  (cX, cY) = (w / 2, h / 2)

  # grab the rotation matrix (applying the negative of the
  # angle to rotate clockwise), then grab the sine and cosine
  # (i.e., the rotation components of the matrix)
  M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
  cos = np.abs(M[0, 0])
  sin = np.abs(M[0, 1])

  # Compute the new bounding dimensions of the image
  nW = int((h * sin) + (w * cos))
  nH = int((h * cos) + (w * sin))

  # Adjust the rotation matrix to take into account translation
  M[0, 2] += (nW / 2) - cX
  M[1, 2] += (nH / 2) - cY

  # Perform the actual rotation and return the image
  return cv2.warpAffine(image, M, (nW, nH))


####################################################

cap = cv2.VideoCapture(0)

while True:
  # Capture frame-by-frame
  ret, frame = cap.read()
  time.sleep(5)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  smooth = cv2.GaussianBlur(gray, (9, 9), 0)

  thresh = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

  # Since we're interested in the borders, and they are black, we invert the image color.
  # Then, the borders of the chessboard are white (along with other noise).
  thresh = cv2.bitwise_not(thresh)

  kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)
  thresh = cv2.dilate(thresh, kernel, iterations=1)

  try:
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse = True)

    peri = cv2.arcLength(cnts[0], True)
    biggest_cnt = cv2.approxPolyDP(cnts[0], 0.025 * peri, True)

    transformed = perspective_transform(frame, biggest_cnt)

    # transformed = rotate_image(transformed, -90)

    PADDING = (15, 15)
    OUTPUT_IMAGE_SIZE = (500, 500)

    h, w = transformed.shape[:2]
    padding_horizontal, padding_vertical = PADDING

    output_img_h, output_img_w, = OUTPUT_IMAGE_SIZE

    pts1 = np.float32([
      PADDING,
      (w - padding_horizontal, padding_vertical),
      (padding_horizontal, h - padding_vertical),
      (w - padding_horizontal, h - padding_vertical)
    ])

    pts2 = np.float32([
    [0, 0],
    [output_img_w, 0],
    [0, output_img_h],
    [output_img_w, output_img_h]
    ])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(transformed, M, OUTPUT_IMAGE_SIZE)
      
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    # Blur the image a little. This smooths out the noise a bit and
    # makes extracting the grid lines easier.
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Canny algorithm
    edges = canny_edge(gray_blur)
    
    # Hough Transform
    lines = hough_line(edges)

    # Separate the lines into vertical and horizontal lines
    h_lines, v_lines = h_v_lines(lines)

    # Find and cluster the intersecting
    intersection_points = line_intersections(h_lines, v_lines)
    points = cluster_points(intersection_points)

    for (idx, point) in enumerate(points):
      color = random_color()
      cv2.putText(dst, str(idx), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_PLAIN, 1.0, color, 2)
      cv2.circle(dst, (int(point[0]), int(point[1])), 3, color, -1)

    # Convert the list to a numpy array
    points_array = np.array(points)

    try:
      # Reshape the array to 9x9x2
      points_matrix_9x9 = points_array.reshape((9, 9, 2))
      
      squares = {}

      for i in range(8):
          # for j in range(8):
          for j in range(7, -1, -1): 
            top_left = tuple(points_matrix_9x9[i, j].astype(int))
            top_right = tuple(points_matrix_9x9[i, j+1].astype(int))
            bottom_left = tuple(points_matrix_9x9[i+1, j].astype(int))
            bottom_right = tuple(points_matrix_9x9[i+1, j+1].astype(int))
            # Draw lines to form squares
            cv2.line(dst, top_left, top_right, (0, 255, 0), 2)
            cv2.line(dst, top_left, bottom_left, (0, 255, 0), 2)
            cv2.line(dst, bottom_left, bottom_right, (0, 255, 0), 2)
            cv2.line(dst, top_right, bottom_right, (0, 255, 0), 2)

            # Calculate the center of the square
            center_x = int((top_left[0] + top_right[0] + bottom_left[0] + bottom_right[0]) / 4)
            center_y = int((top_left[1] + top_right[1] + bottom_left[1] + bottom_right[1]) / 4)
            
            # Put text at the center
            square_key = f"{chr(ord('a')+j)}{i+1}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1
            text_size = cv2.getTextSize(square_key, font, font_scale, font_thickness)[0]
            text_x = center_x - text_size[0] // 2
            text_y = center_y + text_size[1] // 2
            cv2.putText(dst, square_key, (text_x, text_y), font, font_scale, (255, 0, 0), font_thickness)
            squares[square_key] = [top_left, top_right, bottom_right, bottom_left]
      
      cv2.imshow('Webcam', dst)
      
      # Wait for a key press
      key = cv2.waitKey(1) & 0xFF

      # If 's' is pressed, save the frame
      if key == ord('s'):
        chess_board = {k: [tuple(map(int, v)) for v in l] for k, l in squares.items()}
        with open('squares.json', 'w') as f:
            json.dump(chess_board, f, indent=4)
        break
            
    except Exception as err:
      print(err)

  except Exception as err:
    print(err)
    
# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()