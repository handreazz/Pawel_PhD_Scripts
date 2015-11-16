#=======================================================================
# DRAW SECONDARY STRUCTURE BAR
#=======================================================================
ss_str='''C B C C H H H H H H H H H H H C T T T G G G C C H H H H H H H H H 
H H H T T B T T T E E E T T T T C E E E T T T T E E T T T T C B T T T T 
T T T C T T T T C B G G G G C T T T H H H H H H H H H H H H H H C C C G 
G G C H H H H H H H T T T C G G G G G T T T C C '''
ss=ss_str.split()

dict1={
	'H':'b',
	'I':'b',
	'G':'b',
	'E':'r',
	'B':'r',
	'b':'r',
	'T':'y',
	'C':'g'
}

from matplotlib.patches import Rectangle
for i in range(len(ss)):
	if i==0:
		curr_ss=ss[i]
		len_ss=1
		start_pos=0.5
	else:
		prev_ss=curr_ss
		curr_ss=ss[i]
		if dict1[curr_ss]==dict1[prev_ss]:
			len_ss+=1
			
		else:
			el1 = Rectangle((start_pos,1), len_ss, 2, facecolor=dict1[prev_ss], fill='True',alpha=1)
			ax.add_patch(el1)		
			len_ss=1
			start_pos=i+0.5
el1 = Rectangle((start_pos,1), len_ss, 2, facecolor=dict1[prev_ss], fill='True',alpha=1)
ax.add_patch(el1)								
			
el1 = Rectangle((4,60), 16, 19.5, ec='k',linewidth=2, fill=False,alpha=1)
el2 = Rectangle((5,65), 5, 1, facecolor='b')
el3 = Rectangle((5,68), 5, 1, facecolor='r')
el4 = Rectangle((5,71), 5, 1, facecolor='y')
el5 = Rectangle((5,74), 5, 1, facecolor='g')
ax.add_patch(el1)
ax.add_patch(el2)
ax.add_patch(el3)
ax.add_patch(el4)
ax.add_patch(el5)
plt.annotate('Helix',xy=(12,68), xytext=(12,65))			
plt.annotate('Sheet',xy=(12,71), xytext=(12,68))			
plt.annotate('Turn',xy=(12,68), xytext=(12,71))			
plt.annotate('None',xy=(12,68), xytext=(12,74))				
plt.annotate('STRIDE sec_strc',xy=(12,68), xytext=(5,77))	
