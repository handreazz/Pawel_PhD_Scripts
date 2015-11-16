#! /bin/bash

function print_array  {
	echo ${colors[*]}
        #~ array_name=$1
        #~ echo $array_name[2]
        #~ eval echo \${$array_name[2]}
        #~ return
}
#~ 
#~ 
#~ colors=( 1 3 6 9 )
#~ 
#~ print_array colors

#!/bin/bash

    array=( "$@" )
	echo ${array[*]}
    #~ array_string="$1[*]"
    #~ echo array_string
    #~ echo $1
    #~ loc_array=(${!array_string})
    #~ echo ${loc_array[*]}
    #~ newarray=(${colors[*]})
    #~ newstring="$1"
    #~ newarray=(${$newstring[*]})
    #~ echo ${newarray[1]}


# create an array and display contents
colors=('Pink' 'Light Gray' 'Green')
#~ echo ${colors[*]}

# call function with positional parameter $1 set to array's name
print_array 


