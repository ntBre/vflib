#!/usr/bin/env python

import json

import click
import numpy as np
from openff.qcsubmit.results import (
    OptimizationResultCollection,
    TorsionDriveResultCollection,
)
from openff.toolkit.typing.engines.smirnoff.forcefield import ForceField
from vflib.curate import select_parameters


@click.group()
def cli():
    pass


@cli.command("td")
@click.option("--dataset", required=True)
@click.option("--forcefield", required=True)
@click.option("--output-smirks", required=True)
@click.option("--ring-torsions", required=True)
def select_td(dataset, forcefield, output_smirks, ring_torsions):
    dataset = TorsionDriveResultCollection.parse_file(dataset)

    ff = ForceField(
        forcefield,
        allow_cosmetic_attributes=True,
    )

    explicit_ring_torsions = np.loadtxt(ring_torsions, dtype=str)

    selected_parameters = select_parameters(
        dataset,
        ["ProperTorsions"],
        force_field=ff,
        explicit_ring_torsions=explicit_ring_torsions,
    )

    with open(output_smirks, "w") as f:
        json.dump(selected_parameters, f, indent=2)


@cli.command("opt")
@click.option("--dataset", required=True)
@click.option("--forcefield", required=True)
@click.option("--output-smirks", required=True)
def select_opt(dataset, forcefield, output_smirks):
    dataset = OptimizationResultCollection.parse_file(dataset)

    ff = ForceField(
        forcefield,
        allow_cosmetic_attributes=True,
    )

    selected_parameters = select_parameters(
        dataset,
        ["Bonds", "Angles"],
        force_field=ff,
    )
    with open(output_smirks, "w") as file:
        json.dump(selected_parameters, file, indent=2)


if __name__ == "__main__":
    cli()
