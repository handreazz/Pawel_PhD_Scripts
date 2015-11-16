#! /bin/bash

cat >params.eff <<EOF
refinement {
  main {
    number_of_macro_cycles=5
  }
  refine {
    strategy = *individual_sites individual_sites_real_space rigid_body \
               individual_adp group_adp tls occupancies group_anomalous
    adp {
      individual {
        anisotropic = "not (element H)"
	isotropic = "element H"
      }
    }
  }
  bulk_solvent_and_scale {
    bulk_solvent = False
    anisotropic_scaling = False
    k_sol_b_sol_grid_search = False
    minimization_k_sol_b_sol = False
  }
}
EOF

phenix.refine 4lzt_shaken.pdb prefix=vs_obs_mdgx 4lzt-sf-truncated.mtz topology_file_name=4lzt.prmtop amber.coordinate_file_name=4lzt.rst7 use_amber=True refinement.input.xray_data.r_free_flags.file_name=md_avg_95_rfree.mtz --overwrite 

phenix.refine 4lzt_shaken.pdb prefix=vs_obs_sander 4lzt-sf-truncated.mtz topology_file_name=4lzt.prmtop amber.coordinate_file_name=4lzt.rst7 use_amber=True refinement.input.xray_data.r_free_flags.file_name=md_avg_95_rfree.mtz --overwrite use_sander=True

phenix.refine 4lzt_shaken.pdb prefix=vs_obs 4lzt-sf-truncated.mtz topology_file_name=4lzt.prmtop amber.coordinate_file_name=4lzt.rst7 use_amber=False refinement.input.xray_data.r_free_flags.file_name=md_avg_95_rfree.mtz --overwrite  use_sander=True
