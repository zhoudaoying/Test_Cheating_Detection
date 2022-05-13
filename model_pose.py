import sys
import cv2
import os
import math
from sys import platform
import argparse
import numpy as np
import pyopenpose as op
from PIL import Image, ImageDraw, ImageFont
import net


pose_data=np.load("D:/Test_Cheating_Detection/pose_data/data_pose.npy")
type_data=np.load("D:/Test_Cheating_Detection/pose_data/data_type.npy")
pose={0:'unknow',1:'normal',2:'Turn head',3:'Turn body',4:'transmit',5:'sleep'}

net.train()
# 读取视频文件
#videoCapture = cv2.VideoCapture("D:/Test_Cheating_Detection/video/3.26.mp4")
# 通过摄像头的方式
videoCapture=cv2.VideoCapture(1)
videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# 读帧
success, frame = videoCapture.read()
#print(frame)
k = 0
# 设置固定帧率
timeF = 5
j = 0
params = dict()
params["model_folder"] = "D:\\openpose\\models\\"
# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
video=cv2.VideoWriter('D:/Test_Cheating_Detection/video/test1.avi',cv2.VideoWriter_fourcc(*'XVID'),10,(1280,720))
while success:
    k = k + 1
    if (k % timeF == 0):
        j = j + 1
        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        # Process Image
        datum = op.Datum()
        imageToProcess = frame
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        # Display Image
        if(datum.poseKeypoints is None):
            continue
        #np.save(path + 'test_pose2', test_pose)
        # print(test_pose)x
        #test_data = np.squeeze(test_pose)
        # print(test_data)
        rem = net.get(datum.poseKeypoints[:, :, :2])
        text = ""
        outdata = datum.cvOutputData
        for i  in range(rem.shape[0]):
            text = str("pose:%s " % pose[int(rem[i])])
            outdata = cv2.putText(outdata, text, (int(datum.poseKeypoints[i, 0, 0]-55), int(datum.poseKeypoints[i, 0, 1])-120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        #cv2.namedWindow("OpenPose 1.7.0 - Tutorial Python API", 0)
        #cv2.resizeWindow("OpenPose 1.7.0 - Tutorial Python API", 900, 600)  # 设置窗口大小
        #cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", outdata)
        #cv2.waitKey(0)

        #save_image(outdata, 'D:/BaiduNetdiskDownload/openpose1/images/', j)
        print('save image:', k)
        # 显示图像
        cv2.imshow("video", outdata)
        cv2.waitKey(10)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        video.write(outdata)

    success, frame = videoCapture.read()

