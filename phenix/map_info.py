import sys, os
import iotbx.ccp4_map

# this file works
print "="*80+"\n"
file_name = sys.argv[1]
map1 = iotbx.ccp4_map.map_reader(file_name=file_name)
map_data1 = map1.data.as_double()
map1.show_summary()
map1.space_group_number
map1.unit_cell_grid



# import code ; code.interact(local=dict(globals(), **locals()))