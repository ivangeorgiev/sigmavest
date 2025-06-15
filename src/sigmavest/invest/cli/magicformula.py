import typer
from rich.console import Console

from sigmavest.dependency import resolve
from sigmavest.invest.adapter.magicformula.magic_formula_scraper import MagicFormulaScraper
from sigmavest.invest.service.database import DatabaseService
from sigmavest.settings import Settings

app = typer.Typer()
console = Console()
settings = resolve(Settings)


@app.command()
def scrape(
    username: str = typer.Option(None, "--username", "-u", help="Username."),
    password: str = typer.Option(None, "--password", "-p", help="User password."),
    output_file: str = typer.Option(None, "--output-file", "-o", help="Output file name."),
    output_table: str = typer.Option(None, "--output-table", "-t", help="Output table name."),
    min_market_cap: int = typer.Option(
        settings.MAGIC_FORMULA_MIN_MARKET_CAP, "--min-market-cap", "-m", min=1, help="Miniumum market capitalization."
    ),
):
    username = username or settings.MAGIC_FORMULA_USERNAME
    password = password or settings.MAGIC_FORMULA_PASSWORD

    try:
        if not username or not password:
            raise ValueError("User credentials are not provided.")
        scraper = MagicFormulaScraper(username, password)
        results = scraper.scrape(min_market_cap)
        if output_file:
            results.to_csv(output_file)
            console.print(f"[green]Results exported to '{output_file}'[/green]")
        if output_table:
            service = resolve(DatabaseService)
            results.to_sql(output_table, service.db.db)
        console.print(results)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
