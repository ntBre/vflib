#!/usr/bin/env python
print(r"""# download an optimization data set from QCArchive
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
	create_msm.py				\
	--initial-force-field $(init)           \
	--optimization-dataset $<		\
	--working-directory working-directory   \
	--output $@

# generate the ForceBalance input. this creates a bunch of stuff, so use a dummy
# fb-ready file to indicate that it's finished
fb-deps := smiles-to-exclude.dat smarts-to-exclude.dat core-opt.json	\
core-td.json opt-smirks.json td-smirks.json msm.offxml

fb-ready: $(fb-deps)
	rm -r fb-fit/targets
	mkdir -p fb-fit/targets
	create_fb_inputs.py                                     \
	--tag                       "fb-fit"                    \
	--optimization-dataset      core-opt.json		\
	--torsion-dataset           core-td.json		\
	--valence-to-optimize       opt-smirks.json		\
	--torsions-to-optimize      td-smirks.json		\
	--forcefield                msm.offxml                  \
	--smiles-to-exclude         smiles-to-exclude.dat	\
	--smarts-to-exclude         smarts-to-exclude.dat	\
	--max-iterations            100                         \
	--port                      55387                       \
	--output-directory          "output"                    \
	--verbose
	date > $@

# pack up the generated files for copying to a supercomputer
fb-fit/targets.tar.gz: fb-ready
	rm $@
	cd fb-fit; tar cfz targets.tar.gz targets

deps := $(addprefix fb-fit/,forcefield/force-field.offxml optimize.in	\
targets.tar.gz)
out.tar.gz: fb-ready $(deps)
	rm $@
	tar cfz $@ $(deps)
""")
