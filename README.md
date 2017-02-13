# PCSF_analysis

## PCSF workflow
1. Parameter search
  1. Run `forest.py` on a parameter grid
  2. Visualize network features for each parameter set, and choose the best network
2. Randomizations

## Generate .yaml file
```yaml
msgPath:        /nfs/apps/bin/msgsteiner9
pythPath:       /nfs/apps/python2.7/bin/python
forestPath:     /nfs/latdata/iamjli/alex/PCSF_analysis/bin/forest.py

projectPath:    /nfs/latdata/iamjli/alex/results/human_binned_weights/
terminals:      /nfs/latdata/iamjli/alex/data/toxicity_screen_human_prizes.tsv
interactome:    /nfs/latdata/iamjli/alex/data/interactome/iRefIndex_v13_MIScore_interactome.txt

# Parameter grid
w:      1,2,3,4
beta:   3,6,9,12
D:      8
mu:     3e-04,1e-03,3e-03,1e-02,3e-02
```

## Pipeline
Run `forest.py` for all parameter sets, with optional parameter for specifying the yaml file:

    python run_PCSF_param_sweep.py [yaml_file]
    
Run summarization scripts and visualize parameter grid results:  

    python PCSF_param_selection.py [yaml_file]
    
This also restructures the project directory. Results found in `param_search/summary/`. Choose best looking parameter set, and run randomization scripts:  

    python run_PCSF_randomizations.py W_3_BETA_3_D_7_mu_1e-05 [yaml_file] 
    
Finally, summarize randomization results:  

    python randomizations2subnetworks.py

This script also performs community clustering (Louvain), finds GO terms for subclusters, and create output files for visualization in Cytpscape. 


TODO: 
-script that fetches GO terms needs to handle empty responses
-restructure randomization->summary steps so that more than one randomization can be run
