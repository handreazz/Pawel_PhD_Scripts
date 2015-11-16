import sys, os
import glob
import hdf5_getters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_files(basedir,ext='.h5') :
    allfiles = []
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        for f in files:
            allfiles.append(f)
    return allfiles

def get_getters():  
  getters = filter(lambda x: x[:4] == 'get_', hdf5_getters.__dict__.keys())
  getters.remove("get_num_songs")
  getters = np.sort(getters)
  return getters

# not efficient (opening/closing files) but fast enough for this miniproject
def get_attributes(files, getters):
  for getter in getters:
    getter_func = hdf5_getters.__getattribute__(getter)
    attrib = []
    for f in files:
      h5 = hdf5_getters.open_h5_file_read(f)
      attrib.append( getter_func(h5) )
      h5.close()
    yield getter, attrib
    
bd='/home/pawelrc/dataIncubator/challenge3/MillionSongSubset/data'
allfiles = get_files(bd)
getters = get_getters()
# ended up being easier to just write the features I was interested in
getters = [
       'get_artist_familiarity',
       'get_artist_hotttnesss',
       'get_artist_mbtags',
       'get_artist_name',
       'get_artist_terms',
       'get_bars_start',
       'get_beats_start',
       'get_danceability',
       'get_duration',
       'get_end_of_fade_in',
       'get_energy',
       'get_key',
       'get_loudness',
       'get_mode',
       'get_release',
       'get_sections_start',
       'get_segments_pitches', 
       'get_song_hotttnesss',
       'get_start_of_fade_out',
       'get_tempo',
       'get_time_signature',
       'get_title',
       'get_year'
       ]

# build data frame       
df = pd.DataFrame()
for getter, attribute in get_attributes(allfiles, getters):
  print getter
  df[getter[4:]] = attribute

# some data adjustments  
df['n_sections'] = df['sections_start'].apply(lambda x: len(x))
df['n_beats'] = df['beats_start'].apply(lambda x: len(x))
df['n_bars'] = df['bars_start'].apply(lambda x: len(x))
df['mean_pitch'] = df['segments_pitches'].apply(lambda x: np.mean(x))
df['year'][df['year']==0] = np.nan
df.drop(['sections_start', 'beats_start', 'bars_start', 
         'segments_pitches'],inplace=True,axis=1)

# save for future
print "saving"
df.to_csv('mysongs.csv')

# explore histograms
features = [u'artist_familiarity', u'artist_hotttnesss',
            u'duration', u'end_of_fade_in', 
            u'key', u'loudness',
            u'song_hotttnesss', u'start_of_fade_out', u'tempo', 
            u'time_signature', u'year', u'n_sections', u'n_beats', 
            u'n_bars', u'mean_pitch']
for feature in features:
  d = df[feature]
  d = d[(d.notnull()) & (d !=0)]
  sns.distplot(d)
  plt.show()
  plt.clf()


# explore scatter plots / joint distributions
for feature1 in [ u'artist_familiarity', u'artist_hotttnesss',
                   u'song_hotttnesss', u'year']:
  for feature2 in [ u'duration', u'end_of_fade_in', 
                     u'key', u'loudness',
                     u'start_of_fade_out', u'tempo', 
                     u'time_signature', u'n_sections', u'n_beats', 
                     u'n_bars', u'mean_pitch']:
    d = df[[feature1, feature2]]
    filt1 = d.iloc[:,0:2].notnull().all(axis=1)
    filt2 = (d.iloc[:,0:2] !=0).all(axis=1)
    d = d[(filt1) & (filt2)]
    with sns.axes_style("white"):
      sns.jointplot(d[feature1], d[feature2])
      plt.show()
      plt.clf()

# make plots for presentation
for feature1 in [ u'song_hotttnesss']:
  for feature2 in [u'loudness', u'tempo', u'mean_pitch']:
    d = df[[feature1, feature2]]
    filt1 = d.iloc[:,0:2].notnull().all(axis=1)
    filt2 = (d.iloc[:,0:2] !=0).all(axis=1)
    d = d[(filt1) & (filt2)]
    if feature2 == 'loudness':
      d = d[(d.iloc[:,1]>-25) & (d.iloc[:,1]<0)]
    if feature2 == 'tempo':
      d = d[(d.iloc[:,1]>50) & (d.iloc[:,1]<225)]
    if feature2 == 'mean_pitch':
      d = d[(d.iloc[:,1]>0.2) & (d.iloc[:,1]<0.6)]
    with sns.axes_style("white"):
      x = sns.jointplot(d[feature1], d[feature2], kind='kde')
      x.ax_joint.set_xlim([0,1])
      if feature2 == 'mean_pitch':
        x.ax_joint.set_ylim([0.15,0.6])
      plt.savefig('%s_VS_%s.png' %(feature1, feature2))
      plt.clf()

d = df[['key', 'loudness', 'tempo', 'time_signature', 'year']]
d = d[(d['year'].notnull()) & (d['year'] >1970) ]
year_bins = np.arange(1970, 2011, 10)
d['year_range']=pd.cut(d['year'], year_bins, labels=[1970, 1980, 1990, 2000])
for feature in ['key', 'loudness', 'tempo', 'time_signature']:
  sns.violinplot(d[feature], d.year_range, names = ['70s', '80s', '90s', '00s'])
  plt.savefig('vp_year_%s.png' %feature)
  plt.clf()

for feature_name in ['key', 'loudness', 'tempo', 'time_signature']:
  d = df[['song_hotttnesss', feature_name]]
  d = d[d['song_hotttnesss'].notnull()]
  hotness_bins = np.arange(0,1.1,0.2)
  d['song_hotness_range']=pd.cut(d['song_hotttnesss'], hotness_bins)
  sns.violinplot(d[feature_name], d.song_hotness_range)
  plt.savefig('vp_hotness_%s.png' %feature_name)
  plt.clf()
