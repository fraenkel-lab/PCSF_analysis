import sys, os
import pandas as pd


def load_tab_file(f_name, cols):
	if os.path.exists(f_name):
		df = pd.read_table(f_name, names=cols)
	else:
		print "File does not exist:", f_name

	return df


def main():
	projectPath = sys.argv[1]
	terminalPath = sys.argv[2]
	garnet = sys.argv[3]

	# projectPath = "/nfs/latdata/iamjli/ALS/results/OI_diMNs_C9_CTR_ALL_PRIZES/W_3_BETA_6_D_8_mu_0.001/"
	# terminalPath = "/nfs/latdata/iamjli/ALS/data/diMNs/protein_log2_change_abs_diMNs_ALL.txt"
	# garnet = "/nfs/latdata/iamjli/ALS/PCSF_analysis/bin/blank_file.tsv"

	# load specificity and robustness files
	specificity_file = projectPath + "/summary/summary_nodes_specificity.txt"
	robustness_file = projectPath + "/summary/summary_nodes_robustness.txt"

	specificity = load_tab_file(specificity_file, ["protein", "specificity"])
	robustness = load_tab_file(robustness_file, ["protein", "robustness"])

	df = specificity.merge(robustness, how="outer", on="protein")
	df.fillna(0, inplace=True)

	# load terminal and garnet files
	terminals = load_tab_file(terminalPath, ["protein", "prize"])
	TFs = load_tab_file(garnet, ["protein", "prize"])
	terminals["type"] = "terminal"
	TFs["type"] = "TF"

	types_df = pd.concat([terminals, TFs])

	# combine specificity/ robusstness files
	df = df.merge(types_df, how="left", on="protein")
	df["prize"].fillna(0, inplace=True)
	df["type"].fillna("steiner", inplace=True)

	df.sort(["robustness", "prize"], ascending=[False, False], inplace=True)

	# output
	outPath = projectPath + "/summary/summary_nodes.txt"
	df.to_csv(outPath, sep='\t', index=False)

main()
