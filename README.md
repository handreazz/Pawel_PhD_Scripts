A collection of the various scripts I wrote during my PhD to assist in multiple tasks.

Directory Listing
/amber
  /average_bond_trajectory
    AvgBond.py/AvgBond.sh - mean length of a bond in a crystal simulation over all copies of asymmetric unit and several trajectory intervals
    BondPerASU.sh - a bond length in each copy of the asymmetric unit in one trajectory frame
    BondPerASU2.sh - like BonPerASU.sh but on reversed symmetry trajectories

  /bfactors
    select_bfacs_byname.py - select subset of B factors based on atom names

  /cpptraj
    checkZN.sh - 
    cpptraj.hbond.in - 
    cpptraj.rmsd_active -
    cpptraj_nowat_merge.in -
    ctraj_chiangles -
    ctraj_cluster12 -
    ctraj_distmatrix - 
    ctraj_nmwiz_quasi - 
    ctraj_quasi -
    ctraj_quasi1 -
    ptraj_01_01 -
    ptraj_bfactor - 
    ptraj_CalcAvgesAvg - 
    ptraj_CalcAvgesbfactor - 
    ptraj_CalcLatRmsd - 
    ptraj_CalcUCbfactor -
    ptraj_CalcUCRMSD -
    ptraj_CreateAvgUC -
    ptraj_density -
    ptraj_densitymatrix - 
    ptraj_imageWat1 -
    ptraj_mergetrajectory -
    ptraj_rmsd - 
    ptraj_supercell_imageWat -
    ptraj_translate - 
    runquasi.sh - 
    StripMerge.sh - 

  /dihedral_analysis
    dihedralX.py -

  /equilibration_hairpin
    MakeEqFile.sh -
    MakeRestraints.py -

  /forceCalc
    LoadHairpin.m
    TestForces.m

  /other
    check_com.py
    check_mask.py
    check_mergetraj.py

  /parametrize_torsion
    check_CAC.sh
    makeAmatBvec_byhand.py
    mk_files_CAC.sh
    runllsp.m

  /prep
    DOALL.sh
    prepscript_nowat.sh
    prepscritp_UC.sh
    prepscript1rpgK.sh
    prepscriptH_NVT.sh
    prepscriptHIS.sh
    prepscriptsIe.sh

  /rmsd
    make_rmsd_table.py

  /rmsd_averages
    averages.py
    makesummary.sh

  /run
    1p7e_prep_min_dynamics.sh
    equil_cdpa_nvt.sh
    equil_cdpa_restraints.sh
    run_cdpa_restraints.sh

  /volume
    cellvolume.m
    makepercentvolume.m
    process_mdout.perl
    volcheck.sh

  /waters
    uc_water.py

/awk
  awk_examples.py
  heatcapacity.awk
  jigglepdb.awk.txt
  md2map.sh
  pressure.sh

/bash
  AbsPath.sh
  bashrc_casegroup
  convert_wma2mp3.sh
  CorrelateRst.sh
  cp_nc_from_Dave.sh
  fix_numbering_pdb.csh
  fix_numbering_pdb_2.csh
  masterRun.sh
  meldwrap.sh
  minimizeEx_tyr.sh
  mov2avi.sh
  pdbget
  prepscript.sh
  print_array.sh
  renumber.sh
  rsync.sh
  run_gyges.sh
  runObelix.sh
  runObelix_mod2.sh
  runObelix_mod3.sh
  runObelix_NVE.sh
  scan_dihedral_amber.sh
  scan_torsions.sh

/bioinfo
  kmeans.py
  NeedlemanWunsh_affine.py

/crystallography
  align_two_maps.sh
  cif_intensity_2_mtz_fobs.sh
  cif2mtzExScrpt.sh
  converst_maps.sh
  density_eds.csh
  diff_maps.sh
  fft.sh
  filter_mtz.py
  frac_translate.sh
  get_r.sh
  get_r_entre_fobs.sh
  hlify.sh
  pdbset.sh
  sfall2.sh
  sfallExScrpt.sh
  unique.sh

/latex
  midterm2.tex
  Duff_Abstract.tex
  latex_subfloats.tex
  phenix-afitt.tex
  research_summary.tex
  SummaryStructures.tex

/matlab
  ErrorFun.m
  RunOpt.m
  FourierT.m
  blackjack.m
  blackjacksim.m
  CellParams.m
  cellvolume.m
  CompAutoCorr.m
  CompXfrmPawel.m
  createFit2.m
  derive_TLS_eq.m
  diffusion_fit.m
  DotProduct.m
  em_1dim.m
  funcs.m
  functionplot.m
  GMM
  InterpDih.m
  Line2Tenso.m
  linearfitplot.m
  MakeGraphs.m
  matave.m
  matconv.m
  matcpy.m
  matrices.m
  matrixdata.m
  MeanSquareDispFrom2Files.m
  MeanSquareDispFromNetCDF.m
  MetricTensor.m
  overfitting_example.m
  peakfitter.m
  plot_latex_title.m
  Recip.m
  restart_volumes.m
  sine_plot.m
  smoothNrg.m
  SmoothRMS.m
  smoothVol.m
  SmoothWatRMS.m
  TLS_cross.m
  Uequiv.m
  vectorization2.m
  VectorLength.m

