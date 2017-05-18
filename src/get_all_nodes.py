from glob import glob
import sys, os

def get_nodes(path):
	regex = path+"/*/*_nodeattributes.tsv"
	files = glob(regex)
	nodes = []
	for file in files:
		with open(file, 'r') as f:
			for line in f.readlines()[1:]:
				node = line.split('\t')[0]
				nodes.append(node)
	print "%d nodes found" %len(set(nodes))
	return set(nodes)		
