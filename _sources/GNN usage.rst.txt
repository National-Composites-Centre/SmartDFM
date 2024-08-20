GNN usage/implementation
========================

Basic GNN models are currently provided with the main SmartDFM repository. 

Folder structure
----------------
	
The "WS_2.0" subfolder in the directory cointains all the configuration files and Python files required to use the GNN models. These are stored in further sub-folder called "models". Each of the models contain a folder of multiple GNNs to increase robustness through voting mechanism.	

Configuration files
-------------------
Configuration files in "WS_2.0" are quite self explanatory. The key is to adjust the "model folder" field when any model is being replaced or added. This needs to be manually edited based on the location of the cloned library on users disc (to be improved). Each set of GNNs should have dedicated .ini config file.

Execution
---------

The models are used within the pre_base.py functions, through command line initiation of the following format:

.. sourcecode::

	conda run -n ws_pyg_42 python [execution location path] single_file_demonstrator.py --file_path [part] --out_path [output .csv file] --config_path [configuration file]

The command line shown is based on author's installation of Python, through Anaconda, using specific environment name. For alternative Python installations user will need to adjust call-outs to GNNs in ``pre_base.py``. This consists of replacing ``conda run -n ws_pyg_42 python`` with the appropriate command line input that specify Python and the environment if applicable. The "ws_pyg" or other up-to-date .yml should be available in WS_2 folder for generation for the right Python environment ; this is purposefully separate environment from the rest of the SmartDFM tool and should be created separately on user machine as well.

Typically OCC_utils library is not installable through standard .yml based generation of environment. Therefore following command has to be exected within the `ws_pyg_42` (or equivalent):

.. sourcecode::

	pip install git+https://github.com/tpaviot/pythonocc-utils.git

If the user is using other than Anaconda Python environment manager the command needs to be adjusted accordingly.


Result files
------------

Typically each GNN produces 3 .csv result files in "WS_2.0" folder, for example: votes_h.csv, votes_h_adj.csv, votes_h.csv . The "votes_h.csv" is the most important; column C-E represent xyz coordinates of each vertex, and column G denotes how many models predicted this vertex to be part of the feature in question (eg. hole). The "votes_h_adj.csv" is mostly used to understand some of the networks that have been created, as this file denotes neighbouring elements to any vertex considered. 


Processing results
------------------

To understand the processing of the results it is recommended to read through the annotations in the pre-rules that deal with GNN execution, or even specific rules that use the results. The documentation is not maintained here as this will likely be subject of further development in near future. 




