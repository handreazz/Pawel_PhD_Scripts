import os,sys,math,string
import util

######################################################    
def get_stat():
    '''all sort of stats (command: tool -stat >all.log )
    After running the command, mv pdb_each_item.html & DAT_STORE/ to
    /net/wwwdev/auto-check/html/dev/stat
    
    '''
    
    ddir='DAT_STORE/'
    os.system('mkdir %s' %ddir) #make a fold to hold all the data
    
    get_html(ddir)   #link all the stat)
    twin_info(ddir)
    sys.exit()
    
    rfact_reso_growth(ddir)  #Rfactor changes with year
    do_reso_entity(ddir)   #resol. with protein,protein-NA, DNA, RNA,
    gnufit(ddir, 1)   #use data by sql, 1 fit by polynom.
    plot_entity(ddir)    #unique molecular weight/in asu
    do_string_stat(ddir)   #all string items 
    do_num_stat(ddir)  # stats for remark 3,200

    sys.exit()
    
#    auto_pop_corr(ddir)


######################################################
def do_num_stat(ddir):
    '''This is a large collection of numerically related plots
    '''
    data_all=[]
    items=get_items()  #all the data items
    for x in items: # stats for remark 3,200
        
        if 'entity' in x[0]: continue
        if 'start:' in x[0]:
            cate=x[0].split(':')[1]
            ofile=cate + '.all' 
            get_file_from_sql(cate,ofile)
            data_all=from_file_to_list(ofile)

            print(cate, len(data_all))
            continue
        elif 'end:' in x[0]:
            continue

        plot_pop(ddir, x, data_all)
        plot_corr(ddir, x, data_all)


######################################################
def plot_pop(ddir, x, data_all):
    '''Plot the data populations (by manually selected boundary)
    data_all must be directly from SQL without change.
    '''
    
    cate, token, minv, maxv, nstep = x[0],x[1],x[3],x[4],x[5]
    shell=data_bin(minv, maxv, nstep)

    if x[1] not in data_all[0]:
        print('Error, %s is not in the data list' %x[1])
        return
    
    i=data_all[0].index(x[1])
    data1=[]
    for y in data_all:
        if not util.is_number(y[i]):continue
        val=float(y[i])
        if val == 0.0 : continue #remove empty values
        data1.append([y[0], val])
        
    data, outlier = filter_data(data1, shell, 1) #only get the 1, 2th column
    fname= ddir + cate + '_' + token + '_outlier.html'
    get_outlier_html(fname, outlier)

    fpop= ddir + cate + '_' + token + '_pop.data'   #for data populations
    data_pop(fpop, data, shell, 1) #2th column
    avg, dev, mini, maxi = util.mean_dev(data,1)

    title = 'population of _%s.%s (mean=%.2f; dev=%.2f; entry=%d)' %(x[0], x[1], avg,dev,len(data))
    xrange,yrange,xlabel,ylabel = '', '','data range of %s' %x[1], 'number of entry'
    bar, rot, key, style = 0, 1, 0, 0
    plot = """plot '%s' using 3:xtic(1) lc rgb "blue" ,'' u 0:3:4 with labels offset 0, 0.5""" %(fpop)
    gnuscr, gnuout = gnu_plot(fpop,title,xrange,yrange,xlabel,ylabel,bar,rot,key,style,plot)

    print('len==',x[1], i, len(data1), len(data_all))

######################################################
def plot_corr(ddir, x, data_all):
    '''get the data correlations with resolution
    '''
    
    cate, token, minv, maxv, nstep = x[0],x[1],x[3],x[4],x[5]

    res='ls_d_res_high'
    if x[1] not in data_all[0] or res not in data_all[0]:
        print('Error, %s (or %s) is not in the data list' %(x[1], res))
        return
    
    i0=data_all[0].index(res) 
    i=data_all[0].index(x[1])
    data1=[]
    for y in data_all:
        if not util.is_number(y[i]) or not util.is_number(y[i0] ):continue
        val=float(y[i])
        val0=float(y[i0])
        if val == 0.0 or  val0 == 0.0 or val<x[3] or val>x[4] : continue
        data1.append([y[0],val0, val])

    shell=data_bin(0.6, 5.0, 20)   #data change with resolution
    fcorr= ddir + cate+ '_'+ token + '_res.data'
    data_corr(fcorr,data1, shell, 1)

    title = 'The mean value of %s in each resolution bin' %(x[1])
    xrange,yrange,xlabel,ylabel = '', '','resolution', '%s' %x[1]
    bar, rot, key, style = 1, 1, 0, 0
    plot = """plot '%s' using 4:5:xtic(1) lc rgb "green" """ %(fcorr)
    gnuscr, gnuout = gnu_plot(fcorr,title,xrange,yrange,xlabel,ylabel,bar,rot,key,style,plot)

    print('len==',x[1], i, len(data1), len(data_all))


######################################################    
def get_file_from_sql(cate, outf):
    item_all=get_items()
    items=[]
    for x in item_all:
        if cate != x[0]: continue
        items.append(x[1])

    print ('items=', items)
    do_sql(cate, items, outf)
    
######################################################
def from_file_to_list(outf):
    ''' input a file and output a list of list
    '''
    
    data_out=[]
    fp=open(outf, 'r')
    for x in fp:
#        if 'structure_id' in x[:20] : continue
        t=x.strip().split()
        data_out.append(t)
    return  data_out
######################################################    
def do_sql(cate, item, outf):
    '''This sql combines two table together (refine, cate)
    The item belongs to cate. 
    '''

    util.delete_file(outf)
    sql = 'mysql -u rcsbuser -prcsb0000 -h pdb-a-linux-9 cleanv1 -e '
    entry_id="(select pdb_id from pdb_entry where method like '%x-ray%' and \
             status_code='REL' and method !='THEORETICAL MODEL')"

    y1= '"select distinct r.structure_id, r.ls_d_res_high, '
#    y2=' x.%s ' %item
    t= ''.join(['x.%s, ' %x for x in item])   #add more 
    y2 =t.strip()[:-1]
    y3= ' from  refine as r , %s as x where  r.structure_id = x.structure_id  ' %cate
    y4= ' and r.structure_id in (%s) ' %entry_id
    y5= 'order by  r.structure_id , x.%s" >%s' %(item[0], outf)

    s=''.join([sql, y1,y2,y3,y4,y5])
    print (s)
    os.system(s)


######################################################    
def do_sql_gen(outf, tabs, type):
    '''This is a generate script to do SQL for any tables items
    outf: the output file from doing sql (only for Xray)
    tabs: the tables (format : [[cate, item1,..], [cate, item1,..] ...]
    type: 'all' for all, 'x-ray' for XRAY, 'nmr' for NMR,
    'NEUTRON DIFFRACTION, X-RAY DIFFRACTION' for xray&neut ,
    'NEUTRON DIFFRACTION' for neut, 'POWDER' for POWDER DIFFRACTION
    'ELECTRON MICROSCOPY' for EM, 'FIBER' for FIBER DIFFRACTION
    '''


    sql = 'mysql -u rcsbuser -prcsb0000 -h pdb-a-linux-9 cleanv1 -e '

    neut= " and  method not like '%neut%' " #exclude xry+neut
    neut= " "
    
    if 'all' in type :
        entry_id="(select pdb_id from pdb_entry where ( \
 status_code='REL' and method !='THEORETICAL MODEL')) "
        
    elif 'xray' in type or 'x-ray' in type: #only xray
        entry_id="(select pdb_id from pdb_entry where (method like '%%x-ray%%' %s and \
 status_code='REL' and method !='THEORETICAL MODEL'))" %neut
        
    else:
        entry_id="(select pdb_id from pdb_entry where (method like '%%%s%%' and \
 status_code='REL' and method !='THEORETICAL MODEL'))" %type
        

    cate=[]
    sel=''
    for x in tabs:
        print(x)
        for i,y in enumerate(x):
            if i==0:
                cate.append(x[0])
            else:
                sel=sel+ '%s.%s, ' %(x[0], x[i])
    sel= 'select distinct ' + sel


    y0=sql

    y1 =sel.strip()[:-1]

    tmp=''
    for x in cate: tmp = tmp + x + ','
    y2 = ' from ' + tmp.strip()[:-1]
    
    tmp=''
    for i,x in enumerate(cate):
        if i==0: continue
        tmp = tmp + ' %s.structure_id= %s.structure_id and ' %(cate[i-1],cate[i])

    rev = ' database_PDB_rev.num =1 and '
    if 'database_PDB_rev' not in cate : rev = ''
    
    y3 = ' where ' + tmp + rev

    y4 = ' %s.structure_id in %s ' %(cate[0], entry_id)
        
    arg = y0 + ' " ' +  y1 + y2 + y3 + y4 + ' " ' + '>%s' %outf

    os.system (arg )
