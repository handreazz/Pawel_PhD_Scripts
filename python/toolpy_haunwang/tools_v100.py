#!/usr/bin/env /apps/python-2.6.1/bin/python
##!/usr/bin/env python

import os,sys,math
import pdb_stat as stat

def usage():
    content='''
    
###############################################################################
usage: tools.py [option] file

    This is a utility tool that performs various jobs (created 2010-12-03)
    
    1. Analyze anisotropy of each atom.ANISOU records must exist in PDB file.
    tools.py -anis pdbfile
    
    2. calculate min,max,mean,standard deviation of nth column in the file.
    tools.py -std file n  
    
    3. calculate min,max,number,mean,deviation of nth column for each
    resolution bins. (resolution & data in m & n columns;  k,number of bins) 
    tools.py -bin file m, n, k
    
    4. add a constant to Biso or (ANISOU) to pdb 
    tools.py -changeB pdbfile  const (or b11 b22 b33 b12 b13 b23)
    
    5. tools.py -scale pdbfile : to calculate the scale matrix in PDB 
    
    6. tools.py -contact pdbfile (id) : to calculate crystal contact in PDB
    (id=0, use crystal frame (remove SCALE); id=1, use SCALE in PDB) 
    
    7. tools.py -res pdbfile : reorder residue number sequentially
    if adding A4_B5 after pdbfile, chain A 4 will be started from chain B 5

    8. tools.py -pick file1 file2  : grep items from first column of file1 and 
    extract the lines in file2 containing the item.
    
    9. tools.py -comp file : compare two pdbs before/after remediation.
    File contains a list of entries in path which contains old PDBs.
    If given as tools.py -comp pdb1 pdb2, compare the two pdb files.
    
    10. tools.py -sftoken  idlist : correct SF cif tokens
     _diffrn.detail to _diffrn.details; input pdbid list
    
    11. tools.py -occ  pdbfile  (find/correct occupance)
     If atom on special position (2/3/4/6 fold), occ is (0.5/0.33/0.25/0.16)
    
    12. tools.py  -mr285  pdbfile  sffile    (07/15/2011)
    coord. not in the crystal frame. Using MR to get new xyz and align the 
    original xyz to the new_xyz to get Matrix(X0). Then generate Remark 285.
    
    13. tools.py  -285  pdbfile1 pdbfile2    (07/15/2011)
    coord. not in the crystal frame. generate (rigid body + refine) pdbfile2
    Align pdbfile1 to pdbfile2 to get Matrix(X0). Then generate Remark 285.
    
    14. tools.py  -twin  sffile     (06/12/2012)
    analysis truncate results and make plots for twin/intesity/Wilson
    (sffile can be in any format: add pdbfile, if no cell in the sffile)
    
    15. tools.py  -sym  sffile     (07/06/2012)
    useing pointless to find best space group.
    
    16. tools.py  -ha  sffile     (07/16/2012) remove H atoms
    
    
###############################################################################

'''
    
    print(content)
    sys.exit()

###############################################################################

def process(*files):
    
    arg=files[0]
    if len(arg)<2 : usage()

    narg=len(arg)
    for k in range(narg):
        if(arg[k].lower() == '-list'):
            flist=arg[k+1]
            
        elif(arg[k].lower() == '-anis'):
            ani=anisotropy(arg[k+1])
            
        elif(arg[k].lower() == '-scale'):
            ani=calc_scale_matrix(arg[k+1])
            
        elif(arg[k].lower() == '-contact'):
            id=0 # using crystal frame
            if len(arg)==4 : id=int(arg[k+2]) 
            ani=get_contact(arg[k+1], id)
            
        elif(arg[k].lower() == '-dev'):
            min,max,mean,std,num = mean_std('',arg[k+1], int(arg[k+2]))
        
        elif(arg[k].lower() == '-bin'):
            t1,t2,t3,t4=arg[k+1], int(arg[k+2]), int(arg[k+3]), int(arg[k+4]) 
            data=mean_std_bin('', t1,t2,t3,t4)
            
        elif(arg[k].lower() == '-changeb'):
            if len(arg)>6:
                t=[float(arg[k+i+2]) for i in range(6)]
            else:
                t=[float(arg[k+2])]
            newpdb=change_bfactor(arg[k+1], t)
            
        elif(arg[k].lower() == '-res'): #rename residue number from start
            if len(arg)==3: #automatic
               newpdb=residue_num_seq(arg[k+1])
            elif len(arg)>3:
               newpdb=residue_num_seq(arg[k+1],arg[k+2])
               
        elif(arg[k].lower() == '-pick'):
            pickup_item_from_firstfile(arg[k+1], arg[k+2])
            
        elif(arg[k].lower() == '-cif'):
            parse_cif(arg[k+1])
            
        elif(arg[k].lower() == '-comp'):
            if len(arg)==3: # check list
                path='/home/hyang/calc/check-occ/2009-01-05/' #old format
                #path='/calc/2009-03-16/'  
                compare_pdbs_in_list(arg[k+1], path)
            elif len(arg)>3:
                info=compare_2pdb_occ(arg[k+1],arg[k+2])
                #info=compare_2pdb(arg[k+1],arg[k+2])
                #for x in info: print(x.strip())
        
        elif(arg[k].lower() == '-sftoken'): #correct _diffrn.detail to _diffrn.details
            change_sf_detail(arg[k+1])  #input a list of pdbid
            sys.exit()
            
        elif(arg[k].lower() == '-mr285'): #generate remark 285 & validate, by MR
            get_285_by_mr(arg[k+1], arg[k+2], 0)  

        elif(arg[k].lower() == '-285'): #generate remark 285 & validate
            get_285_by_mr(arg[k+1], arg[k+2], 1)  

        elif(arg[k].lower() == '-occ'): #find/correct occ
            correct_occ_on_symm(arg[k+1])
            
        elif(arg[k].lower() == '-twin'): #analysis twin
            if k+2==narg:
                sf_from_truncate(arg[k+1], '')
            elif k+2<narg:
                sf_from_truncate(arg[k+1], arg[k+2])

        elif(arg[k].lower() == '-sym'): #get space group
            if k+2==narg:
                sf_symmetry(arg[k+1], '')
            elif k+2<narg:
                sf_symmetry(arg[k+1], arg[k+2])

        elif(arg[k].lower() == '-ha'): #remove H atoms
            remove_h_atom(arg[k+1])

               
        elif(arg[k].lower() == '-stat'): #
            stat.get_stat()
               
        elif(arg[k].lower() == '-tmp'): #
            t='mysql -u rcsbuser -prcsb0000 -h pdb-a-linux-9 cleanv1 -e " describe %s " >t' %arg[k+1]
            os.system(t)
            ag=""" awk '{print "[\\x27%s\\x27,","\\x27"$1"\\x27",", 1, 0.1, 0.95, 20]"}' t""" %arg[k+1]
            print(t, ag)
            os.system(ag) 
         
