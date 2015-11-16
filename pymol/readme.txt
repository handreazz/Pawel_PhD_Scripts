# color by chain
util.cbc('label')

#run commands from '~/c/scripts/pymol'
first need import cmdpml in .pymolrc
then do 'Run script.py' (capital Run)

#representation script
#==== start script ====
fetch 3b6a, async=0
as cartoon
extract ligand, c. c and organic
util.chainbow("3b6a")
color green, elem c and ligand
color oxygen, elem o and ligand
show surface, ligand
set surface_mode, 1
set surface_color, yellow
set transparency=.5
show sticks, ligand
set stick_radius, 0.4
show sticks, c. c and i. 130
set cartoon_side_chain_helper, on
zoom ligand
#==== end script ====




# Make movie
1) Scene--> Buttons (once you store snapshots you should see buttons
appear on the bottom left of your screen, you can click on them to take
you to that snapshot, you can also update them if you want to change something)
2) Make 1st snapshot --> Scenes --> Append (or Store)
3) Make 2nd snapshot --> Scenes --> Append (or Store)
4) Repeat
5) When you're done Program --> Steady --> 1 second
6) If you want it to look nice turn on ray tracing
Movie --> Ray Trace Frames
6) File -> Save movie --> Many png files
7) In command window
-> high quality but windows won't read
mencoder "mf://*.png" -o movie1.avi -ovc lavc -lavcopts vcodec=mjpeg
-> ok windows, slower
mencoder "mf://*.png" -mf type=png:fps=18 -ovc lavc -o output.avi
-> another codec: wmv (also windows) and slower
mencoder "mf://*.png" -o movie_wmv1.avi -ovc lavc -lavcopts vcodec=wmv1
-> high quality and works with windows (I think)
mencoder -mc 0 -noskip -skiplimit 0 -ovc lavc -lavcopts vcodec=mpeg4:vhq:trell:mbd=2:vmax_b_frames=1:v4mv:vb_strategy=0:vlelim=0:vcelim=0:cmp=6:subcmp=6:precmp=6:predia=3:dia=3:vme=4:vqscale=1 "mf://*.png" -mf type=png:fps=18 -o output.avi


#image codes
http://www.pymolwiki.org/index.php/Gallery

#various scripts
http://kpwu.wordpress.com/my-pymol-examples/

#presets
action-> preset for present visualizations

#scenes
scene->append; then scroll through with previous/next and save as psw show file (pse is session) for viewing...

#movies
Movie→Program→Scene Loop→Nutate→2 Seconds Each.

# grid mode
Display→Grid→By Object

#alignment: 
  - use super 
  - or A→Action→Align→All
  - or pair_fit 1uwh//A/563-582/CA, 1z5m///193-212/CA

#Bond valences: Builder

#Electrostatic potential: Actions→generate→vacuum electro-statics→protein contact potential

#Creating One Object Out of Another
Atoms in a selection can be copied into a new object by choosing the A→Action→Create Object for the selection.
A new object name will appear in the names list, and you can then rename this object using A→Actions→Rename
Object. Certain properties of atoms in a newly created object can be manipulated independently from those in the
source object(s), while those properties of a selection cannot. For example, independent objects can have different
transparencies, while a selection must have the transparency of its parent object.

#Wizard→Mutagenesis - mutate residues or change conformers



