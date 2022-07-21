#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json
import urlparse
import requests
requests.packages.urllib3.disable_warnings()

class OCR:

    __cheaterUrl = 'http://i.rcuts.com/update/404'
    __accessTokenUrl = 'https://aip.baidubce.com/oauth/2.0/token'
    # 通用文字识别（高精度版）
    __accurateBasicUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'

    __client = requests

    def __init__(self, image):
        self._image = image
        self._client_id = os.environ.get('client_id') and os.environ.get('client_id').strip()
        self._client_secret = os.environ.get('client_secret') and os.environ.get('client_secret').strip()
        self._connectTimeout = 60.0
        self._socketTimeout = 60.0

    def cheaterConfig(self):
        try:
            config = self.__client.get(self.__cheaterUrl, verify=False).json()
            params = urlparse.parse_qs( urlparse.urlparse( config['api'] ).query )
            return params
        except BaseException as e:
            return None


    def auth(self):
        obj = self.__client.get(self.__accessTokenUrl, verify=False, params={
            'grant_type': 'client_credentials',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        }, timeout=(
            self._connectTimeout,
            self._socketTimeout,
        )).json()
        
        return obj

    def basicAccurate(self):
        """
            通用文字识别（高精度版）
        """
        if self._client_id is None or self._client_secret is None:
            params = self.cheaterConfig()
            if params is None:
                raise RuntimeError('The cheater config is invalid, Please fill in client_id and client_secret')
        else:
            params = self.auth()
            
        data = {}
        data['image'] = self._image;

        response = self.__client.post(
            self.__accurateBasicUrl, 
            data=data,
            params=params,
            verify=False, timeout=(
                self._connectTimeout,
                self._socketTimeout,
            )
        )

        obj = json.loads(response.content) or None
        return obj
        