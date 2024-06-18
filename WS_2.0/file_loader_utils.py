import torch
import pandas as pd
from torch_geometric.utils.convert import from_networkx

def predict_graph(net,data,threshold):
    # is the device on a gpu, working assumption we're not going multi card anytime soon
    gpu = next(net.parameters()).is_cuda
    
    #From Data before it goes to the gpu
    
    #The real world isn't changing from 3d anytime soon either so this holds
    preds = {'x':data.pos[:,0].numpy(),
            'y':data.pos[:,1].numpy(),
            'z':data.pos[:,2].numpy(),
            'node_type':data.x[:,0].numpy()}
    
    # Match data to the net device    
    if gpu:
        data.cuda()
    
    # Get predictions from the network
    pred = torch.sigmoid(net(data))
    
    # move the preds back from gpu if needed
    if gpu:
        pred = pred.cpu()
    
    # Do the gating in one go    
    pred_int = (pred>=threshold).int()
    
    # Get the probability and the gated prediction for each class
    if gpu:
        pred = pred.cpu()
        pred_int = pred_int.cpu()
    preds['prob'] = pred.squeeze(-1).numpy()
    preds['pred'] = pred_int.squeeze(-1).numpy()
        
    #convert the whole thing to a dataframe
    pred_df = pd.DataFrame.from_dict(preds)
    return pred_df


def convert_pyg(g,directed,num_features,num_edge_features):
    if directed:
        g = g.to_directed()
    if 'node_default' in g.graph:
        g.graph.pop("node_default", None)
    if 'edge_default' in g.graph:
        g.graph.pop("edge_default", None)
    data = from_networkx(g,group_node_attrs=all,group_edge_attrs=all)
    data.pos = data.x[:,0:3].float()
    data.x,data.y = data.x[:,3:num_features+3].float(),data.x[:,num_features+3:].float()
    data.edge_attr = data.edge_attr[:,:num_edge_features].float()
    return data