#These are from python-occ and pythonocc-utils
from re import X
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Extend.DataExchange import read_step_file
from OCCUtils import face as ocu_face
from OCCUtils import edge as ocu_edge

#This is the network package - might need replacing for something faster at scale
import networkx as nx

#This is for matrix manipulation and calculating the normal of a vector
from scipy.linalg import orth

#Standard Utility imports
#import matplotlib.pyplot as plt < unnessessary in training.
from pathlib import Path as pth
import pandas as pd
import numpy as np
from typing import Dict, List,Tuple,Union
from itertools import combinations

np.seterr(all="ignore")

def read_tags(label_path:Union[str,pth],tag_type:str,label_column:int=0,blank_rows:int=1)->pd.DataFrame:
    """This function reads in the tags from a tag file and generates a dataframe of the basic details.

    Args:
        lable_path (Path/Str): The path to the file with the tags and co-ords in
        tag_type (str): The label for the model in question e.g. "hole"
        label_column (int) : which column holds the label (default = 2 i.e. third)
        blank_rows (int): how many blank rows are at the top of the file (default = 1 i.e. one blank row)
        

    Returns:
        pd.DataFrame: A data frame format of the data with the tag on every line.
    """

    #This function will read the lines in to three columns (x,y,z) and on lines with a tag (tag,blank, blank)
    df = pd.read_csv(pth(label_path),skiprows=blank_rows,names=['x','y','z'])
    
    #This will 1. Take the first column and return the lines with text (tags) then fill down that column so each line has the tag.
    df['tag'] = df.iloc[:,label_column].str.extract(r'([a-zA-Z]+)',expand=False).ffill(axis=0)
    df['tag'] = df['tag'].str.strip().str.lower()
    df=df[df['tag']==tag_type.strip().lower()]

    #Any row with the base tag will have nulls so drop them leaving only the tagged lines.
    df.dropna(inplace=True)

    #This is the easy way to rename the columns in a simple df
    df.columns = ['x','y','z','tag']

    #Set the types, clean up and return
    df.x = df.x.astype(np.float64)
    df.y = df.y.astype(np.float64)
    df.z = df.z.astype(np.float64)
    df = df.round(7)
    return df

def angle_btw(v1, v2):
    """This calculates the angle between two vectors.

    Based on https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python

    Args:
        v1 (array-like): vector 1 - angle from this
        v2 (array-like): vector 2 - angle too this

    Returns:
        float: The angle from v1 to v2 in radians.
    """
    u1 = v1 / np.linalg.norm(v1)
    u2 = v2 / np.linalg.norm(v2)

    y = u1 - u2
    x = u1 + u2

    # Added this to deal with norm 0 - as the length of opposite tends to inf or adjacent tends to 0 then opp/adj tends to inf and that is 90 degree or pi/2 radians.
    if np.linalg.norm(x)==0:
        a0 = np.pi/2
    else:
        a0 = 2 * np.arctan(np.linalg.norm(y) / np.linalg.norm(x))

    if (not np.signbit(a0)) or np.signbit(np.pi - a0):
        return a0
    elif np.signbit(a0):
        return 0.0
    else:
        return np.pi
    
def vec_gen(graph,n1,n2):
    """Use the co-ordinates for each end of an edge to generate a 3d straight vector i.e.
                                   
         │             (x2,y2)     
         │                  ■      
         │                  •      
         │                  •y2─y1 
         │                  •      
         │                  •      
         │                  •      
         │                  •      
         │                  •      
         │(x1,y1)           •      
         │     ■•••••••••••••      
         │         x2─x1           
         ──────────────────────    
    Args:
        graph (Graph): The graph the nodes are in
        n1 (node/id): The origin node
        n2 (node/id): The destination node

    Returns:
        list: The vectors from n1 to n2
    """
    return [float(graph.nodes[n1]['xpoint'])-float(graph.nodes[n2]['xpoint']),float(graph.nodes[n1]['ypoint'])-float(graph.nodes[n2]['ypoint']),float(graph.nodes[n1]['zpoint'])-float(graph.nodes[n2]['zpoint'])]

