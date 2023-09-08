from ci.report import generate_report
import click


@click.command
@click.argument("year", type=int)
@click.argument("month", type=int)
def cli(year: int, month: int):
    print(f"Running report for: {year}-{month}")
    generate_report(year, month)


if __name__ == "__main__":
    cli()
