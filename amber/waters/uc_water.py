__author__ = 'pjanowsk'
from chemistry.amber.readparm import AmberParm, Rst7
from chemistry.amber.netcdffiles import NetCDFTraj
import ReadAmberFiles as raf
from numpy import dot, array
from copy import copy
import sys

'''
The trajectory has to  be fit to the pdb structure.
res_per_asu is no of residues per unit cell starting with 1.

What I do:
1. Get center of mass of target unit cell and it's translation from [0.5,0.5,0.5]
2. Translate frac coord frame by that amount. Now the target cell is in center of UC1
3. Wrap any waters into [propa,propb,probc] frac coord box.
4. Select waters that are in [1,1,1] box
5. revsym the selected waters from the non-translated frac coord frame

What could be done:
1. take exp supercell. Translate so uc1 com is at 0.5,0.5,0.5. Calculate com of supercell
2. align each supercell frame to that exp. com
3. wrap atoms to [0,prop]
3. for a given target uc, calculate borders and get the atoms in there
4. revsym the selected atoms accordingly



'''


def get_origin_translation(asu_prmtop_file_name, asu_rst7_file_name):
  rst7 = raf.rst7(asu_rst7_file_name)
  coords = rst7.Get_Coords()
  UCbox = rst7.Get_Box()
  u,invu = raf.CompXfrm(UCbox)
  masses = raf.prmtop(asu_prmtop_file_name).Get_Masses()
  com = raf.COM(coords,masses)
  frac_com = dot(u, com)
  origin_translation = array([0.5, 0.5, 0.5]) - frac_com
  return u, origin_translation

def get_U_invU(asu_rst7_file_name):
  rst7 = Rst7.open(asu_rst7_file_name)
  UCbox = rst7.box
  U, invU = raf.CompXfrm(UCbox)
  return U, invU, UCbox

def get_frac_crds(coords, traj, U):
  coords = coords.reshape((traj.atom,3))
  coords = dot(U,coords.T)
  coords = coords.T
  return coords

def get_cart_crds(coords, traj, invU):
  coords = coords.reshape((traj.atom,3))
  coords = dot(invU,coords.T)
  coords = coords.T
  return coords

def calc_start_end_atm(atms,uc, prop_a, prop_b, prop_c):
  assert uc>0, "target unit cell must be a positive number between 1 and %d" %(prop_a*prop_b*prop_c)
  assert uc <= prop_a*prop_b*prop_c, "Only %d unit cells in system " %(prop_a*prop_b*prop_c)
  start = 0+atms*(uc-1)
  end = 0+atms*uc
  return start, end

def center_frac_coords(frac_crds,parm, s, e):
  coords = frac_crds[s:e, :]
  masses = parm.parm_data['MASS'][s:e]
  com = raf.COM(coords,masses)
  shift = array([0.5, 0.5, 0.5]) - com
  cntred_frac_crds = frac_crds + shift
  return cntred_frac_crds

def wrap_coords(parm, frac_crds, cntrd_frac_crds, prop_a, prop_b, prop_c,
                buffer, solvent=True):
  selected_residues = []
  if solvent == True:
    selected_residues = ['HOH','WAT']
  atoms_in_selected_residues = \
    [i for i in range(frac_crds.shape[0]) if parm.atom_list[i].residue.resname in selected_residues]
  # import code; code.interact(local=dict(globals(), **locals()))
  # sys.exit()
  for i in atoms_in_selected_residues:
    while cntrd_frac_crds[i,0] <0-buffer:
      cntrd_frac_crds[i,0] += prop_a
      frac_crds[i,0] += prop_a
    while cntrd_frac_crds[i,0] >= prop_a+buffer:
      cntrd_frac_crds[i,0] += -1*prop_a
      frac_crds[i,0] += -1*prop_a
    while cntrd_frac_crds[i,1] <0-buffer:
      cntrd_frac_crds[i,1] += prop_b
      frac_crds[i,1] += prop_b
    while cntrd_frac_crds[i,1] >= prop_b+buffer:
      cntrd_frac_crds[i,1] += -1*prop_b
      frac_crds[i,1] += -1*prop_b
    while cntrd_frac_crds[i,2] <0-buffer:
      cntrd_frac_crds[i,2] += prop_c
      frac_crds[i,2] += prop_c
    while cntrd_frac_crds[i,2] >= prop_c+buffer:
      cntrd_frac_crds[i,2] += -1*prop_c
      frac_crds[i,2] += -1*prop_c

def select_atoms(crds, parm, buffer, solvent=True):
  selected_residues = []
  if solvent == True:
    selected_residues = ['HOH','WAT']
  atoms_in_selected_residues = \
    [i for i in range(crds.shape[0]) if parm.atom_list[i].residue.resname in selected_residues]
  atom_selection = [i for i in atoms_in_selected_residues
                     if crds[i,0] >= 0.0-buffer and crds[i,0] <1.0+buffer
                    and crds[i,1] >= 0.0-buffer and crds[i,1] <1.0+buffer
                    and crds[i,2] >= 0.0-buffer and crds[i,2] <1.0+buffer ]
  return atom_selection

def rev_translate_frac_crds(frac_crds, uc, prop_a, prop_b, prop_c):
  a_move, remain = divmod(uc-1, prop_b*prop_c)
  b_move, c_move = divmod(remain, prop_c)
  frac_crds = frac_crds - array((a_move, b_move, c_move))
  # print (a_move, b_move, c_move)
  return frac_crds