##########################################################
def get_285_by_mr(pdbfile, sffile, id):
    '''coord. not in the crystal frame. Using MR to get new xyz and align the 
    original xyz to the new_xyz to get Matrix(X0). Then generate Remark 285.
    '''

    
    head='''REMARK 285                                                                      
REMARK 285 THE ENTRY COORDINATES                                                
REMARK 285 ARE NOT PRESENTED IN THE STANDARD CRYSTAL FRAME.                     
REMARK 285                                                                      
REMARK 285 IN ORDER TO GENERATE THE CRYSTAL AU, APPLY THE                       
REMARK 285 FOLLOWING TRANSFORMATION MATRIX OR MATRICES AND SELECTED             
REMARK 285 BIOMT RECORDS TO THE COORDINATES, AS SHOWN BELOW.                    
'''
    pdbnew = pdbfile + '_epmr'
    phelog='phenix_superpose.log'
    delete_file(pdbnew, phelog)

    if id==0: #sf file
        arg= 'auto -mr epmr -pdb %s -sf %s' %(pdbfile, sffile)
        os.system(arg)
    else:
        pdbnew = sffile

    arg = 'auto -match %s %s ' %(pdbnew, pdbfile)
    os.system(arg)

    
    if not os.path.exists(phelog) :
        print('Error! problem of alignment  (%s & %s)' %(pdbnew, pdbfile))
        return

    fp=open(phelog, 'r').readlines()
    
    chain, chain_range = chain_res(pdbfile, 1)
    print(chain_range.keys())
        
    r1,r2,r3,t1=([],)*4
    matrix=''
    for i, x in enumerate (fp):
        if 'r={{' in x and '},' in x :
            r1=x[3:].replace('{','').replace('}','').split(',')
            r2=fp[i+1][3:].replace('{','').replace('}','').split(',')
            r3=fp[i+2][3:].replace('{','').replace('}','').split(',')
            
        elif 't={{' in x and '},' in x :
            t1=x[3:].replace('{','').replace('}','').split(',')
            tt1=[float(x.strip()) for x in t1]
            print(head)
            
            rr1=[float(x.strip()) for x in r1 if len(x.strip())>0]
            rr2=[float(x.strip()) for x in r2 if len(x.strip())>0]
            rr3=[float(x.strip()) for x in r3 if len(x.strip())>0]
            
            #print(rr1,rr2, rr3, tt1 )
            m1='REMARK 285 X0  1 %11.6f%11.6f%11.6f%11.6f \n' %(rr1[0],rr1[1],rr1[2],tt1[0])
            m2='REMARK 285 X0  2 %11.6f%11.6f%11.6f%11.6f \n' %(rr2[0],rr2[1],rr2[2],tt1[1])
            m3='REMARK 285 X0  3 %11.6f%11.6f%11.6f%11.6f \n' %(rr3[0],rr3[1],rr3[2],tt1[2])
            s1='REMARK 285 CRYSTAL AU =\n'
            s2='REMARK 285 (X0) * CHAINS '
            s3=''
            for x in chain.keys() : s3 =  s3 + x + ','
            matrix=m1+m2+m3+s1+s2+s3[:len(s3)-1] + '\n'
            

    print(matrix)

    pdb285=pdbfile + '_r285'
    fw=open(pdb285, 'w')
    pdb=open(pdbfile, 'r').readlines()
    for i, x in enumerate(pdb):
        if 'REMARK' in x[:6] and int(x[6:10])< 290 and 'REMARK 290' in pdb[i+1]:
            fw.write(x)
            fw.write(head)
            fw.write(matrix)
        else:
            fw.write(x)
    fw.close()
    
    arg='dcc -refmac -pdb %s -sf %s ' %(pdb285, sffile)
    os.system(arg)
    print('The new pdb=%s' %pdb285)
    
##########################################################
def change_sf_detail(flist):

    fp=open(flist, 'r').readlines()
    for x in fp:
        os.system('auto  -sf %s' %x)
        sf='r%ssf.ent' %x.strip()
        if (not os.path.exists(sf) or os.path.getsize(sf)<100): continue
        fr=open(sf, 'r')
        sfout=sf+'_new'
        fw=open(sfout, 'w')
        n=0
        for y in fr:
            if '_diffrn.detail' in y and not 'details' in y:
                y=y.replace('_diffrn.detail', '_diffrn.details')
                print('File(%s): _diffrn.detail -> _diffrn.details' %sf)
                n=1
            fw.write(y)
        fr.close(), fw.close()
        delete_file(sf)
        if n==0: delete_file(sfout)


##########################################################
def compare_pdbs_in_list(file, path):
    '''compare pdb file in the path: file contains the list of entries
    '''

    fp=open(file, 'r').readlines()
    log=file + '__log'
    fw= open(log, 'w')
    for x in fp:
        x=x.strip()
        fold=x + '_old'
        fnew=x
        
        gz = x + '.gz'
        tmp=path + x[4:6] + '/' + x + '*'
        arg='cp -f %s . ; gunzip -f %s; mv %s %s_old' %(tmp, gz, x, x)
        os.system(arg)
           
        pdbid=x[3:7]
        os.system('auto -pdb  %s >/dev/null' %pdbid )
        nmr=int(os.popen('egrep "^EXPDTA.*NMR" %s |wc -l' %fnew).read())
        if nmr>0 :
            tmp= fnew + ' is a NMR entry\n'
            fw.write(tmp)
            delete_file(fnew, fold)
            continue

        
        if not (os.path.exists(fold) and os.path.getsize(fold) and
                os.path.exists(fnew) and os.path.getsize(fnew)):
            tmp='Error: Either (%s) or (%s) not exist\n' %(fold, fnew)
            fw.write(tmp)
            continue

        info=compare_2pdb_occ(fold, fnew)
        delete_file(fold, fnew)

        m=0
        for x in info:
            fw.write(x)
            if 'Error' in x or 'Warn' in x : m=1
        #if m==0: delete_file(fold, fnew)
        
    fw.close()
        
##########################################################
def count_atom(file):
    natm, natmh=0,0
    for x in open(file,'r').readlines():
        if 'ATOM' in x[:4] or 'HETA' in x[:4]:
            if ' H' in x[76:78] or ' D' in x[76:78]:
                natmh = natmh +1
            else:
                natm = natm + 1
    return natm, natmh

##########################################################
def compare_2pdb_occ(fold, fnew):

    tf1, tf2 = fold + '_tmp', fnew + '_tmp'
    
    os.system('egrep "^ATOM|^HETATM"  %s  >%s' %(fold,tf1)) #keep ATOM/HETA
    os.system('egrep "^ATOM|^HETATM"  %s  >%s' %(fnew,tf2))


    
    ddf1=open(tf1, 'r').readlines()
    ddf2=open(tf2, 'r').readlines()
    
    nres1=chain_res_list(ddf1) #put chain+residue in a list [[],[]...]
    nres2=chain_res_list(ddf2)
    
    info=['\n=========Checking files (%s : %s) ========\n' %(fold, fnew)]

    #print('\n=========Checking files (%s : %s) ========\n' %(fold, fnew))
    for x in nres1: #for each residue of old pdb
        #for y in x: print (y)
        docc=check_occ(x)  #return uniq atom(as key) and list of occ as val
        #print(docc)
        for y in docc.keys():
            s=sum(docc[y])
            
            if s >1.0: #check new pdb
                tmp=check_new_occ(fold, fnew,docc, y, nres2)
                if len(tmp)>0 : info.append(tmp)
                #print(tmp)
                
    delete_file(fold, fnew)
    return info


    
