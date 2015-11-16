delete all
set matrix_mode, 1
set movie_panel, 1
set scene_buttons, 1
bg_color white
set orthoscopic, on

load 4lztUC.pdb
as cartoon
color black
load AvgCoord_asu.pdb
as cartoon
color orange, AvgCoord_asu 
zoom 4lztUC


mset 1 x150
scene 001, store
mview store, scene=001

turn y, 180
scene 002, store
frame 75
mview store, 75, scene=002

turn y, 180
scene 003, store
frame 150
mview store, 150, scene=003
