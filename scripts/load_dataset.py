from ogb.nodeproppred import NodePropPredDataset
import os
import pandas as pd

# Set dataset storage directory
DATASET_DIR = "dataset/ogbn_arvix"  # Change as needed
os.makedirs(DATASET_DIR, exist_ok=True)

# Load dataset from local storage
dataset = NodePropPredDataset(name="ogbn-arxiv", root=DATASET_DIR)
graph, labels = dataset[0]  # Graph object and node labels

# Print basic details
print("Nodes:", graph['num_nodes'])
print("Edges:", graph['edge_index'].shape)
print("Node Features Shape:", graph['node_feat'].shape)
print("Labels Shape:", labels.shape)

# Convert to DataFrame
df_nodes = pd.DataFrame(graph['node_feat'])
df_labels = pd.DataFrame(labels, columns=['label'])

print(df_nodes.head())  # Preview nodes
print(df_labels.head())  # Preview labels
