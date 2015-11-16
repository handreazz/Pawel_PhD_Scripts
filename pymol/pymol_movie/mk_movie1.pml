delete all
set matrix_mode, 1
set movie_panel, 1
set scene_buttons, 1
bg_color white
set orthoscopic, on
#viewport 390,390

load 4lstSh_super_cent.pdb, sup
select uc, resi 374-502
select sc, resi 235-373| resi 503-1892
select solv, resn WAT
#load 4lztSh_supersuper.pdb, sup2
#select sc2, sup2 and polymer
#select solv2, sup2 and !polymer


deselect
hide all

#as cartoon, sup
#color blue, sup
#as cartoon, uc
#color blue, uc
#as sticks, solv
#color red, solv
#as cartoon, sc2
#color grey, sc2
#as cartoon solv2
#color grey, solv2

mset 1 x100


show cartoon, uc
color blue, uc
set_view (\
     0.948694050,   -0.028416302,   -0.314912558,\
    -0.006315350,    0.994049847,   -0.108724557,\
     0.316128701,    0.105135284,    0.942874014,\
    -0.000278965,   -0.000342071, -324.629821777,\
   117.531166077,   90.844345093,   44.752410889,\
   243.257308960,  406.016143799,   20.000000000 )
zoom uc, -5
frame 1
scene 001, store
mview store, scene=001
frame 5
mview store, scene=001

turn y, 180
scene 002, store
frame 10
mview store, 10, scene=002

turn y, 180
scene 003, store
frame 20
mview store, 20, scene=003

set_view (\
     0.948694050,   -0.028416302,   -0.314912558,\
    -0.006315350,    0.994049847,   -0.108724557,\
     0.316128701,    0.105135284,    0.942874014,\
     0.000000000,    0.000000000, -324.636688232,\
   137.548156738,  110.860862732,   53.738750458,\
   243.257308960,  406.016143799,   20.000000000 )
scene 004, store
frame 30
mview store, 30, scene=004
frame 40
mview store, 40, scene=004

show cartoon, sc
color blue, sc
scene 005, store
frame 41
mview store, 41, scene=005


scene 006, store
frame 100
mview store, 100, scene=006

mview reinterpolate















#set antialias=1
#set line_smooth = 1.00000
#set depth_cue = 1
#set specular = 1.00000
#set surface_quality = 1.00000
#set stick_quality = 25.00000
#set sphere_quality = 2.00000
#set cartoon_sampling = 14.00000
#set ribbon_sampling = 10.00000
#set ray_trace_fog = 1

#
# rebuild is required to rebuild all objects after changing quality settings
#
#rebuild

#
# this is the ray tracing command - notice it is commented about by a # -
# this is a good idea as you don't want to wait for several minutes for
# PyMol to ray trace your image only to find out you don't quite like the
# color of that second alpha helix!
#
#ray

