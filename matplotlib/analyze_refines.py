#! /usr/bin/env python

import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

def load_data():
  cwd = os.getcwd()
  pdbs = []
  with open('success_pdb.txt', 'r') as f:
    for line in f.readlines():
      pdbs.append(line.strip()[0:4])
  bad_pdbs = []
  with open('amberprep_error_pdb.txt', 'r') as f:
      for line in f.readlines():
        bad_pdbs.append(line.strip()[0:4])
  pdbs = [ i for i in pdbs if i not in bad_pdbs]

  wp = pickle.load( open( "pickle.dat", "rb" ) )
  wp = wp.transpose(2,0,1)  #rows:refinement, cols:pdb_code, item:property
  ti = pickle.load( open( "pickle_timings.dat", "rb" ) )
  return wp, ti

def plot_settings():
  plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
  plt.rc('axes',linewidth=3)
  plt.rc('legend', fontsize=20)
  plt.rc('lines', markeredgewidth=2)
  plt.rc('xtick.minor',size=5)
  plt.rc('xtick.major',size=10)
  plt.rc('lines', linewidth=3)
  sns.set_context("poster")

def violinplot(d, prop):
  print prop
  # d = d.iloc[0:100,:]  #reduced data for testing
  # violin plots not really useful because distributions are boring.Box plots clearer
  # ax = sns.violinplot(d)
  # for label in ax.xaxis.get_ticklabels():
  #   label.set_fontsize(12)
  # ax.set_ylabel('%s' %prop,fontsize=20, labelpad=5)
  # plt.savefig('violin_plots/%s_violin.png' %prop)
  # plt.close()

  print "   box"
  ax = sns.boxplot(d)
  for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(12)
  ax.set_ylabel('%s' %prop,fontsize=20, labelpad=5)
  # ax.set_ylim(-1, 100)
  if prop == 'clash':
    plt.ylim((-1, 20))
  elif prop == 'hbond':
    plt.ylim((-10, 1000))
  elif prop == 'Rama_fav':
    plt.ylim((80, 100))
  elif prop == 'Rama_outl':
    plt.ylim((-2, 10))
  elif prop == 'Rdiff':
    plt.ylim((-0.05, 0.2))
  elif prop == 'Rfree':
    plt.ylim((0.1, 0.7))
  elif prop == 'Rwork':
    plt.ylim((0.1, 0.7))
  elif prop == 'Rotam':
    plt.ylim((-1, 25))
  elif prop == 'h_score':
    plt.ylim((-1, 30))
  plt.savefig('violin_plots/%s_box.png' %prop)
  plt.close()

  print "   box_diff"
  d_diff = d.sub(d.EH,0).iloc[:,1:]
  ax = sns.boxplot(d_diff)
  for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(12)
  ax.set_ylabel('%s' %prop,fontsize=20, labelpad=5)
  # ax.set_ylim(-1, 100)
  plt.savefig('violin_plots/%s_box_diff.png' %prop)
  plt.close()

  # big differences in the normalized difference. Can't really plot it.
  # d_norm = d_diff.div(d.EH/100,0)
  # ax = sns.boxplot(d_norm)
  # for label in ax.xaxis.get_ticklabels():
  #   label.set_fontsize(12)
  # ax.set_ylabel('%s' %prop,fontsize=20, labelpad=5)
  # # ax.set_ylim(-1, 100)
  # plt.savefig('violin_plots/%s_box_norm.png' %prop)
  # plt.close()

def violin_by_reso(wp):
  p1 = sns.color_palette('Paired')[0:4]
  p2 = [tuple(i) for i in sns.light_palette("red", 10)]
  p3 = [tuple(i) for i in sns.light_palette("blue", 10)]
  pal =  p1 + p2[1:-1] + p3[1:-1]
  eh = wp.minor_xs('EH')
  amb = wp.minor_xs('0.025')
  reso_bins = np.array([0.9, 1.0, 2.0, 3.0, 4.0])
  labels=["<1.0", "<2.0", "<3.0", "<4.0"]
  reso_bins = np.arange(.9,4.5,.4)
  labels=[i+.2 for i in reso_bins][:-1]
  eh['reso_range'] = pd.cut(eh['Reso'], reso_bins, labels=labels)
  amb['reso_range'] = pd.cut(amb['Reso'], reso_bins, labels=labels)
  for feature in wp.items:
    # feature = 'clash'
    # import code ; code.interact(local=dict(globals(), **locals()))
    sns.boxplot(eh[feature], eh.reso_range, color = pal[11])
    sns.boxplot(amb[feature], amb.reso_range, color = pal[19], alpha=0.5)
    # plt.ylim(-10,60)
    plt.savefig('violin_reso_plots/%s_reso.png' %feature)
    plt.clf()

def line_by_reso(wp):
  eh = wp.minor_xs('EH')
  amb = wp.minor_xs('0.025')
  # reso_bins = np.array([0.9, 1.0, 2.0, 3.0, 4.0])
  reso_bins = np.arange(.9,4.5,.2)
  labels=[i+.1 for i in reso_bins][:-1]
  eh_gr = eh.groupby(pd.cut(eh['Reso'], reso_bins, labels=labels))
  eh_means = eh_gr.mean()
  amb_gr = amb.groupby(pd.cut(amb['Reso'], reso_bins, labels=labels))
  amb_means = amb_gr.mean()
  # eh_std = eh_gr.aggregate(np.std)
  # amb_std = eh_gr.aggregate(np.std)
  for feature in wp.items:
  # for feature in ['clash']:
    fig=plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    l1 = ax.plot(eh_means.index,   eh_means[feature], '-o',label='Engh&Huber')
    l2 = ax.plot(amb_means.index, amb_means[feature], '-o', label='Amber')
    ax.set_ylabel(feature,fontsize=16, labelpad=5)
    ax.set_xlabel('Resolution ($A$)',fontsize=16, labelpad=5)
    ax.legend(bbox_to_anchor=(0, 0, .999, .999), fontsize=14)
    plt.savefig('line_reso_plots/%s.png' %feature)
    plt.close()

