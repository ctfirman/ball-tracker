from collections import deque

import cv2
import imutils


class BallTracker:
    '''
    None
    '''
    def __init__(self, file_name, lower_bound, upper_bound):
        self.file_name = file_name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.points = deque(maxlen=15)

    def __img_process(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound) 

        mask = cv2.dilate(mask, None)
        mask = cv2.erode(mask, None)

        return mask


    def __draw_trail(self, frame, center):
        self.points.appendleft(center)

        for i in range(1, len(self.points)):
            if self.points[i-1] is None or self.points[i] is None:
                continue
            # cv2.line(frame, points[i-1], points[i], (0,0,255), 2)
            cv2.circle(frame, self.points[i], 4, (0,0,255), -1)


    def __draw_circle(self, frame, contour,):
        if len(contour) > 0:
            c = max(contour, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # Change int(20) to radius to get a changing circle
            cv2.circle(frame, (int(x), int(y)), int(20), (0, 255, 255), 5)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            return center


    def read_vid(self):
        '''
        Main Method to track the ball
        '''
        cap = cv2.VideoCapture(self.file_name)

        while cap.isOpened():
            _, frame = cap.read()

            if frame is None:
                break

            mask = self.__img_process(frame)

            cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None

            center = self.__draw_circle(frame, cnts)

            self.__draw_trail(frame, center)


            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