##########################################################
def compare_2pdb(fold, fnew):
    '''compare the two pdb files in XYZ, OCC, Biso.
    heavyly use shell command for fastest calculation
    '''

    info=['\n=========Checking files (%s : %s) ========\n' %(fold, fnew)]
    tf1, tf2 = fold + '_tmp', fnew + '_tmp'
    arg='egrep "^ATOM|^HETATM"  %s | cut -c 29-66 |sort >%s' %(fold,tf1)
    os.system(arg)
    arg='egrep "^ATOM|^HETATM"  %s | cut -c 29-66 |sort >%s' %(fnew,tf2)
    os.system(arg)

    df=os.popen('diff %s %s ' %(tf1, tf2)).read().split('\n')
    df=[x for x in df if len(x)>0]
    
    #for x in df: print(len(df), x)
    natm, natmh= count_atom(fnew)
        
    if len(df) == 0: 
        info.append('Two files(%s %s) are the same.\n' %(fold,fnew))
        delete_file(tf1, tf2)
        return info
    
    os.system('egrep "^ATOM|^HETATM"  %s  >%s' %(fold,tf1)) #keep ATOM/HETA
    os.system('egrep "^ATOM|^HETATM"  %s  >%s' %(fnew,tf2))
    
    df1, df2 = [], []
    for x in df:  #use the difference only
        if '< ' in x[:2]:
            df1.append(x[2:])
        elif '> ' in x[:2]:
            df2.append(x[2:])
    

    ddf1, ddf2 = [], []
    if len(df1)>0: #get full ATOM records
        for x in df1:
            arg = 'grep -m 1 "%s" %s ' %(x, tf1)
            tt = os.popen(arg).read()
            ddf1.append(tt) 
    if len(df2)>0:
        for x in df2:
            arg = 'grep -m 1 "%s" %s ' %(x, tf2)
            tt = os.popen(arg).read()
            ddf2.append(tt) 
            
    #for x in df: print(x)
    ddf1=[x for x in ddf1 if len(x)>0]
    ddf2=[x for x in ddf2 if len(x)>0]
        
    ddf1 = sort_column(ddf1, 20, 26) # sort pdb by colums 20 to 26
    ddf2 = sort_column(ddf2, 20, 26) #
    
    n1,n2 = len(ddf1), len(ddf2)
    info.append('\nWarning: (%s %s) differ in ATOM record (%d %d).\n'
                %(fold,fnew, n1, n2))
    
    if n1==0 or n2==0:
        for x in ddf1: info.append('old! ' + x )
        for x in ddf2: info.append('new! ' + x )
        return info


    aa,ma,lig,hoh, hh=0,0,0,0, 0
    pdb1, pdb2, pdb3 = separate_pdb(fnew)
    chain, chain_range = chain_res(pdb1,0) #poly-peptide
    chain2, chain_range2 = chain_res(pdb2,0) #ligand
    
    nt_res=0
    for x in chain:
        nt_res = nt_res + len(chain[x])
        
    nt_lig=0
    for x in chain2:
        nt_lig = nt_lig + len(chain2[x])
    
    #nres3=chain_res_list(open(pdb1, 'r').readlines())  #only to get the total number of residues
    #nt_res=len(nres3)
    #nres3=chain_res_list(open(pdb2, 'r').readlines())  #only to get the total number of residues
    #nt_lig=len(nres3)
    
    delete_file(pdb1, pdb2, pdb3)
    
    
    nres1=chain_res_list(ddf1) #put chain+residue in a list [[],[]...]
    nres2=chain_res_list(ddf2)


    for x in nres1: 
        docc=check_occ(x)
        for y in x: print(y.strip())
    print('-----------')
    for x in nres2: 
        docc=check_occ(x)
        for y in x: print(y.strip())
    

    nres, nlig=0, 0
    for x in nres1: #for each residue of old pdb
        #for y in x: print (y)
        docc=check_occ(x)  #return uniq atom(as key) and list of occ as val
        #print(docc)
        aa1,ma1,lig1=0,0,0
        for y in docc.keys():
            s=sum(docc[y])
            tmp='\nTotal occupancy for uniq old_pdb atom (%s) == %.2f\n' %(y, s)
            info.append(tmp)
            #print(tmp)
            
            if s >1.0: #check new pdb
                check_new_occ(fold, fnew,docc, y, nres2)
                tmp= 'Occ of the old pdb atom (%s) occ>1. do not check\n' %y
                #info.append(tmp)
                #print(tmp)
                '''
            else:
                tmp='Checking differenec of the old/new for atom(%s)\n' %y
                #info.append(tmp)
                #print(tmp)
                inf, aa1,ma1,lig1,hoh1, hh1=compare_diff(fold, fnew,chain_range, y, x, nres2)
                info.extend(inf)
                aa, ma, lig, hoh, hh = aa+aa1, ma+ma1, lig+lig1, hoh+hoh1, hh+hh1
                '''
        if (aa1+ ma1)>0: nres=nres+1
        if (lig1)>0: nlig=nlig+1
           
            
             
    #print('Summary: %s vs %s (AA,MA,LIG,HOH) %3d %3d %3d %3d' %(fold, fnew,aa,ma,lig,hoh))
    tmp=('\nSummary: %s vs %s (NRES,AA,MA,LIG,HOH, H) %3d %3d %5d %2d | %3d %3d %3d %3d %3d\n'
         %(fold, fnew,  nres, nlig, nt_res, nt_lig, aa,ma,lig,hoh, hh))
    info.append(tmp)
    natmc=aa+ma
    fnatmc=100*(aa+ma)/float(natm)
    if natmh>0 :
        fnatmhc= 100*hh/float(natmh)
    else:
        fnatmhc=0

    tmp=('\nSummary2: %s (RESC,LIGC,REST,LIGT,natmc,fnatmc,hh,fnatmhc) %3d %3d %4d %2d | %3d %6.2f %3d %6.2f %3d %3d\n'
         %(fnew,  nres, nlig, nt_res, nt_lig, natmc, fnatmc, hh, fnatmhc, natmh, natm))
    info.append(tmp)
        
    return info

##########################################################
def check_new_occ(fold, fnew, docc, y, nres2):
    tmp=''
    for x in nres2:
        doccn=check_occ(x)
        if y in doccn.keys() :
            t1=['%.2f' %t for t in docc[y]]
            t2=['%.2f' %t for t in doccn[y]]
            if(len(t1)<2): continue
            s1, s2=sum(docc[y]), sum(doccn[y])
            tmp=('%s :: %s %s=%.2f %s  %s=%.2f\n'
                  %(y,fold, str(t1),s1, fnew, str(t2), s2))
            print(tmp)
            break
        
    return tmp
    
