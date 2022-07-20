#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''test_streamlit
edit ~/.streamlit/credentials.toml
edit ~/.streamlit/config.toml
edit ./.streamlit/config.toml (per-project config)
export STREAMLIT_SERVER_PORT=80
export STREAMLIT_SERVER_COOKIE_SECRET=randomsecretvalue
> streamlit config show
( streamlit run test_streamlit.py --server.port 8501 )
> streamlit run test_streamlit.py [args]
(at the first exec)

  Welcome to Streamlit!

  If you're one of our development partners or you're interested in getting
  personal technical support or Streamlit updates, please enter your email
  address below. Otherwise, you may leave the field blank.

  Email:

  Privacy Policy:
  As an open source project, we collect usage statistics. We cannot see and do
  not store information contained in Streamlit apps. You can find out more by
  reading our privacy policy at: https://streamlit.io/privacy-policy

  If you'd like to opt out of usage statistics, add the following to
  ~/.streamlit/config.toml, creating that file if necessary:

    [browser]
    gatherUsageStats = false

(first and second third ... exec)

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://...:8501
'''

import sys, os
import datetime
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st
import sqlite3 as sl3

DB = 'data/test_streamlit_db.sl3'
OUTDAT = 'data/test_streamlit_out.csv'
CSVDAT = 'data/test_streamlit_data.csv'

def dump_secrets(**kwargs):
  return ', '.join([f'[{k}]=[{kwargs[k]}]' for k in kwargs])

def test_streamlit():
  print('test streamlit')
  df = pd.read_csv(f'./{CSVDAT}', index_col='月')

  st.title('title')
  st.caption('caption')
  stc = st.columns(3)

  with open(f'./{OUTDAT}', 'wb') as f:
    f.write('test\x0A'.encode('utf-8'))
  with open(f'./{OUTDAT}', 'rb') as f:
    st.write(f.read().decode('utf-8'))

  cn = sl3.connect(f'./{DB}')
  cur = cn.cursor()
  for row in cur.execute('''select id, c1 from tbl order by id;'''):
    st.write(f'id: {row[0]}, c1: [{row[1]}]')
  cn.close()

  st.secrets['DB_Section']['some_new'] = 'new' # not set (load only once ?)
  st.secrets['DB_Section']['some_lst'].append('new') # appends every reload
  os.environ['DUMMY'] = 'hoge'
  st.write('public env', os.environ['DUMMY'])
  st.write('secrets', st.secrets)
  st.write('creds', st.secrets.DB_Credentials)
  st.write('creds', dump_secrets(**st.secrets.DB_Credentials))
  st.write('uid', st.secrets['DB_Credentials']['uid'])
  st.write('token', st.secrets['DB_Credentials']['token'])
  st.write('sec', dump_secrets(**st.secrets.DB_Section))
  st.write('key', st.secrets['DB_Section']['some_key'])
  st.write('lst', st.secrets['DB_Section']['some_lst'])
  st.write('dic', st.secrets['DB_Section']['some_dic'])
  st.write('dicx', st.secrets['DB_Section']['some_dicx'])

  with stc[0]:
    st.subheader('subheader 0')

    with st.form(key='form name'):
      rad = st.radio('radio', ('item0', 'item1', 'item2'))
      sel = st.selectbox('selector', ('item0', 'item1', 'item2'))
      mul = st.multiselect('multi sel ordered', ('item0', 'item1', 'item2'))
      name = st.text_input('name')
      btn_submit = st.form_submit_button('send')
      btn_cancel = st.form_submit_button('cancel')
      print(f'{rad}, {sel}, {mul}, {name}, ', end='')
      print(btn_submit, btn_cancel) # unfocused: no event, clicked: (F/T, F/T)

  with stc[1]:
    st.subheader('subheader 1')

    col = st.color_picker('color', '#ffcc33')
    dts = st.date_input('start', datetime.date(2022, 7, 10))
    dte = st.date_input('end', datetime.date(2022, 7, 20))
    sli = st.slider('slider', min_value=123.4, max_value=456.789)
    chk = st.checkbox('check')
    oth = st.text_input('other')
    btn_dummy = st.button('dummy')
    print(f'{col}, {dts}, {dte}, {sli}, {chk}, {oth}, ', end='')
    print(btn_dummy) # enter/unfocused: F, clicked: F+T twice event if changed

  with stc[2]:
    st.subheader('subheader 2')

    st.line_chart(df)
    # st.bar_chart(df['2021年'])
    # st.dataframe(df)
    # st.table(df)

    fig = plt.figure(figsize=(16, 9), dpi=96)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df.index, df['2021年'])
    ax.set_title('matplotlib 0')
    st.pyplot(fig)

if __name__ == '__main__':
  test_streamlit()
