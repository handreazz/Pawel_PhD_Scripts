import time, sys
import iotbx.pdb
from scitbx.array_family import flex
from cctbx import adptbx

def get_hieratchy(file_name):
  pdb_inp = iotbx.pdb.input(file_name=file_name) 
  h = pdb_inp.construct_hierarchy()
  return h
  
def get_anisotropy(u):
  esv = adptbx.eigensystem(u).values()
  return min(esv)/max(esv)

def run(args):
  assert len(args)==2
  p1, p2 = args # p1: source of ADP, p2: target
  #
  h1 = get_hieratchy(file_name=p1)
  h2 = get_hieratchy(file_name=p2)
  #
  A1 = flex.double()
  A2 = flex.double()
  B1 = flex.double()
  B2 = flex.double()
  C1 = flex.double()
  C2 = flex.double()
  def is_good(a):
    get_class = iotbx.pdb.common_residue_names_get_class
    result = False
    resname = a.parent().parent().unique_resnames()[0].strip().upper()
    cl = get_class(name=resname)
    if(cl == "common_amino_acid" or cl == "common_rna_dna"):
      result = True
    if resname in ['HIP', 'HIE', 'HID', 'CYX']:
		return True  
    return result
  cntr = 0
  for a1 in h1.atoms():
    if(is_good(a=a1)):
      for a2 in h2.atoms():
        if(is_good(a=a2)):
          #~ if(a1.name == a2.name and a1.distance(a2)<1.e-3):
          if (a1.name==a2.name and 
              a1.parent().parent().resseq==a2.parent().parent().resseq and
              a2.parent().altloc in ['A','']):
            cntr += 1
            A1.extend(flex.double(a1.uij))
            A2.extend(flex.double(a2.uij))
            #
            C1.append(get_anisotropy(u=a1.uij))
            C2.append(get_anisotropy(u=a2.uij))
            #
            B1.append(a1.b)
            B2.append(a2.b)
            #
            a2.set_b(a1.b)
            a2.set_uij(a1.uij)
            break
  print cntr
  
  h2.write_pdb_file(file_name="my_newADP.pdb")
  # 
  flc = flex.linear_correlation
  print "CC(ADP_anisotropic1, ADP_anisotropic2) =", flc(A1, A2).coefficient()
  print "CC(ADP_isotropic1, ADP_isotropic2)     =", flc(B1, B2).coefficient()
  print "CC(anisotropy1, anisotropy2)           =", flc(C1, C2).coefficient()

if (__name__ == "__main__"):
  run(args=sys.argv[1:])

