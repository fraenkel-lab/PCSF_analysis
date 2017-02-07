import sys,os
from optparse import OptionParser

'''
Driver code to create PCSF parameter files BETA, W, D, tf_beta, and mu parameters.
'''

def frange(start, end=None, inc=None, log=False):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0
    if start == end:
        if log == True:
            return [pow(10,start)]
        else:
            return [start]
    
    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next > end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)

    if log == True: # Wants log-spaced values
        for i in range(0,len(L)):
            L[i] = pow(10,L[i])
        
    return L

def main():
    # options and arguments
    usage = '%prog [options]'
    description='Function creates PCSF protocol parameter files for ranges of BETA, W, D, and mu parameters.'
    parser=OptionParser(usage=usage)
    parser.add_option('-D',type='string',dest='D',help='Provide in format start_stop_increment') 
    parser.add_option('-W',type='string',dest='W',help='') 
    parser.add_option('-B',type='string',dest='B',help='')
    parser.add_option('--tf-beta',type='string',dest='tf_beta',default=None)
    parser.add_option('--mu',type='string',dest='mu',help='') 
    parser.add_option('-r',type='string',dest='r',default=None,
                      help='Optionally provide edge noise parameter values "r".')
    parser.add_option('--resultpath',type='string',dest='resultpath',help='')

    (opts,args) = parser.parse_args()

    # All options are required, check
    if not opts.D:
        print '-D values are required. Exiting.'
        sys.exit()
    if not opts.W:
        print '-W values are required. Exiting.'
        sys.exit()
    if not opts.B:
        print '-B values are required. Exiting.'
        sys.exit()
    if not opts.mu:
        print '--mu values are required. Exiting.'
        sys.exit()
    if not opts.resultpath:
        print 'Must provide result path. Exiting.'
        sys.exit()

    resultpath = opts.resultpath
    if not resultpath.endswith('/'): resultpath+='/'
    if not os.path.exists(resultpath):
        os.makedirs(resultpath)

    # Get value ranges
    Ds = [float(x) for x in opts.D.split('_')]
    D = frange(Ds[0],Ds[1],Ds[2])
    Ws = [float(x) for x in opts.W.split('_')]
    W = frange(Ws[0],Ws[1],Ws[2])
    Bs = [float(x) for x in opts.B.split('_')]
    B = frange(Bs[0],Bs[1],Bs[2])
    MUs = [float(x) for x in opts.mu.split('_')]
    MU = frange(MUs[0],MUs[1],MUs[2])
    if opts.tf_beta != None:
        TFBs = [float(x) for x in opts.tf_beta.split('_')]
        TFB = frange(TFBs[0],TFBs[1],TFBs[2])

    # Loop through and create files
    for d in D:
        for w in W:
            for b in B:
                for mu in MU:
                    if opts.tf_beta == None:
                    
                        ofn = opts.resultpath+'W_%s_BETA_%s_D_%s_mu_%s.params'%(str(w),str(b),str(d),str(mu))
                        of = open(ofn,'w')
                        of.writelines('w = %s\n'%(str(w)))
                        of.writelines('b = %s\n'%(str(b)))
                        of.writelines('D = %s\n'%(str(int(d))))
                        of.writelines('mu = %s\n'%(str(mu)))
                    
                        if opts.r != None:
                            of.writelines('r = %s\n'%(str(opts.r)))
                        of.close()
                    else:
                        for tfb in TFB: 
                            ofn = opts.resultpath+'W_%s_BETA_%s_D_%s_mu_%s_tfBeta_%s.params'%(str(w),str(b),str(d),str(mu),str(tfb))
                            of = open(ofn,'w')
                            of.writelines('w = %s\n'%(str(w)))
                            of.writelines('b = %s\n'%(str(b)))
                            of.writelines('D = %s\n'%(str(int(d))))
                            of.writelines('mu = %s\n'%(str(mu)))
                            of.writelines('tf_beta = %s\n'%(str(tfb)))
                    
                            if opts.r != None:
                                of.writelines('r = %s\n'%(str(opts.r)))
                            of.close()

if __name__ == '__main__': main()
