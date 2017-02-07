# PCSF_analysis

## PCSF workflow
1. Parameter search
  1. Run `forest.py` on a parameter grid
  2. Visualize network features for each parameter set, and choose the best network
2. Randomizations

## Generate .yaml file
```
msgPath:        /nfs/apps/bin/msgsteiner9
pythPath:       /nfs/apps/python2.7/bin/python
forestPath:     /nfs/latdata/iamjli/alex/PCSF_analysis/bin/forest.py

projectPath:    /nfs/latdata/iamjli/alex/results/human_uniform_weights/
terminals:      /nfs/latdata/iamjli/alex/data/toxicity_screen_human_uniform_prizes.tsv
interactome:    /nfs/latdata/iamjli/alex/data/interactome/iRefIndex_v13_MIScore_interactome.txt

# Parameter grid
w:      1,2,3
beta:   1,2,3,4,5,6,7,8,9,10
D:      7
mu:     1e-05
```

## Parameter search
Run `forest.py` for all parameter sets:
`python run_PCSF_param_sweep.py`
