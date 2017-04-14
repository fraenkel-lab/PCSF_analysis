
# NAME
# 	run_PCSF_param_sweep.py
#
# SYNOPSIS
# 	python run_PCSF_param_sweep.py [yaml_path]
#
# DESCRIPTION
# 	Creates parameter grid from yaml file
#	Initializes runs via PCSF_param_sweep.sh
#
# VERSION
#	2017-02-07


import sys, os
import itertools
sys.path.insert(0, 'bin')
from yaml_loader import *
	

def generate_parameters(folder, ws, betas, Ds, mus):
	# Generate parameter folder and individual files and returns a list of their names
	param_folder = folder + "/params/"
	if not os.path.exists(param_folder): # Create param/ folder
		os.makedirs(param_folder)

	param_grid = list(itertools.product(ws, betas, Ds, mus))
	param_names = []
	for param in param_grid: # Iterate through param grid and write
		w, beta, D, mu = param
		stringify = (str(w), str(beta), str(D), str(mu))
		file_name = "W_%s_BETA_%s_D_%s_mu_%s.params" %stringify
		param_name = file_name.rstrip(".params")
		param_names.append(param_name)
		with open(param_folder+file_name, 'w') as f:
			f.write("w = %s\nb = %s\nD = %s\nmu = %s" %stringify)	
	print "%d files successfully written to %s" %(len(param_grid), param_folder)
	return param_names


def main():
	if len(sys.argv)>1:
		yaml_path = sys.argv[1]
	else:
		yaml_path = "specification_sheet.yaml"
	
	paths = load_paths(yaml_path)
	w, beta, D, mu = load_params(yaml_path)

	param_names = generate_parameters(paths["project"], w, beta, D, mu)

	print "Copying YAML file..."
	os.system("cp specification_sheet.yaml "+paths["project"])

	print "Passing to PCSF_param_sweep.sh..."
	CMD = "sh bin/PCSF_param_sweep.sh %s %s %s %s %s %s %s %s" %(paths["python"], paths["forest"], paths["terminals"], \
			paths["interactome"], paths["project"], paths["msg"], paths["label"], paths["garnet"])
	print CMD
	os.system(CMD)



main()	
