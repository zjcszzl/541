import torch
import torch.nn as nn
import random

resized_img = (80, 80)
actions = 2 # action[0] = 1 means no flapping and action[1] = 1 means flapping.

# [None, 4, 80, 80] -> [None, 2]

class DQN(nn.Module):
    '''
        Input: history_size * 4 * 80 * 80
        Output: 1 * 2
    '''
    def __init__(self):
        super(DQN, self).__init__()

        '''
            Build the network
        '''
        # Encoder
        # bs*4*80*80 -> bs*32*20*20
        self.conv1 = nn.Sequential(
            nn.Conv2d(4, 32, kernel_size = 4, stride = 4, padding = 0),
            nn.ReLU(inplace = True)
        )
        # bs*32*20*20 -> bs*64*10*10
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size = 3, stride = 2, padding = 1),
            nn.ReLU(inplace = True)
        )

        # FC
        self.fc_relu = nn.Sequential(
            nn.Linear(64*10*10, 512),
            nn.ReLU(inplace = True),
            nn.Linear(512, actions)
        )
        # self.softmax = nn.Softmax()
    
    # def init_hidden(self):
    #     if torch.cuda.is_available():
    #         return torch.zeros(self.gru_layer_num, 1, self.gru_hidden_size).cuda()
    #     else:
    #         return torch.zeros(self.gru_layer_num, 1, self.gru_hidden_size)

    # Finally get Q-Value
    def forward(self, x):
        # Encoder
        x = self.conv1(x)
        x = self.conv2(x)
        # x = self.conv3(x)

        # GRU
        # hidden = self.init_hidden()
        # x, hidden = self.gru(x.view(-1, 1, 256), hidden)

        # FC
        x = x.view(x.size()[0], -1)
        # x = self.fc_relu(torch.squeeze(x[-1]))
        x = self.fc_relu(x)
        # x = self.softmax(x)

        return x

def weight_init(net):
    for each_module in net.modules():
        if isinstance(each_module, nn.Conv2d):
            torch.nn.init.xavier_uniform_(each_module.weight)
        elif isinstance(each_module, nn.Linear):
            each_module.weight.data.normal_(-0.1, 0.1)
            if each_module.bias is not None:
                each_module.bias.data.zero_()

def randomly_get_action():
    idx = 0 if random.random() < 0.8 else 1
    return idx

if __name__ == '__main__':
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    net = DQN().to(device)
    x = torch.ones((16, 4, 80, 80))
    y = net(x).to(device)
    print(x.shape)
    print(y.shape)