##########################################################
def separate_pdb(pdbfile):
    '''separate PDB file by polymer pdb1 and ligands pdb2, water pdb3
    '''

    pdb1=pdbfile + 'tmp1'
    pdb2=pdbfile + 'tmp2'
    pdb3=pdbfile + 'tmp3'
    
    fw1, fw2, fw3 = open(pdb1,'w'), open(pdb2,'w'), open(pdb3,'w')
    
    n=0
    fr,fr1=[],open(pdbfile, "r").readlines()

    for x in fr1:
        if ('ATOM' in x[:4] or 'HETA' in x[:4]) and ('HOH' in x[17:20] or 'DOD' in x[17:20]):
            fw3.write(x)
        else:
            fr.append(x)
 
    length = len(fr)    
    i=0
    for i in range(length):
        k=length-i-1
        if (('CONECT' in fr[k][:6] or 'MASTER' in fr[k][:6]
             or 'END' in fr[k][:3] or 'HETATM' in fr[k][:6])
             and ('ATOM' in fr[k-1][:4] or 'TER ' in fr[k-1][:4])) :
            n=k
            break
    if i> length-3 : n=length
    for i in range(length):
        if i<n:
            fw1.write(fr[i])
        else:
            fw2.write(fr[i])
            '''
            if 'HOH' in fr[i]:
                fw3.write(fr[i])
            else:
                fw2.write(fr[i])
            '''

    fw1.close(), fw2.close(), fw3.close()
    return pdb1, pdb2, pdb3
    
##########################################################
def chain_res(pdbfile, id):
    '''use dic to contain chain-ID and residue range
    id=0: not include waters; id=1: include waters.
    '''
    
    fr=open(pdbfile, "r")
    
    
    chain={}
    chain_range={}
    n_old=-99999
    ch_old='?'
    for ln in fr:
        if('ATOM' in ln[:4] or 'HETATM' in ln[:6] ): 
            if id==0 and 'HOH' in ln[16:20] : continue
            ch=ln[21:22]
            if ch not in chain.keys() and ch != ' ' : chain[ch]=[]
            nres=ln[22:26]
            n=int(nres)
            if ch in chain.keys():
                if(n == n_old and ch == ch_old) :
                    continue
                chain[ch].append(n)
            n_old=n
            ch_old=ch
            
            
    for key in chain:
        if(len(chain[key])>0): chain_range[key]= [min(chain[key]), max(chain[key])]

    fr.close()
    return chain, chain_range
##########################################################
def compare_diff(fold, fnew, chain, atomo, reso,  nres2):
    '''
    reso: all the atoms in the residue([]); atomo: uniqe atoms; 
    nres2: all for new PDB ([[res1], [res2] ...])
    '''
    aa, ma, lig, hoh, hh=0,0,0,0,0
    info=[]
    for x in reso:
        tmp=x[11:16] + x[17:26]
        #print(tmp, atomo)
        m1, m2, m3 = x[17:20], x[29:54], x[54:60]
        if tmp==atomo : #match uniq atom
            #print ('old:' , x)
        
            for y in nres2:  #new residue
                for z in y[:]:
                    n1, n2, n3 = z[17:20], z[29:54], z[54:60]
                    if m1==n1 and m2==n2 and m3 != n3:
                        if ((m3.strip()=='1.00' and n3.strip()=='0.50')
                            or n3.strip()=='1.00') : continue
                            
                        t1='Error! files (%s : %s) differ in OCC\n' %(fold, fnew)
                        info.append(t1)
                        info.append('old: ' + x)
                        info.append('new: ' + z)
                        if 'ATOM' in z[:4] :
                            aa=aa+1
                            if ' H ' in z[76:79]: hh=hh+1
                            
                        elif 'HETA' in z[:4] :
                            if 'HOH' in z[17:20]:
                                hoh=hoh+1
                            else: #either ligand or modified residue
                                ch , nres= z[21:22], int(z[22:26])
                                if ch in chain.keys():
                                    
                                    if nres>=chain[ch][0] and nres<=chain[ch][1]:
                                        ma=ma+1
                                    else:
                                        lig=lig+1
                                    
                                
                        #print(t1,x,z)
                        y.remove(z)
                        
    return info, aa,ma,lig,hoh, hh
    

##########################################################
def check_occ(pdb):
    '''return a dic with key and a list of occ
    '''
    id, d1=0, {}
    for x in pdb:
        tmp=x[11:16] + x[17:27]
        if tmp not in d1.keys(): d1[tmp]=[]
        d1[tmp].append(float(x[54:60]) )
    return d1
        
    
##########################################################
def chain_res_list(pdb):
    '''put chain+residue in a list [[],[]...]
    '''

    
    n=len(pdb)
    if n==0:
        print('Warning: empty PDB list')
        return []
    
    m , tmp, pdbn = 0, [], []
    for x in pdb:
        if ('ATOM' in x[:4] or 'HETA' in x[:4]):
            m=m+1
            id0 = id= x[21:26] 
            if m<n: id = pdb[m][21:26]
            tmp.append(x)
            
            if id0 != id or m==n:
                pdbn.append(tmp)
                tmp=[]

    #print(pdbn)
    return pdbn
##########################################################
    
def chain_res_atom(fr):
    '''use dic to contain chain-ID and residue range, and atom
    like dic={chain:{resn:[atoms, ...]} , ...}
    '''
    
    n_old , ch_old = -99999, '?'
    chain={}
    for ln in fr:
        if(('ATOM' not in ln[:4] and 'HETATM' not in ln[:6]) or len(ln)<54):
            continue
        ch=ln[21:22]
        if ch not in chain.keys() and ch != ' ' : #1st line of chain
            chain[ch]=[ln]
        elif ch in chain.keys():
            chain[ch].append(ln)
        ch_old=ch


    record={}
    for ch in chain.keys():
        record[ch]={}
        n_old=-99999
        res = {}
        for ln in chain[ch]: #add residues to the chain
            n=int(ln[22:26])
            if n!=n_old : res[n]=[ln] #1st residue
                
            if n==n_old : res[n].append(ln) #add atoms to chain[n]
            n_old=n
        record[ch]=res

    return record

    
##########################################################
def sort_column(pdb, k1, k2):
    ''' Sort the columns (from k1 to k2) of PDB file in order.
    '''

    id=1
    n, d, pdbn = 0,[], []
    for ln in pdb:
        n=n+1
        if('ATOM' in ln[:4] or 'HETATM' in ln[:6] or 'ANISOU' in ln[:6]):
            ch=ln[21:22]
            d.append(ln)
            if id==1: cond = n==len(pdb) 
            if id==2: cond = n==len(pdb) or ch !=pdb[n][21:22]
            if cond :
                d1=[[x[:k1], x[k1:k2], x[k2:]] for x in d] #separate 3 column
                d1.sort(key= lambda y: y[1]) #sort 2th column
                d=[]
                for x in d1: pdbn.append(''.join(x))
            
        else:
            if len(d)>0:
                d1=[[x[:k1], x[k1:k2], x[k2:]] for x in d] #separate 3 column
                d1.sort(key= lambda y: y[1]) #sort 2th column
                d=[]
                for x in d1: pdbn.append(''.join(x))
            pdbn.append(ln)
            
    return pdbn
    
    
##########################################################
def pickup_item_from_firstfile(file1, file2):
    '''grep items from first column of file1 and extract the
    lines in files containing the item.
    '''

    
    script='''#!/bin/csh

set list = `cat $1 | awk '{print $1} '  `
set log = "${1}_picked"
rm -f $log 
foreach id ($list)
echo "========greping $id========="
grep -i $id $2 >>$log
end

'''
    scr='grep_item.csh'
    fw=open(scr, 'w')
    fw.write(script)
    fw.close()
    os.system('chmod +x %s; %s %s %s' %(scr, scr, file1, file2))
              
    
    
