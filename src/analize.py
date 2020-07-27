#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import sys
import numpy as np
import cv2
import pyocr
import pyocr.builders

args = sys.argv

img = Image.open(args[1])

# 16:9にする
offset = max(0, int((img.width - round(img.height * 16 / 9)) / 2))
vw = img.width - offset - offset

img = img.crop((offset, 0, offset + vw, img.height))

# 同じ大きさに固定
img = img.resize((2560, 1440))

diff = img.crop((572, 215, 875, 280))
img = img.convert('L').point(lambda x: 0 if x < 200 else x)

# 切り出し
music = img.crop((678, 280, 1260, 405))

perfect = img.crop((1030, 460, 1205, 517))
great = img.crop((1030, 536, 1205, 596))
nice = img.crop((1030, 615, 1205, 675))
bad = img.crop((1030, 695, 1205, 754))
miss = img.crop((1030, 775, 1205, 832))

combo = img.crop((1010, 890, 1210, 965))
# combo_rank = img.crop((880, 860, 990, 965))
score = img.crop((870, 1075, 1215, 1145))
high_score = img.crop((915, 1165, 1215, 1224))
music_prp = img.crop((540, 1270, 800, 1338))
prp = img.crop((930, 1270, 1200, 1338))
# score_rank = img.crop((1200, 1035, 1550, 1380))


def compareHist(src, target, channel):
    src_hist = cv2.calcHist([src], [channel], None, [256], [0, 256])
    target_hist = cv2.calcHist([target], [channel], None, [256], [0, 256])
    return cv2.compareHist(src_hist, target_hist, cv2.HISTCMP_CORREL)


def match(src, target):
    r = compareHist(src, target, 2)
    g = compareHist(src, target, 1)
    b = compareHist(src, target, 0)
    return (r + g + b) / 3


def level_match(src):
    match_dict = {
        'debut': match(cv2.imread('./dat/debut.jpg'), src),
        'reguler': match(cv2.imread('./dat/reguler.jpg'), src),
        'pro': match(cv2.imread('./dat/pro.jpg'), src),
        'master': match(cv2.imread('./dat/master.jpg'), src),
        'master+': match(cv2.imread('./dat/master+.jpg'), src),
    }
    return max(match_dict, key=match_dict.get)


result = {}
result['diff'] = level_match(np.asarray(diff)[:, :, ::-1])

# OCR
tools = pyocr.get_available_tools()
tool = tools[0]

digit_builder = pyocr.builders.DigitBuilder(tesseract_layout=6)
builder = pyocr.builders.TextBuilder(tesseract_layout=6)
result['music'] = tool.image_to_string(music, lang="jpn", builder=builder)
result['perfect'] = tool.image_to_string(perfect,
                                         lang="eng",
                                         builder=digit_builder)
result['great'] = tool.image_to_string(great,
                                       lang="eng",
                                       builder=digit_builder)
result['nice'] = tool.image_to_string(nice, lang="eng", builder=digit_builder)
result['bad'] = tool.image_to_string(bad, lang="eng", builder=digit_builder)
result['miss'] = tool.image_to_string(miss, lang="eng", builder=digit_builder)

result['combo'] = tool.image_to_string(combo,
                                       lang="eng",
                                       builder=digit_builder)
result['score'] = tool.image_to_string(score,
                                       lang="eng",
                                       builder=digit_builder)
result['high_score'] = tool.image_to_string(high_score,
                                            lang="eng",
                                            builder=digit_builder)
print(result, args[1])
