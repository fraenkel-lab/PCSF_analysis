
import sys, os
import pandas as pd


def main():
	projectPath = sys.argv[1]
	interactome = sys.argv[2]
	
	if len(sys.argv) > 3:
		robust_cutoff = float(sys.argv[3])
	else:
		robust_cutoff = 0.9

	# projectPath = "/nfs/latdata/iamjli/alex/results/human_binned_weights2/"
	# interactome = "/nfs/latdata/iamjli/alex/data/interactome/iRefIndex_v13_MIScore_interactome.txt"

	# import robustness values
	robustnessPath = "%s/summary/summary_nodes_robustness.txt" %(projectPath)
	robustness = pd.read_table(robustnessPath, names=["protein", "robustness"])
	robustness = robustness[robustness["robustness"]>=robust_cutoff]
	robust_nodes = robustness["protein"].tolist()
	print "%d nodes with robustness>=%s found" %(len(robust_nodes), str(robust_cutoff))

	# import interactome 
	edges = []
	with open(interactome, 'r') as f:
		for line in f.readlines():
			p1, p2, score = line.rstrip('\n').split('\t')
			if (p1 in robust_nodes) & (p2 in robust_nodes):
				if p1 != p2: edges.append(line)

	# write edges to file
	out_file = "%s/summary/robust_nodes_edgevals.txt" %(projectPath)
	with open(out_file, 'w') as f:
		for line in edges:
			f.write(line)

	print "%d edges written to %s" %(len(edges), out_file) 	

main()
