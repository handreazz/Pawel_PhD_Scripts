delete all
set orthoscopic, on #turn off perspective
set antialias=1
bg_color white
set cartoon_fancy_helices=1
set cartoon_flat_sheets = 1.0
set cartoon_smooth_loops = 0
set ray_trace_mode=0 # draw border or not

cmd.load( "../../4lztSh.pdb", "mypdb")
hide all
select xy, mypdb///1-139+279-417+557-695+835-973+1113-1251+1391-1529/
show cartoon, xy
color blue, xy
color red (resid 1-139+279-417+557-695+835-973+1113-1251+1391-1529)

set_view (\
     0.999432147,   -0.003605069,    0.033501662,\
     0.010815015,    0.975960314,   -0.217630208,\
    -0.031915426,    0.217873245,    0.975454807,\
     0.000000000,    0.000000000, -234.627639771,\
    79.591812134,   51.717029572,   53.738750458,\
   136.159057617,  333.096405029,   20.000000000 )


run arrow.py
cgo_arrow [45,25,0], [100,25,0],0.5, 0.0, -1, -1, blue red
cgo_arrow [45,25,0], [36.5,60,0]

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
