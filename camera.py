import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self):

        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, image = self.video.read()

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def opti_dense(self):
        _, frame1 = self.video.read()

        img1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        # Create mask to manipulate and set to black to see flow.
        hsv_mask = np.zeros_like(frame1)
        hsv_mask[:, :, 1] = 255

        while True:

            _, frame2 = self.video.read()

            img2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

            flow = cv2.calcOpticalFlowFarneback(img1, img2, None, 0.5, 3, 15, 3, 5, 1.2, 0)

            # Calculate vectors
            magnitude, angle = cv2.cartToPolar(flow[:, :, 0], flow[:, :, 1], angleInDegrees=True)

            # Set mask to show movement with vectors in the hue then normalize the value to be between 0 & 255.
            hsv_mask[:, :, 0] = angle / 2
            hsv_mask[:, :, 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

            bgr_mask = cv2.cvtColor(hsv_mask, cv2.COLOR_HSV2BGR)

            img1 = img2

            ret, jpeg = cv2.imencode('.jpg', bgr_mask)
            return jpeg.tobytes()
