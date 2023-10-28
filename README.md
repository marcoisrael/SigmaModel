# The 2-d O(3) model

In the 2-d O(3) model $\vec{e_{x}}\in S{{}^2}$ is a 3-component unit vector field defined at each point in a 2-dimensional euclidean spacetime. Lattice action is defined by eq (1) and Q is the topological charge defined by eq (2).

$$S[\vec{e}]=-\beta\sum\vec{e}_x\cdot\vec{e}_y \tag{1}$$

$$Q[\vec{e}]=\frac{1}{4\pi}\sum_{t_{xyz}}A_{xyz}\in\mathbb{Z} \tag{2}$$

We consider the 2-d O(3) model using numerical simulations as lattice action. We'll use five different algorithms. Lexicographical Metropolis, Random Metropolis, Lexicographical Glauber, Random Glauber and Single Cluster. I performed $10^{5}$ cooling simulations for $\tau_{Q}\in\{20,30,40\}$ for $V=64$ and $T=4$ to $T=0$ in each algorithm.
