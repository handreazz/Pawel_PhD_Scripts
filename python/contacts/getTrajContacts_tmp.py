#! /net/casegroup2/u2/pjanowsk/bin/phenix_svn/build/bin/phenix.python
## /home/pawelrc/bin/phenix_svn/build/bin/phenix.python
from libtbx import group_args
import sys, os
import numpy as np

#symop1 and symop2 is the ordinal number of the symmetry operation 
# within the unit cell to which that residue belongs

def find_crystal_contacts (xray_structure,
                           pdb_atoms, # atom_with_labels, not atom!
                           selected_atoms=None,
                           distance_cutoff=3.5,
                           ignore_same_asu=True,
                           ignore_waters=True) :
  from scitbx.array_family import flex
  sites_frac = xray_structure.sites_frac()
  unit_cell = xray_structure.unit_cell()
  pair_asu_table = xray_structure.pair_asu_table(
    distance_cutoff=distance_cutoff)
  pair_sym_table = pair_asu_table.extract_pair_sym_table()
  contacts = []
  if (selected_atoms is None) :
    selected_atoms = flex.bool(len(pdb_atoms), True)
  for i_seq,pair_sym_dict in enumerate(pair_sym_table):
    if (not selected_atoms[i_seq]) :
      continue
    site_i = sites_frac[i_seq]
    atom_i = pdb_atoms[i_seq]
    resname_i = atom_i.resname
    atmname_i = atom_i.name
    chainid_i = atom_i.chain_id
    for j_seq,sym_ops in pair_sym_dict.items():
      site_j = sites_frac[j_seq]
      atom_j = pdb_atoms[j_seq]
      resname_j = atom_j.resname
      atmname_j = atom_j.name
      chainid_j = atom_j.chain_id
      for sym_op in sym_ops:
        if sym_op.is_unit_mx() :
          if ignore_same_asu :
            continue
          #~ elif (chainid_i == chainid_j) :
            #~ continue
        if (resname_j in ["HOH","WAT"] and ignore_waters) :
          continue
        site_ji = sym_op * site_j
        distance = unit_cell.distance(site_i, site_ji)
        contacts.append((i_seq, j_seq, sym_op, distance))
        #print resname_i, atmname_i, resname_j, atmname_j, str(sym_op), distance
  return contacts

def find_crystal_contacts_by_residue (xray_structure,
                                      pdb_hierarchy,
                                      **kwds) :
  contacts_by_residue = {}
  atoms = list(pdb_hierarchy.atoms_with_labels())
  contacts = find_crystal_contacts(xray_structure, atoms, **kwds)
  for (i_seq, j_seq, sym_op, distance) in contacts :
    atom_rec = atoms[i_seq].fetch_labels()
    residue_key = (atom_rec.chain_id, atom_rec.resname, atom_rec.resid(),
      atom_rec.altloc)
    if (not residue_key in contacts_by_residue) :
      contacts_by_residue[residue_key] = []
    contacts_by_residue[residue_key].append((j_seq, sym_op, distance))
  all_residues = []
  for chain in pdb_hierarchy.models()[0].chains() :
    chain_id = chain.id
    for residue_group in chain.residue_groups() :
      resid = residue_group.resid()
      for atom_group in residue_group.atom_groups() :
        resname = atom_group.resname
        altloc = atom_group.altloc
        residue_key = (chain_id, resname, resid, altloc)
        residue_contacts = contacts_by_residue.get(residue_key, [])
        all_residues.append((residue_key, residue_contacts))
  return all_residues

########################################################################
# For residue id in a super-cell, get residue id in original asymmetric#
# unit, symmetry operation, and unit cell translation.                 #
# Arguments:                                                           #
#     prop_vec: 3x1 array of the x,y,z propagations used to create the #
#               the super-cell                                         #
#     nres: int number of residues in asymmetric unit                  #
#     nsymop: int number of symmetry operations in the space group     #
#     resid: int query residue number in the super-cell                #
# Returns:                                                             #
#     sc_trans: 3x1 tuple of x,y,z propagations to arrive at the query #
#               residue's unit cell within the super-cell              #
#     symop: int number of the symop used to get to the query residue  #
#            (starts with 0)                                           #
#     asymresid: int corresponding residue id in the asymmetric unit   #
########################################################################

