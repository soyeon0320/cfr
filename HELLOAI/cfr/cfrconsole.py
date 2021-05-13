import os
import sys
import requests
import json
import cv2

client_id = "740k0vejvt"
client_secret = "Rduu1qQwee1StiZpsDurHVsc80aGRuKK3IuGPsHq"

url = "https://naveropenapi.apigw.ntruss.com/vision/v1/face"

my_img_info = {'image': open('C:/cfr/img/sy.jpg', 'rb')}
headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret }
response = requests.post(url,  files=my_img_info, headers=headers)
rescode = response.status_code

json_data = json.loads(response.text)
x, y, w, h = json_data['faces'][0]['roi'].values()

my_img = cv2.imread("C:/cfr/img/sy.jpg", cv2.IMREAD_ANYCOLOR)
cv2.rectangle(my_img, (x, y), (x+w, y+h), (255,0,0), 3)

#'gender': {'value': 'female', 'confidence': 0.999729}
print("AI가 인식한 내 성별은 {0}이고, 확률은 {1}% 입니다. ".format(json_data['faces'][0]['gender']['value'], json_data['faces'][0]['gender']['confidence']*100))
#'age': {'value': '18~22', 'confidence': 1.0}
print("AI가 인식한 내 나이는 {0}이고, 확률은 {1}% 입니다. ".format(json_data['faces'][0]['age']['value'], json_data['faces'][0]['age']['confidence']*100))

if(rescode==200):
    url = "https://naveropenapi.apigw.ntruss.com/vision/v1/celebrity"
    
    my_img_info = {'image': open('C:/cfr/img/sy.jpg', 'rb')}
    headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret }
    response = requests.post(url,  files=my_img_info, headers=headers)
    rescode = response.status_code
    
    json_data = json.loads(response.text)
    
    print("──────────────────────────────────────────────")
    print("AI가 인식한 닮은꼴의 이름은 {0}이고, 확률은 {1}% 입니다. ".format(json_data['faces'][0]['celebrity']['value'], json_data['faces'][0]['celebrity']['confidence']*100))
    
    cv2.imshow("my_img", my_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error Code:" + rescode)