##########################################################
def residue_num_seq(*file):

    pdb=file[0]
    out=pdb+'_new'
    fw=open(out, 'w')
    fr=open(pdb, 'r')
    
    if len(file)>1:
        pdb, ss=file[0],file[1]
        t=ss.split('_')
        s1,s2=t[0], t[1]
        ch11, nres11, ch22, nres22 = s1[:1], s1[1:], s2[:1], s2[1:]
        print('input residue=', ch11, nres11, ch22, nres22)

        nr=int(nres22)
        
        res, ch, nres = '','',''
        for x in fr:
            
            if ('ATOM'  in x[:4] or 'HETA' in x[:4] or 'ANIS' in x[:4]):
                res, ch, nres = x[17:20], x[21:22], x[22:26]
                if ch.strip()==ch11 and nres.strip()==nres11 :
                    s1, s2, s3, s4, s5 = x[:21], '%s' %ch22, '%4d' %nr,' ', x[27:]
                    s=s1+s2+s3+s4+s5
                    fw.write(s)
                    break
                else:
                    fw.write(x)
            else:
                fw.write(x)
                
        print('start residue=', res, ch, nres)
        
            
        for x in fr:
            res2, ch2, nres2 = x[17:20], x[21:22], x[22:26]
            if (('ATOM'  in x[:4] or 'HETA' in x[:4] or 'ANIS' in x[:4]) and ch2==ch11) :
                if res2 != res :
                    nr=nr+1
                    res=res2
                    
                s1, s2, s3, s4, s5 = x[:21], '%s' %ch22, '%4d' %nr,' ', x[27:]
                s=s1+s2+s3+s4+s5
                fw.write(s)
            else:
                fw.write(x)
        fw.close()        
        print('The new pdbfile=%s' %out)        
        return

    
        
    ch_old, nres_old, nr = '?', -999, 0
    for x in fr:
        if 'ATOM'  in x[:4] or 'HETA' in x[:4] or 'ANIS' in x[:4]:
            #print(x[21:22], x[22:26])
            ch = x[21:22]
            s=''
            if ch == ch_old:
                res=x[17:20]
                if res != res_old :
                    nr=nr+1
                    res_old=res
                    
                s1, s2,s3, s4 = x[:22], '%4d' %nr,' ', x[27:]
                s=s1+s2+s3+s4
                #s=''.join(s1,s2,s3,s4)
            else:
                
                ch_old=ch
                res_old=x[17:20]
                y=x[22:26]
                if y[3:4].isalpha() :
                    nres=1
                else:
                    nres= int(y)
                nr=nres
                s1, s2,s3, s4 = x[:22], '%4d' %nr,' ', x[27:]
                s=s1+s2+s3+s4
                
            fw.write(s)
        else:
            fw.write(x)
        
        fw.close()        
        print('The new pdbfile=%s' %out)        
        return
        
##########################################################
def get_contact(pdbfile , id):
    '''Refer contact:  http://www.ccp4.ac.uk/dist/html/contact.html
    <mode> = ALL,IRES,ISUB,IMOL or AUTO (default: MODE IRES).
    '''
    limit=3.0
    pdb_new = pdbfile + '_new'
    fp = open(pdbfile, 'r')
    fw = open(pdb_new, 'w')
    fwc = open('ccp4_contact.csh' , 'w')
    for x in fp:
        if id==0 and 'SCALE' in x[:6] : continue
        if 'ENDMDL' in x[:6] : break
        fw.write(x)
    fw.close(), fp.close()
    
    
    log = pdbfile + '_contact'
    script = '''#!/bin/csh
    #<mode> = ALL,IRES,ISUB,IMOL or AUTO (default: MODE IRES).
    #ALL: for all interatomic distances for chosen residues.
    #ISUB: intersubunit contacts (must have different chain name)
    #IMOL: intermolecular contacts
    #AUTO: as IMOL, but additional (primitive) lattice translations are generated
    contact xyzin  %s <<eof >%s
    mode   AUTO
    ATYPE ALL
    limits 0.0  %f
    ''' %(pdb_new, log,limit)
    
    os.system(script)
    fwc.write(script)
    fwc.close()

    arg='egrep "\[.*\]"  %s |wc -l' %log
    ncont=int(os.popen(arg).read())
    print('Crystal contacts for %s (<%.1fA) = %d' %(pdbfile,limit, ncont))
    delete_file(pdb_new)
    #if ncont < 30: delete_file(log)
    return ncont
    
##########################################################
def delete_file(*files):
    for x in files: os.system('rm -f ' + x)

##########################################################
def calc_scale_matrix(pdbfile):
    ''' compare  scale card in pdb with the calculated one
    refer to : http://en.wikipedia.org/wiki/Fractional_coordinates
    If the fractional coordinate system has the same origin as the cartesian
    coordinate system, the a-axis is collinear with the x-axis, and the b-axis
    lies in the xy-plane, fractional coordinates can be converted to cartesian
    coordinates through the following transformation matrix: 
    
    '''
    #acc=0.002  # used for detecting non-cyrstal frame
    acc=0.000001
#    acc=0.000010
    
    fp=open(pdbfile, 'r')
    
    cell, s1,s2,s3=[],[],[],[] 
    for x in fp:
        if 'CRYST1' in x[:6]:
            v = x[6:].split()
            cell=[float(v[i]) for  i in range(6)]
        elif 'SCALE1' in x[:6]:
            v=  x[6:].split()
            s1=[float(v[i]) for  i in range(3)]
        elif 'SCALE2' in x[:6]:
            v=  x[7:].split()
            s2=[float(v[i]) for  i in range(3)]
        elif 'SCALE3' in x[:6]:
            v=  x[6:].split()
            s3=[float(v[i]) for  i in range(3)]
        elif 'ATOM' in x[:4] or 'HETA' in x[:4] : break
    fp.close()

    if len(cell) !=6 :
        print('No Cell parameters in '  + pdbfile)
        return
    
    a, b, c = cell[0],cell[1],cell[2]
    sa=3.141592654/180. 
    alpha,beta,gamma = sa*cell[3],sa*cell[4],sa*cell[5]

    ca, sa = math.cos(alpha), math.sin(alpha)
    cb, sb = math.cos(beta), math.sin(beta)
    cg, sg = math.cos(gamma), math.sin(gamma)
    
    vol=math.sqrt(1-ca**2-cb**2-cg**2 + 2*ca*cb*cg)
