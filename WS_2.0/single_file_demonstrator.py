'''
To execute use the following:
python single_file_demonstrator.py --file_path C:\Git_projects\Data\sample13\PR_17.stp --out_path PR_17 --config_path config.ini

'''
from Conversion_update import net_gen
from file_loader_utils import predict_graph, convert_pyg
import argparse, configparser
from pathlib import Path
from model_defs import GAThead3L32H12
import torch
import pandas as pd
import numpy as np
import networkx as nx

#Args and config
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--file_path',type=Path,help='file to predict for')
    parser.add_argument('--out_path',type=Path,help='file to save to')
    parser.add_argument('--config_path',type=Path,help='file containing parameters')

args = parser.parse_args()

config = configparser.ConfigParser()

# Get config (slowly changing parameters)
config.read(args.config_path)
nf = int(config['DEFAULT']['NUM_NODE_FEAT'])
nc = int(config['DEFAULT']['NUM_EDGE_FEAT'])
threshold = float(config['DEFAULT']['THRESHOLD'])
mean_agg = bool(int(config['DEFAULT']['MEAN_AGG']))
tag = str(config['DEFAULT']['TAG'])

#load models
models = {}
for f in Path(config['DEFAULT']['MODEL_FOLDER']).glob('*.ptm'):
    models[f.name]= GAThead3L32H12(nf,nc)
    models[f.name] = torch.load(f,map_location=torch.device('cpu'))

#generate net from file
part = net_gen(args.file_path,tag,mean_agg=mean_agg)
adj_list = nx.to_pandas_edgelist(part)
node_list = pd.DataFrame.from_dict(dict(part.nodes(data=True)), orient='index')
node_list.convert_dtypes()
node_list[node_list.select_dtypes(np.float64).columns] = node_list.select_dtypes(np.float64).astype(np.float32)
#print(node_list.head())
adj_list.to_csv(f'{str(args.out_path)}_adj.csv')

#convert net to pyg data
data = convert_pyg(part,False,nf,nc)

#predict models
dfs = []
for k,v in models.items():
    v.eval()
    with torch.no_grad():
        df = predict_graph(v,data,threshold)
    dfs.append(df)

#combine votes
votes = pd.concat(dfs,ignore_index=True)
g_cols = ['x','y','z','node_type']
agg_dict = {c:('mean' if c[:4]=='prob' else 'sum') for c in [col for col in votes.columns if col not in g_cols]}
votes_count = votes.groupby(g_cols).agg(agg_dict)
votes_count.reset_index(inplace=True)
for c in [col for col in votes_count.columns if col not in g_cols]:
    if c[:4]=='prob':
        votes_count[f"{c}_thresh"] = np.where(votes_count[c]>=threshold,1,0) 
        votes_count.rename(columns={c:'vote.'+c},inplace=True)
    else:
        votes_count[f"{c}_thresh"] = np.where(votes_count[c]>=len(models.keys())/2,1,0) 
        votes_count.rename(columns={c:'vote.'+c},inplace=True)


#save as csv
node_list.reset_index(inplace=True)
node_list.rename(columns={'index':'node'},inplace=True)
votes_count = pd.merge(votes_count,node_list, left_on=['x','y','z'],right_on=['xpoint','ypoint','zpoint'],how='left')
votes_count[votes_count['node_type_x'] == 0].drop(columns=['xpoint','ypoint','zpoint','node_type_y','face_orient_fwd','face_orient_rev','edge_type0','edge_type1','edge_type2','edge_type3','edge_type4','edge_type5','edge_type6','edge_type7','edge_type8','face_basis_degree', 'node_angles', 'degree', 'tag'])[['node','x','y','z','vote.prob','vote.pred','prob_thresh','pred_thresh']].to_csv(str(args.out_path)+'.csv')
votes.to_csv(str(args.out_path)+'_votes.csv') #manual add