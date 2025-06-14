from decimal import Decimal

import typer
from rich.console import Console
from rich.table import Table

from sigmavest.dependency import resolve
from sigmavest.track.domain import Transaction
from sigmavest.track.service import TransactionService

from ..validators import validate_date, validate_decimal, validate_portfolio_id

app = typer.Typer()
console = Console()

DATA_PATH = ".dev/track_data"
DB_PATH = ":memory:"


@app.command(name="list")
def list_():
    """List transactions"""
    try:
        service: TransactionService = resolve(TransactionService)
        transactions = service.list_transactions()

        table = Table(
            title="Transactions",
            show_header=True,
            header_style="bold magenta",
        )

        field_names = Transaction.get_field_names()
        for f in field_names:
            table.add_column(f)

        for row in transactions:
            values = [getattr(row, field) for field in field_names]
            table.add_row(*map(str, values))

        console.print(table)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def buy(
    portfolio_id: str = typer.Argument(
        ..., help="ID of the portfolio to which the transaction belongs", callback=validate_portfolio_id
    ),
    ticker: str = typer.Argument(..., help="Ticker symbol of the asset to buy"),
    quantity: str = typer.Argument(..., help="Quantity of the asset to buy", callback=validate_decimal),
    price: str = typer.Argument(..., help="Price per unit of the asset", callback=validate_decimal),
    fees: str = typer.Argument(..., help="Transaction fees for the buy", callback=validate_decimal),
    amount_paid: str = typer.Argument(..., help="Total amount paid for the transaction", callback=validate_decimal),
    currency: str = typer.Argument(..., help=""),
    date: str = typer.Argument(..., help="Date of the transaction (YYYY-MM-DD)", callback=validate_date),
):
    """Record a buy transaction"""
    try:
        fees = fees or Decimal("0")  # type: ignore
        transaction = Transaction(
            id=None,
            portfolio_id=portfolio_id,
            date=date,  # type: ignore
            transaction_type="BUY",
            ticker=ticker,
            quantity=quantity,  # type: ignore
            price=price,  # type: ignore
            fees=fees,  # type: ignore
            amount_paid=Decimal(amount_paid or quantity * price + fees),  # type: ignore
            currency=currency,
            exchange_rate=None,
        )
        service: TransactionService = resolve(TransactionService)
        transaction = service.add_transaction(transaction)

        console.print(f"[green]Transaction recorded: {transaction}[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