#    vol = sg*sb*sa
    sc1=[sc11, sc12, sc13] = [1/a, -cg/(a*sg), (ca*cg-cb)/(a*vol*sg)]
    sc2=[sc21, sc22, sc23] = [  0, 1.0/(b*sg), (cb*cg-ca)/(b*vol*sg)]
    sc3=[sc31, sc32, sc33] = [  0,          0,  sg/(c*vol) ]

    sct=[]
    sct.extend(sc1)
    sct.extend(sc2)
    sct.extend(sc3)

    sst=[]
    sst.extend(s1)
    sst.extend(s2)
    sst.extend(s3)


    df=0
    if len(sct) == 9 and len(sst) == 9:
        for i in range(9):
            if math.fabs(sct[i] - sst[i])>acc :
                df = 1
                break
        
    if df==1:
        print('Error! Calculated & reported(%s) SCALE matrix is different(acc=%.6f).' %(pdbfile, acc))
        print ('         calculated                  reported')
        print ('%10.6f%10.6f%10.6f  %10.6f%10.6f%10.6f'  %(sc11,sc12,sc13, s1[0],s1[1],s1[2]))
        print ('%10.6f%10.6f%10.6f  %10.6f%10.6f%10.6f'  %(sc21,sc22,sc23, s2[0],s2[1],s2[2]))
        print ('%10.6f%10.6f%10.6f  %10.6f%10.6f%10.6f'  %(sc31,sc32,sc33, s3[0],s3[1],s3[2]))
    else:
        print('Calculated and reported(%s) SCALE matrix is the same(acc=%.6f).' %(pdbfile,acc))
        

##########################################################
def change_bfactor(pdbfile, t):
    '''Add a constant to Biso or ANISOU which comes from overall scaling
    '''
    
    fp=open(pdbfile, 'r').readlines()
    out=pdbfile + '_newB'
    fw=open(out, 'w')
    n=len(t)
    v=t[0]
    if n==6: v=(t[0] + t[1] + t[2])/3.0
    for x in fp:
        if 'ATOM'  in x[:4] or 'HETA' in x[:4]:
            t1, t2, t3=x[:60], float(x[60:66])+v, x[66:].rstrip()
            tmp='%s%6.2f%s\n' %(t1, t2, t3)
            fw.write(tmp)
        elif 'ANISOU' in  x[:6] and n==6 :
            u=[float(x1) for x1 in x[29:71].split()]
            v1=[(x1 * 10**4)/(8*3.14156**2) for x1 in t]
            ut=[int(u[i] + v1[i]) for i in range(6)]
            #print(x)
            y1, y3 = x[:28], x[70:]
            y2 = ''.join('%7d' %ut[i] for i in range(6))
            tmp=y1+y2+y3
            fw.write(tmp)
        else:
            fw.write(x)
    fw.close()
    print('The new pdb = ' + out)
    return out
    
##########################################################
def mean_std_bin(list1, file, m, n, k):
    ''' get min,max,number,mean,standard deviation of nth column  for each
    resolution bins. (resolution & data in m & n columns;  k,number of bins)
    
    '''
    
    all_data=[]

    fp=list1
    if len(list1)==0: fp=open(file, 'r').readlines()
    res=[]
    for x in fp: # put resol in a list
        t=float(x.strip().split()[m-1])
        res.append(t)
    min1, max1=min(res), max(res)
    shell=reso_shell(min1, max1, k)

    for y in shell:
        s1, data=0,  []
        for x in fp:
            t=x.strip().split()
            y1, x1= float(t[m-1]), float(t[n-1])
            if y1 >= y[0] and y1 < y[1]:
                data.append(x1)
                s1=s1+x1
        min1, max1, mean, std, num=mean_std(data,'', 1)
        avg=(y[0]+ y[1])/2.
        tmp=('%6.2f %6.2f %6.2f  %8.3f %8.3f %8.3f %8.3f %5d'
             %(y[0], y[1], avg, min1, max1, mean, std, num))
        all_data.append(tmp)

    print('\nres1, res2, avg, min1, max1, mean, std, num')
    for x in all_data: print(x)
    return all_data

##########################################################
def reso_shell(min1, max1, nstep):
    ''' get resolution shell from the range min-max and step
    '''

    step=(max1-min1)/nstep
    shell=[]
    y1=min1
    
    for x in range(nstep):
        y2=y1+step
        shell.append([y1, y2])
        y1=y2
        
    return shell
   
##########################################################
def mean_std(list1,file, n):
    ''' get min,max,mean,standard deviation of nth column in the file
    id=0, use file; id=1, use list1
    '''
    
    id=len(list1)
    res=[]
    if id==0: 
        fp=open(file, 'r').readlines()
        for x in fp:
            v=float(x.strip().split()[n-1])
            res.append(v)
    else:
        res=list1
        
    nlist=len(res)
    min1, max1, mean = min(res), max(res), sum(res)/float(nlist)
    
    s=0
    for x in res:
        a=x-mean
        a2=a*a
        s=s+a2
    std=math.sqrt(s/float(nlist))
    
    print('min, max, mean, std, num = %8.3f %8.3f %8.3f %8.3f %6d'
          %(min1, max1, mean, std, nlist))
    
    return min1, max1, mean, std, nlist
    
##########################################################
def anisotropy(pdbfile):
    '''Analyze anisoutropy of each atom.
    '''

    fr=open(pdbfile, 'r')
    output=pdbfile + '.anis'
    fo=open(output, 'w')
    
    head='''
    Note: column 1 is atom id.
    column 2,3,4 are the principle axis (eigenvalues) of ellipsoid of
    each atom.
    column 5 is the anisotropy of each atom (defined as longest axis
    divided by shortest axis. The ratio is 1.0 for a perfectly isotropic
    (spherical) atom.

    use 'sort output -n -k 5' to sort anisotropy in order


'''
    
    fo.write(head)
    n=0
    for ln in fr:
        if 'ANISOU' in ln[:6]:
            n=n+1
            atom=ln[12:26].lstrip().replace(' ', '_')
            
            u=[float(ln[27:35]), float(ln[35:42]), float(ln[42:49]), 
               float(ln[49:56]), float(ln[56:63]), float(ln[63:70])]
            u=[x*0.0001 for x in u]
            id, e1, e2, e3=eigenvalue(u)
            if id ==0 or e2==0 :
                print('Warning: anisotropy can not be determined for ' + atom)
                continue
            
            anis=e2/e1
            tmp = '%s %8.4f %8.4f %8.4f  %8.4f\n' %(atom, e1,e2,e3, anis)
            if e1 <=0 or e2 <=0 or e3 <=0 :
                print('Error: [%s] has negative eigenvalues' %ln[12:26])
                
            fo.write(tmp)
            
#            all_ani.append(tmp)
#            print(tmp)

#    sorted=all_ani.sort(key= lambda ln: float(ln.split(' ')[3]))
#    for ln in all_ani: fo.write('%s' %ln)
#    fo.write('below is sorted\n')
#    for ln in sorted: fo.write(ln)
    
    fo.close(),fr.close()
    if n==0:
        print ('Error: No ANISOU records in ' + pdbfile)
        os.remove(output)
        return 
    print('The output file = ' + output)
    
