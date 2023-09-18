import click
from vflib.coverage import ParameterType, check_coverage


@click.command()
@click.option("--forcefield", "-f")
@click.option("--dataset", "-d")
@click.option(
    "--parameter-type",
    "-p",
    type=click.Choice(["bond", "angle", "torsion"], case_sensitive=False),
)
def main(forcefield, dataset, parameter_type):
    match parameter_type:
        case "bond":
            parameter_type = ParameterType.Bonds
        case "angle":
            parameter_type = ParameterType.Angles
        case "torsion":
            parameter_type = ParameterType.Torsions

    check_coverage(forcefield, dataset, parameter_type)


if __name__ == "__main__":
    main()
