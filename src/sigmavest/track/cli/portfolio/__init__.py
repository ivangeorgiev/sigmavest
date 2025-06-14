import typer
from rich.console import Console
from rich.table import Table


from sigmavest.track.domain import Portfolio
from sigmavest.track.service import PortfolioService
from sigmavest.dependency import resolve

app = typer.Typer()
console = Console()


@app.command()
def list():
    """List porfolios"""
    try:
        service = resolve(PortfolioService)
        table = Table(
            title="Portfolios",
            show_header=True,
            header_style="bold magenta",
        )

        field_names = Portfolio.get_field_names()
        for f in field_names:
            table.add_column(f)

        for row in service.list_portfolios():
            table.add_row(str(row.id), row.name, row.description)

        console.print(table)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
