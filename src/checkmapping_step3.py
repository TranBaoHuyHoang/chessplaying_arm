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


def distance(p, q):
  return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


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

def random_color():
  """
  Generate a random color
  """
  color = list(np.random.choice(range(256), size=3))
  return (int(color[0]), int(color[1]), int(color[2]))

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

with open('squares.json', 'r') as fp:
    sq_points = json.load(fp)


def put_centered_text(image, text, x, y, w, h):
    # Calculate the center of the rectangle
    rect_center_x = x + w // 2
    rect_center_y = y + h // 2

    # Get the text size
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

    # Calculate the bottom-left corner of the text to be centered
    text_origin = (rect_center_x - text_width // 2, rect_center_y + text_height // 2)

    # Put the text on the image
    cv2.putText(image, text, text_origin, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


def draw_outlines(sq_points: dict, frame) -> None:
    for square in sq_points:
      points = sq_points[square]
      points = np.array(points, dtype=np.int32)
      cv2.polylines(frame, [points], True, (255, 255, 255), thickness=1)
      x, y, w, h = cv2.boundingRect(points)
      put_centered_text(frame, square, x, y, w, h)
        

image = cv2.imread('captured_image1.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

smooth = cv2.GaussianBlur(gray, (9, 9), 0)

thresh = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Since we're interested in the borders, and they are black, we invert the image color.
# Then, the borders of the chessboard are white (along with other noise).
thresh = cv2.bitwise_not(thresh)

kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)
thresh = cv2.dilate(thresh, kernel, iterations=1)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse = True)

peri = cv2.arcLength(cnts[0], True)
biggest_cnt = cv2.approxPolyDP(cnts[0], 0.025 * peri, True)

transformed = perspective_transform(image, biggest_cnt)
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

draw_outlines(sq_points, dst)

cv2.imshow('Webcam', dst)

cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()