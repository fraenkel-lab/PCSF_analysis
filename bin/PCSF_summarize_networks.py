from collections import OrderedDict, Counter
import networkx as nx
import operator
import optparse
import os.path
import re
import pdb

DEFAULT_MAX_DEG_SCORE_LOWER_LIM = 0.75

SEPARATOR = "\t"
MATCH_STRING = 'optimalForest'
LABEL_IS_TERMINAL = "IS_TERMINAL"
META_KEY_UNION = "__UNION__"
TAG_PARAM_B = "BETA"
TAG_PARAM_W = "W"
TAG_PARAM_D = "D"
TAG_PARAM_M = "mu"

NR_TERM="terminal"
NR_COUNT="N"
META_HIGHEST_DEG_NODES_N = 15

META_FILENAME = "file"
META_PARAM_B = "beta"
META_PARAM_M = "mu"
META_PARAM_W = "omega"
META_PARAM_D = "D"
META_N_TREES = "# trees"
META_N_EDGES = "# edges"
META_N_NODES = "# nodes"
META_N_STEINER = "# Steiner"
META_N_TERMINAL = "# Terminal"
META_N_TERMINAL_INPUT = "# Input Term"
META_N_LEAFS = "# of leaf nodes"
META_DEG_MIN = "min degree"
META_DEG_AVG = "avg degree"
META_DEG_MAX = "max degree"
META_AVG_INTERACTOME_DEGREE = "avg degree in interactome"
META_AVG_INTERACTOME_DEGREE_TERM = "terminal avg degree in interactome"
META_AVG_INTERACTOME_DEGREE_STEIN = "steiner avg degree in interactome"
META_DEG_MAX_SCORE = "max deg score" # (1 - max degree / nNodes) --- bigger is better
META_DEGCENT_MAX = "max deg centr"
META_BETWCENT_MAX = "max betw centr"
META_NETW_COHERENCY = "netw coherency" # (nTerm - nSingleton)/nSteiner (or NA if nSteiner=0)  --- bigger is better
META_N_SINGLETONS = "# singletons"
META_TREE_SCORE = "tree score" # (1 - nTrees/nNodes) --- bigger is better
# BELOW: NRBS-> normalized rank based score = (sum of ranks of nodes in top n) / (sum of all ranks), e.g. top 2 are in top3 -> (2+3)/(1+2+3)  --- bigger is better, assuming that nodes that come up frequently across solutions are appreciated
META_TOP_NODE_SCORE = "NRBS.n Nodes"
META_TOP_TERM_SCORE = "NRBS.t Terminals"
META_TOP_STEINER_SCORE = "NRBS.s Steiner"
META_HIGHEST_DEG_NODES = str(META_HIGHEST_DEG_NODES_N)+" highest degree nodes"
META_FIELDS = [META_PARAM_B, META_PARAM_M, META_PARAM_W, META_PARAM_D, # PARAMS
               META_N_TREES, META_N_EDGES, META_N_NODES, META_N_STEINER, META_N_TERMINAL, # BASIC NETW STATS

               META_TOP_NODE_SCORE, META_TOP_TERM_SCORE, META_TOP_STEINER_SCORE, # TOP NODE SCORES
               META_TREE_SCORE, META_DEG_MAX_SCORE, META_NETW_COHERENCY,
               META_DEG_MAX, META_HIGHEST_DEG_NODES, META_N_TERMINAL_INPUT,
               META_AVG_INTERACTOME_DEGREE_TERM, META_AVG_INTERACTOME_DEGREE_STEIN, META_AVG_INTERACTOME_DEGREE,
               META_N_SINGLETONS, META_N_LEAFS, META_DEGCENT_MAX, META_BETWCENT_MAX, META_DEG_MIN, META_DEG_AVG]

def parseFileNameParam(filename, regex):
  try:
    tmp = filename.split(regex+"_")[1]
    val = tmp.split("_")[0]
    return val
  except:
    return ""

def groupFilesByName(allFiles):
  groups = {}
  for f in allFiles:
    rem = re.match('(^.+)_[adeino]\w+(\..+)', f) # if other grouping is wanted, here's the line to change!
    #rem = re.match('(^.+_[rx]\d+).+(\..+)', f) # if other grouping is wanted, here's the line to change!
    #print '\t'.join(rem.groups())
    if rem:
      if rem.group(1) in groups.keys():
        groups[rem.group(1)].append(f)
      else:
        groups[rem.group(1)] = []
        groups[rem.group(1)].append(f)
    #print "next item"
  return groups

def readTerminalList(terminalFile):
  terminals = []
  with open(terminalFile, "r") as FIN:
    for line in FIN:
      line = line.rstrip()
      terminals.append(line.split('\t')[0])
  return terminals

