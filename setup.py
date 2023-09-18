import os
import stat

from setuptools import setup

with open("example.mk", "r") as inp:
    contents = inp.read()

example = "bin/example_makefile.py"
if os.path.exists(example):
    os.remove(example)

with open(example, "w") as out:
    out.write(
        f"""#!/usr/bin/env python
print(r\"\"\"{contents}\"\"\")
"""
    )
st = os.stat(example)
os.chmod(example, st.st_mode | stat.S_IEXEC)

setup(
    scripts=[
        "bin/check_coverage.py",
        "bin/create_fb_inputs.py",
        "bin/create_msm.py",
        "bin/download_dataset.py",
        "bin/example_makefile.py",
        "bin/select_parameters.py",
    ],
)
