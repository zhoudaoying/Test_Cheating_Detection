import face_recognition
import cv2
import os
import numpy as np

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

video_capture = cv2.VideoCapture(1)
#url = 'rtsp://admin:admin@192.168.102.72:8554/live'
#video_capture = cv2.VideoCapture(url)
# 本地图像
zhou_image = face_recognition.load_image_file("D:/Test_Cheating_Detection/face_images/zhou.jpg")
zhou_face_encoding = face_recognition.face_encodings(zhou_image)[0]
# 本地图像二
li_image = face_recognition.load_image_file("D:/Test_Cheating_Detection/face_images/li.jpg")
li_face_encoding = face_recognition.face_encodings(li_image)[0]


# Create arrays of known face encodings and their names
# 脸部特征数据的集合
known_face_encodings = [
    zhou_face_encoding,
    li_face_encoding
]

# 人物名称的集合
known_face_names = [
    "zhou",
    "li",
]


sign_stu=[]


while True:
    # 读取摄像头画面
    ret, frame = video_capture.read()
    # 改变摄像头图像的大小，图像小，所做的计算就少
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # 根据encoding来判断是不是同一个人，是就输出true，不是为flase
        face_locations = face_recognition.face_locations(rgb_small_frame,model="hug")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # 默认为unknown
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"


            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            face_names.append(name)
            if (name in sign_stu) or (name=='Unknown'):
                pass
            else:
                sign_stu.append(name)

    process_this_frame = not process_this_frame

    # 将捕捉到的人脸显示出来
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # 矩形框
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #加上标签
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display
    cv2.imshow('monitor', frame)

    # 按Q退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("已签到人员：",sign_stu)

video_capture.release()
cv2.destroyAllWindows()
