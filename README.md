# vflib
tools for optimizing valence terms in OpenFF force fields

# Usage
The basic usage is through the provided scripts in `/bin`. `download_dataset.py`
is used to download data sets from QCArchive; `select_parameters.py` selects the
parameters to optimize using
[ForceBalance](https://github.com/leeping/forcebalance); `create_msm.py`
generates initial force field values using the [Modified Seminario
Method](https://doi.org/10.1021/acs.jctc.7b00785), as implemented in
[QUBEKit](https://github.com/qubekit/QUBEKit); and `create_fb_inputs.py`
converts the outputs of the other scripts into input for ForceBalance.

Rather than running each of these by hand in that sequence, I recommend using a
Makefile. This way, when one of the scripts inevitably crashes, you can resume
from the last finished step. As such, the package also provides the
`example_makefile.py` script, which writes the contents of `example.mk` to
stdout. With all of that said, basic usage could look something like:

``` shell
# installing vflib and its dependencies inside the vflib repo
mamba env create -f devtools/conda-envs/dev.yaml -n vflib
mamba activate vflib
pip install -e .

# work on your project
cd /path/to/project
example_makefile.py > Makefile
make out.tar.gz -j2 # -j is optional, but td and opt parts can run concurrently
```

`out.tar.gz` is the final product of the Makefile: an archive of all of the
ForceBalance inputs, ready to be copied to a supercomputer. Of course, you'll
likely need to edit the generated Makefile to suit your needs. By default it
downloads quite small data sets and expects you to have your initial force field
in a file called `initial.offxml`. It also expects several other files:
- `explicit_ring_torsions.dat` - a list of ring torsions for selection torsion
  parameters
- `smiles-to-exclude.dat` - a list of SMILES strings to exclude from the
  training data
- `smarts-to-exclude.dat` - a list of SMARTS patterns to exclude from the
  training data

Everything else is generated by the included scripts.

# Dependencies
See [devtools/conda-envs/dev.yaml](devtools/conda-envs/dev.yaml) for the most
up-to-date list. The current list is shown below, but I'll probably forget to
update this as the environment changes:

``` yaml
dependencies:
  - python
  - pip
# openff stuff
  - openff-toolkit
  - openff-qcsubmit
  - openff-units
  - openff-bespokefit
# misc chemistry
  - qubekit
# qcarchive
  - qcportal
# utilities
  - click
  - tqdm
  - numpy
```