##########################################################
def eigenvalue(u):
    '''
    reference:http://en.wikipedia.org/wiki/Eigenvalue_algorithm
    
    
    get eigen values for a 3X3 matrix (u) that has 3 REAL eigen values

        a  b  c  u11 u12 u13 or u[0] u[3] u[4]
    u = d  e  f  u21 u22 u23    u[3] u[1] u[5]
        g  h  i  u31 u32 u33    u[4] u[5] u[2]

    det= -l**3 +L**2(a+e+i) + L(d*b+g*c+f*h-a*e-a*i-e*i) +
    (a*e*i -a*f*h -d*b*i +d*c*h + g*b*f -g*c*e)
        
    Eqn = a1L**3 + b1L**2 + c1L + d1 = 0
    '''
    a,  b,  c = u[0], u[3], u[4]
    d,  e,  f = u[3], u[1], u[5]
    g,  h,  i = u[4], u[5], u[2]


    a1=-1
    b1=(a+e+i)
    c1=(d*b+g*c+f*h-a*e-a*i-e*i)
    d1=(a*e*i - a*f*h - d*b*i + d*c*h + g*b*f -g*c*e)

    a, b, c, d=a1, b1, c1, d1
    
    if a==0: return 0, 0, 0, 0
    
    x=((3*c/a)-(b*b/a*a))/3.0
    y=((2*math.pow(b,3)/math.pow(a,3)) - 9*b*c/(a*a) + (27*d/a))/27.0
    z = y*y/4. + math.pow(x,3)/27.0

    t1=y*y/4. - z
    if t1<=0: return 0, 0, 0, 0
    i = math.sqrt(t1)
    
    j = -math.pow(i,(1./3))
    t2=-(y/(2*i))
    if math.fabs(t2)>1 : return 0, 0, 0, 0
    k = math.acos(t2)
    
    m = math.cos(k/3.)
    n = math.sqrt(3)*math.sin(k/3.)
    p = -(b/3*a)

    Eig1 = -2*j*m + p
    Eig2 = j *(m + n) + p
    Eig3 = j*(m - n) + p


    return 1, Eig1, Eig2, Eig3
    
##########################################################
def check_pdb_occ(pdbfile):

    tf1 = pdbfile + '_tmp'
    
    os.system('egrep "^ATOM|^HETATM"  %s  >%s' %(pdbfile,tf1)) #keep ATOM/HETA
    
    ddf1=open(tf1, 'r').readlines()
    nres1=chain_res_list(ddf1) #put chain+residue in a list [[],[]...]

    for x in nres1: #for each residue in pdb
        docc=check_occ(x)  #return uniq atom(as key) and list of occ as val
        #print(docc)
        for y in docc.keys():
            s=sum(docc[y])
            
            if s >1.2: #
                print('Error: Sum of occupancy with atom(%s) >1.2' %y)
                
    delete_file(tf1)
     

##########################################################
def is_cif(file):

    n=0
    for x in open(file, 'r').readlines():
        t=x.strip()
        if ('data_' in t[:5] or 'loop_' in  t[:5]  or
            ('_' == t.split()[0][0] and '.' in t.split[0])):
            n=1
            break
        elif 'HEADER ' in x[:7]:
            break
        
    return n 

##########################################################
def correct_occ_on_symm(file) :
    ''' if file is cif, export corrected cif file; if pdb, then export pdb
    
    '''
    
    if not is_cif(file):  #pdbfile
        find_atom_on_symm(file, 'pdb')
    else: # cif
        pdb=runmaxit(file,2,'')
        site=find_atom_on_symm(pdb, 'cif')
        newcif=parse_cif(file, site)
        delete_file(pdb)
        os.system('diff %s %s' %(file, newcif))
        
        
        

##########################################################
def runmaxit(file, option, other):
    ''' some options to run maxit
        use '-exchange_in' to get tls (from mmcif of pdb_extract)
    '''
    print('Converting %s by Maxit with option %d ...' %(file, option))
    nfile=file + ".pdb"
    
    if option==2:
        nfile=file + ".pdb"
    else:
        nfile=file + ".cif"
    
    arg='maxit-v8.01-O  -i %s -o %d  %s '  %(file, option, other) 
    os.system(arg)
    
    return nfile

##########################################################
def find_atom_on_symm(pdbfile, mode):
    '''find atoms on special position and return site = {id: fold, }
    mode = pdb; correct pdbfile. Otherwise,
    '''

    check_pdb_occ(pdbfile)
    
    arg='phenix.pdbtools ' + pdbfile
    lines=os.popen(arg).read().split('\n')
    delete_file(pdbfile + '_modified.pdb',  'maxit.err', 'CifParser.log')

    
    if len(lines)<50:
        print('\nError: Source (as below) the phenix package first.')
        print('source /apps/phenix-1.6-289/phenix-1.6-289/phenix_env')
        sys.exit()

    site={}
    for i, x in enumerate(lines):
        if 'Number of sites at special positions:' in x:
            print (x.strip())
        elif 'pdb=' in x and '(' in x and ')' in x and 'original' in x:
            n=0
            tmp=x.split('pdb=')[1].split('"')[1]
            if ('site sym' in lines[i+1] and '(' in lines[i+1]
                and 'exact' in lines[i+1]):
                n=int (lines[i+1].split('sym')[1].split('(')[0])
                
            site[tmp]=n


    rmk375=os.popen('egrep "^REMARK 375.*ON A SPECIAL POSITION" %s' %pdbfile ).read().split('\n')
    for x in sorted(site.keys()):
        nn=0
        for y in rmk375:
            if len(y[16:25])>0 and y[16:25].strip() in x:
                nn=1
                break
            
        if nn==0:
            print('Warning: SKIPPED! (%s : symmetry fold=%d), not match PDB criteria(min. dist=0.15)' %(x, site[x]))
            site.pop(x)
        else:
           print('%s :   symmetry fold=%d  ' %(x, site[x]))
                  

    if len(site)==0 or mode=='cif' : return site
    print('\nDoing occupancy correction if necessary\n')

    out=pdbfile + '_occ'
    fp, fw = open(pdbfile, 'r'), open(out, 'w')
    
    for x in fp:
        if ('ATOM' in x[:4] or 'HETA' in x[:4]):
            line = check_occ_site(x, site)
            if len(line)>10:
                print('old:' + x.strip())
                print('new:' + line.strip())
                fw.write(line)
            else:
                fw.write(x)
        else:
            fw.write(x)
                
                
                
    fp.close(), fw.close()

    return site

    
##########################################################

def check_occ_site(x, site):

    occ={2:0.5, 3:0.33, 4:0.25, 6:0.16}
    line=''
    for y in site.keys():
        if y in x:
            oc=float(x[54:60])
            if site[y] not in occ.keys():
                print('Warning: symmetry fold (%d) not (2,3,4,6). site=%s ' %(site[y], site))
                continue
                
            if  oc != occ[site[y]] : #
                line=x[:54] + '%6.2f' %occ[site[y]] + x[60:]
                site.pop(y)
                break

    return line


##########################################################

