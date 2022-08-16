#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''0000_media
'''

import sys, os
import datetime
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import qrcode
#(Unable to find zbar shared library)
#from pyzbar import pyzbar

ICO = 'data/supuuu.png'
MOVDAT = 'data/CASIO_sample_CIMG1226.mov'
IMAGES = ('data/4colors_sense_test_org.png', 'data/4colors_sense_test.png')

URL = 'https://gist.github.com/nomissbowling/7382984d890cda695d875f86b70743e0'

def imread_via_numpy(fn):
  flg = cv2.IMREAD_COLOR # cv2.IMREAD_UNCHANGED
  img = np.fromfile(fn, dtype=np.uint8)
  im = cv2.imdecode(img, flg) # not use cv2.imread for jp file
  if im.ndim == 3: im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
  return im

def asbytes(fn):
  b = b''
  with open(fn, 'rb') as f: b = f.read()
  return b

def media():
  print('0000 media')
  ims = [Image.open(_) for _ in IMAGES]
  # ias = [cv2.cvtColor(cv2.imread(_), cv2.COLOR_BGR2RGB) for _ in IMAGES]
  ias = [imread_via_numpy(_) for _ in IMAGES]

  ico = Image.open(f'./{ICO}')
  st.set_page_config(page_title='Hello Media', page_icon=ico, layout='wide')

  qr = qrcode.QRCode(version=2, # 1 to 40
    error_correction=qrcode.constants.ERROR_CORRECT_M, # L M Q H
    box_size=4, border=8)
  qr.add_data(URL)
  qr.make()
  qim = qr.make_image(fill_color='#000000', back_color='white').convert('RGB')
  qim = np.asarray(qim, dtype=np.uint8)
  #qtx = [_[0].decode('utf-8') for _ in pyzbar.decode(qim)]

  # bdy = '- [test0](https://youtube.com/)'
  bdy = urllib.request.urlopen(URL).read().decode('utf-8')
  bs = BeautifulSoup(bdy, features='html.parser')
  src = bs.find('a', class_='btn-sm btn')['href']
  src = f'https://gist.github.com{src}'
  bdy = urllib.request.urlopen(src).read().decode('utf-8')
  bdy = '\n'.join(bdy.split('\nvideos\n======\n')[0].split('\n')[:2+35])

  st.header('Media')
  stc = st.columns([3, 2])

  with stc[0]:
    st.subheader('subheader 0')

    #for tx in qtx: st.text(tx)
    st.image(qim, width=200)

    st.markdown('[media](media)', unsafe_allow_html=True)

    webrtc_streamer(key='webrtc example')

    tmp = Image.open('./data/supuuu.png')
    st.image(np.asarray(tmp, dtype=np.uint8), width=200)

    st.video(asbytes('./data/30Hz8Hz.wav')) # OK chrome and ff
    # st.video(asbytes('./data/32Hz8Hz.wav')) # OK chrome and ff

    # st.video(asbytes('./data/_animation.gif')) # OK chrome but not play
    # st.video(asbytes('./data/_ttf.mp4')) # OK chrome but not play
    # st.video(asbytes('./data/clip_py.avi')) # OK chrome but not play
    # st.video('file:///d:/prj/test_streamlit/data/clip_py.avi') # os error

    # st.video(asbytes(f'./{MOVDAT}')) # OK chrome
    # st.video(f'd:/prj/test_streamlit/{MOVDAT}') # OK chrome
    # st.video('http://arch.casio.jp/file/dc/CIMG1226.mov') # OK chrome

    st.image(ims, width=200)
    st.image(ias, width=200)

  with stc[1]:
    st.subheader('subheader 1')

    st.markdown(bdy, unsafe_allow_html=True)

    st.text('text\nabc\nxyz')
    code = '''
import streamlit as st
st.title('test')
'''
    st.code(code, language='python')
    st.text('text\nabc\nxyz')

if __name__ == '__main__':
  media()