#    print (arg )



######################################################    
def get_items():
    '''all the annotated items
    '''
    
    items=[
        ['start:refine', '', 0, 0, 0, 0],
        ['refine', 'ls_d_res_high', 1, 0.5, 6.0, 20],
        ['refine', 'ls_d_res_low', 1, 5, 150, 20],
        ['refine', 'ls_R_factor_R_work', 1, 0.08, 0.40, 20],
        ['refine', 'ls_R_factor_R_free', 1, 0.08, 0.40, 20],
        ['refine', 'overall_SU_R_Cruickshank_DPI', 1, 0.005, 0.95, 20],
        ['refine', 'overall_SU_R_free', 1, 0.005, 0.95, 20],
        ['refine', 'solvent_model_param_bsol', 1, 2, 250, 20],
        ['refine', 'solvent_model_param_ksol', 1, 0.1, 0.95, 20],
        ['refine', 'ls_percent_reflns_R_free', 1, 0.5, 30, 20],
        ['refine', 'B_iso_mean', 1, 2, 200, 20],
        ['refine', 'correlation_coeff_Fo_to_Fc', 1, 0.6, 1.1, 20],
        ['refine', 'correlation_coeff_Fo_to_Fc_free', 1, 0.6, 1.1, 20],
        ['refine', 'rcsb_overall_ESU_R', 1, 0.01, 0.95, 20],
        ['refine', 'rcsb_overall_ESU_R_Free', 1, 0.01, 0.95, 20],
        ['refine', 'overall_SU_B', 1, 0.1, 60, 20],
        ['refine', 'overall_SU_ML', 1, 0.01, 0.95, 20],
        ['refine', 'ls_percent_reflns_obs', 1, 50, 105, 20],
        ['refine', 'ls_percent_reflns_R_free', 1, 0.5, 20, 20],
        ['refine', 'ls_number_reflns_all', 1, 1000, 500000, 30],
        ['refine', 'ls_number_reflns_obs', 1, 1000, 500000, 30],
        ['refine', 'ls_number_reflns_R_free', 1, 20, 50000, 30],
        ['refine', 'ls_number_reflns_R_work', 1, 1000, 150000, 30],
        ['refine', 'ls_number_restraints', 1, 100, 50000, 30],
        ['refine', 'occupancy_max', 1, 0.4, 1.1, 20],
        ['refine', 'occupancy_min', 1, 0.05, 1.1, 20],
        ['refine', 'ndb_ls_sigma_I', 1, -6, 6, 20],
        ['refine', 'ndb_ls_sigma_F', 1, -6, 6, 20],
        ['refine', 'ndb_data_cutoff_high_absF', 1, 10000, 100000000, 30],
        ['refine', 'ndb_data_cutoff_low_absF', 1, 0, 4,  20],
        ['end:refine', '', 0, 0, 0, 0],
        
        ['start:refine_ls_shell', '' , 1, 0.1, 0.95, 20],
        ['refine_ls_shell', 'd_res_high', 1, 0.5, 5.5, 20],
        ['refine_ls_shell', 'd_res_low', 1, 0.5, 6.5, 20],
        ['refine_ls_shell', 'percent_reflns_obs' , 1, 30, 106, 20],
        ['refine_ls_shell', 'percent_reflns_R_free' , 1,  0.5, 30, 20],
        ['refine_ls_shell', 'R_factor_all' , 1, 0.08, 0.70, 20],
        ['refine_ls_shell', 'R_factor_R_free' , 1, 0.08, 0.70, 20],
        ['refine_ls_shell', 'R_factor_R_free_error' , 1, 0.01, 0.2, 20],
        ['refine_ls_shell', 'R_factor_R_work' , 1, 0.08, 0.70, 20],
        ['refine_ls_shell', 'ndb_total_number_of_bins_used' , 1, 2, 40, 20],
        ['refine_ls_shell', 'number_reflns_all' , 1, 100, 30000, 30],
        ['refine_ls_shell', 'number_reflns_obs' , 1, 100, 40000, 30],
        ['refine_ls_shell', 'number_reflns_R_free' , 1, 10, 2000, 30],
        ['refine_ls_shell', 'number_reflns_R_work' , 1, 100, 40000, 30],
        ['end:refine_ls_shell', '' , 1, 0.1, 0.95, 20],

        ['start:reflns', '' , 1, 0.1, 0.95, 20],
        ['reflns', 'd_resolution_high' , 1, 0.5, 6.5, 20],
        ['reflns', 'd_resolution_low' , 1, 5, 150, 20],
        ['reflns', 'B_iso_Wilson_estimate' , 1,  2, 200, 20],
        ['reflns', 'observed_criterion_sigma_F' , 1, -5, 5, 20],
        ['reflns', 'observed_criterion_sigma_I' , 1, -5, 5, 20],
        ['reflns', 'percent_possible_obs' , 1, 40, 105, 20],
        ['reflns', 'ndb_redundancy' , 1, 0.5, 40, 20],
        ['reflns', 'ndb_netI_over_av_sigmaI' , 1, 1.0, 50, 20],
        ['reflns', 'ndb_netI_over_sigmaI' , 1, 1, 50, 20],
        ['reflns', 'Rmerge_F_obs' , 1, 0.01, 0.90, 20],
        ['reflns', 'ndb_Rmerge_I_obs' , 1, 0.01, 1.0, 20],
        ['reflns', 'ndb_Rsym_value' , 1, 0.01, 1.0, 20],
        ['reflns', 'pdbx_Rrim_I_all' , 1, 0.01, 1.0, 20],
        ['reflns', 'pdbx_Rpim_I_all' , 1, 0.01, 1.0, 20],
        ['reflns', 'pdbx_number_measured_all' , 1, 1000, 800000, 30],
        ['reflns', 'number_all' , 1, 1000, 800000, 30],
        ['reflns', 'number_obs' , 1, 1000, 800000, 30],
        ['end:reflns', '' , 1, 0.1, 0.95, 20],
        
        ['start:reflns_shell', '' , 1, 0.1, 0.95, 20],
        ['reflns_shell', 'd_res_high' , 1, 0.5, 5., 20],
        ['reflns_shell', 'd_res_low' , 1, 0.5, 6., 20],
        ['reflns_shell', 'percent_possible_all' , 1, 30, 105, 20],
        ['reflns_shell', 'percent_possible_obs' , 1, 30, 105, 20],
        ['reflns_shell', 'meanI_over_sigI_obs' , 1,  0.5, 50, 20],
        ['reflns_shell', 'ndb_redundancy' , 1, 0.5, 50, 20],
        ['reflns_shell', 'Rmerge_F_obs' , 1, 0.02, 1.0, 20],
        ['reflns_shell', 'Rmerge_I_all' , 1, 0.02, 1.0, 20],
        ['reflns_shell', 'Rmerge_I_obs' , 1, 0.02, 1.0, 20],
        ['reflns_shell', 'ndb_Rsym_value' , 1, 0.02, 0.95, 20],
        ['reflns_shell', 'pdbx_Rrim_I_all' , 1, 0.02, 0.95, 20],
        ['reflns_shell', 'number_measured_all' , 1, 100, 80000, 30],
        ['reflns_shell', 'number_measured_obs' , 1, 100, 80000,  30],
        ['reflns_shell', 'number_unique_all' , 1, 100, 40000, 30],
        ['reflns_shell', 'number_unique_obs' , 1, 100, 40000, 30],
        ['end:reflns_shell', '' , 1, 0.1, 0.95, 20],

        ['start:exptl_crystal', '' , 0, 0, 0, 0],
        ['exptl_crystal', 'pdbx_mosaicity' , 1, 0.1, 4.0, 20],
        ['exptl_crystal', 'density_Matthews' , 1, 1, 8.0, 20],
        ['exptl_crystal', 'density_percent_sol' , 1, 15, 92.0, 20],
        ['end:exptl_crystal', '' , 0, 0, 0, 0],
        
        ['start:exptl_crystal_grow', '' , 0, 0, 0, 0],
        ['exptl_crystal_grow', 'pH' , 1, 2, 11.0, 20],
        ['exptl_crystal_grow', 'temp' , 1, 4, 360.0, 30],
        ['end:exptl_crystal_grow', '' , 1, 0.1, 4.0, 20],
 
        ['start:entity', '' , 0, 0, 0, 0],         
        ['entity', 'water-weight-in-ASU' , 1, 80, 60000, 20],
        ['entity', 'polymer-weight' , 1, 500, 100000, 30],
        ['entity', 'non-polymer-weight' , 1, 30, 3000, 30],
        ['entity', 'total-weight-in-ASU' , 1, 500, 800000, 30],
        ['end:entity', '' , 1, 0.1, 4.0, 20],
        
        ['start:diffrn_radiation_wavelength', '' , 0, 0, 0, 0],         
        ['diffrn_radiation_wavelength', 'wavelength' , 1, 0.5, 5, 20],
        ['end:diffrn_radiation_wavelength', '' , 1, 0.1, 4.0, 20],

        ]

    return items

    