def parse_cif(pdb, site):

    occ_assign={2:0.5, 3:0.33, 4:0.25, 6:0.16}
    table='_atom_site'
    fp=open(pdb, 'r').readlines()
    fp1,fp2,fp3,fp4=[], [], [], []
    n1,n2,n3,n4=0,0,0,len(fp)
    out=pdb+'new'
    fw=open(out, 'w')
    
    for i, x in enumerate(fp):
        cate, item ='',''
        if '.' in x :
            t=x.split('.')
            cate, item = t[0].strip(), t[1].strip()
            
        if cate == table and len(item)>1 and i>0 and  table not in  fp[i-1] :
            n1=i
        elif cate == table and len(item)>1 and i<n4-1 and  table not in  fp[i+1] :
            n2=i+1
        elif n1>0 and '#' in  x:
            n3=i
            break


    fp1=fp[:n1]
    fp2=fp[n1:n2]  #table
    fp3=fp[n2:n3]  #coord
    fp4=fp[n3:n4]

    tab={}
    nfield=n2-n1
    for i, x in enumerate(fp2): #parse table
        t=x.split('.')
        cate, item = t[0].strip(), t[1].strip()
        tab[item]=i

    atom='auth_atom_id'
    resid='auth_comp_id'
    chain='auth_asym_id'
    nres='auth_seq_id'
    occ='occupancy'
    
    #site={' O   HOH B 104 ': 2, 'MG    MG A 100 ': 2}

    fp3_new=[]
    for i, x in enumerate(fp3): #coord
        t = x.split()
        if len(t) != nfield :
            print('Warning: nfield != parsed column')
            
        occ_old=float(t[tab[occ]])
        ln=''
        for y in site.keys(): #check through site
            atom1, resid1 = y[:4].strip(),y[4:8].strip()
            chain1, nres1 = y[9:10].strip(), y[10:14].strip()
            if site[y] in occ_assign.keys() : occ_new = float(occ_assign[site[y]])

            if (t[tab[atom]]==atom1 and t[tab[resid]]==resid1 and
                t[tab[chain]]==chain1 and t[tab[nres]]==nres1 ):
                if occ_new != occ_old :
                    t[tab[occ]] = str(occ_new)
                    #print( atom1, resid1, chain1, nres1, site[y], occ_new, occ_old)
                    ln=' '.join(t) + '\n'
                    break
                
                
                    
        if not ln:
            fp3_new.append(x)
        else:
            fp3_new.append(ln)
            

        

    for x in fp1: fw.write(x)
    for x in fp2: fw.write(x)
    for x in fp3_new: fw.write(x)
    for x in fp4: fw.write(x)
    fw.close()
    return out

##########################################################

def sf_from_truncate(sffile, pdbfile):
    '''run ctruncate and analysis the result
    '''

    
    trun_log=sffile + '_trunc.log'
    sf_tmp=sffile + '.tmp'
    if pdbfile:
        arg="sf_convert -o mtz -pdb %s -sf %s -out %s>/dev/null" %(pdbfile,sffile,sf_tmp)
    else:
        arg="sf_convert -o mtz -sf %s -out %s>/dev/null " %(sffile, sf_tmp)

    print("Converting the %s to mtz" %sffile)
    
    os.system(arg)
    
    if not os.path.exists(sf_tmp) or os.path.getsize(sf_tmp)<500:
        print("Error: Either your sf file has no symmetry/cell or you did not provide a PDB file")
        sys.exit()
        

    print("Doing ctruncate to analyze twin/intesity/B_Wilson")
    arg='ctruncate -hklin %s -amplitudes -colin "/*/*/[FP,SIGFP]" >& %s' %(sf_tmp,trun_log)
    os.system(arg)
    delete_file('sf_information.txt', 'sf_format_guess.text', sf_tmp)

    print("The output file = %s" %trun_log)

    plot_data=sffile+'.data'
    fp=open(trun_log, 'r')
    fw=open(plot_data, 'w')
    
    for x in fp:
        if ' Expected_untwinned ' in x and 'Expected_twinned' in x :
            n=0
            if n>1: break
            for y in fp:
                n=n+1
                if '$$' in y and n<3 :continue
                if '$$' in y and n>3 : break
                fw.write(y)

    fw.close()
        
    plot = " using 3 t 'reported' , '' u 9 t 'with TLS, include water' "

    xlabel='|L|'
    ylabel=''
    title='The Padilla-Yeates |L| test '
    plot ='''  using 1:2 t "Observed_data",  '' u 1:3 t "Untwinned_by_theory" ,  '' u 1:4 t "Twinned_by_theory" ''' 
    gnu_plot1(plot_data, xlabel, ylabel, title, plot )
    
    

##########################################################
def gnu_plot1(file, xlabel, ylabel, title, plot):
    '''Plot the data using gnuplot, controled by key.
    if key==0, plot all of them
    '''
    gnu_scr= file + '.gnu'
    fw=open(gnu_scr, 'w')

    plot_gnu = '''
#set terminal jpeg large size 840,640 #transparent nocrop enhanced font arial 8 size 420,320
set terminal png  
set output '%s.png'
#set boxwidth 0.5 relative
#set style histogram clustered gap 1 title offset 0, 0, 0
#set style data histograms
set style data linespoints
set datafile missing '.'
set style fill  solid 1.0 border -1
#set key on   #default right top
set key  left top
set grid ytics
set size 1.0,1.0
set autoscale
set xtics rotate by 90 
set ytics
set xlabel "%s"
set ylabel "%s"
set title "%s"

#set colorbox vertical origin screen 0.9, 0.2, 0 size screen 0.05, 0.6, 0 bdefault
#plot 'struct_growth.data' using 2:xtic(1) t "all",'' u 3 t "altered"    
#plot 'filename'   using 1:2:3:xtic(1) t "hell" with  yerrorlines, '' u 1:4:5 t "altered"   with  yerrorlines
#plot 'datafile'   using 1:2:xtic(1) t "hell",  '' u 1:4:5 t "altered"   with  yerrorlines

plot '%s'  %s 

set term x11
#replot 
#pause 10

''' %(file, xlabel, ylabel, title, file,  plot)

    fw.write(plot_gnu)
    fw.close()
    os.system('gnuplot %s' %gnu_scr)
    print('output image = ' + file + '.png')
    os.system('display ' +  file + '.png')
    
##########################################################
def sf_symmetry(sffile, pdbfile):
    ''' get the best space group by pointless.
    '''

    mtz=sffile + '.mtz'
    out = sffile + '.sym'

    print('Converting to mtz format ...')
    if len(pdbfile):
        arg='sf_convert -o mtz -sf %s -pdb %s >/dev/null  ' %(sffile, pdbfile)
    else:
        arg='sf_convert -o mtz -sf %s >/dev/null ' %(sffile)
        
    os.system(arg)

    if not os.path.exists(mtz) or os.path.getsize(mtz)<500:
        print("Error: MTZ file is not generated, check symmetry/cell in sf file.")
        sys.exit()

    
    print('Getting the best space group by pointless...')
    arg='pointless hklin %s > %s' %(mtz, out)
    os.system(arg)
    
    os.system('grep "Best Solution" %s ' %out)

    print('For details, please see the output file =%s' %out)
        
    delete_file(mtz ,  'sf_format_guess.text', 'sf_information.txt')

##########################################################
def remove_h_atom(pdbfile):
    out=pdbfile + '_noH'
    fp = open(pdbfile, 'r')
    fw = open(out, 'w')

    for x in fp:
        if ('ATOM ' in x[:6] or 'HETATM' in x[:6]) and ' H' in x[76:78] :
            continue
        fw.write(x)
    fp.close(), fw.close()
    print ('The output file without H atoms = %s' %out)
##########################################################

if __name__ == '__main__':
    process(sys.argv)
    




