def SC_mapping(prop_vec,nres,nsymop,resid):
  from cctbx_sgtbx_ext import rt_mx
  xnres=prop_vec[2]*prop_vec[1]*nres*nsymop
  ynres=prop_vec[2]*nres*nsymop
  znres=nres*nsymop
  (xmoves,resid)=divmod(resid-1,xnres)
  (ymoves,resid)=divmod(resid,ynres)
  (zmoves,resid)=divmod(resid,znres)
  (sym_op,resid)=divmod(resid, nres)
  tr_op=rt_mx('x+%d,y+%d,z+%d' %(xmoves,ymoves,zmoves))
  return tr_op, sym_op, resid+1

def is_same_asu(nres,resid1,resid2):
  if divmod(resid1-1,nres)[0] == divmod(resid2-1,nres)[0]:
    return True
  else:
    return False

def find_supercell_contacts_by_residue(residue_contacts, atoms, prop_vec,
                    nres, nsymop,ignore_waters=True):
  supercell_contacts={}
  #skip all solvent ions added that does not belong to any asymmetric unit
  #by calculating maxresidue and skipping residues above that
  maxres=nres*prop_vec[0]*prop_vec[1]*prop_vec[2]*nsymop  
  for (residue,contacts) in residue_contacts:
    debug=False
    i_resid=int(residue[2])
    i_resname=residue[1]
    if (ignore_waters and i_resname in ["HOH","WAT"]):
      continue
    if i_resid >= maxres: continue  
    # residue_contacts may have multiple entries for contacts between
    # different atoms of the same residues. Duplicate_test{} is used
    # to filter this so that only one contact is returned with the 
    # shortest atom to atom distance reported.    
    duplicate_test={}
    for contact in contacts:
      sym_op=contact[1]
      j_seq=contact[0]
      j_resid = int(atoms[j_seq].fetch_labels().resid())
      j_resname = atoms[j_seq].fetch_labels().resname
      dist=contact[2]
      if j_resid >= maxres: continue
      
      #~ if i_resname in ["Na+"] and j_resname in ["ASN"]:
        #~ print i_resname, i_resid
        #~ print j_resname, j_resid
        #~ print sym_op
        #~ debug=True
      #~ elif i_resname in ["ASN"] and j_resname in ["Na+"]:
        #~ print i_resname, i_resid
        #~ print j_resname, j_resid
        #~ print sym_op
        #~ debug=True 
        
      # unit_mx sym_op means the contact is in the original supercell
      # if same asu in same supercell, it's an "intra_asu" contact so
      #ignore
      if is_same_asu(nres,i_resid,j_resid):
         print i_resid, j_resid, sym_op
         if sym_op.is_unit_mx() :
           continue
      if (ignore_waters and j_resname in ["HOH","WAT"]):
        continue
      # populate duplicate_test{} with only one instance of a given 
      # residue pair, keeping the shortest distance value
      if (j_resid, j_resname,sym_op) in duplicate_test.keys():
        if dist < duplicate_test[(j_resid,j_resname,sym_op)]:
          duplicate_test[(j_resid,j_resname,sym_op)]=dist
      else:
        duplicate_test[(j_resid,j_resname,sym_op)]=dist


    #~ if i_resname=="ASN" and i_resid==324:
      #~ print duplicate_test
      #~ for key in duplicate_test.keys():
        #~ print key[2]
      #~ debug=True 
      
      
    # for contact residue pair, get residue's number in original asu
    # and symmetry operation relating res_j to res_i
    for (j_resid, j_resname,sym_op) in duplicate_test.keys():
      dist=duplicate_test[(j_resid, j_resname,sym_op)]
      i_transop, symop1, i_asymresid = SC_mapping(prop_vec, nres, nsymop,i_resid)
      j_transop, symop2, j_asymresid = SC_mapping(prop_vec, nres, nsymop,j_resid)
      if debug:
        print i_transop, symop1, i_asymresid
        print j_transop, symop2, j_asymresid
      #both residues within the original supercell
      if sym_op.is_unit_mx() : 
        transop=j_transop.multiply(i_transop.inverse())
      #res_j outside the original supercell 
      else: 
        t=sym_op.t().as_double()
        t=[t[0]*prop_vec[0],t[1]*prop_vec[1],t[2]*prop_vec[2]]
        t=[int(i) for i in t]
        from cctbx_sgtbx_ext import rt_mx,tr_vec
        t=rt_mx(tr_vec(t,tr_den=1))
        j_transop, symop2, j_asymresid = SC_mapping(prop_vec, nres, nsymop,j_resid)
        j_transop=j_transop.multiply(t)
        transop=j_transop.multiply(i_transop.inverse())
        
      ##################################################################  
      ###TO DO and TEST!: for multiple asyms in unit cell
      #transop=j.transop.multiply(symop2).multiply(symop1.inverse())
      #where symop1 and symop2 must be turned into an rt_mx first...
      #################################################################
        
      #populate supercell_contacts{}. To avoid duplicates chose by highest
      #x trans op, then y then z
      if transop.t().as_double()[0] > transop.inverse().t().as_double()[0]:
        i_key=(i_asymresid, i_resname, j_asymresid, j_resname,transop.as_xyz())
      elif transop.t().as_double()[0] < transop.inverse().t().as_double()[0]:  
        i_key=(j_asymresid, j_resname, i_asymresid, i_resname,transop.inverse().as_xyz())
      else:
        if transop.t().as_double()[1] > transop.inverse().t().as_double()[1]:
          i_key=(i_asymresid, i_resname, j_asymresid, j_resname,transop.as_xyz())
        elif transop.t().as_double()[1] < transop.inverse().t().as_double()[1]:  
          i_key=(j_asymresid, j_resname, i_asymresid, i_resname,transop.inverse().as_xyz())     
        else:
          if transop.t().as_double()[2] > transop.inverse().t().as_double()[2]:
            i_key=(i_asymresid, i_resname, j_asymresid, j_resname,transop.as_xyz())
          elif transop.t().as_double()[2] < transop.inverse().t().as_double()[2]:  
            i_key=(j_asymresid, j_resname, i_asymresid, i_resname,transop.inverse().as_xyz())     
          else:
            print "something is wrong. Transop is: "
            print transop.as_xyz()
            import code; code.interact(local=locals())
            
      # This was the old way. It would avoid duplicates in the same frame but
      # not between frames (eg. would have (x+1,y,z) iface in one frame 
      # and (x-1,y,z) contacts in another.
      #~ if transop.inverse().as_xyz() in [i[4] for i in supercell_contacts.keys()]:
        #~ i_key=(j_asymresid, j_resname, i_asymresid, i_resname,transop.inverse().as_xyz())
      #~ else:
        #~ i_key=(i_asymresid, i_resname, j_asymresid, j_resname,transop.as_xyz())

      if i_key in supercell_contacts.keys():
        supercell_contacts[i_key].append(dist)
      else:
        supercell_contacts[i_key]=[dist]
  return supercell_contacts

