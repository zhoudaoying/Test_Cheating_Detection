import torch
import torch.nn as nn
import numpy as np
from tqdm import tqdm

input_num = 25 * 2
layer1_num = 32
layer2_num = 16
layer3_num = 8
output_num = 6
lr = 0.001
steps = 1000


def load(path_X, path_y):
    X = torch.tensor(np.load(path_X))
    y = torch.tensor(np.load(path_y), dtype=torch.int64)
    return X, y

def test_data(len):
    X = torch.zeros(len, 25, 2)
    X[1] = 1
    X[2] = 2
    y = torch.randint(1, output_num, (len,), dtype = torch.int64)
    return X, y

X, y = load('D:/Test_Cheating_Detection/pose_data/data_pose.npy', 'D:/Test_Cheating_Detection/pose_data/data_type.npy')


print('数据总大小:', y.shape[0])
#borad = int(input('输入训练数据大小:\n'))



train_X = X
train_y = y


#train_X = X[:borad]
#train_y = y[:borad]
#test_X = X[borad:]
#test_y = y[borad:]


Net = nn.Sequential(
                    nn.Flatten(),
                    nn.Linear(input_num, layer1_num),
                    nn.ReLU(),
                    nn.Linear(layer1_num, layer2_num),
                    nn.ReLU(),
                    nn.Linear(layer2_num, layer3_num),
                    nn.ReLU(),
                    nn.Linear(layer3_num, output_num)
                    )

optim = torch.optim.Adam(Net.parameters(), lr = lr)
loss = nn.CrossEntropyLoss()

def train():
    for i in tqdm(range(steps)):
        l = loss(Net(train_X), train_y)
        optim.zero_grad()
        l.backward()
        optim.step()

    print('训练集正确率：{:.0%}'.format((((torch.argmax(Net(train_X), dim = 1) == train_y)*1).sum() / torch.tensor(train_y.size())).item()))
    #print('测试集正确率：{:.0%}'.format((((torch.argmax(Net(test_X), dim = 1) == test_y)*1).sum() / torch.tensor(test_y.size())).item()))


def get(data):
    X = torch.tensor(data)
    print(X.shape)
    return torch.argmax(Net(X), dim = 1)