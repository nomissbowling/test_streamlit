#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''0001_algebra
'''

import sys, os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import streamlit as st
from streamlit_webrtc import webrtc_streamer

ICO = 'data/supuuu.png'

def algebra():
  print('0001_algebra')

  ico = Image.open(f'./{ICO}')
  st.set_page_config(page_title='Hello Algebra', page_icon=ico, layout='wide')

  st.header('Algebra')
  stc = st.columns([3, 2])

  rot = st.slider('Rotation', min_value=2, max_value=360)

  with stc[0]:
    st.subheader('problem')

    fig = plt.figure(figsize=(16, 9), dpi=96)
    ax = fig.add_subplot(1, 1, 1)
    th = np.linspace(0, 2 * np.pi, 100)
    x = 141.4 * np.cos(th)
    y = 141.4 * np.sin(th)
    ax.plot(x, y, 'r-')
    ax.set_xlim([-150, 150])
    ax.set_ylim([-150, 150])
    ax.set_title('Rotation')
    ax.set_aspect('equal')
    st.pyplot(fig)

  with stc[1]:
    st.subheader('solve')

if __name__ == '__main__':
  algebra()
