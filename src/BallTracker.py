from collections import deque

import cv2
import imutils


class BallTracker:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_file(self):
        cap = cv2.VideoCapture(self.file_name)

        points = deque(maxlen=15)

        while cap.isOpened():
            _, frame = cap.read()

            if frame is None:
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # For Soccer
            ball_lower = (20,200,100)
            ball_upper = (35,255,200)

            # For Ping
            # ball_lower = (30,0,0)
            # ball_upper = (40,255,255)

            mask = cv2.inRange(hsv, ball_lower, ball_upper) 

            mask = cv2.dilate(mask, None)
            mask = cv2.erode(mask, None)

            cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # Change int(20) to radius to get a changing circle
                cv2.circle(frame, (int(x), int(y)), int(20), (0, 255, 255), 5)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

            points.appendleft(center)
            for i in range(1, len(points)):
                if points[i-1] is None or points[i] is None:
                    continue
                cv2.line(frame, points[i-1], points[i], (0,0,255), 2)


            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break