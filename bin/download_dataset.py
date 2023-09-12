import click
from openff.qcsubmit.results import (
    OptimizationResultCollection,
    TorsionDriveResultCollection,
)
from qcportal import FractalClient


@click.command()
@click.option("--output", "-o")
@click.option("--dataset", "-d", multiple=True)
@click.option(
    "--type",
    "-t",
    "type_",
    type=click.Choice(["opt", "td"]),
    help="The type of dataset to download",
)
@click.option("--spec-name", "-s", default="default")
def main(output, dataset, type_, spec_name):
    client = FractalClient()
    match type_:
        case "opt":
            cls = OptimizationResultCollection
        case "td":
            cls = TorsionDriveResultCollection
        case t:
            # should be unreachable because of click
            raise ValueError(f"unrecognized data set type {t}")

    dataset = cls.from_server(
        client=client,
        datasets=dataset,
        spec_name=spec_name,
    )

    with open(output, "w") as out:
        out.write(dataset.json(indent=2))


if __name__ == "__main__":
    main()
