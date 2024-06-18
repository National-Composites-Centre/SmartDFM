Feature Recognition
===================

Feature recognition is important for many different design related rules. In the SmartDFM base demonstrator GNNs are use for identifiaciton of holes, tool radii, and fillets. The GNN library is to be expanded. There are also alternatives to using GNNs. For instance, if a specific CAD software is used, the design tree can be interogated. However, out of multiple options considered GNNs seemed like the most flexible and versatile, working with any .stp file and being completely software agnostic.

Graph Neural Networks
---------------------

The development, training and validation of the graph neural networks (GNNs) is done in separate repository by a colleague of the author. If you are specifically interested in this, i.e. for developing your own bespoke identifications using GNNs contact the author, and you will be forwarded.

.. toctree::

	GNN usage

	GNN Training
	
	Alternatives to GNNs