/matplotlib
  analyze_refines.py - includes seabron KDE distribution, violin, box and scatter plots
  axes.py
  axes_legend.py
  axes2.py
  bargraph.py
  broken_axes.py
  centercolormapatzero.py
  fromgroup.py
  histogram.py
  kmeans_plot.py
  legend.py
  plot_benchmarks.py
  plot_chi.py
  plot_comshifts_3Dscatter.py
  plot_energy_r_pub.py
  plot_histograms_pub.py
  plot_mogul.py
  plot_PheTorsions.py
  plot_PhiPsi.py
  plot_UC_hist.py
  plot_UC_series.py
  plotAutoCorr.py
  plotpy.py
  quickplotsmth.py
  scatter_plot_bug.py
  scatter_seaborn.py
  secondary_structure_color_bar.py
  simpleplot.py
  tickmarks.py

/namd
  clean_prmtop_namd.sh
  namdcheck.sh
  tyr_namd_min.sh
  tyr_namd_run.sh

/pandas
  analyze_pandas.py
  analyze_refines.py
  data_reduce.py
  process_songs_clean.py
  taxi.py

/PBS
  gordonequil1.sh
  gordonMasterEquil_1.sh
  gordonMasterEquil_1_S.sh
  gordonMasterEquil_2_S.sh
  gordonMasterEquil_S.sh
  gygesmin.sh
  kraken_multiple_jobs_maria.sh
  kraken_namd.sh
  krakenequil.sh
  krakenMasterEquil.sh
  krakenMasterRun.sh
  krakenMasterRun_namd.sh
  krakenrun.sh
  minimize_krakow.sh
  ranger_masterRun.sh
  rangerrun.sh
  run_casegroup3.sh
  run_gordon.sh
  run_Gyges.sh
  run_tyr.sh
  run_tyr_1rpg.sh
  run_tyr_4lzt.sh
  run_tyr_namd.sh
  runRangerEx1.sh
  runRangerEx2.sh

/phenix
  /afitt
    afitt.py
    afitt_fd.py
  /amber_adaptbx
    __init__.py
    amber_geometry_minimization.py
    amber_library_server.py
    fix_ambpdb.py
    get_candidates.py
    get_charge_and_multiplicity.py
    getmdgxfrc.c
    getmdgxfrc.h
    lbfgs.py
    pdb4amber.py
    restraints.py
    tst_minimization.py
    tst_refinement.py
    AmberPrep.py
  /cci_scripts
    crawl_results.py
    get_clash.py
    getfiles.py
    run_tests.py
    test_amber_hydrogens.py
  /Tom_SF_from_MD
    run_demo.csh
  analyze_pandas.py
  changeHIS.py
  check_failed_volumes.py
  check_special_pos.py
  cif_read.py
  crawl_refines_print_Rfactor.py
  file_setup_for_refine.py
  filter_mtz.py
  find_ligands.py
  find_success_pdb.py
  gather_analyze_plot.py
  get_candidates.py
  get_clashscores.py
  get_CRYST1.py
  get_nsymops.py
  make_SMTRY.py
  map_info.py
  mine_refine_100.py
  molprobity_coot.py
  pavel_examples.py
  pbd_hier_sg.py
  phenix_sander_api.py
  phenix_unitcell.py
  refine_ligandme_errors.py
  restr_from_pdb_cif.py
  rism_vs_bulk_2g04.py
  run_check_weights.py
  run_ratio_tests.py
  run_refine.py
  run_refine_100.py
  run_refine_doover.py
  run_refine_elbow.py
  run_refine_nigel.py
  sander_api2.py
  special_pos_test.py
  test_hierarcy.py
  testcart.py
  tst_steepest.py
  vector_to_list.cpp

/pymol
  movie_fade.py
  mk_movei.pml
  mk_movie1.pml
  mk_movie2.pml
  mk_movie3.pml
  align_rmsd.pml
  arrow.py
  axes.py
  draw_supercell_xy.py
  draw_supercell_yz.py
  electron_density_mesh.pml
  get_rmsd_pymol.py
  nm_original.py
  nmodes.py
  pmlrc.py
  pymol_axes.py
  pymol_EDmesh.pml
  states_nmd1.py
  states_nmd2.py
  supercell.py
  SuperSymPlugin12.py
  update_pymol.sh

/python
  /com
    bfacs_com.py
    bfacs_RevSymm.py
    com.py
    select_bfacs_byname.py

  /comshifts
    analyze_com_shifts.py
    checkcom.py
    comshifts_fixed.py
    plot_comshifts.py
    plotcom.py
    traj_com_scatter.py

  /contacts
    contacts.py
    getTrajContacts.py
    plot_contacts.py
    plot_TrajContacts.py
    run_getTrajContacts.py
    summarize_contacts.py
    sumTrajContacts.py

  /fav8
    avgmatrix.py
    avgwaterstate.py
    avgwaterstate2.py
    bigmatrix.py
    dihedral.py
    dihedral2.py
    dihedralfirstframe.py
    dssp.py
    dssp4corr.py
    makedistancegraphs.py
    mat2bin.py
    matrix_dist.py
    percentage.py
    waterdistance.py
    waterstateshift.py

  /quasiharmonics
    make_nmd.py
    make_nmd_bynumber.py

  /sasa
    asa.py
    molecule.py
    vector3d.py

  /toolpy_huanwang
    pdb_stat.py
    tools_v100.py
    util.py