def scatterplot(wp):
  for feature in wp.items:
    eh = wp.minor_xs('EH')
    amb = wp.minor_xs('0.025')
    x = eh[feature]
    y = amb[feature]
    plt.scatter(x,y)
    if min(x) > min(y): minc= min(y)
    else: minc = min(x)
    if max(x) > max(y): maxc = max(x)
    else: maxc = max(y)
    plt.plot([minc,maxc], [minc,maxc], c='r', linewidth=1)
    plt.xlim(minc,maxc)
    plt.ylim(minc,maxc)
    plt.xlabel('Engh&Huber', fontsize=25, labelpad=0)
    plt.ylabel('Amber', fontsize=30)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.title('%s' %feature, fontsize=30)
    plt.savefig("scatter_plots/%s.jpg" %feature)
    plt.close()

def kde_histogram(wp):
  for feature in wp.items:
  # for feature in ['clash']:
    eh = wp.minor_xs('EH')
    amb = wp.minor_xs('0.025')
    x = eh[feature]
    y = amb[feature]

    fig=plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    cmap = sns.color_palette()
    l1 = sns.distplot(x, label = 'Engh&Huber', hist=True, norm_hist=True, color=cmap[0])
    l2 = sns.distplot(y, label = 'Amber', hist=True, norm_hist=True, color=cmap[1])
    # ax.plot([median(x), median(x)], [0, 0.532], color=cmap[0], ls='--')
    # ax.plot([median(y), median(y)], [0, 0.752], color=cmap[1], ls='--')
    if feature == 'clash':
      plt.xlim((-1, 30))
      plt.ylim((0, 0.35))
    if feature == 'Cbeta':
      plt.xlim((--1, 50))
      plt.ylim((0, 0.3))
    if feature == 'Rama_fav':
      plt.xlim((50, 101))
      plt.ylim((0, 0.25))
    if feature == 'Rama_outl':
      plt.xlim((-.2, 5))
      plt.ylim((0, 1.2))
    if feature == 'Rdiff':
      plt.xlim((-0.05, 0.2))
      plt.ylim((0, 25))
    if feature == 'clash':
      plt.xlim((-1, 30))
      plt.ylim((0, 0.35))
    if feature == 'Rfree':
      plt.xlim((0, 0.6))
    if feature == 'RMS_ang':
      plt.xlim((0, 4))
    if feature == 'RMS_bnd':
      plt.xlim((0, .1))
      plt.ylim((0, 100))
    if feature == 'Rotam':
      plt.xlim((-1, 30))
      plt.ylim((0, 0.25))
    if feature == 'Rwork':
      plt.xlim((0, 0.6))

    ax.tick_params(axis='both', labelsize=18)
    for spine in ax.spines.values():
      spine.set_linewidth(2)
      spine.set_color('k')
    # ax.set_xticklabels([0,.01,.02,.03,.04,.05,.06,.07,.08])
    ax.legend(bbox_to_anchor=(0, 0, .999, .999), fontsize=14)
    ax.set_xlabel('%s' %feature, fontsize=28)
    fig.tight_layout()
    plt.savefig("kde_plots/%s.png" %feature)
    plt.close()

def print_stats(wp,ti):
  print "=== TIMINGS ==="
  mean_time = ti.mean()[2]
  b = (ti['amber']>ti['EH'])
  print " Mean amber time as percent of EH time: %5.2f%%"  %mean_time
  print " Number of amber runs longer than EH runs: %d = %5.2f%%" %(sum(b), 100.*sum(b)/len(b))
  print ""

  print "=== RESOLUTION ==="
  print "Bin         No.  %Total"
  reso_bins = np.array([0.9, 1.0, 2.0, 3.0, 4.0, 5.0])
  labels = ['<1.0A', '1.0-2.0A', '2.0-3.0A', '3.0-4.0A', '>4.0A']
  r = wp.minor_xs('EH')
  gb = r.groupby(pd.cut(r['Reso'], reso_bins, labels=labels))
  for label in labels:
    print " %8s  %4d  %5.2f%%"  %(label, len(gb.groups[label]), 100.*len(gb.groups[label])/len(r))
  print ""

  print "=== QUALITY ==="
  print "Feature     No.AmberBetter   PercentAmberBetter"
  eh = wp.minor_xs('EH')
  amb = wp.minor_xs('0.025')
  for feature in wp.items:
    if feature in ['hbond', 'Rama_fav']:
      better = eh[feature]<=amb[feature]
    else:
      better = eh[feature]>=amb[feature]
    print " %9s      %4d          %5.2f%%" %(feature, sum(better), 100.*sum(better)/len(eh))
  print ""


if __name__ == "__main__":
  wp, ti = load_data()
  plot_settings()
  # for prop in wp.items:
  #   d = wp[prop]
  #   violinplot(d, prop)
  # violinplot(ti, 'timing')
  # violin_by_reso(wp)
  # line_by_reso(wp)
  # scatterplot(wp)
  # kde_histogram(wp)
  #print_stats(wp, ti)
  #import code ; code.interact(local=dict(globals(), **locals()))
  d = wp['h_score']
  violinplot(d, 'h_score')
  sys.exit()
