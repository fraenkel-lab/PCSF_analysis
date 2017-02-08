
# NAME
# 	PCSF_randomizations.sh
#
# SYNOPSIS
# 	sh PCSF_randomization [paramsFromPythonWrapper]
#
# DESCRIPTION
# 	Runs forest randomizations (node and terminal) via run_PCSF_randomizations.py
#
# VERSION
# 	2017-02-07 


pyth=$1
forest=$2
terminals=$3
interactome=$4
resultbase=$5
msgpath=$6
label=$7
param=$8
paramLabel=$9

numSamples=50

for i in `seq 1 $numSamples`;
do 
	# Create scripts for edge randomization
	newDirectory=$resultbase'/edge_results/randomization_edge_'$i
	postLabel=$paramLabel'_randomization_'$i
	echo $newDirectory
	mkdir -p $newDirectory
	
	COMMAND="$pyth $forest -p $terminals -e $interactome -c $param/${paramLabel}.params --msgpath=$msgpath --outpath=$newDirectory --outlabel=$postLabel --noisyEdges 2"
	CMD="/home/asoltis/wqsub.py --wqsub-name=$newDirectory/$postLabel $COMMAND --wqsub-no-submit"
	echo $CMD

	# Create scripts for node randomization
	newDirectory2=$resultbase'/terminal_results/randomization_terminals_'$i
	mkdir -p $newDirectory2
	COMMAND2="$pyth $forest -p $terminals -e $interactome -c $param/${paramLabel}.params --msgpath=$msgpath --outpath=$newDirectory2 --outlabel=$postLabel --randomTerminals 2"
	CMD2="/home/asoltis/wqsub.py --wqsub-name=$newDirectory2/$postLabel $COMMAND2 --wqsub-no-submit"
	echo $CMD2

	id=`$CMD`
	jobids="$id $jobids"
	id2=`$CMD2`
	jobids="$id2 $jobids"
done

wait_for_jobid.py $jobids


for i in `seq 1 $numSamples`;
do
	newDirectory=$resultbase'/edge_results/randomization_edge_'$i
	qsub -q oldhosts.q $newDirectory/$paramLabel'_randomization_'${i}_python.script
	
	newDirectory2=$resultbase'/terminal_results/randomization_terminals_'$i
	qsub -q oldhosts.q $newDirectory2/$paramLabel'_randomization_'${i}_python.script
done
