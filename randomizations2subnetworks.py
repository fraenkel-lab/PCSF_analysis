


import sys, os
sys.path.insert(0, 'bin')
from yaml_loader import *
import glob


def main():
	if len(sys.argv)>1:
		yaml_path = sys.argv[1]
	else:
		yaml_path = "specification_sheet.yaml"

	paths = load_paths(yaml_path)

	parameters = glob.glob(paths["project"]+"/W*")
	for path in parameters:
		if not os.path.isdir(path+"/summary"):	
			# Run randomization summary script
			print "Running randomization summary..."
			os.system("Rscript bin/summarize_randomizations.R "+path)
			os.system("python bin/summarize_nodes.py %s %s %s" %(path, paths["terminals"], paths["garnet"]))
			th = 0.9 # robustness threshold
			os.system("python clustering/generate_output_network_file.py %s %s %s" %(path, paths["interactome"], str(th)))

			# Run clustering algorithm (Louvian)
			print "Running clustering algorithm..."
			os.system("python clustering/louvain_clustering.py %s %s" %(path, paths["terminals"]))

main()
