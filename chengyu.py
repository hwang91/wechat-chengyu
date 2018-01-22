# coding: utf-8

import cv2
import os
import time
import re
import numpy as np 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#6763 常用字
word_dict = u''
with open('cy_6763.txt') as f:
	word_dict += f.read()


def get_screenshot():
    os.system("adb shell screencap -p | perl -pe 's/\x0D\x0A/\x0A/g' > screen.png")

def get_words_list():
	im = cv2.imread('screen.png', 0)
	for i in range(24):
		x = 77 + 126 * (i % 8)
		y = 1338 + 135 * (i / 8)
		cv2.imwrite('words/word_%d.png' % i, im[y+1:y+43, x:x+43])

def search_and_press(chengyu):
	for s in chengyu:
		word_dict_idx = word_dict.find(s)
		print word_dict[word_dict_idx], word_dict_idx
		im = cv2.imread('6763/%d.png' % word_dict_idx, 0)
		_, im = cv2.threshold(im,120,255,cv2.THRESH_BINARY_INV)
		im = im.astype(float)
	
		min_dist = 200
		min_idx = 24
		for i in range(24):
			word = cv2.imread('words/word_%d.png' % i, 0)
			_, word = cv2.threshold(word,120,255,cv2.THRESH_BINARY_INV)
			word = word.astype(float)
			dist = np.sum(np.abs(word - im))/word.size
			if dist < min_dist:
				min_dist = dist
				min_idx = i
		# 用过的字不能再用，用纯色覆盖原来的图片
		cv2.imwrite('words/word_%d.png' % min_idx, np.zeros((42,43)))
	
		x = 97 + (min_idx % 8) * 126
		y = 1360 + (min_idx /8) * 137
		cmd = 'adb shell input swipe %d %d %d %d 2' % (x, y, x, y)
		os.system(cmd)
		#time.sleep(0.1)
	# press 确定
	get_screenshot()
	im = cv2.imread('screen.png', 0)
	row_sum = np.sum(im, axis=1)
	y = np.where(row_sum > 255*900)[0][-1] - 90
	os.system('adb shell input swipe 812 %d 812 %d 10' % (y,y))



def main():
	while True:
		chengyu = u''+raw_input()
		get_screenshot()
		get_words_list()	
		search_and_press(chengyu)

if __name__ == '__main__':
	main()












