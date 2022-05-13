# 使用方法

## 前提

### 硬件

- 支持CUDA的GPU
CUDA=11.0
pytorch=1.7.0

------------

### 请确认安装以下组件

    python 3.7
    tqdm
    PIL
    numpy
    opencv-python
    dlib
    facerecognition
    pyopenpose
    yolov5(训练好的权重已放在weights中）
    pymysql
    jupyter notebook

    演示视频中主要展示了目前的项目进展
    face_images文件中存放想要识别的人脸图片
    knn中是尝试使用knn算法进行姿态识别的代码和实例
    pose_data中存放人体关节点的训练数据与测试数据


## 修改配置

### 1.face_register.py

    修改第15行对应的人脸图片路径
    修改第24行输入对应的人名

### 2.model——face.py

    修改第对应的文件存放路径

### 3.模块功能
    data_set.ipynb      实现从视频图像中提取人体关节点信息并进行类型标注
    database.py         实现数据库连接
    examination.sql     实现数据库的创建
    face_register.py    实现根据本地人脸图片进行人脸识别
    mask_detection.py   实现口罩检测功能
    model_face.py       实现从数据库中获取人脸数据进行对比并签到
    model_pose.py       实现利用训练好的模型进行人体姿态检测
    net.py              实现将标注好的人体关节点信息通过神经网络进行训练
    phone_detection.py  实现人体与手机的实时目标检测





