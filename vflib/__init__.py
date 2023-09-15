import json
from typing import Literal, Union

from openff.qcsubmit.results import (
    OptimizationResultCollection,
    TorsionDriveResultCollection,
)
from openff.toolkit import Molecule


# helper class for returning a sized iterator
class Molecules:
    def __init__(self, dataset):
        self.data = [v for value in dataset.entries.values() for v in value]
        self.length = len(self.data)

    def __len__(self):
        return self.length

    def __iter__(self):
        for r in self.data:
            yield Molecule.from_mapped_smiles(
                r.cmiles, allow_undefined_stereo=True
            )


def to_molecules(dataset) -> Molecules:
    return Molecules(dataset)


# monkey patch for cute calls
TorsionDriveResultCollection.to_molecules = to_molecules
OptimizationResultCollection.to_molecules = to_molecules


def load_dataset(
    dataset: str,
    type_: Literal["torsion", "optimization"] = None,
) -> Union[OptimizationResultCollection, TorsionDriveResultCollection]:
    """Peeks at the first entry of `dataset` to determine its type and then
    loads it appropriately. If `type_` is passed, use that as the type instead.

    Raises a `TypeError` if the first entry is neither a `torsion`
    record nor an `optimization` record.

    """
    if type_ is None:
        with open(dataset, "r") as f:
            j = json.load(f)
        entries = j["entries"]
        keys = entries.keys()
        assert len(keys) == 1  # only handling this case for now
        key = list(keys)[0]
        type_ = j["entries"][key][0]["type"]

    match type_:
        case "torsion":
            return TorsionDriveResultCollection.parse_file(dataset)
        case "optimization":
            return OptimizationResultCollection.parse_file(dataset)
        case t:
            raise TypeError(f"Unknown result collection type: {t}")
