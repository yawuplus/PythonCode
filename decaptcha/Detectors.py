########################################################################

'''

Author: Kuo Chun-Lin
Date  : 2020.05.11
'''

########################################################################

import os
import cv2
import time
import numpy as np
from skimage.util.shape import view_as_windows as vaw

########################################################################


class HerrisCorner(object):
    """docstring for HerrisCorner"""

    def __init__(self, k=0.04, kernel_size=(5, 5), threshold=10000):
        self.k = k
        self.kernel_H = kernel_size[0]
        self.kernel_W = kernel_size[1]
        self.kernel_size = kernel_size
        self.threshold = threshold

        # Calc the offsets coordinates between the original image ...
        # ... and the sliding windows.
        self.offset_H = int(kernel_size[0] / 2)
        self.offset_W = int(kernel_size[1] / 2)

    def detect(self, img):
        # Only the gray-scale image is accepted.
        self.imgH, self.imgW = img.shape

        # Get the gradient of an image.
        dy, dx = np.gradient(img)
        # Seq: Ixx, Ixy, Iyy
        I = np.stack([dx ** 2, dy * dx, dy ** 2], axis=0)

        # Apply sliding windows at once.
        windows = np.squeeze(vaw(I, (3, self.kernel_H, self.kernel_W)))
        windows = windows.reshape(self.imgH - self.offset_H * 2,
                                  self.imgW - self.offset_W * 2, 3, -1)

        # Calculate the determinant and trace values in batch.
        S = np.sum(windows, axis=-1)
        dets = S[:, :, 0] * S[:, :, 2] - S[:, :, 1] ** 2
        traces = S[:, :, 0] + S[:, :, 2]
        r = dets - self.k * (traces ** 2)

        # Indices those r value greater than threshold.
        idx_pick = np.where(r > self.threshold)
        return (idx_pick[0] + self.offset_H, idx_pick[1] + self.offset_W)


########################################################################


# if __name__ == '__main__':
#     # For testing code ...
#     import matplotlib.pyplot as plt

#     PATH = '/Users/kcl/Documents/TBSI/课程/2020_02_Semester/Computational Photography/project_2/code'

#     # Read the image and transform it into gray scale format.
#     img = cv2.imread(os.path.join(PATH, 'pyd.jpg'))
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Detect the corners using Herris algorith.
#     herris = HerrisCorner(k=0.22, kernel_size=(5, 5), threshold=1000000)
#     idx = herris.detect(img_gray)

#     # Visualize the detection.
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.scatter(idx[1], idx[0])

#     # for i in range(len(idx[0])):
#     #     plt.scatter(idx[1][i], idx[0][i], c=np.random.rand(3), alpha=0.3)

#     plt.show()

########################################################################


class MarrHildrethEdge(object):
    """docstring for MarrHildrethEdge"""

    def __init__(self, arg):
        super(MarrHildrethEdge, self).__init__()
        self.arg = arg


########################################################################


class Keypoint2Descriptor(object):
    """docstring for Keypoint2Descriptor"""

    def __init__(self):
        self.version = cv2.__version__.split('.')[:2]
        self.version = int(self.version[0]) + int(self.version[1]) * 0.1

    def sift(self, img):
        # SIFT is a patent algorithm, which is not allowed to use this
        # algorithm for commercial purposes.
        assert self.version <= 3.4, 'SIFT algo is not involved in \
                                     OpenCV with version higher than 3.4.'
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _sift = cv2.xfeatures2d.SIFT_create()
        kp, des = _sift.detectAndCompute(img, None)
        return kp, des

    def surf(self, img):
        # SURF is a patent algorithm, which is not allowed to use this
        # algorithm for commercial purposes.
        assert self.version <= 3.4, 'SURF algo is not involved in \
                                     OpenCV with version higher than 3.4.'
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _surf = cv2.xfeatures2d.SURF_create()
        kp, des = _surf.detectAndCompute(img, None)
        return kp, des

    def orb(self, img):
        # ORB is a MIT license algorithm integrated in OpenCV.
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _orb = cv2.ORB_create()
        kp, des = _orb.detectAndCompute(img, None)
        return kp, des

    def fast2brief(self, img):
        kp = self.fast(img)
        kp, des = self.brief(img, kp)
        return kp, des

    def fast(self, img):
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _fast = cv2.FastFeatureDetector_create()
        kp = _fast.detect(img, None)
        return kp

    def brief(self, img, kp):
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        kp, des = _brief.compute(img, kp)
        return kp, des


########################################################################


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    img1 = cv2.imread('houseL.jpeg')
    img2 = cv2.imread('houseR.jpeg')

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Algorithms provided by OpenCV.
    algo = Keypoint2Descriptor()
    # kp1, des1 = algo.sift(gray1)
    # kp2, des2 = algo.sift(gray2)

    # kp1, des1 = algo.surf(gray1)
    # kp2, des2 = algo.surf(gray2)

    kp1, des1 = algo.orb(gray1)
    kp2, des2 = algo.orb(gray2)

    # kp1, des1 = algo.fast2brief(gray1)
    # kp2, des2 = algo.fast2brief(gray2)

    # flann = cv2.FlannBasedMatcher(dict(algorithm=0, trees=5),
    #                               dict(checks=50))
    # matches = flann.knnMatch(des1, des2, k=2)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test: get the 1st & 2nd closest points. Only when ...
    # ... the ratio 1st / 2nd is less than "0.?", we can consider it ...
    # ... as a match.
    good = []
    for m, n in matches:
        if m.distance < 0.9 * n.distance:
            good.append(m)

    # Gain the keypoints from both keypoint set.
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # "cv2.RANSAC" is a method used to compute a homography matrix.
    # The following methods are possible:
    #   + CV_RANSAC - RANSAC-based robust method
    #   + CV_LMEDS - Least-Median robust method
    # The 4th param should remain between 1 to 10.
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    # M is a transformation matrix.

    # Use this to make sure that the matched keypoints are all ...
    # ... remained in a wanted region.
    matchesMask = mask.ravel().tolist()

    # Get the height and width of the original image ...
    h, w, c = img1.shape
    # ... and gain the coordinates of 4 corners of the orignal image.
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1],
                      [w - 1, 0]]).reshape(-1, 1, 2)

    # Use the transformation matrix "M" to determine the new coordinates.
    # shape 3D: (4, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    # Draw the transformed image FRAME to the 2nd image.
    img2 = cv2.polylines(img2, [np.int32(dst)], True,
                         (0, 255, 0), 2, cv2.LINE_AA)

    # Add the frame boundary restriction when we match the features.
    draw_params = dict(singlePointColor=None,
                       matchesMask=matchesMask,
                       # matchColor=(0, 255, 0),
                       flags=2)

    # Match the 2 images and return a matched-image result.
    img_match = cv2.drawMatches(img1, kp1, img2, kp2,
                                good, None, **draw_params)

    plt.imshow(cv2.cvtColor(img_match, cv2.COLOR_BGR2RGB))
    plt.show()
