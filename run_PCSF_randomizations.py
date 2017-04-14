
# NAME
# 	run_PCSF_randomizations.py
#
# SYNOPSIS
#	python run_PCSF_randomizations.py [yaml_path] [param_label]
#
# DESCRIPTION
#	Takes chosen parameter set from param sweep and runs randomizations
#	Wrapper script for PCSF_randomizations.sh
#
# VERSION
# 	2017-02-07


import sys, os
sys.path.insert(0, 'bin')
from yaml_loader import *


def main():
	if len(sys.argv) > 2:
		yaml_path = sys.argv[2]
	else:
		yaml_path = "specification_sheet.yaml"

	param_label = sys.argv[1]

	paths = load_paths(yaml_path)
	paths["params"] = paths["project"] + "/param_search/params/"

	print paths["params"]

        print "Passing to PCSF_randomizations.sh..."
        CMD = "sh bin/PCSF_randomizations.sh %s %s %s %s %s %s %s %s %s %s" %(paths["python"], paths["forest"], paths["terminals"], \
                        paths["interactome"], paths["project"], paths["msg"], paths["label"], paths["params"], param_label, paths["garnet"])
        os.system(CMD)
	

main()