######################################################    
def get_outlier_html(fname, data):
    '''write the outliers into a html file, data has two columns
    '''
    
    url='http://www.rcsb.org/pdb/explore/explore.do?structureId'
    fw=open(fname, 'w')
    
    fw.write('<!DOCTYPE html> \n<html>\n<body>\n')
    fw.write('<style type="text/css">a {text-decoration: none}</style>\n')
    s1='The outlier data are excluded from the plot. They are not neccessary wrong, \
    but the wrong data should be in the outlier values!<p>\n'
    fw.write(s1)
    fw.write('<table>\n')

    data.sort(key=lambda y: y[1])
    for x in data:
        t1='<tr> <td> <a href="%s=%s" target="dynamic"> %s </a> </td>' %(url,x[0],x[0])
        t2='<td>  outliers (%s)</td></tr>\n' %x[1]
        fw.write(t1+t2)
 

    fw.write('</table> \n</body>\n</html>\n')
    fw.close()
            
######################################################    
def get_html(ddir):
    '''get a html table 
    '''

    
    items=get_items()
    html='index.html'
#    html='pdb_each_item.html'
    fw=open(html, 'w')

    fw.write('<!DOCTYPE html> \n<html>\n<body>\n')
    fw.write('<style type="text/css">a {text-decoration: none}</style>\n')

    s1='''<hr> <p>Tables below listed the population of the annotated cif
    items, the correlation with resolution, the data that was generated for
    ploting, and the outliers.  
    
    <p><b>For the graph of population:</b>
    The number on the top of each bar is the percentage of the population of the
    item. It was calculated by the number of the entries in the data range at the
    bottom of the graph divided by the total number of entries having proper values
    (outlier values excluded). The overall average is the summation of the values
    divided by the total number of entries (outliers excluded). The numbers on
    left axis are the number of entries corresponding to each bar.
    <br><b>For the graph of correlation:</b>
    Each bar is the mean value (vertical axis) of the data item in the resolution
    range (horizontal axis). The error bars (the standard diviation) are given to each value.

    <p>
    '''
    fw.write(s1)
    
    sp='&nbsp;&nbsp; '
    for x in items:
        if 'start:' in x[0]:
            s1=x[0].split(':')[1]
            s2='<p><h3> Data population and correlation with resolution for the table of <i>%s </i><p></h3>' %s1.upper()
            fw.write(s2)
            fw.write('<table>\n')
        elif 'end:' in x[0]:
            fw.write('</table>\n')
            
        else:
            
            fw.write('<tr>\n')
            y1='<td><a href="%s/%s_%s_pop.data.png" target="dynamic">_%s.%s %s</a></td> \n' %(ddir, x[0],x[1],x[0],x[1],sp)
            y2='<td bgcolor="#99ccff" ><a href="%s/%s_%s_pop.data" target="dynamic"> (data) %s </a></td> \n' %(ddir,x[0],x[1],sp)
            y3='<td><a href="%s/%s_%s_res.data.png" target="dynamic">change with resolution  %s </a></td>\n' %(ddir,x[0],x[1],sp)
            y4='<td bgcolor="#99ccff" ><a href="%s/%s_%s_res.data" target="dynamic">(data) %s  </a></td> \n' %(ddir,x[0],x[1],sp)
            y5='<td><a href="%s/%s_%s_outlier.html" target="dynamic">outliers </a></td> \n' %(ddir,x[0],x[1])
            fw.write(''.join([y1, y2, y3, y4, y5]))
            fw.write('</tr>\n')
        
        
        
    fw.write('\n<hr> \n')
    str_item=get_items_str()
    
    for x in str_item:
        if 'start:' in x[0]:
            s1=x[0].split(':')[1]
            s2='<p><h3> Data population and yearly growth and the growth rate for the <i>%s</i> items. </h3>  <p> (Numbers on the top of the bar is the percentage calculated from the number of population and the total non-null entries. The yearly growth rate is calculated  by the entry number divided total number for the year.)  <p>' %s1.upper()
            fw.write(s2)
            fw.write('<table>\n')
        elif 'end:' in x[0]:
            fw.write('</table>\n')
            
        else:
            
            fw.write('<tr>\n')
            y1='<td><a href="%s/%s_%s.all_pop.data.png" target="dynamic">_%s.%s %s</a></td> \n' %(ddir, x[0],x[1],x[0],x[1],sp)
            y2='<td bgcolor="#99ccff" ><a href="%s/%s_%s.all_pop.data" target="dynamic"> (data) %s </a></td> \n' %(ddir,x[0],x[1],sp)
            y3='<td><a href="%s/%s_%s.all.data.png" target="dynamic"> yearly growth  %s </a></td>\n' %(ddir,x[0],x[1],sp)
            y4='<td bgcolor="#99ccff" ><a href="%s/%s_%s.all.data" target="dynamic">(data) %s  </a></td> \n' %(ddir,x[0],x[1],sp)
            y5='<td><a href="%s/%s_%s.all.data_rate.png" target="dynamic"> yearly growth rate %s </a></td>\n' %(ddir,x[0],x[1],sp)
            y6='<td bgcolor="#99ccff" ><a href="%s/%s_%s.all.data" target="dynamic">(data) %s  </a></td> \n' %(ddir,x[0],x[1],sp)
            fw.write(''.join([y1, y2, y3, y4, y5, y6]))
            fw.write('</tr>\n')
        
        
        
    fw.write('\n<hr> \n')

    
    fw.write('<p> <h3> Other statistics </h3> \n')
    s2='PDB growth and prediction of the growth in next five years'
    y1='<a href="%s/pdb_growth.txt_acum.data.png" target="dynamic">%s %s</a> \n' %(ddir,s2,sp)
    y2='<a href="%s/pdb_growth.txt_acum.data" target="dynamic"> (plot data) </a> \n'%(ddir)
    fw.write(y1+y2)


    s2 = '<p> Population of resolution with different entities' 
    y1='<a href="%s/resolution_entity.png" target="dynamic">%s %s</a> \n' %(ddir,s2,sp)
    y2='<a href="%s/resolution_entity.data" target="dynamic"> (plot data) </a> \n' %(ddir)
    fw.write(y1+y2)


    s2 = '<p> R_factor (different resolution groups) change in each year. ' 
    y1='<a href="%s/rfact_reso_growth.all.data.png" target="dynamic">%s %s</a> \n' %(ddir,s2,sp)
    y2='<a href="%s/rfact_reso_growth.all.data" target="dynamic"> (plot data) </a> \n' %(ddir)
    fw.write(y1+y2)

    s2 = '<p> Resolution (different data ranges) change in each year. '
    y1='<a href="%s/rfact_reso_growth.all_res.data.png" target="dynamic">%s %s</a> \n' %(ddir,s2,sp)
    y2='<a href="%s/rfact_reso_growth.all_res.data" target="dynamic"> (plot data) </a> \n' %(ddir)
    fw.write(y1+y2)



    
    fw.write('\n<hr> </body>\n</html>\n')
    fw.close()
    

