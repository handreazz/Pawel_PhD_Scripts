#===========================================================
# this module contains the utility functions 
#===========================================================


import os , math
#from  config import *


##########################################################
def sort_column(data, col):
    data.sort(key=lambda y: y[col])
##########################################################
def chain_res_atom(pdb):
    ''' parse the pdb  into chain-residnum-atom list. a dictionary
    dd[x][y]: atom list, x:chainID, y:residue_number_in_string, 
    '''

    if check_file(300, pdb)==0: return

    fp=open(pdb, 'r')

    dd = {}
    for x in fp:
        if not('ATOM' in x[:4] or 'HETATM' in x[:6] or (x.strip())<50):continue
        ch=x[21:22]
        if ch not in dd.keys() and ch != ' ' : dd[ch]={}
        res=x[22:27] #include inserted
        if ch in dd.keys() and res not in dd[ch].keys() : dd[ch][res]=[]
        dd[ch][res].append(x)

    return dd

##########################################################
def cif2pdb(ciffile):
    os.system("maxit-v8.01-O  -i %s  -o 2 -exchange_in " % ciffile)
    pdbfile=ciffile + ".pdb"
    return pdbfile

##########################################################
def delete_file(*files):
    for x in files: os.system('rm -f ' + x)

##########################################################
def check_file(size, *files):
    n=1
    for f in files:
        if not os.path.exists(f) or  os.path.getsize(f)<size :
#            print('Error: file (%s) does not exist (or file size=0).' %f)
            n=0
            break
    return n

##########################################################
def str_after_id(line, id):
    """ get string after a given id """
    
    if id not in line :
        print('Warning: %s not in string (%s)' %(id, line))
        return line
    
    n = line.index(id)
    value=line[n+len(id):].strip()
    if len(value) <=0 or value.upper() == 'NULL' : value= "?"
    return value

##########################################################

def float_after_id(line, id):
    """ get float after a given id """
    
    if id not in line :
        print('Warning: %s not in string.' %(id))
        return 9999.0
    
    n = line.index(id)
    li=line[n+1:].strip().split()
    if len(li)<=0:
        print('Error! No value after id (%s).' %(id))
        return 9999.0
    else:
        if isnum(li[0]):
            return float(li[0])
        else:
            print('Error! %s is not a numeric.' %li[0])
            return 9999.0
        
##########################################################

def int_after_id(line, id):
    """ get int after a given id """
    
    if id not in line :
        print('Warning: %s not in string.' %(id))
        return 9999
    
    n = line.index(id)
    li=line[n+1:].strip().split()
    if len(li)<=0:
        print('Error! No value after id (%s).' %(id))
        return 9999
    else:
        if isnum(li[0]):
            return int(li[0])
        else:
            print('Error! %s is not a numeric.' %li[0])
            return 9999

##########################################################
def str_between_id(line, id1,id2):
    """ get string between the two ids """
    
    if id1 not in line or id2  not in line :
        print('Warning: either %s or %s not in string' %(id1, id2))
        return "?"
    n1, n2 = line.index(id1)+len(id1), line.index(id2)
    return line[n1+1:n2].strip()

##########################################################
def float_between_id(line, id1,id2):
    """ get float value between the two ids """
    
    if id1 not in line or id2  not in line :
        print('Warning: either %s or %s not in string' %(id1, id2))
        return  9999.
    n1, n2 = line.index(id1), line.index(id2)
    return float(line[n1+1:n2])

##########################################################
def int_between_id(line, id1,id2):
    """ get int value between the two ids """
    
    if id1 not in line or id2  not in line :
        print('Warning: either %s or %s not in string' %(id1, id2))
        return  9999
    n1, n2 = line.index(id1), line.index(id2)
    return int(line[n1+1:n2])

##########################################################
def isnum(value):
    return str(value).replace(".", "").replace("-", "").isdigit()

##########################################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        #print('Error: %s is not a number.' %s)
        return False

##########################################################
def is_digit(s):
    
    n=0
    if len(s)==0: return 0
    if s[0:1] == '-' :
        if s[1:].isdigit() : n=1
    else:
        if s.isdigit() : n=1

    return n

##########################################################
def get_value_after_id(line, id):
    """ get value after a given id """
    
    if id not in line : return "?"
    li=line.split(id)
    value=li[1].strip()
    if len(value) <=0 or value.upper() == 'NULL' : value= "?"
    return value

##########################################################
def is_cif(file):

    n, m=0, 0
    if not os.path.exists(file): return n
    
    for x in open(file, 'r').readlines():
        m=m+1
        if m>100: break
        t=x.strip()
        if len(t)<4: continue

        if ('data_' in t[:5] or 'loop_' in  t[:5]  or
            ('_' == t.split()[0][0] and '.' in t.split()[0])):
            n=1
            break
        elif 'HEADER ' in x[:7]:
            break
        
    return n 
##########################################################
def value_between_string(ln, s1, s2):
    ''' get the string between two strings (s1,s2) in a line(case sensitive)
    '''
    if s1 not in ln or s2 not in ln:
        print('Warning: string (%s or %s) not in %s' %(s1,s2,ln))
        return ''
    n=ln.index(s1)+len(s1)
    t1=ln[n:]
    n=t1.index(s2)
    return t1[:n]

##########################################################
def residue():
    '''non-ligand residues
    '''

    res=['GLY','ALA','VAL','LEU','ILE','CYS','MET','PRO','PHE','TRP','TYR',
         'HIS','LYS','ARG','ASP','GLU','ASN','GLN','THR','SER','MSE',
         'HOH','DOD',
         '  A','  G','  C','  T',' DA',' DG', ' DC',' DT', ' DI','  U','  I',
         'ADE', 'THY', 'GUA', 'CYT', 'URA']

    return res


