import os
import sys
import requests
import json
import cv2
import ctypes
from PyQt5.QtWidgets import *
from PyQt5 import uic

Ui_MainWindow, QtBaseClass = uic.loadUiType("imgAlert.ui");

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pb.clicked.connect(self.btn_clicked)
        
    def btn_clicked(self):
        client_id = "740k0vejvt"
        client_secret = "Rduu1qQwee1StiZpsDurHVsc80aGRuKK3IuGPsHq"
        
        #내 얼굴 인식
        my_face_url = "https://naveropenapi.apigw.ntruss.com/vision/v1/face"
        
        my_img_info = {'image': open('soyeon.jpg', 'rb')}
        headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret }
        response = requests.post(my_face_url,  files=my_img_info, headers=headers)
        rescode = response.status_code
        
        if(rescode==200):
            my_json_data = json.loads(response.text)
            x, y, w, h = my_json_data['faces'][0]['roi'].values()
            
            #이미지 출력
            my_img_read = cv2.imread("soyeon.jpg", cv2.IMREAD_ANYCOLOR)
            cv2.rectangle(my_img_read, (x, y), (x+w, y+h), (255,0,0), 3)
            cv2.imshow("my img show", my_img_read)
            
            #유명인 얼굴 인식
            similar_face_url = "https://naveropenapi.apigw.ntruss.com/vision/v1/celebrity"
            
            my_img_info = {'image': open('soyeon.jpg', 'rb')}
            headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret }
            response = requests.post(similar_face_url,  files=my_img_info, headers=headers)
            rescode = response.status_code
            
            similar_json_data = json.loads(response.text)
            
            ctypes.windll.user32.MessageBoxW(None
                                             ,"[AI가 인식한 "+self.ui.le.text()+"님의 정보]\n성별은 {0}이고 확률은 {1}%이며, 나이는 {2}이고 확률은 {3}%입니다.\n[AI가 인식한 닮은꼴의 정보]\n이름은 {4}이고 확률은 {5}% 입니다.".format(my_json_data['faces'][0]['gender']['value'], my_json_data['faces'][0]['gender']['confidence']*100, my_json_data['faces'][0]['age']['value'], my_json_data['faces'][0]['age']['confidence']*100, similar_json_data['faces'][0]['celebrity']['value'], similar_json_data['faces'][0]['celebrity']['confidence']*100)
                                             ,"CFR(Clova Face Recognition) 연습 - 김소연"
                                             ,0)
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Error Code:" + rescode)
 
if __name__ == "__main__":
            app = QApplication(sys.argv)
            window = MyWindow()
            window.show()           
            app.exec_()