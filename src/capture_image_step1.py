import cv2

# Open the default webcam (0 is usually the default ID for the primary webcam)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

print("Press 's' to capture an image and 'q' to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # If the frame was captured correctly
    if ret:
        # Display the resulting frame
        cv2.imshow('Webcam', frame)

        # Wait for a key press
        key = cv2.waitKey(1) & 0xFF

        # If 's' is pressed, save the frame
        if key == ord('s'):
            cv2.imwrite('captured_image3.jpg', frame)
            print("Image captured and saved as captured_image.jpg")

        # If 'q' is pressed, exit the loop
        elif key == ord('q'):
            break
    else:
        print("Error: Could not read frame")
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()