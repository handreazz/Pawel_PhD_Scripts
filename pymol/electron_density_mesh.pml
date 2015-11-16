# to get the ccp4 map use either md_avg.map or phenix.mtz2map. In the latter case, the pdb model
# defines the area of space of the map but does not bias it. Don't use phenix.maps as this
# biases the model by the phases of the pdb that you need to provide.

delete all
set mesh_width, 0.3
bg_color white


load 424d_refine_002.pdb, amber
select r40a, amber and resi 40-42+31-33
load 424d_refine_001.pdb, phenix
select r40p, phenix and resi 40-42+31-33
hide all
show sticks, r40a
show sticks, r40p
util.cbag r40a
color orange, r40p
alter r40p, vdw=0.3
show spheres, r40p
alter r40a, vdw=0.3
show spheres, r40a



load 424d_2mFo-DFc_map.ccp4, expmap
map_double expmap
isomesh exp19, expmap, 1.5, resi 40+33, carve=1.6
color grey10, exp19

origin (resi 40 and name o6)
cmd.set_view((-0.2079739272594452, -0.955011248588562, 0.21140432357788086, -0.9310407042503357, 0.12704065442085266, -0.342057466506958, 0.29981663823127747, -0.2679612338542938, -0.9155850410461426, 0.0004115123301744461, 0.0005099400877952576, -25.26689338684082, 39.98386001586914, 14.803436279296875, -6.682119369506836, 22.26454734802246, 28.761884689331055, -20.0))


set dash_gap, 0.2
set dash_radius, 0.05
distance d1, phenix and i. 40 and n. N1,  phenix and i. 33 and n. N3
distance d2, phenix and i. 40 and n. N2,  phenix and i. 33 and n. O2
color magenta, d1
color magenta, d2
hide labels,d1
hide labels,d2

#ray 2400,2400
#png asp19.png, dpi=300
