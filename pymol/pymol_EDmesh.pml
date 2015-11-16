# to get the ccp4 map use either md_avg.map or phenix.mtz2map. In the latter case, the pdb model
# defines the area of space of the map but does not bias it. Don't use phenix.maps as this
# biases the model by the phases of the pdb that you need to provide.

delete all
set mesh_width, 0.3
bg_color white


load asu_active_aligned.pdb, exp
load AvgCoord_asu.pdb, sim
select e_act, exp and resi 12+41+119+125+126 and !hydrogen
select s_act, sim and resi 12+41+119+125+126
deselect
hide all
show sticks, e_act
#show sticks, s_act

#color orange, s_act
#alter s_act, vdw=0.3
#show spheres, s_act

util.cbag e_act
alter e_act, vdw=0.3
show spheres, e_act

load md_avg_1.ccp4, ed, format=ccp4
#map_double ed
isomesh ed_act, ed, 1.0, resi 12+41+119+125+126, carve=1.2
color grey10, ed_act

origin (resi 126 and name P)
cmd.set_view((0.7716495990753174, -0.2767021358013153, 0.5726991891860962, 0.3131563663482666, 0.9489925503730774, 0.036563850939273834, -0.5536009073257446, 0.15113084018230438, 0.8189427852630615, -0.00025289133191108704, -8.661672472953796e-05, -53.80708694458008, 33.554195404052734, 15.818671226501465, 9.422401428222656, 18.910507202148438, 88.67802429199219, 20.0))
cmd.set_view((0.5895265340805054, -0.6376563906669617, 0.4958285689353943, 0.4274454712867737, 0.7671236991882324, 0.47833144664764404, -0.6853689551353455, -0.07005032151937485, 0.7248051762580872, -0.0001959092915058136, -1.948140561580658e-05, -53.261287689208984, 33.030086517333984, 18.156829833984375, 8.723562240600586, 21.838886260986328, 84.62960815429688, 20.0))

#set dash_gap, 0.2
#set dash_radius, 0.05
#distance d1, phenix and i. 40 and n. N1,  phenix and i. 33 and n. N3
#distance d2, phenix and i. 40 and n. N2,  phenix and i. 33 and n. O2
#color magenta, d1
#color magenta, d2
#hide labels,d1
#hide labels,d2

ray 2400,2200
png 1rpg_ed_act.png, dpi=600
