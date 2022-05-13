import face_recognition
import cv2
import os
from database import db_login
import numpy as np

video_capture = cv2.VideoCapture(1)
video=cv2.VideoWriter('D:/Test_Cheating_Detection/video/face.avi',cv2.VideoWriter_fourcc(*'XVID'),20,(640,360))
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


known_face_names=[]
known_face_encodings=[]
sign_stu=[]

def database_login():
    database=db_login()
    cursor = database.cursor()# 使用cursor()方法获取操作游标

    sql = "select * from face"

    cursor.execute(sql)  # 执行sql语句
    results = cursor.fetchall()  # 获取查询的所有记录
    print(type(results))
    print("id", "imformation")
    # 遍历结果
    for row in results:
        id = row[0]
        id=str(id)
        known_face_names.append(id)
        face_imformation = row[1]
        list1 = face_imformation.split(' ')
        list1 = list(map(float, list1))
        arr1 = np.array(list1)
        known_face_encodings.append(arr1)
        #print(id, face_imformation)

    database.close()  # 关闭连接


database_login()  #连接数据库并将数据库中的人脸信息导入
#print(known_face_names)
#print(known_face_encodings)
#face=(' '.join(str(e) for e in li_face_encoding.tolist()))
#str = ' '.join(zhou_face_encoding(i) for i in zhou_face_encoding)
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
    video.write(frame)
print("已签到人员：",sign_stu)

video_capture.release()
cv2.destroyAllWindows()