######################################################################
def data_pop(fpop, fp, shell, col):
    '''get the data populations using the COL of the list FP
    '''
    
    nt=len(fp)
    if nt==0: return
    
    fw=open(fpop,'w')
    fp.sort(key=lambda y: y[col])  #sort fp by the col
    s1='#data_range  avg_bin   entry_number  percentage\n'
    print(s1)
    fw.write(s1)
    
    nstep=len(shell)
    j=0
    nnt=0
    for i in range(nstep):
        if i==0: continue
        bin=(shell[i-1] + shell[i])/2.0
        n=0
        for k in range(j, nt):
            if fp[k][col]>shell[i]:
                j=k
                break
            elif shell[i]>fp[k][col]>=shell[i-1]:
                n=n+1
                nnt=nnt+1
        
        p=100*float(n)/nt
        print('pop:  "%8.2f %8.2f" %8.2f  %5d %6.1f ' %( shell[i-1], shell[i],bin, n, p))
        fw.write('"%.2f %.2f" %8.2f  %5d %6.1f \n' %( shell[i-1], shell[i],bin, n, p))
        
    fw.close()
    print('selected data (%s)= %d  %d ' %(fpop, nt, nnt))

######################################################################
def data_corr(fcorr, fp, shell, col):
    '''get data correlations for any item with resolution
    fp: contains a list of pdbid, date, 00, item1, item2
    '''
    
    fw=open(fcorr,'w')
    fp.sort(key=lambda y: y[col])
    
    nt=len(fp)
    nstep=len(shell)
    j=0
    s1='#data_range  avg_bin  number  mean  deviation  minimum  maximum\n'
    print(s1)
    fw.write(s1)
    for i in range(nstep):
        if i==0: continue
        
        bin=(shell[i-1] + shell[i])/2.0
        n, subg = 0, []
        for k in range(j, nt):
            if fp[k][col]>shell[i]:
                j=k
                break
            elif shell[i]>fp[k][col]>=shell[i-1]:
                subg.append(fp[k][col+1])  #data after resolution
                n=n+1
                
        if len(subg):
            avg, dev, mini, maxi = util.mean_dev(subg,-1)
            print('corr: "%8.2f %8.2f" %8.2f %5d %8.3f %8.3f %8.3f %8.3f' %(shell[i-1], shell[i], bin, n, avg, dev, mini,maxi))
            fw.write('"%.2f %.2f" %8.2f %5d %8.3f %8.3f %8.3f %8.3f\n' %( shell[i-1], shell[i], bin, n, avg,dev, mini,maxi))
            
    fw.close()
    

######################################################################
def clean_data(infile, idd):
    '''infile has 3 columns (pdbid, resolution, items)
    idd=0: Do not clean data, idd==1: remove data with non-values
    it returns a list with proper values
    '''
    
    print('Cleaning data (%s).'%infile)
    data=[]
    fp=open(infile, 'r')
    c1,c2=1, 2 # change if other columns 
    for x in fp:
        if 'structure' in x : continue
        t=x.strip().split()
        n=len(t)
        if not util.is_number(t[1]) or (n>2 and not util.is_number(t[2])):
            print('Error: value of (%s) is not a number.' %x)
            continue
        if idd==0:
            if n==2:
                data.append([t[0], float(t[1])])
            elif n==3:
                data.append([t[0], float(t[1]), float(t[2])])
        else:
            if n==2:
                if float(t[1])!=0.0 :  data.append([t[0], float(t[1])])
            elif n==3:
                if float(t[1])!=0.0 and float(t[2])!=0.0 : 
                    data.append([t[0], float(t[1]), float(t[2])])
            
    fp.close()
    
    return data

######################################################################
def filter_data(data_in, shell, col):
    '''filter the data according to the shell & col values. 
    '''

    data_new, outlier = [],[]
    for x in data_in:
        if x[col]<shell[0] or  x[col]>shell[-1]:
            outlier.append([x[0], x[col]])
        else:
            data_new.append(x)
            
    return  data_new, outlier
    
######################################################################
def data_bin(lowv,upv,nstep):
    '''Use the low and upper values and the nsteps to get a list
    '''
    shell=[]
    if nstep ==0: return shell
    d=(upv - lowv)/float(nstep)
    a=lowv
    for x in range(1,nstep+1):
        shell.append(a)
        a=lowv+d*x

    return shell

######################################################################
def plot_entity(ddir):
    '''plot the entity
    '''
    
    out='entity_data.all'
    items=['formula_weight', 'id', 'type', 'ndb_number_of_molecules ']
    do_sql('entity', items, out)

    items=[
        ['entity', 'water-weight-in-ASU' , 1, 60, 50000, 20],
        ['entity', 'polymer-weight' , 1, 200, 100000, 30],
        ['entity', 'non-polymer-weight' , 1, 10, 1500, 25],
        ['entity', 'total-weight-in-ASU' , 1, 400, 600000, 30],
    ]
    
    data_all=from_file_to_list(out)
    data_water=[['structure_id', 'ls_d_res_high', 'water-weight-in-ASU']]
    data_poly=[['structure_id', 'ls_d_res_high','polymer-weight']]
    data_nonpoly=[['structure_id', 'ls_d_res_high','non-polymer-weight']]
    data_allw=[['structure_id', 'ls_d_res_high','total-weight-in-ASU']]
    nt=len(data_all)
    sm=0
    for i, x in enumerate(data_all):
        
        if 'structure_id' in x[0]:
            continue
        elif 'water' == x[4]:
            wat=float(x[2]) * float(x[5])
            data_water.append([x[0], float(x[1]), wat])
        elif 'non-polymer' == x[4]:
            data_nonpoly.append([x[0], float(x[1]), float(x[2])])
        elif 'polymer' == x[4] :
            data_poly.append([x[0], float(x[1]), float(x[2])])
            
        sm=sm + float(x[2]) * float(x[5])
        if i<nt-1 and x[0] not in data_all[i+1][0]:
            data_allw.append([x[0], float(x[1]), sm])
            sm=0
    
    for x in items: #
                
        data_all=[]
        if x[1]=='water-weight-in-ASU':
            data_all = data_water
        elif x[1]=='non-polymer-weight':
            data_all = data_nonpoly
        elif x[1]=='polymer-weight':
            data_all = data_poly
        elif x[1]=='total-weight-in-ASU':
            data_all = data_allw
        print(x)    
        if not data_all: continue   
        plot_pop(ddir, x, data_all)
        plot_corr(ddir, x, data_all)

    
