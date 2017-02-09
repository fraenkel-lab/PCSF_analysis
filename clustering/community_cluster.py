import sys,os
#sys.path.insert(0,'/home/asoltis/Software/networkx/networkx-1.8.1-py2.6.egg')
import networkx as nx
import community
import fileinput

args = sys.argv[1:]
if len(args) < 3:
    print '\nUsage: python %s <in.sif> <in.edges> <out.prefix>'%(sys.argv[0])
    print 'Perform community clustering with Louvain algorithm on network in in.sif.'
    print 'in.edges expects format as: A B score'
    print 'Creates two output files:' 
    print '    out.community_cluster.txt - text file with cluster number in col 1 and node in col 2'
    print '    out.community_cluster.sif - SIF file of clustered network, with cluster number in 4th column'    
    print ''
    sys.exit()

nf = args[0]
ef = args[1]
ofn = args[2]

# Read in edges from edge file
master_edges = {}
for line in fileinput.input(ef):
    l = line.strip().split()
    if len(l) < 2: continue
    n1,n2,score = l
    
    key1 = n1+'_'+n2
    master_edges[key1] = float(score)
    key2 = n2+'_'+n1
    master_edges[key2] = float(score)

# Create graph object from graph
G = nx.Graph()
for line in open(nf).readlines():
    l = line.strip().split()
    n1,typ,n2 = l[0:3]
  
    try:
        key = n1+'_'+n2
        w = master_edges[key]
    except KeyError:
        w = 0.5
        print n1,n2
    G.add_edge(n1,n2,weight=w,data=typ)

# Run community partitioning
partition = community.best_partition(G)
modularity = community.modularity(partition,G)
print 'Modularity of best partition: %0.4f'%(modularity)

# Write node membership in communities file
of = open(ofn+'_community_output.txt','w')
for com in set(partition.values()):
    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
    for n in list_nodes:
        ol = '%d\t%s\n'%(com,n)
        of.writelines(ol)

of.close()

# Create graph of communities
of2=open(ofn+'_community_output.sif','w')
edges_out=set()
for com in set(partition.values()):
    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
    for n in list_nodes:
        edges = G.edges(n)
        for e in edges:
            n1,n2 = e[0],e[1]
            if n1 == n and n2 in list_nodes:
                if not (n2,n1) in edges_out:
                    edges_out.add(e) 
            elif n2 == n and n1 in list_nodes:
                if not (n2,n1) in edges_out:
                    edges_out.add(e)

# Write output graph
for e in edges_out:
    n1,n2 = e[0],e[1]
    typ = G.get_edge_data(*e)['data']
    clust_num = partition[n1]
    of2.writelines('%s %s %s %d\n'%(n1,typ,n2,clust_num))

of2.close()
        
            
