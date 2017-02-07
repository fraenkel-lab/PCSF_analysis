import sys,os
import fileinput 
import cPickle

args = sys.argv[1:]
if len(args) != 4:
    print '\nUsage: python %s <in.sif> <node_degrees_dict.pkl> <terminals.txt> <output_fn_base>\n'%(sys.argv[0])
    print 'Input terminals can be a comma-separated list of multiple files.'
    print 'Two output files are created: <output_fn_base>.terminal_degrees and '
    print '<output_fn_base>.Steiner_degrees for node degrees of terinals and Steiner nodes.'
    sys.exit()

# Parse args
insif = args[0]
degrees = cPickle.load(open(args[1]))
terminals_fns = args[2]
ofn = args[3]

# Read in network and store nodes
network_nodes = set()
for line in fileinput.input(insif):
    n1,typ,n2 = line.strip().split()
    if n1 != 'DUMMY': network_nodes.add(n1)
    if n2 != 'DUMMY': network_nodes.add(n2)

# Read in terminals
terminals = set()
for fn in terminals_fns.split(','):
    for line in fileinput.input(fn):
        t = line.strip().split()[0]
        terminals.add(t)

# Determine which nodes are Steiner nodes
Steiner_nodes = set()
for n in network_nodes:
    if n in terminals: continue
    else: Steiner_nodes.add(n)

# Write output for terminals
ofn_t = ofn+'.terminal_degrees'
oft = open(ofn_t,'w')
for n in network_nodes:
    if n not in terminals: continue
    try:
        deg = degrees[n]
    except:
        print '  Terminal %s not in degrees dictionary!'%(n)
        continue

    oft.writelines('%s\t%d\n'%(n,deg))
oft.close()

# Write output for Steiner nodes
ofn_s = ofn+'.Steiner_degrees'
ofs = open(ofn_s,'w')
for n in Steiner_nodes:
    try:
        deg = degrees[n]
    except:
        print '  Steiner node %s not in degrees dictionary!'%(n)
        continue

    ofs.writelines('%s\t%d\n'%(n,deg))
ofs.close()

