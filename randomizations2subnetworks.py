


import sys, os
sys.path.insert(0, 'bin')
from yaml_loader import *



def main():
	if len(sys.argv)>1:
		yaml_path = sys.argv[1]
	else:
		yaml_path = "specification_sheet.yaml"

	paths = load_paths(yaml_path)

		
	# Run randomization summary script
	print "Running randomization summary..."
	os.system("Rscript bin/summarize_randomizations.R "+paths["project"])
	th = 0.25 # robustness threshold
	os.system("python clustering/generate_output_network_file.py %s %s %s" %(paths["project"], paths["interactome"], str(th)))

	# Run clustering algorithm (Louvian)
	print "Running clustering algorithm..."
	os.system("python clustering/louvain_clustering.py "+paths["project"])

main()
