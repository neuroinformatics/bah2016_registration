import ipyparallel as ipp
c = ipp.Client()
print("Number of engines: %d" % len(c.ids))
print(c.ids)
