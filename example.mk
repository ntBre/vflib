# download an optimization data set from QCArchive
core-opt.json:
	download_dataset.py --output $@						\
	--dataset "OpenFF multiplicity correction optimization set v1.0"	\
	--type opt

# download a torsiondrive data set from QCArchive
core-td.json:
	download_dataset.py --output $@						\
	--dataset "OpenFF multiplicity correction torsion drive data v1.1"	\
	--type td
