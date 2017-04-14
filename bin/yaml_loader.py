
import yaml
import sys, os


def yaml_loader(path):
	with open(path, 'r') as f:
		data = yaml.load(f)
	return data


def process_params(v):
        # Load parameters into optimal format
        vals = str(v).split(',')
        all_ints = True
        for val in vals: # check if all ints
                if float(val) != int(float(val)):
                        all_ints = False
        if all_ints:
                return [int(x) for x in vals]
        else:
                return [float(x) for x in vals]


def load_params(yaml_path="../specification_sheet.yaml"):
	data = yaml_loader(yaml_path)
	w = process_params(data["w"])
	beta = process_params(data["beta"])
	D = process_params(data["D"])
	mu = process_params(data["mu"])
	print "Params loaded..."
	print "\tw:", w
        print "\tbeta:", beta
        print "\tD:", D
        print "\tmu:", mu
	return w, beta, D, mu


def load_paths(yaml_path="../specification_sheet.yaml"):
	data = yaml_loader(yaml_path)
	paths = {}
	paths["project"] = data["projectPath"]
	paths["label"] = os.path.basename(paths["project"].rstrip('/'))
	paths["python"] = data["pythPath"] 
	paths["forest"] = data["forestPath"]
	paths["terminals"] = data["terminals"] 
	paths["interactome"] = data["interactome"] 
	paths["msg"] = data["msgPath"]
	if "garnet" in data:
		paths["garnet"] = data["garnet"]
	else:
		paths["garnet"] = "blank_file.tsv"
		print "No garnet file indicated."
	print "Paths loaded..."
	for path in paths:
		print "\t%s:\t%s" %(path, paths[path])
	return paths

	
