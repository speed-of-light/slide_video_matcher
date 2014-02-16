# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ##Normalize 2 sets of features

# <codecell>

import numpy as np
featA = [ 'apple', 'cake', 'bed', 'duck' ]
featB = [ 'apple', 'book', 'bed', '']
featC = [ 'applepie', 'dorm', 'bed', '']
featD = [ 'bed', 'cookie', 'apple', '']
feats = [ featA, featB, featC, featD]
data = np.array(feats).T
data = np.insert(data, 0, [1,2,3,4], axis=1)
data = data.tolist()
data.insert( 0, ['id', 'a','b','c','d'])
print data
make_table(data)
set_row_style(0, color='lightGreen')

# <codecell>

data = np.array(feats).T
data = np.insert(data, 0, [1,2,3,4], axis=1)
data = data.tolist()
data.insert( 0, ['id', 'a','b','c','d'])
data = np.array(data).T[:-2]
data = data.tolist()
data.append(['dist', 1,'-',1,'-'])
make_table(np.array(data).T)
set_row_style(0, color='lightGreen')
set_cell_style(3, 2, color='#FeCC23')
set_cell_style(3, 1, color='#FeCC23')
set_cell_style(3, 3, color='#FeCC23')
set_cell_style(1, 1, color='#FeABBA')
set_cell_style(1, 2, color='#FeABBA')
set_cell_style(1, 3, color='#FeABBA')

# <codecell>

data = np.array([ featA, featC]).T
data = np.insert(data, 0, [1,2,3,4], axis=1)
data = data.tolist()
data.insert( 0, ['id', 'a', 'c'])
data = np.array(data)
data = np.insert(data, 3, ['dist', .8,'-',1,'-'], axis=1)
make_table(np.array(data))
set_row_style(0, color='lightGreen')
set_cell_style(3, 1, color='#FeCC23')
set_cell_style(3, 2, color='#FeCC23')
set_cell_style(3, 3, color='#FeCC23')

# <codecell>

data = np.array([ featA, featD]).T
data = np.insert(data, 0, [1,2,3,4], axis=1)
data = data.tolist()
data.insert( 0, ['id', 'a', 'c'])
data = np.array(data)
data = np.insert(data, 3, ['dist', 1, .7, 1, '-'], axis=1)
make_table(np.array(data))
set_row_style(0, color='lightGreen')
set_cell_style(1, 2, color='#FeCC23')
set_cell_style(3, 1, color='#FeCC23')
set_cell_style(1, 3, color='#FeCC23')
set_cell_style(1, 1, color='#FeABBA')
set_cell_style(3, 2, color='#FeABBA')
set_cell_style(3, 3, color='#FeABBA')

# <markdowncell>

# ## Keg

# <codecell>

import scipy as sp
import VSmain, os, cv2
reload(sys.modules['VSmain'])
from VSmain import Video as vid
from VSmain import PdfFrame as pdf
from VSmain import Frame as frm

def get_good_matches(src, dest):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch( src, dest, k=2)
    good = []
    for m,n in matches:
        if m.distance < 0.4*n.distance:
            good.append(m)
    return good

def draw_matches(matches, kp_src, kp_dest, img_src, img_dest):
    h1, w1 = img_src.shape[:2]
    h2, w2 = img_dest.shape[:2]
    view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
    view[:h1, :w1] = kf_img
    view[:h2, w1:] = si_img
    view[:, :, 1] = view[:, :, 0]
    view[:, :, 2] = view[:, :, 0]
    for i,m in enumerate(matches):
        color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
        #print m.queryIdx
        src_pt = (int(kp_src[m.trainIdx].pt[0]), int(kp_src[m.trainIdx].pt[1]))
        dest_pt = (int(kp_dest[m.queryIdx].pt[0] + w1), int(kp_dest[m.queryIdx].pt[1]))
        if abs(slope(src_pt, dest_pt)) > 0.01: print (i, m.trainIdx, m.queryIdx)
        cv2.line(view, src_pt, dest_pt, color)
        cv2.putText(view, str(src_pt), src_pt, cv2.FONT_HERSHEY_SIMPLEX, .35, color)
    return view

def slope(pts, ptd):
    slope = (float(ptd[1]-pts[1])/(ptd[0]-pts[0])) 
    return slope

home = os.getenv("HOME")
proj_root = 'Projects/slide_matching/pdfs/log_expert'
kf_path= "{}/{}/{}/{}.jpg".format( home, proj_root, 'ffkf', 38)
si_path= "{}/{}/{}/{}.jpg".format( home, proj_root, 'jpg', 1)
kf = frm(cv2.imread(kf_path))
si = pdf( "{}/{}/{}.pdf".format( home, 'Projects/slide_matching/pdfs', 'log_expert'))
kf_kp, kf_des, kf_img = kf.sift_kp()

img = si.get_img(1, size=(kf_img.shape[1], kf_img.shape[0]) )
si_kp, si_des, si_img = si.sift_kp()

gm = get_good_matches(si_des, kf_des)
mres = draw_matches(gm, kf_kp, si_kp, kf_img, si_img)
fig = plt.figure(figsize=(18, 9))
plt.imshow(mres)

# <codecell>

def show_match_progress(src, dest, select):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch( src, dest, k=2)
    good = []
    shit = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)
            try:
                select.index(len(good)-1)
                shit.append([ m.distance, n.distance, m.queryIdx, m.trainIdx, n.queryIdx, n.trainIdx])
            except ValueError:
                continue
    return shit

make_table(show_match_progress(si_des, kf_des, sa))

# <codecell>

print len(gm)
sa = [60, 64, 65, 115, 126, 127]
selected = list( gm[i] for i in sa )
make_table([(sa[i], k.distance, k.queryIdx, k.trainIdx, si_kp[k.queryIdx].pt, kf_kp[k.trainIdx].pt) for i,k in enumerate(selected)])
set_row_style(1, color='#FECCDD')
set_row_style(2, color='#FECCDD')
set_row_style(4, color='#FEeF86')
set_row_style(5, color='#FEeF86')

# <codecell>

mres = draw_matches(selected, kf_kp, si_kp, kf_img, si_img)
fig = plt.figure(figsize=(18, 9))
plt.imshow(mres)

# <codecell>

import scipy as sp
import VSmain, os, cv2
reload(sys.modules['VSmain'])
from VSmain import Video as vid
from VSmain import PdfFrame as pdf
from VSmain import Frame as frm

home = os.getenv("HOME")
proj_root = 'Projects/slide_matching/pdfs/log_expert'
kf_path= "{}/{}/{}/{}.jpg".format( home, proj_root, 'ffkf', 26)
si_path= "{}/{}/{}/{}.jpg".format( home, proj_root, 'jpg', 1)
kf = frm(cv2.imread(kf_path))
si = pdf( "{}/{}/{}.pdf".format( home, 'Projects/slide_matching/pdfs', 'log_expert'))
kf_kp, kf_des, kf_img = kf.sift_kp()

img = si.get_img(1, size=(kf_img.shape[1], kf_img.shape[0]) )
si_kp, si_des, si_img = si.sift_kp()

gm = get_good_matches(kf_des, si_des)
mres = draw_matches(gm, kf_kp, si_kp, kf_img, si_img)
fig = plt.figure(figsize=(18, 9))
plt.imshow(mres)

# <codecell>

print 'test'
print 'ok'

# <codecell>

%connect_info

# <markdowncell>

# ## List of matchings

# <codecell>

answer = raw_input("What is your favourite colour? ")
answer

# <codecell>