def node_angle_calc(graph,node_type=0,neighbors_of_type = False):
    """Calculate the average angle for each node:
        1. get all the relevant nodes
        2. Generate the list of vectors for each node
        3. Generate the angles for each vector pair at a node
        4. Return the average

    Args:
        graph (Graph): The underlying graph object
        node_type (int, optional): Do you want to do real nodes (0) or face nodes 1. Defaults to 0.
        neighbors_of_type (bool, optional): Include only nodes of the specified type in in the calc i.e. only real node pairs as opposed to only real nodes but for those nodes include the faces. Defaults to False.

    Returns:
        _type_: _description_
    """
    type_nodes = [n for n in graph.nodes() if graph.nodes[n]['node_type'] == node_type]
    vecs = {n:[vec_gen(graph,n,adj) for adj in graph.neighbors(n) if graph.nodes[adj]['node_type'] == node_type or not neighbors_of_type] for n in type_nodes}
    angles = {k:[angle_btw(n[0],n[1]) for n in combinations(v,2)] for k,v in vecs.items()}
    return {n:np.mean(v) if not np.isnan(np.mean(v)) else 0 for n,v in angles.items()}

def node_edge_agg(graph:nx.Graph,mean_agg=True)->Dict:
    #print([[e for e in graph.edges(nbunch=[n])] for n in graph.nodes()])
    node_agg = []
    degree_dict = {node:val for (node, val) in graph.degree()}
    if mean_agg:
        for i in range(1,9):
            node_agg.append({n:np.mean([graph.get_edge_data(e[0],e[1])['curve_type_'+str(i)] for e in graph.edges([n])]) for n in graph.nodes()})
    else:
        for i in range(1,9):
            node_agg.append({n:np.count_nonzero([graph.get_edge_data(e[0],e[1])['curve_type_'+str(i)] for e in graph.edges([n])]) for n in graph.nodes()})
        node_agg.insert(0,{n:(degree_dict[n]-sum([l[n] for l in node_agg])) for n,d in graph.nodes(data=True)})
    return node_agg,degree_dict

def face_basis_degree(graph,face):
    """Calculate the dgree of the basis for the vectors that span a face.
    i.e. a flat face will have degree 2, a curved face will have degree 3.

    Args:
        graph (Graph): The underlying graph object
        face (Node id): the face node identifier

    Returns:
        int: the number of none zero basis vectors.
    """
    fn0 =  list(graph.neighbors(face))
    fe = [e for e in graph.edges() if e[0] in fn0 and e[1] in fn0]
    vecs= [vec_gen(graph,e[0],e[1]) for e in fe]
    ortho = orth(np.transpose(vecs))
    zero_basis = np.where(np.sum(np.abs(ortho), axis=1)==0)[0]
    return ortho.shape[0]-len(zero_basis)

def verbose_part(t:TopologyExplorer,tags:pd.DataFrame)->None:
    """Print out the part specs for debugging

    Args:
        t (TopologyExplorer): The TE object from the loaded shape
        tags (pd.DataFrame): the tags from the tag function
    """
    print('Shape data:')
    print('compound solids:',t.number_of_comp_solids())
    print('solids:',t.number_of_solids())
    print('shapes:',t.number_of_shells())
    print('faces:',t.number_of_faces())
    print('wires:',t.number_of_wires())
    print('verticies:',t.number_of_vertices())
    print('edges:',t.number_of_edges())
    print('tags:')
    print(tags)

def basic_edge_features(t:TopologyExplorer)->Tuple[List,Dict,Dict]:
    """Calculate the basic features of edges that don't rely on other features

    Args:
        t (TopologyExplorer): A part toplogy

    Returns:
        Tuple[List,Dict,Dict]: The list of edges (with self-loops for networkx), the curve types, and curve length
    """
    al = [[e.__hash__() for e in t.vertices_from_edge(edge)] for edge in t.edges()]
    al = [l if len(l) >1 else l*2 for l in al]
    curve_types ={tuple(e.__hash__() for e in t.vertices_from_edge(edge)) if len(list(t.vertices_from_edge(edge)))==2 else tuple(e.__hash__()  for e in t.vertices_from_edge(edge))*2:BRepAdaptor_Curve(edge).GetType() for edge in t.edges()}
    return al, curve_types

