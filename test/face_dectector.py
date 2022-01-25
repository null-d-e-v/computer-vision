# --IMPORTS--
import cv2
import dlib

# Video capture
cap = cv2.VideoCapture(0)

# Detector pattern
detector = dlib.get_frontal_face_detector()

other_detector = dlib.get_frontal_face_dectector()

# Main loop
while True:

    # Get frame from video
    ret, frame = cap.read()

    # Flip frame
    frame = cv2.flip(frame, 1)

    # Convert frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Send frame to detector faces function
    faces = detector(gray)

    # Initialize face counter
    i = 0

    # Get individual face from faces
    for face in faces:

        # Get let, right, top, bottom coords
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()

        # Draw a rectangle in frame
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

        # Increment face counter
        i = i + 1

        # Draw a text in frame with face counter
        cv2.putText(
            frame,
            "face num" + str(i),
            (x - 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

        # Print face data and count
        print(face, i)

    # Draw frame in external window
    cv2.imshow("frame", frame)

    # Check if 'q' key is pressed for break loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# End video and close window
cap.release()
cv2.destroyAllWindows()