def write_amber_files(coords, parm0, filename, atom_selection=False):
  parm = copy(parm0)
  parm.load_coordinates(coords)
  if atom_selection:
    atom_mask = '!@'
    atom_mask += ','.join(['%d' % (x+1) for x in atom_selection])
    # print atom_mask
    atom_list = []
    for atom in atom_selection:
      # print "%d %8.3f %8.3f" %(atom, coords.reshape((len(coords)/3,3))[atom][0], parm.atom_list[atom].xx)
      atom_list.append(parm.atom_list[atom])
    # import code; code.interact(local=dict(globals(), **locals()))
    parm.delete_mask(atom_mask)
    # print len(atom_list), len(parm.atom_list)
    # for x, y in zip(atom_list, parm.atom_list):
    #   print x.xx, y.xx
  parm.writeParm('%s.prmtop' %filename)
  parm.writeRst7('%s.rst7' %filename)
  print len(parm.atom_list)

def write_pdb(coords, parm, atom_selection, filename, box, sg, occupancy=1.0, bfactor=0.0):
  elements = {1:'H', 7:'N', 6:'C', 8:'O', 16:'S', 20:'Ca', 11:'Na'}
  parm.load_coordinates(coords)
  last_resid = 0
  with open('%s.pdb' %filename, 'w') as f:
    f.write('CRYST1%9.3f%9.3f%9.3f%7.2f%7.2f%7.2f %s\n'
            %(box[0], box[1], box[2],
              box[3], box[4], box[5],
              sg))
    for atom_id in atom_selection:
      atom = parm.atom_list[atom_id]
      atomname = atom.atname
      if atomname == 'EPW': continue
      altloc = ' '
      resname = atom.residue.resname
      chain = ' '
      resid = atom.residue.idx
      insertion_code = ' '
      xx = atom.xx
      xy = atom.xy
      xz = atom.xz
      occup = occupancy
      bfac = bfactor
      if elements.has_key(atom.element):
        element = elements[atom.element]
      else:
        import code; code.interact(local=dict(globals(), **locals()))
        print "unknown element %d" %atom.element
        sys.exit()
      if last_resid==0:
        last_resid=resid
      elif last_resid != resid:
        last_resid=resid
        f.write('TER\n')
      f.write('ATOM  %5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f%12s\n'
          %(atom_id, atomname, altloc, resname, chain, resid, insertion_code, xx, xy, xz, occup, bfac, element))
    f.write('TER\nEND\n')

def run(parm_file_name,
      traj_file_name,
      asu_prmtop_file_name,
      asu_rst7_file_name,
      prop_a, prob_b, prop_c,
      target_unit_cell,
      atoms_per_uc,
      wrap,
      buffer,
      spacegroup = ' '):
  parm = AmberParm(parm_file_name)
  traj = NetCDFTraj.open_old(traj_file_name)
  n_frames = traj.frame
  U, invU, UCbox = get_U_invU(asu_rst7_file_name)
  start_atm, end_atm = calc_start_end_atm(atoms_per_uc, target_unit_cell,
                                          prop_a, prop_b, prop_c)

  # for frame in range(n_frames):
  #   parm = AmberParm(parm_file_name)
  for frame in range(0,1):
    coords = traj.coordinates(frame)
    frac_crds = get_frac_crds(coords, traj, U)
    cntred_frac_crds = center_frac_coords(frac_crds, parm, start_atm, end_atm)
    # atom_selection1 = select_atoms(cntred_frac_crds, parm, buffer, solvent=True)
    print frame
    # print atom_selection1
    # print frac_crds[9794]
    # print cntred_frac_crds[9794]
    # if wrap:
    #   wrap_coords(parm, frac_crds, cntred_frac_crds, prop_a, prop_b, prop_c, buffer, solvent=True)
    atom_selection = select_atoms(cntred_frac_crds, parm, buffer, solvent=True)
    frac_crds = rev_translate_frac_crds(frac_crds, target_unit_cell, prop_a, prop_b, prop_c)
    coords = get_cart_crds(frac_crds, traj, invU).flatten()
    # print atom_selection
    # print cntred_frac_crds[9794]
    write_pdb(coords, parm, atom_selection, 'uc%d_frame%d' %(target_unit_cell,frame), UCbox, spacegroup)
    # write_pdb(coords, parm, atom_selection1, 'uc%d_frame%d_nowrap' %(target_unit_cell,frame))
    write_amber_files(coords, parm, 'uc%d_frame%d' %(target_unit_cell,frame), atom_selection)
    # import code; code.interact(local=dict(globals(), **locals()))
  return atom_selection

if __name__ == "__main__" :
  parm_file_name = 'fav8_sc.prmtop'
  traj_file_name = 'test_wat_fav8.nc'
  asu_rst7_file_name = 'asu_fav8.rst7'
  asu_prmtop_file_name = 'asu_fav8.prmtop'
  prop_a = 4
  prop_b = 3
  prop_c = 3
  target_unit_cell = 1
  atoms_per_uc = 272
  wrap = True
  buffer = 0.00
  spacegroup = "P 1"


run(parm_file_name,
      traj_file_name,
      asu_prmtop_file_name,
      asu_rst7_file_name,
      prop_a, prop_b, prop_c,
      target_unit_cell,
      atoms_per_uc,
      wrap,
      buffer,
      spacegroup)

  # atsel=[]
  # for target_unit_cell in range(1,37):
  #   atsel = atsel + run(parm_file_name,
  #     traj_file_name,
  #     asu_prmtop_file_name,
  #     asu_rst7_file_name,
  #     prop_a, prop_b, prop_c,
  #     target_unit_cell,
  #     atoms_per_uc,
  #     wrap,
  #     buffer)
  # atsel.sort()
  # print atsel
  # print len(atsel)
