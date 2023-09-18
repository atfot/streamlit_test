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


credentials_file = st.secrets['my_cred'] # 외부 배포시 꼭, 환경변수로 만들어서 배포
bucket_name = st.secrets['my_bucket'] # 버킷이름
button=st.button('load')
if button:
    with st.spinner('loading..'):
        st.title('')
        st.divider()
       	# 서비스키 인증 , Google Cloud Storage용 클라이언트 객체를 생성합니다.
        cd = service_account.Credentials.from_service_account_file(credentials_file) 
        client = storage.Client(credentials=cd)
       
       	# 지정해놓은 버킷 이름 검색 ('waktaverse')
        bucket = client.bucket(bucket_name)
        blobs = bucket.list_blobs()
       
       	# CSV 파일만 필터링
        h5_blobs = [blob for blob in blobs if blob.name.endswith('.h5')]
    
        # CSV files 을 DataFrames 으로
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
