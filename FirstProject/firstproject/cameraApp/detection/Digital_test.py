
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

class eyeTracking(object):
    def __init__(self):
        predictor_path='./FirstProject/firstproject/cameraApp/detection/shape_predictor_68_face_landmarks.dat'
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)
        self.left = [36, 37, 38, 39, 40, 41]
        self.right = [42, 43, 44, 45, 46, 47]
        self.kernel = np.ones((9, 9), np.uint8)
        self.shape = None
    
    
    def shape_to_np(self, shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)
        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        # return the list of (x, y)-coordinates
        return coords

    def eye_on_mask(self, mask, side):
        points = [self.shape[i] for i in side]
        points = np.array(points, dtype=np.int32)
        mask = cv2.fillConvexPoly(mask, points, 255)
        return mask

    def contouring(self, thresh, mid, img, right=False):
        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        try:
            cnt = max(cnts, key = cv2.contourArea)
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if right:
                cx += mid
            cv2.circle(img, (cx, cy), 4, (0, 0, 255), 2)
        except:
            pass

    def run(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 1)
        for rect in rects:

            self.shape = self.predictor(gray, rect)
            self.shape = self.shape_to_np(self.shape)
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            mask = self.eye_on_mask(mask, self.left)
            mask = self.eye_on_mask(mask, self.right)
            mask = cv2.dilate(mask, self.kernel, 5)
            eyes = cv2.bitwise_and(img, img, mask=mask)
            mask = (eyes == [0, 0, 0]).all(axis=2)
            eyes[mask] = [255, 255, 255]
            mid = (self.shape[42][0] + self.shape[39][0]) // 2
            eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
            threshold = 200
            _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
            thresh = cv2.erode(thresh, None, iterations=2) #1
            thresh = cv2.dilate(thresh, None, iterations=4) #2
            thresh = cv2.medianBlur(thresh, 3) #3
            thresh = cv2.bitwise_not(thresh)
            self.contouring(thresh[:, 0:mid], mid, img)
            self.contouring(thresh[:, mid:], mid, img, True)
        return img
        #cv2.imshow('eyes', img)
    

class anglesOfHead(object):
    c_angle = 0

    def __init__(self):
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    def run(self, frame, logg, logg2):
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        
        # To improve performance
        frame.flags.writeable = False
        
        # Get the result
        results = self.face_mesh.process(frame)
        
        # To improve performance
        frame.flags.writeable = True
        
        # Convert the color space from RGB to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        img_h, img_w, img_c = frame.shape
        face_3d = []
        face_2d = []
        
        if results.multi_face_landmarks:
            
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)
                            
                        x, y = int(lm.x * img_w), int(lm.y * img_h)
                        
                        # Get the 2D Coordinates
                        face_2d.append([x, y])
                        
                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])
                        
                # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)
                
                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)
                
                # The camera matrix
                focal_length = 1 * img_w
                
                cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                    [0, focal_length, img_w / 2],
                                    [0, 0, 1]])
                
                # The Distance Matrix
                dist_matrix = np.zeros((4, 1), dtype=np.float64)
                
                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                
                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)
                
                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
                
                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                
                # print(y)
                
                # See where the user's head tilting
                if y < -10:
                    text = "Looking Right"
                    logg.append("right")

                    self.c_angle += 1
                    if self.c_angle > 10:
                        logg2.append("우측 응시 의심")
                        self.c_angle = 0

                elif y > 10:
                    text = "Looking Left"
                    logg.append("left")

                    self.c_angle += 1
                    
                    if self.c_angle > 10:
                        logg2.append("좌측 응시 의심")
                        self.c_angle = 0
                elif x < -10:
                    text = "Looking Down"
                    self.c_angle = 0
                else:
                    text = "Forward"
                    self.c_angle = 0
                    
                    # Display the nose direction
                nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
                    
                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
                
                cv2.line(frame, p1, p2, (255, 0, 0), 2)
                
                # Add the text on the image
                cv2.putText(frame, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        #frame = cv2.flip(frame, 1)
        return frame
        #cv2.imshow('Head Pose Estimation', frame)


class detectAndDisplay(object):
    count_person = 0
    c_people = 0
    c_device = 0

    def __init__(self):
        model_file = './FirstProject/firstproject/cameraApp/detection/yolov3.weights' #경로 설정 필요
        config_file = './FirstProject/firstproject/cameraApp/detection/yolov3.cfg' #경로 설정 필요
        self.net = cv2.dnn.readNet(model_file, config_file)
        self.classes = []
        with open("./FirstProject/firstproject/cameraApp/detection/coco.names", "r") as f:
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
                #부정행위 탐지 -> 핸드폰, 랩탑, 모니터 검출 -> 로그[멀티기기 탐지] 및 화면 캡처
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
                print(i, label)

                 # 사람 수 list
                # if self.classes[class_ids[i]] == "person" and i >=2:
                #     logg.append("more people")
                if self.classes[class_ids[i]]=='person':
                    self.count_person += 1


                # 멀티기기 list
                if self.classes[class_ids[i]] == "cell phone" or self.classes[class_ids[i]] == "laptop" or self.classes[class_ids[i]] == "tvmonitor":
                    logg.append("use digital device")

                    self.c_device += 1
                                        
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
        img = cv2.flip(img, 1)
        return img