def createNetwork(inputDir, file, isInteractomeFormat=False):
  net = nx.Graph()
  fin = os.path.join(inputDir, file)
  with open(fin, "r") as FIN:
    for line in FIN:
      line = line.rstrip()
      spl = line.split('\t')
      if isInteractomeFormat:
        net.add_edge(spl[0], spl[1], weight=float(spl[2]))
      else:
        net.add_edge(spl[0], spl[2]) # idx 1 is 'pp'
  return net

def getNetworkMetaData(net, terminals, filename, nodeRanking, interactome=None):
  metadata = {}
  if net.size() > 0:
    degrees = list(net.degree().values())
    dcs = nx.degree_centrality(net)
    bcs = nx.betweenness_centrality(net)

    metadata[META_FILENAME] = filename
    metadata[META_N_EDGES] = str(net.number_of_edges())
    metadata[META_N_NODES] = str(net.number_of_nodes())
    metadata[META_N_TREES] = str(len(list(nx.connected_component_subgraphs(net)))) #+" ("+",".join([sg.number_of_nodes() for sg in nx.connected_component_subgraphs(net)])+ ")"
    metadata[META_TREE_SCORE] = str( 1- int(metadata[META_N_TREES]) / float(net.number_of_nodes()))
    metadata[META_DEG_MIN] = str(min(degrees))
    metadata[META_DEG_AVG] = str(sum(degrees)/len(degrees))
    metadata[META_DEG_MAX] = str(max(degrees))
    metadata[META_DEG_MAX_SCORE] = str(1 - max(degrees) / float(net.number_of_nodes()))
    metadata[META_N_TERMINAL] = str(len(set(net.nodes()) & set(terminals)))
    metadata[META_N_LEAFS] = str(len([n[0] for n in net.degree().items() if n[1] == 1]))
    metadata[META_N_STEINER] = str(len(net.nodes()) - int(metadata[META_N_TERMINAL]))
    metadata[META_DEGCENT_MAX] = str(max([dc[1] for dc in dcs.items()]))
    metadata[META_BETWCENT_MAX] = str(max([bc[1] for bc in bcs.items()]))
    metadata[META_HIGHEST_DEG_NODES] = ",".join([x[0] for x in sorted(net.degree().items(), key=operator.itemgetter(1), reverse=True)[0:META_HIGHEST_DEG_NODES_N]])
    metadata[META_N_SINGLETONS] = str(sum([1 for x in net.degree().items() if  x == 0]))
    metadata[META_NETW_COHERENCY] = str((int(metadata[META_N_TERMINAL]) - int(metadata[META_N_SINGLETONS])) / float(metadata[META_N_STEINER])) if float(metadata[META_N_STEINER]) > 0 else "NA"

    # get top ranked nodes based on nodeRanking param
    nTopNodes = int(metadata[META_N_NODES])
    nTopTerminal = int(metadata[META_N_TERMINAL])
    nTopSteiner = int(metadata[META_N_STEINER])
    topNodes = [ n[0] for n in sorted(nodeRanking.items(), key=operator.itemgetter(1) ,reverse=False) ] #[0:nTopNodes]
    topTerminal = [ n[0] for n in sorted(nodeRanking.items(), key=operator.itemgetter(1) ,reverse=False) if n[1][NR_TERM] ] #[0:nTopTerminal]
    topSteiner = [ n[0] for n in sorted(nodeRanking.items(), key=operator.itemgetter(1) ,reverse=False) if not n[1][NR_TERM] ] #[0:nTopSteiner]

    metadata[META_TOP_NODE_SCORE] = str(sum([ i + 1 for i in range(len(topNodes)) if topNodes[i] in net.nodes() ]) / float(sum(range(nTopNodes+1)))) if nTopNodes > 0 else "NA"
    metadata[META_TOP_TERM_SCORE] = str(sum([ i + 1 for i in range(len(topTerminal)) if topTerminal[i] in net.nodes() ]) /  float(sum(range(nTopTerminal+1)))) if nTopTerminal > 0 else "NA"
    metadata[META_TOP_STEINER_SCORE] = str(sum([ i + 1 for i in range(len(topSteiner)) if topSteiner[i] in net.nodes() ]) / float(sum(range(nTopSteiner+1)))) if nTopSteiner > 0 else "NA"

    if interactome is not None:
      intomeDegs = [interactome.degree(n) for n in net.nodes()]
      metadata[META_AVG_INTERACTOME_DEGREE] = str(sum(intomeDegs) / float(len(intomeDegs))) if len(intomeDegs) > 0 else "NA"
      intomeDegs = [interactome.degree(n) for n in net.nodes() if n in terminals]
      metadata[META_AVG_INTERACTOME_DEGREE_TERM] = str(sum(intomeDegs) / float(len(intomeDegs))) if len(intomeDegs) > 0 else "NA"
      intomeDegs = [interactome.degree(n) for n in net.nodes() if n not in terminals]
      metadata[META_AVG_INTERACTOME_DEGREE_STEIN] = str(sum(intomeDegs) / float(len(intomeDegs))) if len(intomeDegs) > 0 else "NA"
  else:
    for mf in META_FIELDS:
      metadata[mf] = "0"

  # Get parameter values-god whoever wrote this script from the 9th layer hell shoot me now
  filename = filename.split("/")[-1]
  metadata[META_PARAM_B] = parseFileNameParam(filename, TAG_PARAM_B)
  metadata[META_PARAM_M] = parseFileNameParam(filename, TAG_PARAM_M)
  metadata[META_PARAM_W] = parseFileNameParam(filename, TAG_PARAM_W)
  metadata[META_PARAM_D] = parseFileNameParam(filename, TAG_PARAM_D)
  metadata[META_N_TERMINAL_INPUT] = str(len(set(terminals)))

  return metadata

