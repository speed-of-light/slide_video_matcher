# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os
import matplotlib.pyplot as plt
import cv2, cv

class Frame:
  def __init__(self, img):
    self.img = img

  def gray(self):
    #img = cv2.imread('home.jpg')
    gray= cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    return gray

  def sift_kp(self):
    sift = cv2.SIFT()
    gray= cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    kp, des = sift.detectAndCompute(gray,None)
    img = cv2.drawKeypoints(gray,kp, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return kp, des, img
    #cv2.imwrite('sift_keypoints.jpg',img)

  def surf_kp(self):
    surf = cv2.SURF(4000)
    gray= cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    kp, des = surf.detectAndCompute( gray,None)
    uimg = cv2.drawKeypoints(gray, kp, None, (255,0,0),4)
    return kp, des, uimg

class Video:
  def __init__(self, video_path=""):
    capture = cv2.VideoCapture(video_path)
    self.frame_count = capture.get(cv.CV_CAP_PROP_FRAME_COUNT)
    self.vpath = video_path

  def get_frame(self, index):
    if index > self.frame_count: raise Exception("Frame index is out of range.")
    capture = cv2.VideoCapture(self.vpath)
    capture.set(cv.CV_CAP_PROP_POS_FRAMES, index)
    ret, img = capture.read()
    return img[:,:,[2,1,0]] #convert for matplotlib


# <codecell>

from PyPDF2 import PdfFileReader, PdfFileWriter
from pgmagick import Image
import numpy as np
import os

class PdfFrame(Frame):
  def __init__(self, pdf_path):
    filename = os.path.splitext(os.path.basename(pdf_path))
    if filename[1] == 'pdf':  raise Exception("Not a pdf file extension.")
    self.file_name = filename[0]
    self.dir_name = os.path.dirname(os.path.abspath(pdf_path))
    self.pdf_path = pdf_path
    if not os.path.exists( self._working_dir("jpg") ): os.makedirs( self._working_dir("jpg") )
    if not os.path.exists( self._working_dir("pdf") ): os.makedirs( self._working_dir("pdf") )
    #self.convert_to_jpg()
    myfile = PdfFileReader(self.pdf_path)
    self.pages = myfile.getNumPages()
    self.inited = True

  def convert_to_jpg(self):
    if self.pages <= 0: return
    conv = Image()
    conv.density( '100')
    for page in np.arange( 1, self.pages, 1):
      conv.read( "{}[{}]".format(self.pdf_path, page) )
      conv.write( self._working_path('jpg', page))
    print(" Convert pdf to images finished")

  def convert_to_jpg2(self):
    if self.pages <= 0: return
    conv = Image()
    conv.density( '100')
    pdfi = PdfFileReader(self.pdf_path)
    for page in np.arange( 1, self.pages, 1):
      tmpdf = self._working_path('pdf', 'tmp')
      pdfo = PdfFileWriter()
      pdfo.addPage( pdfi.getPage(page))
      pdfo.write(file(tmpdf,'wb'))
      conv.read( tmpdf )
      conv.write( self._working_path('jpg', page))
    print(" Convert pdf to images ver2 finished")

  def get_img(self, page, size=None):
    if not self.inited:  raise Exception("PdfFrame is not initialized. Please make sure the file is loaded properly.")
    if page <= 0 or page > self.pages: raise Exception("Frame index is out of range.")
    self.img = cv2.imread( self._working_path('jpg', page) )
    if size is not None: self.img = cv2.resize(self.img, size, interpolation=cv2.INTER_CUBIC)
    return self.img

  def _working_dir(self, dir_name):
    return "{}/{}/{}".format(self.dir_name, self.file_name, dir_name)

  def _working_path(self, dir_name, page):
    return "{0}/{1}/{2}/{3}.{2}".format(self.dir_name, self.file_name, dir_name, page)

# <codecell>


