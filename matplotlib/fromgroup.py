import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(20, 20))
ax = fig.add_subplot(111)
ax.set_title("Subtitle")
ax.plot([1, 2, 3], [3, 2, 1])
st = fig.suptitle("Horray!", fontsize=20)
plt.savefig("test.png")