addwaters2.py
adp2tls.py
adp2tls_cov.py
adp_analyze.py
analyse_supercell.py
analyze_geo_min.py
anisotropic.py
asu_res.py
bfactor_correlation.py
bond_angle_rmsd.py
broken_axes.py
cc_std_dev.py
channelProfile.py
channelProfile3.py
checkcom.py
check_com.py
check_memory.py
check_mergetraj.py
clean_bibliography.py
clean_prmtop_namd.sh
cluster_freq.py
comparepdb.py
convert_string_array.py
cpptraj_quasih_play.py
crawl_results.py
ctraj_cluster.py
dbscan.py
decorator_howmanytimes.py
density.py
difference_vector.py
dssp.py
fileread_Raik_Grunberg.py
find_successful_pdbs.py
fix_ambpdb.py
flatten.py
gather_pickle.py
getatoms.sh
GetBfacsFromCif4SupCell.py
GetBfacsfromPdb2Pdb.py
getbfactors.py
GetBox.py
GetFracCoordArray.py
getTrajContacts.py
GetVolume.py
get_amber_email_stats.py
GMM.py
hbond_diff.py
hbond_summary.py
heatmap.py
histogramathome.py
imit_cpptraj_quasiharm.py
journal_abbreviations.txt
kabsch.py
kabsch2.py
ls.py
MakeRestraints.py
mergepdbs.py
misc.py
MolProb_Trajalyze.py
my_run_transfer_adps.py
nccoords
ncframes
NeedlemanWunsch.py
new_template.py
NS_SmithWaterman.py
numberlines.py
parsedata.py
pdb2rst7.py
pdb4amber.py
pdb_chain.py
PermanenceTimes2.py
phipsi.py
pickle_data.py
pickle_timings.py
play_w_pca.py
plotcom.py
plotpy.py
plot_heatmap.py
popen.py
python_def.py
ReadAmberFiles.py
readDCD.py
README_python
regexp.py
removewaters.py
remove_waters.py
residueContacts.py
residueContacts.sh
resid_select.py
ringer_ne_dist.py
rmsd.py
roll.py
RunTime.py
sander_api.py
search.py
smooth_signal.py
smtry_C121.py
smtry_P6122.py
smtry_P6122_send.py
test_rmsd.py
timing_decorator.py
timing_example.py
timing_example2.py
trajectoryContacts.py
traj_com_scatter.py
trans2pdb.py
uc_water.py
walk.py
watersPerCell.py  

/R
  final.tex
  R1.tex
  R2.tex
  R4.tex
  R6.tex
  studentst.R

/readmes
  Amber
  Bash
  C++
  computer_freeze_restart_notes
  crystallography
  GIT
  lyx
  matlab
  matplotlib
  openmm
  pandas
  PBS
  phenix
  prmtop_amber_notes
  pycharm
  pymol
  python
  R
  TCL
  VMD

/tcl
  _sasa_res.tcl
  analyze_1aho_contacts.tcl
  calculatetransformationmatrixnottcl
  change_beta_occupancy.tcl
  COM.tcl
  difference_matrix.tcl
  diffusion_constant.tcl
  frame_rmsd.tcl
  ftomek_atom_interaction.tcl
  Script_S2_calc_Brushweiler.tcl
  tomek_atom_interaction.tcl
  vmd_monomers.tcl
  vmdview.tcl
  vmdview2.tcl

/xtalutil
  /Analyze
    AnalyzeIndivASU.py
    AnalyzeRevSym.py
    GetBfactors.py
    GetSym.py
    GetTrajContacts.py
    GetVolume.py
    MakeASU.py
    MakePDB4Map.py
    md2map.sh
    NoStripMerge.sh
    plotBfac.sh
    plotIndivASU.py
    plotRMSD.py
    plotRMSD_v4.py
    plotRMSDPerASU.py
    plotVolume.py
    ReadAmberFiles.py
    RevSym.py
    RevSym_com.py
    SplitTrajectory.py
    XtalAnalyze.sh
    XtalPlot.sh

  /Auxiliary
    adp.py
    adp_flex.py
    adp2tls.py
    compare_adp.py
    density.py
    difference_vector.py
    distance_matrix.py
    filter_mtz.py
    fit_supercell_com.py
    make_nmd.py
    MolProb_Trajalyze.py
    ncframes
    prepscript_asu.sh
    prepscript_nowat.sh
    pressure.sh
    process_mdout.perl
    pymol_nmodes.py
    StripMerge.sh

  /Phenix
    amber.py
    compile.sh
    getmdgxfrc.{c,h}
    Makefile
    phenix_amber_interface.cpp
    ReadAmberFilesLight.py
    tst_steepest.py
    