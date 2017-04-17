
import sys, os
import pandas as pd
import fnmatch
import matplotlib.pyplot as plt
import seaborn as sns
import pickle as pkl


SUMMARY_SUFFIX = "summary_nodes.txt"


def get_shortened_name(f_name):
	out = '/'.join(f_name.rstrip("/summary/summary_nodes.txt").split('/')[-2:])
	return out


def load_tab_file(f_name):
	df = pd.read_table(f_name)
	df = df[df["robustness"] > 0]
	df["experiment"] = get_shortened_name(f_name)
	return df[["protein", "experiment", "robustness"]]


def search_files_recursive(basedir, suffix):
	matches = []
	for root, dirnames, filenames in os.walk(basedir):
		for filename in fnmatch.filter(filenames, suffix):
			matches.append(os.path.join(root, filename))
	return matches


def main():
	# get all summary_nodes.txt files to compare
	paths_to_search = sys.argv[1:]
	all_matches = sum([search_files_recursive(path, SUMMARY_SUFFIX) for path in paths_to_search], [])

	print "Analyzing %d files:" %len(all_matches)
	print '\n'.join(all_matches)

	# load all dataframes
	dfs = [load_tab_file(f) for f in all_matches]
	df = pd.concat(dfs)

	df.to_csv("raw.csv")
	df = df[df["robustness"] >= 0.9]

	df.drop_duplicates(["protein", "experiment"], inplace=True)

	df.to_csv("raw_no_dups.csv")

	print df.head()
	print df.shape

	data = df.pivot("protein", "experiment", "robustness")
	data.fillna(0, inplace=True)

	data.to_csv("data.csv")

	# with open("pickle.pkl", 'w') as f: 
	# 	pkl.dump(data, f)


	g = sns.clustermap(data)
	g.savefig("test.png")

main()