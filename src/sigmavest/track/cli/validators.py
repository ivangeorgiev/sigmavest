import datetime
from decimal import Decimal, InvalidOperation
import typer

from sigmavest.track.service import PortfolioService
from sigmavest.dependency import resolve


def validate_decimal(value: str) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation:
        raise typer.BadParameter(f"{value} is not a valid Decimal")


def validate_transaction_type(value: str) -> str:
    if value not in ["BUY", "SELL"]:
        raise typer.BadParameter(f"{value} is not a valid transaction type")
    return value


def validate_portfolio_id(value: str) -> str:
    service: PortfolioService = resolve(PortfolioService)
    if not service.portfolio_exists(value):
        raise typer.BadParameter(f"{value} is not a valid portfolio ID.")
    return value


def validate_date(value: str) -> datetime.date:
    if value.upper() in ["TODAY", "-"]:
        return datetime.date.today()
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        raise typer.BadParameter(f"{value} is not a valid date.")
