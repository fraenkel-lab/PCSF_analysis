
# NAME
# 	PCSF_param_selection.py
#
# SYNOPSIS
# 	python PCSF_param_selection.py [yaml_path]
#
# DESCRIPTION
# 	Generates parameter selection figures, and also cleans up project path file structure
# 
# VERSION
# 	2017-02-07


import sys, os
sys.path.insert(0, 'bin')
from yaml_loader import *


BASH_SYM_LINKS="bin/create_symbolicLink.sh"
SCRIPT_PY_SUMMARIZE="bin/PCSF_summarize_networks.py"
SCRIPT_R_HEATMAP="bin/heatmapFromNodeFrequencyMatrix.R"
SCRIPT_R_PARAMPLOT="bin/PCSF_degree_param_plot.R"
SCRIPT_R_SUMMARY_NODES="bin/summarize_TF_proteomic_steiner.R"
JOBNAME="PCSF_JLI"


def main():
	if len(sys.argv)>1:
		yaml_path = sys.argv[1]
	else:
		yaml_path = "specification_sheet.yaml"

	paths = load_paths(yaml_path)
	w, beta, D, mu = load_params(yaml_path)

	paths["output"] = paths["project"] + "/out_data/"
	
	CMD1 = "bash %s %s %s" %(BASH_SYM_LINKS, paths["project"], paths["output"])
	CMD2 = "python %s -i %s -o %s/summary -n %s -t %s -b %s" %(SCRIPT_PY_SUMMARIZE, paths["output"], paths["output"], JOBNAME, paths["terminals"], paths["interactome"])
	CMD3 = "Rscript %s %s/summary/%s_networkNodeMatrix.tsv" %(SCRIPT_R_HEATMAP, paths["output"], JOBNAME)
	CMD4 = "Rscript %s %s/summary/%s_networkSummary.tsv" %(SCRIPT_R_PARAMPLOT, paths["output"], JOBNAME)
	CMD5 = "Rscript %s %s" %(SCRIPT_R_SUMMARY_NODES, paths["project"])

	print "CMD1:", CMD1
	print "CMD2:", CMD2
	print "CMD3:", CMD3
	print "CMD4:", CMD4
	print "CMD5:", CMD5

	os.system(CMD1)
	os.system(CMD2)
	os.system(CMD3)
	os.system(CMD4)
	os.system(CMD5)

	# Clean up file structure
	os.system("sh bin/restructure_folders.sh "+paths["project"])

main()
