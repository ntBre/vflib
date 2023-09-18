from collections import defaultdict
from enum import Enum

from openff.toolkit import ForceField
from tqdm import tqdm

from vflib import load_dataset
from vflib.utils import Timer


class ParameterType(Enum):
    Bonds = "Bonds"
    Angles = "Angles"
    Torsions = "ProperTorsions"


def check_coverage(forcefield, dataset, parameter_type: ParameterType):
    """Check parameter coverage in `forcefield` using `dataset`."""

    print("checking coverage with")
    print(f"forcefield = {forcefield}")
    print(f"dataset = {dataset}")

    timer = Timer()

    ff = ForceField(forcefield, allow_cosmetic_attributes=True)
    td_data = load_dataset(dataset)

    timer.say("finished loading collection")

    h = ff.get_parameter_handler(parameter_type.value)
    tors_ids = [p.id for p in h.parameters]

    records_and_molecules = td_data.to_molecules()

    timer.say("finished to_records")

    results = defaultdict(int)
    for molecule in tqdm(records_and_molecules, desc="Counting results"):
        all_labels = ff.label_molecules(molecule.to_topology())[0]
        torsions = all_labels[parameter_type.value]
        for torsion in torsions.values():
            results[torsion.id] += 1

    timer.say("finished counting results")

    got = len(results)
    want = len(tors_ids)
    pct = 100.0 * float(got) / float(want)
    print(f"{got} / {want} ({pct:.1f}%) ids covered:")

    for id in tors_ids:
        smirk = h.get_parameter(dict(id=id))[0].smirks
        print(f"{id:5}{results[id]:5}   {smirk}")

    missing_ids = [k for k in results.keys() if results[k] == 0]
    missing_smirks = [
        h.get_parameter(dict(id=p))[0].smirks for p in missing_ids
    ]
    print("\nmissing ids:")
    for i, (id, smirk) in enumerate(zip(missing_ids, missing_smirks)):
        print(f"{i:5}{id:>7}   {smirk}")

    timer.say("finished")


def check_record_coverage(forcefield, dataset, parameter_type: ParameterType):
    """Like `check_coverage` but calls `to_records` instead of `to_molecules`
    and returns the list of QCArchive record ids that matched each parameter

    """
    print("checking record coverage with")
    print(f"forcefield = {forcefield}")
    print(f"dataset = {dataset}")

    timer = Timer()

    ff = ForceField(forcefield, allow_cosmetic_attributes=True)
    dataset = load_dataset(dataset)

    timer.say("finished loading collection")

    records_and_molecules = dataset.to_records()

    timer.say("finished to_records")

    results = defaultdict(list)
    for record, molecule in tqdm(
        records_and_molecules, desc="Counting results"
    ):
        all_labels = ff.label_molecules(molecule.to_topology())[0]
        labels = all_labels[parameter_type.value]
        for label in labels.values():
            results[label.id].append(record.id)

    timer.say("finished")

    return results
