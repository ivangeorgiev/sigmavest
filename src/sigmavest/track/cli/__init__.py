import typer
from rich.console import Console
from rich.table import Table

from sigmavest.track.repository.db import TrackDb
from sigmavest.dependency import resolve

from .portfolio import app as portfolio_app
from .transaction import app as transaction_app

app = typer.Typer()

app.add_typer(portfolio_app, name="portfolio")
app.add_typer(transaction_app, name="transaction")

console = Console()


@app.command()
def summary():
    """
    Provides a summary of TRACK-related commands.
    """
    print("This is the `track` command summary.")


@app.command()
def query(
    query: str = typer.Argument(..., help="SQL query to execute against the DuckDB database"),
):
    """
    Execute a SQL query against the DuckDB database.
    """

    try:
        db: TrackDb = resolve(TrackDb)

        table = Table(
            title=query,
            show_header=True,
            header_style="bold magenta",
        )

        results = db.db.execute(query)

        if results:
            field_names = [col[0] for col in results.description]  # type: ignore
            for f in field_names:
                table.add_column(f)

            for row in results.fetchall():
                table.add_row(*map(str, row))

            console.print(table)

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
