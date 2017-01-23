for i in range(nodes - 1):
	G.add_edge(i, i + 1)
G.add_edge(0, nodes - 1)
