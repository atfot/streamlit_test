# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 13:54:24 2023

@author: ITWILL
"""
import streamlit as st
from tensorflow.keras.models import load_model
from st_files_connection import FilesConnection

button=st.button('load')
if button:
    with st.spinner('loading..'):
        st.title('')
        st.divider()
        conn = st.experimental_connection('gcs', type=FilesConnection)
        models = conn.read("gs://csac_final_v2/new/model_resnetrs50_lion_dense10240.h5")
        if models:
            result='loading complete'
        else:
            result='loading failed'
        st.write(result)
