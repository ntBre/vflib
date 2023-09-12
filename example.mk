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

init := initial.offxml

# select optimization parameters to optimize
opt-smirks.json: core-opt.json $(init)
	select_parameters.py opt \
	--dataset $<		\
	--forcefield $(init)	\
	--output-smirks $@

# select torsiondrive parameters to optimize
td-smirks.json: core-td.json $(init)
	select_parameters.py td \
	--dataset $<		\
	--forcefield $(init)	\
	--output-smirks $@	\
	--ring-torsions explicit_ring_torsions.dat

# initialize force field with the modified seminario method
msm.offxml: core-opt.json $(init)
	create_msm.py                        \
	--initial-force-field $(init)           \
	--optimization-dataset $<		\
	--working-directory working-directory   \
	--output $@
