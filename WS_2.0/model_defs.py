import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv

class GAThead3L32H12(torch.nn.Module):
   def __init__(self,num_node_features,num_edge_feature) -> None:
       super().__init__()
       #(2763x32 and 192x6)
       self.gatconv1 = GATv2Conv(num_node_features,32,12,dropout=0.5,edge_dim=num_edge_feature)
       self.gatconv2 = GATv2Conv(32*12, 32, heads=6, dropout=0.5,edge_dim=num_edge_feature)
       self.gatconv3 = GATv2Conv(32*6,1,heads=1,dropout=0.5,edge_dim=num_edge_feature,concat=False)
    
   def forward(self,data):
       x, edge_index,edge_attr = data.x, data.edge_index,data.edge_attr
       x = self.gatconv1(x, edge_index,edge_attr)
       x = F.elu(x)
       x = F.dropout(x, p=0.5, training=self.training)
       x = self.gatconv2(x, edge_index,edge_attr)       
       x = F.elu(x)
       x = F.dropout(x, p=0.5, training=self.training)
       x = self.gatconv3(x, edge_index,edge_attr)
       return x

class GCN3_Lin1(torch.nn.Module):
    def __init__(self,dataset):
        super().__init__()
        self.conv1 = GCNConv(dataset.num_node_features, 32)
        self.conv2 = GCNConv(32, 24)
        self.conv3 = GCNConv(24,12)
        self.fc1 = Linear(12,6)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv3(x,edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.fc1(x)
        return F.log_softmax(x, dim=1)