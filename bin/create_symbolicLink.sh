#!/bin/bash
set -e
set -u
set -o pipefail

# 
# NAME
# 	create_symbolicLink.sh
#
# SYNOPSIS
# 	bash create_symbolicLink.sh [networkPath] [linkedPath]
#
# DESCRIPTION
# 	This script takes an array of paths, finds bam files and creates symbolic links to a target directory
#
# v 2016-07-17

#arg1=$1; shift
array=( "$@" )
last_idx=$(( ${#array[@]} - 1 ))
linkedPath=${array[$last_idx]}
unset array[$last_idx]

#echo "arg2=$linkedPath"
#echo "array contains:"
networkPath="${array[@]}"
printf "%s\n" "${networkPath[@]}"
mkdir -p $linkedPath

echo $linkedPath
echo $networkPath
#------------------------------------------------
# Create symbolic links to path
#------------------------------------------------

for i in "${networkPath[@]}"
do
	find $i -type f \( -name "*.sif" -o -name "*.tsv" -o -name "*.txt" \) -exec ln -s {} $linkedPath ";"
	echo $i
done

