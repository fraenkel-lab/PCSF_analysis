
import sys, os
import networkx as nx
import community



def create_NX_obj(edges):
	# takes list of edges of format [p1, p2, weight]
	G = nx.Graph()
	for edge in edges:
		G.add_edge(edge[0], edge[1], weight=float(edge[2]))
	print "%d edges added." %(len(edges))
	return G


def main():
	# define paths
	projectPath = sys.argv[1]
	terminalPath = sys.argv[2]	
	robustPath = projectPath+"/summary/robust_nodes_edgevals.txt"
	f_out = projectPath+"/summary/louvian_clustering/"
	robustnessVals = projectPath+"/summary/summary_nodes_robustness.txt"	
	
	if not os.path.exists(f_out): os.makedirs(f_out)
	

	# read optimal forest (set with cutoff) into array
	edges = []
	with open(robustPath, 'r') as f:
		for line in f.readlines():
			edges.append(line.rstrip('\n').split('\t'))
	
	# create NX object
	G = create_NX_obj(edges)

	# Louvain clustering
	partition = community.best_partition(G)
	clusters = []
	for com in set(partition.values()):
		list_nodes = [nodes for nodes in partition.keys() if partition.keys() if partition[nodes] == com]
		clusters.append(list_nodes)		
	clusters.sort(key=lambda a: -len(a))
	print "%d clusters found with sizs:" %len(clusters)
	print [len(x) for x in clusters]

	# match cluster nodes with node type (from terminal folder). This will not identify TFs!!! TODO
	terminals = []
	with open(terminalPath, 'r') as f:
		for line in f.readlines():
			node = line.split('\t')[0]
			terminals.append(node)

	# match with robustness
	robustness = {}
	with open(robustnessVals, 'r') as f:
		for line in f.readlines():
			data = line.rstrip('\n').split('\t')
			robustness[data[0]] = data[1]

	# write out cluster information
	with open(f_out+"node_membership.txt", 'w') as f:
		for i, cluster in enumerate(clusters):
			for node in cluster:
				if node in terminals: nodeType="Terminal"
				else: nodeType="Steiner"
				f.write("%d\t%s\t%s\t%s\n" %(i, node, nodeType, robustness[node]))
	
	# write annotations
	os.system("python clustering/analyze_gene_clusters_enrichr.py "+f_out+"node_membership.txt")	

main()