def getFileName(outDir, baseName, str, postFix):
  return os.path.join(outDir, '%s_%s.%s'%(baseName,str,postFix))

def writeToFile(lines, fileName, p=True):
  if p:
    with open(fileName, 'w') as FOUT:
      FOUT.writelines("\n".join(lines))

def stemleafplot(nrs):
  lines = []
  if (len(nrs) > 0):
    d = OrderedDict( ((str(v)[:-1], ' ')[v<10], Counter()) for v in sorted(nrs))
    for s in ((str(v),' '+str(v))[v<10] for v in nrs):
      d[s[:-1]][s[-1]] += 1
    m = max(len(s) for s in d)
    for k in d:
      lines.append('%s%s | %s'%(' '*(m-len(k)), k, ' '.join(sorted(d[k].elements()))))
  return "\n".join(lines)

def summarizeNetworksInFiles(networkFiles, jobName, terminals, inputDir, outDir, interactome=None):
  # load networks, create union of networks
  networks = []
  unionNet = nx.Graph()
  for f in networkFiles:
    net = createNetwork(inputDir, f)
    networks.append(net)
    unionNet.add_edges_from(net.edges())

  # write gene x network matrix
  lines = list()
  lines.append(SEPARATOR.join(['Node'] + networkFiles + [META_KEY_UNION, LABEL_IS_TERMINAL]))
  nodesInUnion = sorted(unionNet.degree().items(), key=operator.itemgetter(1), reverse=True)
  nodeRanking = {}
  for gene, degree in nodesInUnion:
    nodeRanking[gene] = {}
    line = [gene]
    count = 0
    for net in networks:
      deg = net.degree()
      if gene in deg:
        line.append(str(deg[gene]))
        count += 1
      else:
        line.append("0")
    line.append(str(unionNet.degree()[gene]))
    nodeRanking[gene][NR_TERM] = gene in terminals
    nodeRanking[gene][NR_COUNT] = count
    if nodeRanking[gene][NR_TERM]:
      line.append("1")
    else:
      line.append("0")
    lines.append(SEPARATOR.join(line))
  writeToFile(lines, getFileName(outDir, jobName, 'networkNodeMatrix', 'tsv'))

  # collect metadata (requires nodeRanking from above code block)
  metadata = {}
  for inet in range(len(networks)):
    metadata[networkFiles[inet]] = getNetworkMetaData(networks[inet], terminals, networkFiles[inet], nodeRanking, interactome)
  metadata[META_KEY_UNION] = getNetworkMetaData(unionNet, terminals, META_KEY_UNION, nodeRanking, interactome)

  # write file with degree distributions
  lines = list()
  for i in range(len(networks)):
    net = networks[i]
    lines.append(networkFiles[i])
    lines.append(stemleafplot([it[1] for it in net.degree().items()]))
    lines.append("\n")
  lines.append(META_KEY_UNION)
  lines.append(stemleafplot([it[1] for it in unionNet.degree().items()]))
  writeToFile(lines, getFileName(outDir, jobName, 'degreeDistributions', 'txt'))

  # write metadata to file
  lines = list()
  lines.append(SEPARATOR.join(['FILENAME']+META_FIELDS))
  for fn in sorted(metadata.keys()):
    meta = metadata[fn]
    lines.append(SEPARATOR.join([fn] + [meta[x] for x in META_FIELDS]))
  writeToFile(lines, getFileName(outDir, jobName, 'networkSummary', 'tsv'))

  # write union network file
  netw = list()
  anno= list()
  anno.append(SEPARATOR.join(["Edge", "Weight"]))
  for edge in unionNet.edges():
    netw.append(SEPARATOR.join([edge[0], 'pp', edge[1]]))
    anno.append(SEPARATOR.join([edge[0]+' (pp) '+edge[1], str(interactome.get_edge_data(edge[0], edge[1])["weight"])]))
  writeToFile(netw, getFileName(outDir, jobName, 'family', 'sif'))
  writeToFile(anno, getFileName(outDir, jobName, 'family.annotations.edges', 'tsv'))

  nodes = list()
  nodes.append(SEPARATOR.join(["ID", "isTerminal", "degreeInInteractome"]))
  for node in unionNet.nodes():
    nodes.append(SEPARATOR.join([node, "1" if node in terminals else "0", str(interactome.degree(node))]))
  writeToFile(nodes, getFileName(outDir, jobName, 'family.annotations.nodes', 'tsv'))

  return metadata