def report_supercell_contacts (supercell_contacts): 
  transops=set([i[4] for i in supercell_contacts.keys()])
  for transop in transops:
    tmp_l=[(k, v) for k, v in supercell_contacts.iteritems() if k[4]==transop]
    print "S%12s %3d|\n" %(transop, len(tmp_l)),
    for h,i in enumerate(tmp_l):
      #~ if h==0:
        #~ print "%4d %3s %4d %3s %3d" %(i[0][0],i[0][1],i[0][2],i[0][3], len(i[1]))
      #~ else: 
      print "                  %4d %3s %4d %3s %3d" \
             %(i[0][0],i[0][1],i[0][2],i[0][3], len(i[1]))
    
  
if __name__ == "__main__" :
  prop_vec=[1,1,1]        #propagation forming supercell
  nres=139              #n residues in asymmetric unit  
  nsymop=1            #n symmetry operations in spacegroup
  cutoff=3.5            #angstrom cutoff to find contacts
  pdb_file = sys.argv[1]    #CRYST1 record w/supercell box required
  from iotbx import file_reader
  pdb_in = file_reader.any_file(pdb_file).file_object
  pdb_hierarchy = pdb_in.construct_hierarchy()
  xrs = pdb_in.xray_structure_simple()
  residue_contacts = find_crystal_contacts_by_residue(xrs, pdb_hierarchy,
    distance_cutoff=cutoff,ignore_same_asu=False, ignore_waters=False)
  atoms = list(pdb_hierarchy.atoms_with_labels())
  supercell_contacts=find_supercell_contacts_by_residue(residue_contacts,
            atoms, prop_vec, nres, nsymop, ignore_waters=True)
  report_supercell_contacts(supercell_contacts)



  #~ l=sorted(supercell_contacts.iteritems(), key=lambda x: x[0][4] )
  #~ for i in l:
    #~ print i