######################################################################
def twin_info(ddir):


    pdbrev=['database_PDB_rev', 'structure_id', 'date_original']
    twin=['pdbx_reflns_twin', 'fraction' ]
    refine=['refine', 'ls_d_res_high','ls_R_factor_R_work']
    sym=['symmetry', 'space_group_name_H_M']

    tabs=[pdbrev, twin, refine, sym]
    outf='twin-data.all'
    #do_sql_gen(outf, tabs, 'x-ray')
    rawdata=from_file_to_list(outf)

    data1=[]
    for x in rawdata:
        if 'structur' in x[0]: continue
        s='_'.join(x[6:])
        data1.append([x[1][:4] , x[4], x[5], s])

    data2 = uniq_list_of_list(data1)
    data=[]
    for x in data2:
        ss=[x[0], x[3], float(x[1]), float(x[2])]
        data.append(ss)
        print(ss)
        
    shell=data_bin(0.6, 5.0, 20)   #data change with resolution
    fcorr= 'twin_res.data'
    data_corr(fcorr,data, shell, 2)

    fyear='twin_year_growth.data'
    fw=open(fyear,'w')
    data3=uniq_string_pop(data, 0)
    for x in data3:
        s=' '.join([x[0], '%.1f'%x[1], '%.1f'%x[2]] ) + '\n'
        fw.write(s)
        print(s)
    fw.close()
        

    for x in data3: print (x)
    
    data4=uniq_string_pop(data, 1)
    for x in data4: print (x)
    
    

######################################################################
def uniq_list_of_list(data):
    '''get uniq list 
    '''
    data_new=[]
    for x in data:
        if x not in data_new:  data_new.append(x)
        
    return data_new
######################################################################
def rfact_reso_growth(ddir):
    '''test the mean resolution change with year
    '''
    
    out='%srfact_reso_growth.all' %ddir
    
    plot_data=out + '.data'
    plot_data1=out + '_res.data'
    fw = open(plot_data,'w')
    fw1 = open(plot_data1,'w')
    
    arg='''mysql -u rcsbuser -prcsb0000 -h pdb-a-linux-9 cleanv1 -e " \
select distinct  d.structure_id, d.date_original , r.ls_d_res_high ,  \
r.ls_R_factor_R_work from database_PDB_rev as d , refine as r \
where d.num=1 and d.structure_id = r.structure_id and r.ls_R_factor_R_work != '' \
and r.structure_id in (select pdb_id from pdb_entry  where method like '%%x-ray%%' \
and status_code='REL' and method !='THEORETICAL MODEL')  \
order by d.date_original,  r.ls_d_res_high \
">%s
''' %(out)
    os.system(arg)
    data1=from_file_to_list(out)
    dic={}

    reso=[0, 1.5, 2, 2.5, 3.0,5.0]

    s='#year  (0.0->1.5) dev (1.5->2.0) dev (2.0->2.5) dev (2.5->3.0) dev (3.0->4.0) dev '
    print(s)
    
    fw.write(s+'\n')
    
    
    for i in range(2000, 2013):
        n=0
        rf=[]
        for x in data1[:]:
            if 'structure_id' in x : continue
            if str(i) in x[1] :   
                n=n+1
                rf.append([float(x[3]), float(x[4])])
            elif str(i) not in x[1] and n>0:
                break
            
        nrf=len(rf)
        
        tmp=['.','.  . ','.  .','.  . ','.  .','.  .']
        tmp1=[0,0,0,0,0,0]
        if rf:
            for k, z in enumerate(reso):
                if k==0: continue
                t1=[]
                ns=0
                for y in rf:
                    if reso[k-1]<= y[0] <reso[k]:
                        t1.append([y[1]])
                        ns=ns+1

                avg, dev=-1.0,-1.0
                if t1:
                    avg, dev, mini, maxi = util.mean_dev(t1,0)
                    tmp[k]= '%.3f %.3f ' %(avg, dev)
                    
                    p1=100*float(ns)/nrf
                    tmp1[k]= '%.2f ' %(p1)
           
                    s1='(%.2f->%.2f)  %.3f %.3f  %d' %(reso[k-1],reso[k], avg, dev, len(t1))
                    s2='%d  (%.2f->%.2f) %d  %d  %.2f' %(i, reso[k-1],reso[k], ns,nrf, p1)
                 #   print(s2)


              #  print(k, z, t1,avg, dev)
            ss='%d %s  %s %s %s %s ' %(i, tmp[1], tmp[2],tmp[3],tmp[4],tmp[5])
            print(ss)
            fw.write(ss +'\n')
#            ss1='%d %.2f %.2f %.2f %.2f %.2f \n' %(i, tmp1[1], tmp1[2],tmp1[3],tmp1[4],tmp1[5])
            ss1='%d %s  %s %s %s %s \n' %(i, tmp1[1], tmp1[2],tmp1[3],tmp1[4],tmp1[5])
            fw1.write( ss1)
        dic[i]=rf
    
    fw.close()
    fw1.close()
    
    title = 'The mean Rfactors change with year' 
    xrange,yrange,xlabel,ylabel = '', '', 'Year' ,'R_work'
    bar, rot, key, style = 0, 1, 2, 1
    plot = """plot '%s' using 2:xtic(1) t "reso: 0.0->1.5" , \
        '' u 4 t "reso: 1.5->2.0" , '' u 6 t "reso: 2.0->2.5", \
        '' u 8 t "reso: 2.5->3.0" , '' u 10 t "reso: 3.0->4.0"  \
        """ %(plot_data)
        
    gnuscr, gnuout = gnu_plot(plot_data,title,xrange,yrange,xlabel,ylabel
                              ,bar,rot,key,style,plot)
    

    
    title = 'The mean reasolutino change with year' 
    xrange,yrange,xlabel,ylabel = '', '', 'Year' ,'resolution'
    bar, rot, key, style = 0, 1, 2, 1
    plot = """plot '%s' using 2:xtic(1) t "reso: 0.0->1.5" , \
        '' u 3 t "reso: 1.5->2.0" , '' u 4 t "reso: 2.0->2.5", \
        '' u 5 t "reso: 2.5->3.0" , '' u 6 t "reso: 3.0->4.0"  \
        """ %(plot_data1)
        
    gnuscr, gnuout = gnu_plot(plot_data1,title,xrange,yrange,xlabel,ylabel
                              ,bar,rot,key,style,plot)
    

