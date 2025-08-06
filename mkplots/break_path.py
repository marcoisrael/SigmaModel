import numpy as np
import matplotlib.pyplot as plt
x = np.array([4,3,4,5,4,3,2,3,2,1,2,3,4,2])
labels = ["0","a","2a","3a","4a",
               "5a","6a","7a",r"$\dots$",
               r"$(n-4)a$",r"$(n-3)a$",
               r"$(n-2)a$",r"$(n-1)a$","t"]
fig, ax = plt.subplots()
ax.set(xlim=(0,13), ylim=(0,6), yticks=[])
ax.set_xticks(np.arange(14), labels, rotation=90)
for i in np.arange(13):
    ax.plot([i,i],[0,x[i]], color="gray", linestyle="dashed")
ax.plot(x, color="tab:blue")
ax.text(-0.5,3.9, "q",fontsize=18)
ax.text(13.1,1.8, "q'",fontsize=18)

fig.savefig("output/break_path.pdf", format="pdf" , bbox_inches="tight")

