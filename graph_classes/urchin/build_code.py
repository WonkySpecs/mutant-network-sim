n = nodes // 2
if nodes % 2 == 0:
	for c in range(n - 1):
		for c2 in range(c + 1, n):
			G.add_edge(c, c2)
	for m in range(n):
		G.add_edge(m, m + n)
else:
	print("nodes must be even for an Urchin graph")