######################################################################
def get_items_str():
    '''The format of the items must be fixed for the data base.
    col_1, col_2: the cif category, the cif item
    col_3: if 'x-ray', only get XRAY; if 'all', include all method
    col_4,5,6,7,8: if given, manual contral the first five strings
    '''
    items=[
        ['start:string', '', '', ''],
        
        ['computing', 'rcsb_data_reduction_ii', 'x-ray', 'DENZO', 'HKL', 'MOSFLM', 'XDS/XSCALE', 'D*TREK/DTREK'],
        ['computing', 'rcsb_data_reduction_ds', 'x-ray', 'SCALEPACK', 'HKL', 'SCALA', 'XDS/XSCALE', 'D*TREK/DTREK'],
        ['computing', 'structure_refinement', 'x-ray', 'REFMAC', 'PHENIX', 'BUSTER', 'SHELX','CNS/X-PLOR' ],
        ['computing', 'structure_solution', 'x-ray', 'PHASER', 'CNS/X-PLOR', 'MOLREP', 'SOLVE', 'AMORE'],
        ['computing', 'ndb_structure_refinement_method', 'x-ray', '', '', '', '', ''],
        
        ['refine', 'ndb_method_to_determine_struct', 'x-ray', 'MOLECULAR_REPLACEMENT/MR', 'SAD/SIRAS', 'MAD/MIRAS', 'MIR/MULTIPLE_ISOMORPHOUS_REPLACEMENT', 'AB_INITIO/DIRECT_METHOD'],
        
        ['diffrn_detector', 'detector', 'x-ray', 'CCD', 'IMAGE_PLATE', 'AREA_DETECTOR', 'PIXEL', 'FILM'],
        ['diffrn_detector', 'type', 'x-ray', 'MARRESEARCH/MAR', 'ADSC', 'RIGAKU', 'SIEMENS', 'PSI_PILATUS'],
        
        ['diffrn_source', 'source', 'x-ray', '', '', '', '', ''],
        ['diffrn_source', 'type', 'x-ray', '', '', '', '', ''],
        
        ['symmetry', 'space_group_name_H_M', 'x-ray', '', '', '', '', ''],
        
        ['exptl', 'method', 'all', '', '', '', '', ''],
        
        ['end:string', '', '', ''],
        
    ]
    return items

######################################################################
def do_string_stat(ddir):
    '''The function is to do populations for string
    (date is from database_PDB_rev   fixed)
    '''
    
    pdbrev=['database_PDB_rev', 'structure_id', 'date_original']
    items=get_items_str()
    
    for x in items:
        print(x)
        if 'start:' in x[0] or  'end:' in x[0]: continue
        tabs=[pdbrev, [x[0], x[1]]]
        outf='%s%s_%s.all' %(ddir, x[0], x[1])
        do_sql_gen(outf, tabs, x[2])
        first5, file1, file2 = string_stat(outf, x)

        title = 'The population of %s.%s' %(x[0], x[1])
        xrange,yrange,xlabel,ylabel = '', '', 'Year' ,'PDB entry'
        bar, rot, key, style = 0, 1, 0, 0
        plot = """plot '%s' using 2:xtic(1) lc rgb "green" , \
        '' u 0:2:3 with labels offset 0, 0.5 """ %(file1)
        
        gnuscr, gnuout = gnu_plot(file1,title,xrange,yrange,xlabel,ylabel
                                  ,bar,rot,key,style,plot)

        title = 'Growth of %s.%s' %(x[0], x[1])
        xrange,yrange,xlabel,ylabel = '', '', 'Year' ,'PDB entry'
        bar, rot, key, style = 0, 1, 2, 0
        plot = """plot '%s' using 2:xtic(1) t "%s" ,'' u 4 t "%s" ,'' u 6 t "%s"  \
        ,'' u 8 t "%s" , '' u 10 t "%s" \
        """ %(file2,first5[0], first5[1], first5[2], first5[3], first5[4])
        gnuscr, gnuout = gnu_plot(file2,title,xrange,yrange,xlabel,ylabel,
                                  bar,rot,key,style,plot)


        title = 'Growth rate of %s.%s' %(x[0], x[1])
        xrange,yrange,xlabel,ylabel = '', '', 'Year' ,'percentage (%)'
        bar, rot, key, style = 0, 1, 2, 0
        plot = """plot '%s' using 3:xtic(1) t "%s" ,'' u 5 t "%s" ,'' u 7 t "%s"  \
        ,'' u 9 t "%s" ,'' u 11 t "%s" \
        """ %(file2,first5[0], first5[1], first5[2], first5[3], first5[4])
        file3=file2+'_rate'
        gnuscr, gnuout = gnu_plot(file3,title,xrange,yrange,xlabel,ylabel,
                                  bar,rot,key,style,plot)



######################################################################
def uniq_string_pop(data1, col):
    '''get unique string populations
    data: a list,  col: the column that contains the string
    '''
    
    data1.sort(key=lambda y: y[col])
    nnt=len(data1)  #accumulate the unique strings
    n,data2=0,[] 
    for i,x in enumerate(data1):
#        print(i, col,x)
        if i== nnt-1 or (i<nnt-1 and data1[i][col] != data1[i+1][col]):
            pn=100*float(n)/nnt
            data2.append([x[col], n, pn])
            n=0
        n=n+1
    data2.sort(key=lambda y: y[col])

    return data2
    
######################################################################
def string_stat(outf,prog):
    '''This is a general stat for string (plot population in order), growth and
    growth rate.
    outf contains more than 3 columns (id, date1, 0000 ..)
    prog is the list (column 4,5,6,7,8 contains programs)
    
    '''
    
    fp=open(outf, 'r')
    data1=[]  #remove null values
    for x in fp:
        t=x.split()
        if 'structure_id' in x or len(t)<=3: continue
        s='_'.join(t[3:])
        data1.append([t[1][:4], s.upper()])
    fp.close()
    data1.sort(key=lambda y: y[1])

    data2=uniq_string_pop(data1, 1) #accumulate the unique strings
    data2.reverse()
    
    plot_data1 = outf + '_pop.data'
    fw=open(plot_data1, 'w')
    fw.write('# unique-intem  number-of-entry  percentage (n/n_total_per_year)\n')
    for i, x in enumerate (data2):
        s= '    ' .join([str(y) for y in x]) + '\n'
        fw.write(s)
        print(s.strip())
        if i>25: break
    fw.close()    
    

    first5=[]  #plot the first top 5 string (programs)
    if len(prog[3]) and len(prog[4]):
        first5 = [prog[3], prog[4], prog[5], prog[6], prog[7]]
    else:
        for i in range(5): first5.append(data2[i][0])
    print('using ', first5, ' for yearly growth')
    
    
    plot_data2 = outf + '.data'
    fw=open(plot_data2, 'w')
    s ='#Year  ' +  '    '.join([' %s rate ' %x for x in first5])
    print(s)
    fw.write(s + '\n')
    
    for i in range(1994, 2013):
        num=[]
        for y in first5:
            
            n, pn,ny=0,0,0
            for x in data1:
                
                if i == int(x[0]) :
                    ny=ny+1
                    if len(y)>2 :
                        if '/' in y:
                            tt1=y.split('/')
                            if tt1[0] in x[1] or tt1[1] in x[1]: n=n+1
                        else:
                            if y in x[1] : n=n+1
                            
#                    if y==x[1] :
                        
            if ny>0 : pn=100*float(n)/ny
            num.append(  n  )     
            num.append(  '%.1f' %pn )     
            #print(i, y, n, ny)

                    
        ss= '%d  ' %i + '   '.join([str(x) for x in num])
        print(ss)
        fw.write(ss + '\n')

    
    fw.close()
    
    return  first5, plot_data1,  plot_data2

