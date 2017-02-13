import os.path

__all__ = []

for filename in os.listdir(os.path.dirname(__file__)):
	if filename.startswith("graphclass_") and filename.endswith(".py"):
		__all__.append(filename[:-3])