def basic_node_attributes(t:TopologyExplorer,tags:pd.DataFrame,tag_name:str,unlabled:bool=True)->Dict:
    """The basic node attributes, not reliant on other nodes

    Args:
        t (TopologyExplorer): A part toplogy
        tags (pd.DataFrame): The xyz labelled nodes
        tag_name (str): give the name of the one feature being trained in this model
        unlabled (bool, optional): If this isn't for training load it with blank lables and don't require them. Defaults to True.

    Returns:
        Dict: _description_
    """
    points = {v.__hash__():(BRep_Tool.Pnt(v).X(),BRep_Tool.Pnt(v).Y(),BRep_Tool.Pnt(v).Z()) for v in t.vertices()}
    points_df = pd.DataFrame.from_dict(points,orient='index')
    points_df.reset_index(inplace=True)
    points_df.columns = ['node','x','y','z']
    if not unlabled:
        tags['tag_bin'] = np.where(tags['tag']==tag_name,1,0)
        tags['node_type'] = 0
        node_tags_df = pd.merge(points_df.round(7),tags,on=['x','y','z'],how='left')[['node','x','y','z','tag_bin','node_type']]
        node_tags_df[['tag_bin','node_type']] = node_tags_df[['tag_bin','node_type']].fillna(0)
        node_tags_df['face_orient_fwd']=0
        node_tags_df['face_orient_rev']=0
        node_tags = node_tags_df.set_index('node').to_dict()
    else:
        points_df['tag_bin'] = np.nan
        points_df['node_type'] = 0
        points_df['face_orient_fwd']=0
        points_df['face_orient_rev']=0
        node_tags = points_df.round(7).set_index('node').to_dict()
        
    return node_tags


    


