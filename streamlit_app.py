# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 13:54:24 2023

@author: ITWILL
"""

import io
import streamlit as st
from tensorflow.keras.models import load_model

from google.cloud import storage
from google.oauth2 import service_account


credentials_file = st.secrets.connection.gcs
bucket_name = st.secrets['my_bucket'] # 버킷이름
st.write(st.secrets.connection.gcs)
button=st.button('load')
if button:
    with st.spinner('loading..'):
        st.title('')
        st.divider()
        cd = service_account.Credentials.from_service_account_info(credentials_file) 
        client = storage.Client(credentials=cd)
       
        bucket = client.bucket(bucket_name)
        blobs = bucket.list_blobs()
       
        h5_blobs = [blob for blob in blobs if blob.name.endswith('.h5')]
    
        models = []
        for blob in h5_blobs:
            h5_data = blob.download_as_string()    
            model = load_model(io.StringIO(h5_data.decode('utf-8')))    
            models.append(model)    
     
        models=models[0]
        if models:
            result='loading complete'
        else:
            result='loading failed'
        st.write(result)
