#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tempfile
import datetime
import os
import helper
import base64
from ocr import OCR

def getImagePath():
    temp_dir = 'alfred_img_to_text'
    osascript_path = './mac.applescript'
    temp_path = os.path.join(tempfile.gettempdir(), temp_dir)
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    file_name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.png')
    save_file_path = os.path.join(temp_path, file_name)
    img = os.popen('osascript {} {}'.format(osascript_path, save_file_path))
    imageList = str(img.read()).strip().split('\n')
    if imageList[0] == 'no image':
        raise RuntimeError('The clipboard is empty')
    return imageList[0]

def main():
    try:
        img = getImagePath()
        with open(img, 'rb') as image:
            b64Image = base64.b64encode(image.read())
            content = OCR(b64Image).basicAccurate()
            if content is None:
                raise RuntimeError('Fail to identify!')
            else:
                result = '\n'.join(map(lambda word: word['words'], content['words_result']))
                os.system('echo "{}"|pbcopy'.format(result.encode('utf-8')))
                helper.notify('Success', 'Identified And copy to the clipboard.')

    except BaseException as e:
        helper.notify('Error',str(e))

if __name__ == '__main__':
    main()
 




