import pandas as pd
import numpy as np
from ogb.nodeproppred import NodePropPredDataset
import os

# Set dataset storage directory
DATASET_DIR = "dataset/ogbn_arvix"  # Change as needed
os.makedirs(DATASET_DIR, exist_ok=True)

# Load dataset from local storage
dataset = NodePropPredDataset(name="ogbn-arxiv", root=DATASET_DIR)
data = dataset[0]  # Graph object
edge_index = data[0]['edge_index']  # Citation edges
node_features = data[0]['node_feat']  # Node features (128D embeddings)
labels = data[1]  # Research field labels

# Create output directory
OUTPUT_DIR = "neo4j_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Extract paper nodes
paper_ids = np.arange(node_features.shape[0])
embeddings = [','.join(map(str, row)) for row in node_features]
papers_df = pd.DataFrame({
    'paper_id': paper_ids,
    'embedding': embeddings,
    'label': labels.flatten()
})
papers_df.to_csv(os.path.join(OUTPUT_DIR, "nodes_papers.csv"), index=False)

# Extract citation edges
edges_df = pd.DataFrame({
    'source_id': edge_index[0],
    'target_id': edge_index[1]
})
edges_df.to_csv(os.path.join(OUTPUT_DIR, "edges_citations.csv"), index=False)

# Extract research field labels
unique_labels = np.unique(labels)
fields_df = pd.DataFrame({
    'field_id': unique_labels,
    'field_name': [f"Field_{i}" for i in unique_labels]
})
fields_df.to_csv(os.path.join(OUTPUT_DIR, "nodes_fields.csv"), index=False)

print("CSV files generated successfully!")
