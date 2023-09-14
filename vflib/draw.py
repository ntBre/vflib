from openff.toolkit import Molecule
from rdkit.Chem.Draw import MolsToGridImage, rdDepictor, rdMolDraw2D
from rdkit.Chem.rdmolops import RemoveHs


def draw_rdkit(
    mol: Molecule,
    smirks,
    matches=None,
    filename=None,
    show_all_hydrogens=True,
    max_matches=None,
):
    """Draw `mol` using rdkit and write the resulting PNG to `filename`.

    `smirks` is a target smirks to highlight in the resulting image.
    Adapted from openff.toolkit.Molecule.visualize
    """
    if matches is None:
        matches = mol.chemical_environment_matches(smirks)
    rdmols = []
    highlight_atom_lists = []
    for m in matches:
        highlight_atom_lists.append(sorted(m))
        rdmol = mol.to_rdkit()
        if not show_all_hydrogens:
            rdmol = RemoveHs(rdmol, updateExplicitCount=True)
        rdDepictor.SetPreferCoordGen(True)
        rdDepictor.Compute2DCoords(rdmol)
        rdmol = rdMolDraw2D.PrepareMolForDrawing(rdmol)
        rdmols.append(rdmol)

    if max_matches is not None:
        rdmols = rdmols[:max_matches]
        highlight_atom_lists = highlight_atom_lists[:max_matches]

    BASE = 450
    match len(rdmols):
        case 1:
            size = (BASE, BASE)
            per_row = 1
        case 2 | 3 | 4:
            size = (BASE // 2, BASE // 2)
            per_row = 2
        case 5 | 6:
            size = (BASE // 3, BASE // 3)
            per_row = 3
        case _:
            # fall back on the defaults
            size = (200, 200)
            per_row = 3

    png = MolsToGridImage(
        rdmols,
        highlightAtomLists=highlight_atom_lists,
        subImgSize=size,
        molsPerRow=per_row,
        returnPNG=True,
    )

    if filename is not None:
        with open(filename, "wb") as out:
            out.write(png)
