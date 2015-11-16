#! /usr/bin/env phenix.python
import scitbx.array_family.flex
from libtbx.introspection import virtual_memory_info
from libtbx.utils import Sorry
from libtbx.utils import get_memory_from_string

kilobyte=1024
megabyte=kilobyte*1024
vmi=virtual_memory_info()
vms=vmi.virtual_memory_size()
maximum_memory=8000*megabyte

print vmi
print vms//megabyte
print float(vms)/maximum_memory*100
