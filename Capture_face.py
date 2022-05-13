import face_recognition
import cv2
import os


video_capture = cv2.VideoCapture(1)

while True:
    # 读取摄像头信息
    # ret表示是否正常捕获到图像
    # frame表示当前帧，即一张图片
    ret, frame = video_capture.read()
    # 开始处理
    if ret:
        # 转换 BGR(opencv使用) 为 RGB(face_recognition使用)
        rgb_img = frame[:, :, ::-1]
        # 识别图片中的脸部（可能存在多个脸）
        face_locations = face_recognition.face_locations(rgb_img)
        # 遍历人脸位置信息
        for top, right, bottom, left in face_locations:
            # 对人脸画框
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("video", frame)
    if cv2.waitKey(1) == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