######################################################################
def do_reso_entity(ddir):
    sql='mysql -u rcsbuser -prcsb0000 -h pdb-a-linux-9 cleanv1 -e '
    xray_id="select pdb_id from pdb_entry  where \
    method like '%x-ray%' and status_code='REL' and method !='THEORETICAL MODEL'"
    
    
    four = '''%s "select  r.structure_id,  r.ls_d_res_high from refine as r where  \
r.structure_id  in ( select structure_id from entity_poly where lcase(type) like '%%polypeptide%%' ) \
and r.structure_id not in (select structure_id from entity_poly where lcase(type) like '%%polyribo%%' ) \
and r.structure_id not in (select structure_id from entity_poly where lcase(type) like '%%polydeoxy%%' ) \
and r.structure_id in (%s) order by r.ls_d_res_high \
">protein_reso.list


%s "select  r.structure_id,  r.ls_d_res_high from refine as r where  \
r.structure_id  in ( select structure_id from entity_poly where lcase(type) like '%%polyribo%%' ) \
and r.structure_id not in (select structure_id from entity_poly where lcase(type) like '%%polypeptide%%' ) \
and r.structure_id not in (select structure_id from entity_poly where lcase(type) like '%%polydeoxy%%' ) \
and r.structure_id in (%s) order by r.ls_d_res_high \
">rna_reso.list


%s "select  r.structure_id,  r.ls_d_res_high from refine as r where  \
r.structure_id  in ( select structure_id from entity_poly where lcase(type) like '%%polydeoxy%%' ) \
and r.structure_id not in (select structure_id from entity_poly where lcase(type) like '%%polypeptide%%' ) \
and r.structure_id not in (select structure_id from entity_poly where lcase(type) like '%%polyribo%%' ) \
and r.structure_id in (%s) order by r.ls_d_res_high \
">dna_reso.list


%s "select  r.structure_id,  r.ls_d_res_high from refine as r where  \
(r.structure_id  in ( select structure_id from entity_poly where lcase(type) like '%%polydeoxy%%' ) \
or r.structure_id in (select structure_id from entity_poly where lcase(type) like '%%polyribo%%' )) \
and r.structure_id in ( select structure_id from entity_poly where lcase(type) like '%%polypeptide%%' ) \
and r.structure_id in (%s) order by r.ls_d_res_high \
">protein_na_reso.list


''' %(sql, xray_id,sql, xray_id, sql, xray_id,sql, xray_id)

    #print (four)

    os.system(four)
    
    shell=data_bin(0.7, 4.8, 13)   #data change with resolution
    four=['protein_reso.list', 'protein_na_reso.list', 'rna_reso.list', 'dna_reso.list']
    s1=' '.join(four)
    os.system('cat %s > %s/resolution_entity.data' %(s1, ddir))
    
    res, dv=[],[]
    col=1  #data is in this column
    for x in four:
        data_clean = clean_data(x, col)
        data, outlier = filter_data(data_clean, shell, col)
        fpop=  x + '_pop.data'   #for data populations
        data_pop(fpop, data, shell, col)
        avg, dev, mini, maxi = util.mean_dev(data,col)
#        print(avg, dev, mini, maxi)

        res.append(avg)
        dv.append(dev)

    title = 'Population of resolution with different entity' 
    xrange,yrange,xlabel,ylabel = '', '','resolution' , 'percentage' 
    bar, rot, key, style = 0, 1, 1, 1 
    plot = """plot '%s_pop.data' using 4:xtic(1) t "protein (mean=%.2f, dev=%.2f)" , \
    '%s_pop.data' u 4:xtic(1) t "protein-NA (mean=%.2f, dev=%.2f)" ,  \
    '%s_pop.data' u 4:xtic(1) t "RNA (mean=%.2f, dev=%.2f)", \
    '%s_pop.data' u 4:xtic(1) t "DNA (mean=%.2f, dev=%.2f)" """ \
    %(four[0], res[0],dv[0], four[1], res[1],dv[1], four[2],res[2], dv[2], four[3],res[3],dv[3])

    fpop= ddir + 'resolution_entity'
    
    gnuscr, gnuout = gnu_plot(fpop,title,xrange,yrange,xlabel,ylabel,bar,rot,key,style,plot)
    
       
######################################################################
def fast_sort(file_in, k1,k2):
    '''fast sort; k1 column for string, k2 column for number.
    '''
    out=file_in + '.sorted'
    arg='sort -k %d,%d -k %d,%dn %s > %s' %(k1, k1, k2,k2, file_in, out)
    os.system(arg)
    return out

######################################################################
def sort_multi_column(file_in):
    file_in='tt' 
    fp=open(file_in, 'r').readlines()
    fp.sort(key=lambda y: y[0])
    print('puting it to dic')
    dic={}
    for x in fp:
        t=x.split()
        if t[0] not in dic.keys(): dic[t[0]]=[]
        if t[0] in dic.keys():
            dic[t[0]].append([t[1],t[2]])

    print('printting')


     
    keys=dic.keys()
    keys.sort()
    for x in keys:
	dic[x].sort(key=lambda y: y[1])
	for m in dic[x]:
            print(x, m)
    
        
######################################################################
def auto_pop_corr(ddir):
    '''auto plot population or correlation of  item1 & item2
    '''
    
    item1,item2='refine.ls_d_res_high' , 'refine.ls_R_factor_R_work'

    sql = 'mysql -u rcsbuser -prcsb0000 -h pdb-a-linux-9 cleanv1 -e '
    t=item1.split('.')
    cate1, token1 = t[0], t[1]
    n2=len(item2)
    if n2:
        t=item2.split('.')
        cate2, token2 = t[0], t[1]

    outf=cate1 + '.all'
    yy="x1.structure_id in (select pdb_id from pdb_entry where  method like '%x-ray%') " + \
       "and x1.structure_id in (select pdb_id from pdb_entry where status_code='REL' " + \
       "and method !='THEORETICAL MODEL'  "

    if n2:
        y1= '"select distinct x1.structure_id , %s  '%item1
        y2= 'from %s as x1 ' %cate1
        y3='where %s' %yy
        y4='order by  x1.%s  " >%s' %(token1,outf)
    else:
        y1= '"select distinct x1.structure_id , %s,  %s '%(item1,item2)
        y2= 'from %s as x1 %s as x2 ' %(cate1,cate2)
        y3='where x1.structure_id = x2.structure_id and %s' %yy
        y4='order by  x1.%s  " >%s' %(token1,outf)
        

    s=''.join([sql, y1,y2,y3,y4])
    print (s)
    os.system(s)
   

######################################################################
def gnufit(ddir, idd):
    '''fit the data by equation
    if the data is given, data must be two columns (1st, year; 2,growth)
    if data is not given, use the database.
    '''
    
    out, data = pdb_growth(1976,2013)

    fp=open(data,'r').readlines()
    d=[x for x in fp  if len(x)>1]
    
    x0=int(d[0].split()[0])  #first year
    xf=int(d[-1].split()[0]) #last year 
    x0_fit, xf_fit=2000,2011    #used to fit data 
    a,b,c = fitted(data,x0_fit,xf_fit, idd)
    pout=predict(data, a, b, c, x0_fit, xf, idd)

    eq='f(x)=2024.76*((x-2000)**1.443) + 13877.3'
    title = 'The PDB growth and prediction (by %s).' %(eq)
    xrange,yrange,xlabel,ylabel = '', '', 'Year' ,'PDB entry'
    bar, rot, key, style = 0, 1, 1, 1 
    plot = """plot '%s' using 1:2:xtic(1) t  "deposited" ,'' u 1:3 t "predicted" """ %(pout)


    gnuscr, gnuout = gnu_plot(pout,title,xrange,yrange,xlabel,ylabel,bar,rot,key,style,plot)

    os.system('mv pdb_growth.txt_acum.* %s' %(ddir))
    util.delete_file('pdb_growth.txt_acum__tmp*')
    
    

