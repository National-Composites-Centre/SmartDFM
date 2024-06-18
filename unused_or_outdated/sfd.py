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

def WS1(file_path):
    out_path = "D:\\CoSinC_WP4.2\\WS_2.0\\votes"
    config_path = "D:\\CoSinC_WP4.2\WS_2.0\\config.ini"

    #Args and config
    #if __name__ == "__main__":
    #    parser = argparse.ArgumentParser()
    #
    #    parser.add_argument('--file_path',type=Path,help='file to predict for')
    #    parser.add_argument('--out_path',type=Path,help='file to save to')
    #    parser.add_argument('--config_path',type=Path,help='file containing parameters')

    #args = parser.parse_args()

    config = configparser.ConfigParser()

    # Get config (slowly changing parameters)
    config.read(config_path)
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
    part = net_gen(file_path,tag,mean_agg=mean_agg)

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
    agg_dict = {c:('mean' if c[:4]=='prob' else lambda s: pd.Series.mode(s).iloc[0]) for c in [col for col in votes.columns if col not in g_cols]}
    votes_count = votes.groupby(g_cols).agg(agg_dict)
    votes_count.reset_index(inplace=True)
    for c in [col for col in votes_count.columns if col not in g_cols]:
        if c[:4]=='prob':
            votes_count[c] = np.where(votes_count[c]>=threshold,1,0) 
            votes_count.rename(columns={c:'vote.'+c},inplace=True)
        else:
            votes_count.rename(columns={c:'vote.'+c},inplace=True)


    #save as csv
    votes_count[votes_count['node_type'] == 0].to_csv(str(out_path)+'.csv')

WS1("D:\cosinc_WP4.2\WS_old_1.0\sample\s-100.stp")