##########################################################
def perror(info):
    '''print error messages 
    '''
    if info not in ERRLOG:
        ERRLOG.append(info)
        print(info.strip())
    
##########################################################
def space_group_crystal_match(spg):
    ''' 
    The dic spg_cell contains all the chiral space groups.
    
    http://www.ruppweb.org/Xray/comp/space_instr.htm
    '''
    spg_cryst={
        
#TRICLINIC
        
        "A1":1,
        "P1":1,
        "P1-":1,
        "P-1":1,
        
# MONOCLINIC

        "A121":2,
        "A2":2,
        "B112":20, #C is unique axis. alpha, beta, =90
        "B2":20,  #C is unique axis. alpha, beta, =90
        "C2":2,
        "C121":2,
        "C21":2,
        "C1211":2,
        "C2(A112)":2,
        "I121":2,
        "I1211":2,
        "I2":2,
        "I21":2,
        "P2":2,
        "P121":2,
        "P112":2,
        "P21":2,
        "P1211":2,
        "P1121":2,
        "P21(C)":2,
        
#ORTHORHOMBIC
        
        "P222":3,
        "P2221":3,
        "P21212":3,
        "P212121":3,
        "P22121":3,
        "P21221":3,
        "P21212A":3,
        "B2212":3,
        "C222":3,
        "C2221":3,
        "I222":3,
        "I212121":3,
        "F222":3,

#TETRAGONAL
        
        "P4":4,
        "P41":4,
        "P42":4,
        "P43":4,
        "P422":4,
        "P4212":4,
        "P4122":4,
        "P41212":4,
        "P4222":4,
        "P42212":4,
        "P4322":4,
        "P43212":4,
        "I4":4,
        "I41":4,
        "I422":4,
        "I4122":4,
        
#TRIGONAL   #hexagonal axis a=b gamma=120

        "P3":5,
        "P31":5,
        "P32":5,
        "P312":5,
        "P321":5,
        "P3112":5,
        "P3121":5,
        "P3212":5,
        "P3221":5,
        "R3":50,  #(rhombohedral axis, a=b=c & alpha=beta=gamma)
        "R32":50, #(rhombohedral axis, a=b=c & alpha=beta=gamma)
        "H3":5,  
        "H32":5,
        
#HEXAGONAL

        "P6":6,
        "P61":6,
        "P62":6,
        "P63":6,
        "P64":6,
        "P65":6,
        "P622":6,
        "P6122":6,
        "P6222":6,
        "P6322":6,
        "P6422":6,
        "P6522":6,
        
#CUBIC
        
        "C4212":7, #?
        "F422":7, #?
        
        "P23":7,
        "F23":7, 
        "I23":7,
        "P213":7,
        "I213":7,
        
        "P432":7,
        "P4132":7,
        "P4232":7,
        "P4332":7,
        "F432":7,
        "F4132":7,
        "I432":7,
        "I4132":7,

# others
        "P121/c1":2,
        "I41/a":4
       
        }        
    tmp=spg.replace(' ','')
    if tmp in spg_cryst.keys():
        return spg_cryst[tmp]
    else:
        print('Warning: The space group (%s) is not in the list' %spg)
        return 0

##########################################################
def get_file_by_pdbid(pdbid_in):

    pdb_path= "/data/remediation-alt/ftp-v4.0/pdb/data/structures/all/pdb/"
    sf_path= "/data/remediation-alt/ftp-v4.0/pdb/data/structures/all/structure_factors/"
    www_path = "http://www.rcsb.org/pdb/files"


    pdbid=pdbid_in.lower()

    pdb=pdb_path + "pdb" + pdbid + ".ent.gz"
    sf =sf_path  +  "r" + pdbid + "sf.ent.gz"

    pdbfile = "pdb" + pdbid + ".ent"
    sffile  = "r" + pdbid + "sf.ent"

    os.system ("zcat  %s > %s " % (pdb, pdbfile))
    os.system ("zcat  %s > %s " % ( sf, sffile ))

    if not os.path.exists(pdbfile) or not os.path.exists(sffile) : #try wget
        pdb = pdbid + ".pdb.gz"
        sf  = pdbid + "-sf.cif.gz"
        os.system ("wget %s/%s" %(www_path, pdb))
        os.system ("wget %s/%s" %(www_path, sf))
        os.system ("gunzip -f %s %s  " %(pdb, sf))
        pdbfile = pdbid + ".pdb"
        sffile  = pdbid + "-sf.cif"
    if os.path.exists(pdbfile) and  os.path.exists(sffile) :
        return (pdbfile, sffile)
    else :
        print ('Error! No pdbfile and sffile were generated.')
        return (pdbfile, sffile)

##########################################################
def mean_dev(data_in, col):
    '''get the min, max, average and deviation
    if col=-1, data_in is a list of data, else a list of list!
    '''
    if len(data_in)==0: return 0,0,0,0 
    data=[]
    if col<0:
        data=data_in
    else:
        for x in data_in : data.append(float(x[col]))
    #print(data)
    mini, maxi=min(data), max(data)
    n=len(data)
    if n==0: return 0,0,0,0
    avg=sum(data)/float(n)
    s1=0
    for x in data:
        a2=(x-avg)*(x-avg)
        s1=s1+a2
    dev=math.sqrt(s1/float(n))

    return avg, dev, mini, maxi
        