def net_gen(part_path:pth,tag_name:str,lable_path:pth=None,verbose:bool=False,unlabled:bool=True,mean_agg=True)->nx.Graph:
    """From a given part (stp) and lable (txt) generate a graph and all the features.

    Args:
        part_path (pth): location of the step file
        lable_path (pth): location of the tag file
        verbose (bool, optional): Print part info. Defaults to False.
        tag_map (Dict[str,List[int]], optional): Provide a tag mapp in string:list of ints format. Defaults to None.

    Returns:
        nx.Graph: a graph object with all the relevant features added
        
        1798842155 dict_keys(['tag', 'node_type', 'face_orient_fwd', 'face_orient_rev', 'edge_type1', 'edge_type2', 'edge_type3', 'edge_type4', 'edge_type5', 'edge_type6', 'edge_type7', 'edge_type8', 'face_basis_degree', 'node_angles', 'degree'])
1798899995 dict_keys(['node_type', 'edge_type1', 'edge_type2', 'edge_type3', 'edge_type4', 'edge_type5', 'edge_type6', 'edge_type7', 'edge_type8', 'face_basis_degree', 'tag', 'face_orient_fwd', 'face_orient_rev', 'node_angles', 'degree'])
    """
 
    shp = read_step_file(str(part_path))

    t = TopologyExplorer(shp)
    
   
    #get edges and attributes
    al, curve_types = basic_edge_features(t)


    #Generate base graph
    g = nx.from_edgelist(al,nx.Graph)

    if not unlabled:
        tags = read_tags(lable_path,tag_name)
    else:
        tags = pd.DataFrame(data=[[0.,0.,0.,None] for x in range(len(g))],columns=['x','y','z','tag'])

    if verbose:
        verbose_part(t,tags)

    #set edge attributes
    for i in range(1,9):
        nx.set_edge_attributes(g,{k:1 if v==i else 0 for k,v in curve_types.items()},'curve_type_'+str(i))
        

    
    #get and set node basic attributes
    node_tags = basic_node_attributes(t,tags,tag_name,unlabled)


    nx.set_node_attributes(g,node_tags['x'],'xpoint')
    nx.set_node_attributes(g,node_tags['y'],'ypoint')
    nx.set_node_attributes(g,node_tags['z'],'zpoint')    
    nx.set_node_attributes(g,node_tags['node_type'],'node_type')
    nx.set_node_attributes(g,node_tags['face_orient_fwd'],'face_orient_fwd')
    nx.set_node_attributes(g,node_tags['face_orient_rev'],'face_orient_rev')


    #Generate dependent tags for faces etc    
    face_node_edges = [(f.__hash__(),v.__hash__(),{'curve_type_'+str(i):1 if i==8 else 0 for i in range(1,9)}) for f in t.faces() for v in t.vertices_from_face(f)]
    face_nodes = [(f.__hash__(),{'xpoint':ocu_face.Face(f).mid_point()[1].X(),'ypoint':ocu_face.Face(f).mid_point()[1].Y(),'zpoint':ocu_face.Face(f).mid_point()[1].Z(),'node_type':1}) for f in t.faces()]


    g.add_nodes_from(face_nodes)
    g.add_edges_from(face_node_edges)

        
    face_orient_fwd = {f.__hash__():1 if ocu_face.Face(f).Orientation() else 0 for f in t.faces()}
    face_orient_rev = {f.__hash__():0 if ocu_face.Face(f).Orientation() else 1 for f in t.faces()}
    
    nx.set_edge_attributes(g, {(e[0],e[1]):e[2] for e in face_node_edges})

    fb = {f:face_basis_degree(g,f) for f,v in g.nodes(data=True) if  v['node_type'] == 1}


    node_angles_0  = node_angle_calc(g,node_type=0,neighbors_of_type=True)
    node_angles_1 = node_angle_calc(g,node_type=1,neighbors_of_type=False)
    for n in g.nodes():
        if n not in fb.keys():
            fb[n]=0
            
    node_angles = {**node_angles_0,**node_angles_1}
    
    nx.set_node_attributes(g,face_orient_fwd,'face_orient_fwd')
    nx.set_node_attributes(g,face_orient_rev,'face_orient_rev')
    
    node_agg,degree_dict = node_edge_agg(g,mean_agg=mean_agg)
    for i,et in enumerate(node_agg,int(mean_agg)):
        nx.set_node_attributes(g,et,'edge_type'+str(i))
        

    nx.set_node_attributes(g,fb,'face_basis_degree')
    nx.set_node_attributes(g,node_angles,'node_angles')
    nx.set_node_attributes(g,degree_dict,'degree')
    

        
    nx.set_node_attributes(g,node_tags['tag_bin'],'tag')
    face_tags = {}
    for f, _ in face_nodes:
        face_tags[f] = int(all([g.nodes[n]['tag'] for n in g.neighbors(f)]))
    nx.set_node_attributes(g,face_tags,'tag')
    
    return g
'''
def show_network(g, col_map=None):
    if col_map is None:
        col_map = ['red','yellow','blue','violet','cyan','magenta','black','green','pink']
    n_labels = {k:np.round(np.array(v),2) for k,v in nx.get_node_attributes(g,'point').items()}
    colors = [col_map[g[u][v]['curve_type']] for u,v in g.edges()]

    #edge_color = colors,labels = n_labels, with_labels = True
    fig = plt.figure(1, figsize=(2, 2), dpi=480)
    pos = nx.spring_layout(g,k=0.3)
    nx.draw(g,pos,edge_color = colors,labels = n_labels, with_labels = True,node_size=2,font_size =0.52)
    nx.draw_networkx_edge_labels(g,pos,edge_labels=nx.get_edge_attributes(g,'curve_type'),font_size=0.5);
'''

def save_graph(g,oPath,name):
    nx.write_graphml(g,str(pth(oPath,name+'.graphml')))