########################################################################################################################
########################################################################################################################
def main():
  op = optparse.OptionParser()
  op.add_option('-o', '--out', dest='outDir',
                help="Output directory (doesn't need to exist). Output files will be created in this directory.")
  op.add_option('-i', '--in', dest='inputDir',
                help="Input directory (likely your PCSF output directory).")
  op.add_option('-t', '--terminals', dest='terminalFile',
                help="File containing the terminals used for the PCSF runs. Can be a single- or a multi-column "
                     "file with the terminals in the first column (prize-/PCSF-input file).")
  op.add_option('-n', '--jobname', dest='jobName', default=MATCH_STRING,
                help="(optional) Name of this PCSF run. Keep it short. This will be part of the output filenames. Default is the match string (-m)." )
  op.add_option('-b', '--interactome', dest='interactome', default=None,
                help="(optional) Background interactome that was used for running PCSF.")
  op.add_option('-m', '--match', dest='matchString', default=MATCH_STRING,
                help="(optional) A string that is used to identify (string.contains(matchString)) network files (files ending with .sif are used). Default is: " + MATCH_STRING)
  op.add_option('-a', '--onlyAll', dest='noPromisingSubsetAnalysis', action="store_false", default=True,
                help="(optional) This option will TURN OFF re-running the summarization procedure for promising networks. See `limit` option for how promising networks are defined. Default is: On")
  op.add_option('-l', '--limit', dest='minDegScoreLimitForPromising', default=DEFAULT_MAX_DEG_SCORE_LOWER_LIM,
                help="(optional) A lower limit for the maximum degree score (1-maxDegree/nNodes) of a promising network. Default is: %s" % str(DEFAULT_MAX_DEG_SCORE_LOWER_LIM))

  (opts, args) = op.parse_args()
  if opts.outDir is None or opts.terminalFile is None or opts.inputDir is None:
    print("Please provide all the required parameters!\n")
    op.print_help()
    exit(1)
  jobName = opts.jobName
  matchString = opts.matchString
  outDir = opts.outDir
  inputDir = opts.inputDir
  terminalFile = opts.terminalFile
  useInteractome = opts.interactome is not None
  if useInteractome:
    interactomePath = opts.interactome
  doPromisingSubsetAnalysis = not bool(opts.noPromisingSubsetAnalysis)
  minDegScoreLimitForPromising = float(opts.minDegScoreLimitForPromising) if 0 < float(opts.minDegScoreLimitForPromising) <= 1 else DEFAULT_MAX_DEG_SCORE_LOWER_LIM
  
  #Summary path creation
  if not os.path.exists(outDir):
    os.makedirs(outDir)

  terminals = readTerminalList(terminalFile)
  allFiles = os.listdir(inputDir)
  groupedFiles = groupFilesByName(allFiles)
  #pdb.set_trace()
  if useInteractome:
    interactome = createNetwork(os.path.dirname(interactomePath), os.path.basename(interactomePath), True)
  else:
    interactome = None

  # Get all *optimalForest.sif files
  optimalForests = []
  for path, subdirs, files in os.walk(inputDir):
    for name in files:
      if matchString in name and name.endswith(".sif"):
        optimalForests.append(os.path.join(path, name))

  if len(optimalForests) == 0:
    print("No forests found in the input directory!")
  else:
    print("%s networks will be summarized..." %str(len(optimalForests)))
    metadata = summarizeNetworksInFiles(optimalForests, jobName, terminals, inputDir, outDir, interactome)

    if doPromisingSubsetAnalysis:
      promisingForests = []
      for name, data in metadata.items():
        if float(data[META_DEG_MAX_SCORE]) >= minDegScoreLimitForPromising:
          if name is not META_KEY_UNION:
            promisingForests.append(name)
      if len(promisingForests) > 0:
        print(" Out of these, %s networks look promising (MAX_DEG_SCORE > %s). Summarizing these networks separately..." %(str(len(promisingForests)), str(minDegScoreLimitForPromising)))
        summarizeNetworksInFiles(promisingForests, jobName+"_promising", terminals, inputDir, outDir, interactome)
      else:
        print(" None of these networks looked promising based on their maximum degrees (None was greater than %s)." %str(minDegScoreLimitForPromising))





########################################################################################################################
if __name__ == "__main__":
  main()
