
# Clean up file structure after parameter selection script

odir=$1

mkdir -p ${odir}/param_search/results/
mv ${odir}/W_* ${odir}/param_search/results/
mv ${odir}/params ${odir}/param_search/
mv ${odir}/out_data/summary ${odir}/param_search/
# mv ${odir}/out_data/summarize.sh ${odir}/param_search/summary/
mv ${odir}/out_data ${odir}/param_search/sym_links
