#! /usr/bin/python

from ReadAmberFiles import *
from numpy import *
from Scientific.IO import NetCDF


#======================================================================#
#                                                                      #
#  Parses a set of RevSym netcdf trajectories and writes an array of   #
#  cartesian and an array of fractional coordinates of a specific atom #
#  in all frames of the trajectories.                                  #
#                                                                      #
#  Arguments: set below                                                # 
#  Returns: write CartArray.dat and FracArray.dat. nx3 where n is the  #
#             number of frames and columns are the 3 xyz dimensions    #
#                                                                      #
#======================================================================#

# SET VARIABLES #

unitcells=12
asus=1
traj_dir='../revsym' #location of netcdf Revsym trajectories
UCBox=array([27.24, 31.87, 34.23, 88.52, 108.53, 111.89]) #experimental unit cell box

#use .getatoms.sh to get these lists of atoms

# all residues not on high b-factor
residues_lowb=[8, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21,
 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40,
 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
 63, 64, 65, 66, 69, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 88,
 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 104, 105, 106, 107, 
 108, 109, 110, 111, 112, 113, 114, 115, 116]
 
 
atoms_lowb=[118, 137, 147, 157, 167, 184, 255, 
 274, 286, 300, 321, 345, 352, 373, 384, 403, 410, 424, 448, 464, 474, 
 484, 494, 516, 536, 551, 576, 596, 610, 624, 641, 651, 665, 679, 750, 
 761, 775, 787, 808, 815, 834, 853, 870, 889, 903, 914, 938, 962, 986, 
 996, 1010, 1053, 1099, 1123, 1137, 1156, 1166, 1180, 1207, 1213, 1223, 
 1234, 1244, 1263, 1316, 1335, 1349, 1359, 1370, 1386, 1400, 1410, 1420, 
 1442, 1464, 1483, 1499, 1543, 1550, 1567, 1581, 1591, 1615, 1631, 1641, 
 1665, 1689, 1703, 1727, 1737]


#high b-factor residues
residues_highb=[14,15,16,37,46,47,48,49,67,68,70,71,72,85,86,87,101,102,103,117,118,119]
atoms_highb=[206,230,248,562,703,717,731,743,1022,1029,1075,1081,1088,1282,1293,1304,1510,1522,1529,1759,1766,1780]
        #~ # atom whose coordinates you want, REMEMBER atom count starts with 0 not 1
		#~ # so if the pdf file has atom 100, the netcdf file (here) will have 99

#test case		
atoms_test=[494, 1207]
residues_test=[33, 79]

########################################################################
########################################################################

def coord_arrays(residues, atoms):

	dictionary=dict(zip(atoms,residues))	
	for atom in atoms:
		print "Getting residue %d, atom %d" %(dictionary[atom],atom)
		FracArray=[]
		CartArray=[]
		u,invu=CompXfrm(UCBox)

		for uc in range(unitcells):
			for asu in range(asus):
				filename='%s/RevSym_%02d_%02d.nc' %(traj_dir,uc+1,asu+1)		
				ofile = NetCDF.NetCDFFile(filename, 'r')
				coords=ofile.variables['coordinates']
				frames=coords.shape[0]
				
				for frame in range(1500,7426):
					cart_coord=coords[frame,atom,:]
					frac_coord= dot(u,cart_coord)
					CartArray.append(cart_coord)
					FracArray.append(frac_coord)
				ofile.close()
					
		CartArray=array(CartArray).astype(float32)
		FracArray=array(FracArray).astype(float32)

		savetxt("CartArray_:%d@%d.dat" %(dictionary[atom],atom), CartArray, fmt="%7.4f")
		savetxt("FracArray_:%d@%d.dat" %(dictionary[atom],atom), FracArray, fmt="%6.4f")


coord_arrays(residues_test,atoms_test)
#~ coord_arrays(residues_highb, atoms_highb)
#~ coord_arrays(residues_lowb, atoms_lowb)
	

