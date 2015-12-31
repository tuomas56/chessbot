from setuptools import setup, find_packages
setup(name="chess", 
	package_dir={'':'src'},
	version="0.1",
	packages=find_packages('src'),
	scripts=['src/play'])
