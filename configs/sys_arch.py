from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='Quantum-Assisted Multimodal Fusion (QMF) Sequence')

# Style options
dot.attr(rankdir='LR', size='10')

# Nodes (Entities)
dot.node('U', 'User', shape='box', style='filled', fillcolor='lightblue')
dot.node('S', 'System', shape='box', style='filled', fillcolor='lightgray')
dot.node('M', 'MRI Preprocessing', shape='ellipse', style='filled', fillcolor='lightyellow')
dot.node('P', 'PET Preprocessing', shape='ellipse', style='filled', fillcolor='lightyellow')
dot.node('E', 'EEG Preprocessing (Planned)', shape='ellipse', style='filled', fillcolor='lightpink')
dot.node('Q', 'Quantum Neural Network (QNN)', shape='hexagon', style='filled', fillcolor='lightgreen')
dot.node('C', 'Epilepsy Classifier', shape='diamond', style='filled', fillcolor='lightcyan')
dot.node('R', 'Report/Output Generator (Planned)', shape='box', style='filled', fillcolor='lightpink')

# Arrows (Sequence)
dot.edge('U', 'S', label='Upload BIDS Data')
dot.edge('S', 'M', label='Process MRI')
dot.edge('S', 'P', label='Process PET')
dot.edge('S', 'E', label='Process EEG')
dot.edge('M', 'Q', label='MRI Features')
dot.edge('P', 'Q', label='PET Features')
dot.edge('E', 'Q', label='EEG Metrics')
dot.edge('Q', 'C', label='Latent Embeddings')
dot.edge('C', 'R', label='Classification Result')
dot.edge('R', 'U', label='Return Report')

# Render to file or visualize
dot.render('qmf_sequence_diagram', format='png', view=True)
