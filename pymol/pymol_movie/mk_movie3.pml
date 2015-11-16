# more movies in /home/pjanowsk/c/Case/pymol_movie
delete all
set matrix_mode, 1
set movie_panel, 1
set scene_buttons, 1
bg_color white
set orthoscopic, on
viewport 800,600

load 4lstSh_super_cent.pdb, sup
select uc, resi 374-502
select sc, resi 235-373| resi 503-1892
select solv, resn WAT
load 4lztSh_bigsupernew.pdb, sup2
select sc2, sup2 and polymer
select solv2, sup2 and resn WAT
deselect
hide all

mset 1 x800
set_color lblue= [63  , 133  , 223 ]
set_color orange=[204,102,0]

show cartoon, uc
color orange, uc
scene 001, store

show cartoon, sc
color orange, sc
scene 002, store

as sticks, solv
color lblue, solv
scene 003, store

show cartoon, sc2
color grey, sc2
show sticks, solv2
color grey, solv2
scene 004, store

mdo 1: scene 001, view=0, quiet=1
scene 001, animate=0
set_view (\
     0.948694050,   -0.028416302,   -0.314912558,\
    -0.006315350,    0.994049847,   -0.108724557,\
     0.316128701,    0.105135284,    0.942874014,\
    -0.000278965,   -0.000342071, -324.629821777,\
   117.531166077,   90.844345093,   44.752410889,\
   243.257308960,  406.016143799,   20.000000000 )
zoom uc, -5
mview store, 1
mview store, 10

turn y, 180
mview store, 70

turn y, 180
mview store, 130

set_view (\
     0.948694050,   -0.028416302,   -0.314912558,\
    -0.006315350,    0.994049847,   -0.108724557,\
     0.316128701,    0.105135284,    0.942874014,\
     0.000000000,    0.000000000, -324.636688232,\
   137.548156738,  110.860862732,   53.738750458,\
   243.257308960,  406.016143799,   20.000000000 )
mview store, 160
mview store, 165


mdo 166: scene 002, view=0, quiet=1
scene 002, animate=0
set_view (\
     0.948694050,   -0.028416302,   -0.314912558,\
    -0.006315350,    0.994049847,   -0.108724557,\
     0.316128701,    0.105135284,    0.942874014,\
     0.000000000,    0.000000000, -324.636688232,\
   137.548156738,  110.860862732,   53.738750458,\
   243.257308960,  406.016143799,   20.000000000 )
mview store, 166
mview store, 200

turn y, -110
mview store, 290
turn y, 110
mview store, 380
turn x, 95
mview store, 470
turn x, -95
mview store, 560

mdo 561: scene 003, view=0, quiet=1
scene 003, animate=0
set_view (\
     0.948694050,   -0.028416302,   -0.314912558,\
    -0.006315350,    0.994049847,   -0.108724557,\
     0.316128701,    0.105135284,    0.942874014,\
     0.000000000,    0.000000000, -324.636688232,\
   137.548156738,  110.860862732,   53.738750458,\
   243.257308960,  406.016143799,   20.000000000 )
mview store, 561
mview store, 680

mdo 681: scene 004, view=0, quiet=1
scene 004, animate=0
set_view (\
     0.948694050,   -0.028416302,   -0.314912558,\
    -0.006315350,    0.994049847,   -0.108724557,\
     0.316128701,    0.105135284,    0.942874014,\
     0.000000000,    0.000000000, -324.636688232,\
   137.548156738,  110.860862732,   53.738750458,\
   243.257308960,  406.016143799,   20.000000000 )
mview store, 681
mview store, 800

movie_fade transparency, 561, 0, 620, 1, solv
mview reinterpolate
#mview smooth
#mview smooth
rewind

set antialias=1
set line_smooth = 1.00000
set depth_cue = 1
set specular = 1.00000
set surface_quality = 1.00000
set stick_quality = 25.00000
set sphere_quality = 2.00000
set cartoon_sampling = 14.00000
set ribbon_sampling = 10.00000
set ray_trace_fog = 1
rebuild

set ray_trace_frames=1
set cache_frames=0
mclear
mpng mov

