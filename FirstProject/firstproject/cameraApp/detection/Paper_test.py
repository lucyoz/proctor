

import cv2
import numpy as np
import time # -- 프레임 계산을 위해 사용
import datetime
import logging # -- 금지 물체 탐지 시 로그 남기기
import mediapipe as mp
import dlib

logger = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler() #콘솔에 로그 출력을 위함
logger.addHandler(consoleHandler)

min_confidence = 0.5

class detectAndDisplay2(object):
    count_person = 0
    c_people = 0
    c_device = 0
    def __init__(self):
        model_file = './FirstProject/firstproject/cameraApp/detection/yolov3.weights' #경로 설정 필요
        config_file = './FirstProject/firstproject/cameraApp/detection/yolov3.cfg' #경로 설정 필요
        self.net = cv2.dnn.readNet(model_file, config_file)
        self.classes = []
        with open("./FirstProject/firstproject/cameraApp/detection/coco.names", "r") as f: #경로 설정 필요
            self.classes = [line.strip() for line in f.readlines()]
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i-1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        

    def run(self, frame, logg, logg2):
        img = cv2.resize(frame, None, fx=0.8, fy=0.8)
        height, width, channels = img.shape

        #-- 창 크기 설정
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        #-- 탐지한 객체의 클래스 예측
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                

                cheating = False
                #cnt = 0
                #부정행위 탐지 -> 핸드폰, 랩탑, 모니터, 사람 수 검출
                if (class_id==67 or class_id==63 or class_id==62 or class_id==0) and confidence > min_confidence:
                    now = datetime.datetime.now().strftime("%y_%m_%d_%H-%M-%S")
                    now_check = datetime.datetime.now().strftime("%y_%m_%d_%H-%M") #now변수의 분까지
                    #now_time = now - datetime.datetime(d)
                    # 탐지한 객체 박싱
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                   
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

                    
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
        font = cv2.FONT_HERSHEY_DUPLEX
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = "{}: {:.2f}".format(self.classes[class_ids[i]], confidences[i]*100)
                print(label)
                
                # 사람 수 list
                # if self.classes[class_ids[i]] == "person" and i >=2:
                #     logg.append("more people")
                if self.classes[class_ids[i]]=='person':
                    self.count_person += 1
    

                # 멀티기기 list
                if self.classes[class_ids[i]] == "cell phone" or self.classes[class_ids[i]] == "laptop" or self.classes[class_ids[i]] == "tvmonitor":
                    logg.append("use digital device")

                    self.c_device +=1
                    
                    if self.c_device > 10:
                        logg2.append("멀티기기 사용 의심")
                        self.c_device = 0
                
                color = self.colors[i] #-- 경계 상자 컬러 설정 / 단일 생상 사용시 (255,255,255)사용(B,G,R)
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 5), font, 1, color, 1)

        if self.count_person > 1:
            logg.append("more people")
            self.c_people += 1
            
            if self.c_people >10:
                logg2.append("동시 시험 의심")
                self.c_people = 0

        elif self.count_person == 0:
            logg.append("no person")
            self.c_people += 1
            
            if self.c_people > 10 :
                logg2.append("자리 이탈 의심")
                self.c_people = 0

        self.count_person = 0    
    #    end_time = time.time()
    #    process_time = end_time - start_time
        #print("=== A frame took {:.3f} seconds".format(process_time))
        # img = cv2.flip(img, 1)
        return img
        #cv2.imshow("YOLO test", img)
