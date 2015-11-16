delete all
set orthoscopic, on #turn off perspective
set antialias=1
bg_color white
set cartoon_fancy_helices=1
set cartoon_flat_sheets = 1.0
set cartoon_smooth_loops = 0
set ray_trace_mode=0 # draw border or not
set cartoon_side_chain_helper, on  #make side chain stick out of cartoon nicely

cmd.load( "../../4lztSh.pdb", "mypdb")
hide all
select xy, mypdb///1-556/
show cartoon, xy
color blue, xy
color red (resid 1-556)

set_view (\
    -0.101256892,   -0.143091634,   -0.984511316,\
    -0.090036631,    0.986841023,   -0.134170815,\
     0.990772903,    0.075059414,   -0.112807170,\
     0.000000000,    0.000000000, -245.993072510,\
    79.591812134,   51.717029572,   53.738750458,\
   147.524490356,  344.461730957,   20.000000000 )


run arrow.py
cgo_arrow [45,18,10], [45,12,60],0.5, 0.0, -1, -1, blue red
cgo_arrow [45,18,10], [45,60,9]

#~ from pymol.cgo import *
#~ from pymol import cmd
 #~ 
#~ w = 0.06 # cylinder width 
#~ l = 0.75 # cylinder length
#~ h = 0.25 # cone hight
#~ d = w * 1.618 # cone base diameter
 #~ 
#~ obj = [CYLINDER, 0.0, 0.0, 0.0,   l, 0.0, 0.0, w, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
       #~ CYLINDER, 0.0, 0.0, 0.0, 0.0,   l, 0.0, w, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
       #~ CYLINDER, 0.0, 0.0, 0.0, 0.0, 0.0,   l, w, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
       #~ CONE,   l, 0.0, 0.0, h+l, 0.0, 0.0, d, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 
       #~ CONE, 0.0,   l, 0.0, 0.0, h+l, 0.0, d, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 
       #~ CONE, 0.0, 0.0,   l, 0.0, 0.0, h+l, d, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0]
 #~ 
#~ cmd.load_cgo(obj, 'axes')


#~ # zoom on the hetero atom (ligand and not water) within 5 Angstroms
#~ select hh, het and not resn HOH
#~ zoom hh, 5
 #~ 
#~ # turn on depth cueing
#~ set depth_cue, 1
 #~ 
#~ # now, select stuff to hide; we select everything that is 
#~ # farther than 8 Ang from our main selection
#~ select th, (all) and not ( (all) within 8 of hh) )
 #~ 
#~ hide everything, th