######################################################    
def fitted(datain,x0,xf, idd):
    ''' fit the equation by the data (two columns; 1: year, 2:data)
    idd=1: fit (a,b,c) for Polynomial  f(x) = a*(x-x0)**b + c
    idd=2: fit (a,b,c) for Exponential f(x) = a*exp(b*(x-x0)) + c
    x0, xf: the start & end data range used for fitting
    '''

    data=datain + '__tmp'
    fw=open(data,'w')
    for x in open(datain, 'r').readlines():
        t=x.split()
        if int(t[0])<x0 or int(t[0])>xf: continue
        fw.write(x)
    fw.close()

    fit=data + '_fit'
    fw=open(fit,'w')
    if idd==1:
        fw.write('f(x)=a*((x-%d)**b) + c \n' %x0)
        fw.write('a=105; b=1.5;  c=1000; \n' ) #initial values (adjust)
    elif  idd==2:
        fw.write('f(x)=a*exp(b*(x-%d)) + c \n' %x0)
        fw.write('a=303.995; b= 0.51;  c=-100.165463;  \n' )
        
    fw.write('fit f(x) "%s" u 1:2 via a, b, c \n' %data)
    fw.close()

    log=data+'_fit.log'
    arg= 'gnuplot  %s >& %s' %(fit, log)
    os.system(arg)
    
    util.delete_file('fit.log')
#    print(x0,xf,d)

    a, b, c, da,db,dc = 0,0,0,0,0,0
    fp = open(log,'r').readlines() #get fitted values from log
    for x in fp:
        if 'a' in x[:3] and '+/-' in x[30:45] and '(' in x [49:]:
            t=x.split()
            a, da =float(t[2]), float(t[4])
        elif 'b' in x[:3] and '+/-' in x[30:45] and '(' in x [49:]:
            t=x.split()
            b, db =float(t[2]), float(t[4])
        elif 'c' in x[:3] and '+/-' in x[30:45] and '(' in x [49:]:
            t=x.split()
            c, dc =float(t[2]), float(t[4])
            
    print('fitted values using data (%d->%d) a=%.4f  da=%.4f, b=%.4f db=%.4f, c=%.4f dc=%.4f' %(x0,xf, a, da, b, db, c, dc))
    return a, b, c
 
############################################################
def  predict(data, a, b, c, x0, xf, idd):
    '''
    '''

    pout = data + '.data'
    fw=open(pout, 'w')
    
    year=range(1976, xf+6) #get data 5 year more
    fr=open(data,"r").readlines()
    print ("Year  Deposited  Predicted  Accuracy(%)")
    fw.write("Year  Deposited  Predicted  Accuracy(%)\n")

    t1=0
    for x in fr:
        if 'year' in x : continue
        t=x.strip().split()
        t1,t2=int(t[0]),int(t[1])
        if t1 < x0 :
            print("%4d %6d   ?      ? "% (t1,t2))
            fw.write("%4d %6d   ?      ? \n"% (t1,t2))
        else:
            y = fiteq(a, b, c,  t1, x0, idd)
            percent=100*math.fabs(t2-y)/t2
            print("%4d %6d %6d   %.1f  " % (t1, t2, y, percent))
            fw.write("%4d %6d %6d   %.1f  \n" % (t1, t2, y, percent))
    if xf+6>=t1+1:
        for x in range(t1+1, xf+6):
            y = fiteq(a, b, c,  x, x0, idd)
            print("%4d     ?  %6d   ?  " % (x, y))
            fw.write("%4d     ?  %6d   ?  \n" % (x, y))

    fw.close()

    return pout

            
############################################################
def fiteq(a, b, c,  x, x0, idd):
    '''fited equation
    '''

    y=0
    if idd==1 :
        y=a*((x - x0)**b) + c
    elif idd==2 :
        y=a*math.exp(b*(x-x0)) + c
        
    return y


############################################################
def pdb_growth(start,end):
    '''get growth of PDB using sql
    '''

    out='pdb_growth.txt'
    sql = 'mysql -u rcsbuser -prcsb0000 -h pdb-a-linux-9 cleanv1 -e '
    
    scr = '''%s \
"select year(r.date), count(d.pdb_id) from pdb_entry_tmp d, database_PDB_rev r \
where r.structure_id = d.pdb_id and r.date >='%d' and r.date <='%d' \
and r.num=1  and d.method!='theoretical model' and d.status_code ='REL'  \
group by year(r.date)" >%s \
    ''' %(sql, start,end,out)
    
#    print(sql, start,end,out, scr)
    os.system(scr)

    out_acum = out +'_acum'
    fp = open(out, 'r')
    fw = open(out_acum, 'w')
    n=0
    for x  in fp:
        if 'year' in x : continue
        t=x.split()
        year, val = int(t[0]), int(t[1])
        n=n+val
        fw.write('%4d  %6d\n' %(year, n))
        
    fw.close()

    return out, out_acum

############################################################
def gnu_plot(datafile,title,xrange,yrange,xlabel,ylabel,bar,rot,key,style,plot):
    '''some head infor for gnuplot (one data set plot by default)
    bar>0: add error bar on the histogram
    rot>0, xlabel rotation;
    key=0: key>0, on;  key=2,left;
    style=0, histogram ; =1 linepoints; =1, points; =3 dot
    
    '''

    gnuscr=datafile + '.gnu'
    gnuout=datafile + '.png'
    fw=open(gnuscr, 'w')

    x1='set terminal  png large size 1000,740 # 840,640\n'
    x2="set output '%s'\n" %gnuout
    fw.write(x1+x2)
    if(style==0):  #histogram
        fw.write("set boxwidth 0.5 relative\n")
        fw.write("set style histogram clustered gap 1 title offset 0, 0, 0\n")
        fw.write("set style data histograms\n")
        if bar : fw.write("set style histogram errorbars\n")
    elif (style==1): #line
        fw.write("set style data linespoints\n")
    elif (style==2): #point
        fw.write("set style data points\n")
        fw.write("set pointsize  1\n")
    elif (style==3): #dot
        fw.write("set style data dots\n")
        fw.write("set pointsize  1\n")


    if(len(xrange)>1) : fw.write("set xrange %s\n" %xrange)
    if(len(yrange)>1) : fw.write("set yrange %s\n" %yrange)
    
    fw.write('set title "%s" \n' %title)
    fw.write("set datafile missing '.'\n")
    fw.write("set style fill  solid 1.0 border -1\n")
    
    if(key==0):
        fw.write("set key off\n")
    else:
        fw.write("set key on\n") 
        if(key==2): fw.write("set key reverse left Left\n")
    
    fw.write("set grid ytics\n")
    fw.write("set size 1.0,1.0\n")
    fw.write("set autoscale\n")
    
    if (rot>0):
        fw.write("set xtics rotate by 90 \n")
    else:
        fw.write("set xtics\n")
        
    fw.write("set ytics\n")
   
    
    if(len(xlabel)>0):
        if(rot>0):
            fw.write('set xlabel "%s" offset 0, -1, 0\n' %xlabel) #offset xlabel down -1
        else:
            fw.write('set xlabel "%s" offset 0, 0, 0\n' %xlabel)
    else:
        fw.write('set xlabel " " \n')
    
    
    if(len(ylabel)>0):
        fw.write('set ylabel "%s" \n' %ylabel)
    else:
        fw.write('set ylabel " " \n')
    
    fw.write("set colorbox vertical origin screen 0.9, 0.2, 0 size screen 0.05, 0.6, 0 bdefault\n")
        
    fw.write(plot)
       

    fw.write("\n# memo: to plot error bar, use the following line\n")
    fw.write("# plot 'filename'   using 1:2:3:xtic(1) t \"all\" with  yerrorlines, '' u 1:4:5 t \"altered\" with yerrorlines\n")
    
    
#    fw.write("set term x11\nreplot \npause 4\n")
    
    fw.close()
    os.system('/bin/csh -c "gnuplot %s" ' %gnuscr) #if not given /bin/csh -c, use B shell

    return gnuscr, gnuout

############################################################



#if __name__ == '__main__':
#    accumulate()
#    predict()
    
    
            
