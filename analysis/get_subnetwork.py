import pandas as pd
import networkx as nx
import numpy as np
import community
import sys, os

import itertools


def main():
	path, interactome_path, thresh = sys.argv[1:]

	# read in node file, get nodes above threshold
	nodes_attr = pd.read_csv(path+"/summary_nodes.txt", sep='\t')
	print nodes_attr.head()
	nodes_attr = nodes_attr[nodes_attr["robustness"] >= float(thresh)]
	nodes = list(set(nodes_attr["protein"]))

	print nodes
	
	interactome = nx.Graph()
	with open(interactome_path, 'r') as f:
		for line in f.readlines():
			n1, n2, weight = line.rstrip('\n').split('\t')
			interactome.add_edge(n1, n2, weight=float(weight))
		
	
	subgraph = interactome.subgraph(nodes)
	
	# Clustering
	partition = community.best_partition(subgraph)
	clusters = []
	for com in set(partition.values()):
			list_nodes = [nodes for nodes in partition.keys() if partition.keys() if partition[nodes] == com]
			clusters.append(list_nodes)
	clusters.sort(key=lambda a: -len(a))
	print "%d clusters found with sizse:" %len(clusters)	
	print clusters[0]
	cluster_df = []
	for i, cluster in enumerate(clusters):
		for gene in cluster:
			cluster_df.append([gene, i])
	cluster_df = pd.DataFrame(cluster_df, columns=["protein", "cluster_number"])


	nodes_attr = nodes_attr.merge(cluster_df, on="protein", how="left")
	nodes_attr.to_csv("%s/summary_nodes_%s.txt" %(path, thresh), index=False, sep='\t')
	
	out = []
	for n1, n2, w in subgraph.edges(data=True):
		out.append([n1, n2, w["weight"]])

	edge_attr = pd.DataFrame(out, columns=["node1", "node2", "weight"])
	edge_attr.to_csv("%s/edge_attributes_%s.txt" %(path, thresh), sep='\t', index=False)

main()

