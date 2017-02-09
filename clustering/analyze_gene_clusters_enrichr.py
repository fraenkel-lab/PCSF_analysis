'''
 
 DESCRIPTION
 
 This script takes the output of a communities algorithm and then searches the list of terms for different enriched terms using the enrichr API.

 The script will have the following subroutines read_clusters, add_gene_list and download gene list (get_enrichment)

 VERSION

 2016-08-20

'''

import pdb 
import pandas as pd
import numpy as np
import re
import os
import json
import requests
from argparse import ArgumentParser

def get_enrichment(filename):
    print 'The file for clustering is ' + filename
    outputDir=os.path.dirname(filename)
    df = pd.read_table(filename,header=None)
    df.columns=['cluster_number','genes']
    df_colNames=list(df.columns.values)
    clusters = df.ix[:,0].values
    #df = df.set_index('PatientID')
    genes = df.ix[:,1:].values#Data values

    #Find all unique values in array
    unique_clusters = np.unique(clusters)

    #Standardization of data
    for current_cluster in zip(unique_clusters):
	#print current_cluster
	current_df = df[df.cluster_number==current_cluster[0]]
	tmp = current_df[[1]]
	gene_list = tmp['genes'].tolist()
	genes_str = '\n'.join(gene_list)
	descriptor = 'Cluster_' + str(current_cluster[0])
  	#Add gene list to enrichr	
	gene_id = add_gene_list(genes_str,descriptor)
	all_databases =['KEGG_2016', 'GO_Biological_Process_2015', 'GO_Cellular_Component_2015', 'GO_Molecular_Function_2015', 'WikiPathways_2016', 'Human_Gene_Atlas']
	# all_databases =['LINCS_L1000_Chem_Pert_down', 'LINCS_L1000_Chem_Pert_up', 'Old_CMAP_down', 'Old_CMAP_up']
	for database in zip(all_databases):
		database= str(database[0])
		download_enrichr(gene_id,descriptor,outputDir,database)
		#pdb.set_trace()

    #####
def add_gene_list(genes_str,descriptor):
	print genes_str
	
	# ENRICHR tool
	ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/addList'
	description = descriptor
	payload = {
    'list': (None, genes_str),
    'description': (None, description)
}

	response = requests.post(ENRICHR_URL, files=payload)
	if not response.ok:
	    raise Exception('Error analyzing gene list')
	
	data = json.loads(response.text)
	print(data)
	gene_id = data['userListId']
	return gene_id
	#pdb.set_trace()

def download_enrichr(gene_id,descriptor,outputDir, database):
	ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/export'
	query_string = '?userListId=%s&filename=%s&backgroundType=%s'
	user_list_id = gene_id
	#pdb.set_trace()
	filename = outputDir +'/' +  database + '_' +  descriptor
	#filename = outputDir + 'KEGG_' + descriptor + '_' + str(gene_id)
	gene_set_library = database
	
	url = ENRICHR_URL + query_string % (user_list_id, filename, gene_set_library)
	response = requests.get(url, stream=True)
	
	with open(filename + '.txt', 'wb') as f:
	    for chunk in response.iter_content(chunk_size=1024): 
	        if chunk:
	            f.write(chunk)


def main():

    parser=ArgumentParser(description='Read in communities from clustering algoritithm')
    parser.add_argument('filename',help='Input file with the cluster communities')
 
    args=parser.parse_args()
    
    filename=args.filename
    ##split the comma-delimited files
    get_enrichment(filename)
    
if __name__=='__main__':
    main()
