#Play a full game using Computer Vision

import cv2
import numpy as np
import json
import chess
import chess.svg
from cairosvg import svg2png
import chess.engine
from arm import ChessRobotArm
import random
import imutils
import math
from math import sqrt
import matplotlib.pyplot as plt
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
from statistics import mean
from skimage import exposure
import time

engine = chess.engine.SimpleEngine.popen_uci(r"..\stockfish\stockfish-windows-2022-x86-64-avx2.exe")

with open('squares.json', 'r') as fp:
    sq_points = json.load(fp)

def random_color():
  """
  Generate a random color
  """
  color = list(np.random.choice(range(256), size=3))
  return (int(color[0]), int(color[1]), int(color[2]))

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

#Returns the square given a point within the square
def find_square(x: float, y: float): 
    for square in sq_points:
        points = np.array(sq_points[square], np.int32)
        if cv2.pointPolygonTest(points, (x, y), False) > 0:
            return square
    return None

#Outline the squares
# def draw_outlines(sq_points: dict, frame, show_text = False) -> None:
#         points = np.array(points, dtype=np.int32)
#         cv2.polylines(frame, [points], True, (255, 255, 255), thickness=1)
#         x, y, w, h = cv2.boundingRect(points)
#         if show_text:
#             cv2.putText(frame, square, (x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

#Show board using python-chess SVGRendering
def show_board(board: chess.Board, size=900, move = None) -> None:
        if move is not None:
            sq1, sq2 = chess.parse_square(move[:2]), chess.parse_square(move[2:4])
            svgwrap = chess.svg.board(board, size=size, fill=dict.fromkeys([sq1, sq2], '#ced264'))
        else:
            svgwrap = chess.svg.board(board, size=size)
        svg2png(svgwrap, write_to='output.png')
        cv2.imshow('Game', cv2.imread('output.png')) 

cap = cv2.VideoCapture(0)

initial = []
final = []
bounding_boxes = []
centers = []
highlights = set()
piece_remove = []

board = chess.Board()
robot = ChessRobotArm()
comp_move = True
show_board(board)
cv2.waitKey(2)

while 1:
  ret, frame = cap.read()

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

    transformed = rotate_image(transformed, 90)

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
    
    if comp_move:
      result = engine.play(board, chess.engine.Limit(time=random.random()))
      comp_move = result.move.uci()
      (sq1, sq2) = (comp_move[:2], comp_move[2:4])          
      
      if len(piece_remove) > 0:
        if sq2 in piece_remove:
          robot.move("INIT")
          time.sleep(5)
          
          robot.move(sq2.upper())
          time.sleep(5)
          
          robot.move("KEP")
          time.sleep(5)
          
          robot.move("INIT")
          time.sleep(5)
          
          robot.move("OUT")
          time.sleep(5)
          
          robot.move("THA")
          time.sleep(5)

          robot.move("INIT")
          time.sleep(5)
      
          piece_remove = []
      
      print(f"Robot move :{sq1} to {sq2}")

      robot.move("INIT")
      time.sleep(5)
      
      robot.move(sq1.upper())
      time.sleep(5)
      
      robot.move("KEP")
      time.sleep(5)
      
      robot.move("INIT")
      time.sleep(5)
      
      robot.move(sq2.upper())
      time.sleep(5)
      
      robot.move("THA")
      time.sleep(5)

      robot.move("INIT")
      time.sleep(5)
      
      board.push(result.move)
      print('Robot plays', result.move.uci())
      show_board(board, move=str(result.move))
      comp_move = False

    # for (x, y, w, h) in bounding_boxes:
    #     cv2.rectangle(transformed, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    for (x, y) in centers:
        square = find_square(x, y)
        highlights.add(square)

    if cv2.waitKey(1) & 0xFF == ord('r'):
      if len(initial)==0:
          initial = dst
          print("Recording")
          
      elif len(final)==0:
          print('Move captured')
          final = dst
          
          #Get the absolute difference between the initial and final frames.
          if initial.shape != final.shape:
              # Resize image2 to match the shape of image1
              final = cv2.resize(final, (initial.shape[1], initial.shape[0]))

          diff = cv2.absdiff(initial, final)

          retval, mask_thresh = cv2.threshold(diff, 45, 255, cv2.THRESH_BINARY)

          if mask_thresh.ndim == 3:
            mask_thresh = cv2.cvtColor(mask_thresh, cv2.COLOR_BGR2GRAY)
          elif mask_thresh.dtype != 'uint8':
            mask_thresh = mask_thresh.astype('uint8')
              
          # # set the kernal
          kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
          
          # Apply erosion
          mask_eroded = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN, kernel)
          
          contours, _ = cv2.findContours(mask_eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

          min_contour_area = 0  # Define your minimum area threshold
             
          try:
            large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
            for cnt in large_contours:
                x, y, w, h = cv2.boundingRect(cnt)

            bounding_boxes = [cv2.boundingRect(c) for c in large_contours]
            centers = [(x + w//2, y + 0.7*h) for (x, y, w, h) in bounding_boxes]

            highlights = set()
            for p in centers:
                highlights.add(find_square(*p))
            
            # print(f"person move : {highlights[0]} to {highlights[1]}")
            print(highlights)
            initial = []
            final = []

          except:
              highlights = set()
              highlights.add('rand')
              highlights.add('placeholder')
              initial = []
              final = []
              
          #cv2.imshow('Absolute Difference', diff)
          
          if len(highlights) == 2:
            try:
                sq1, sq2 = highlights.pop(), highlights.pop()
                if board.color_at(chess.parse_square(sq1)) == board.turn:
                    start, end = sq1, sq2
                else:
                    start, end = sq2, sq1
                uci = start+end
                
                board.push(chess.Move.from_uci(uci))
                piece_remove.append(sq1)
                piece_remove.append(sq2)
                
            except:
                print("The frame doesn't capture the moving remove again")
                continue
                
            show_board(board, move=uci)
            highlights = set()
            centers = []
            comp_move = True            

          if len(highlights) > 2:
            print("Recheck Image preprocessing getStructuringElement")
            highlights = set()
            centers = []
            piece_remove = []
            continue
             
    #Black castles 0-0
    if cv2.waitKey(3) & 0xFF == ord('m'):
        move = 'e8g8'
        board.push_uci('e8g8')
        show_board(board, move=move)
        bounding_boxes = []
        comp_move = True

    #Black castles 0-0-0 
    if cv2.waitKey(4) & 0xFF == ord('n'):
        move = 'e8c8'
        board.push_uci('e8c8')
        show_board(board, move=move)
        bounding_boxes = []
        comp_move = True   
            
  except Exception as err:
      print(err)

  cv2.imshow('Webcam', transformed)

  # Break the loop if 'q' is pressed
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
