#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 領域切り抜きテスト """

import cv2
import numpy as np

im = cv2.imread('./img/old.png')

h, w = im.shape[:-1]

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# 色空間を二値化
img2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

# 輪郭を抽出
contours = cv2.findContours(img2, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[0]

x = cv2.boundingRect(contours[0])[0:2]
pos = [list(x), list(x)]
for rect in contours:
    x = cv2.boundingRect(rect)
    if pos[0][0] > x[0]:
        pos[0][0] = x[0]
    if pos[0][1] > x[1]:
        pos[0][1] = x[1]

    if pos[1][0] < x[0] + x[2]:
        pos[1][0] = x[0] + x[2]
    if pos[1][1] < x[1] + x[3]:
        pos[1][1] = x[1] + x[3]

# 左右の帯を削除
img3 = im[pos[0][1]:pos[1][1], pos[0][0]:pos[1][0]]

h, w = img3.shape[:-1]

# 背景の回ってるやつを削除
hsv = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)
_thre, hsv = cv2.threshold(hsv, 200, 255, cv2.THRESH_BINARY)
hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
_thre, hsv = cv2.threshold(hsv, 0, 255, cv2.THRESH_BINARY_INV)

# 縦方向につぶして左端を特定
s = np.sum(hsv[0:h, 0:int(w / 2)], axis=0)
s = np.where(s >= 255, 1, s)
_, i = np.unique(s, return_index=True)

# 若干のノイズ対策
kernel = np.ones((5, 5), np.uint8)
hsv = cv2.dilate(hsv, kernel, iterations=1)

# たぶんいい感じに縦を切り出す
a = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
_, aa = cv2.threshold(hsv, 127, 255, cv2.THRESH_BINARY_INV)
a = aa[:, i[1]]

r = [[a[0], 1]]
for x in a[1:]:
    if r[-1][0] == x:
        r[-1][1] = r[-1][1] + 1
    else:
        r.append([x, 1])

r2 = [r[0]]
for x in r[1:]:
    if x[1] < h / 3:
        r2[-1][1] = r2[-1][1] + x[1]
    else:
        r2.append(x)

for c in range(30):
    if aa[r2[0][1] - c, i[1] + c] == 255:
        break

cv2.imshow('test', aa[r2[0][1] - c + 1:, i[1]:])
cv2.waitKey(0)
cv2.destroyAllWindows()
