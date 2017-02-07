
# NAME
#	PCSF_param_sweep.sh
# 
# SYNOPSIS
# 	sh PCSF_param_sweep.sh [inputFromPythonWrapper]
#
# DESCRIPTION
# 	Runs forest for an array of parameters. Takes input from wrapper script run_PCSF_param_sweep.py
#
# VERSION
#	2017-02-07


pyth=$1
forest=$2
terminals=$3
interactome=$4
resultbase=$5
msgpath=$6
label=$7


pfs=`ls $resultbase/params/`
for params in $pfs
do
	ps=$(basename $params .params)
	resultpath=$resultbase/$ps
	mkdir -p $resultpath

	COMMAND="$pyth $forest -p $terminals -e $interactome -c $resultbase/params/$params --msgpath=$msgpath --outpath=$resultpath --outlabel=${label}_$ps"
	CMD="/home/asoltis/wqsub.py --wqsub-name=$resultpath/${label}_$ps $COMMAND --wqsub-no-submit"
	id=`$CMD`
	jobids="$id $jobids"
done

# Python code that checks for sumbitted job statuses
wait_for_jobid.py $jobids


# Now, loop over jobs and submit for run
for params in $pfs
do
	ps=$(basename $params .params)
	resultpath=$resultbase/$ps
	qsub -q oldhosts.q $resultpath/${label}_${ps}_python.script
done

