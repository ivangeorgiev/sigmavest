from typing import Optional

from ...dependency import resolve
from ..domain import Portfolio
from ..repository import PortfolioRepository


class PortfolioService:
    def __init__(self, repo: Optional[PortfolioRepository]):
        self.repo: PortfolioRepository = repo or resolve(PortfolioRepository)

    def list_portfolios(self):
        transactions = self.repo.list_portfolios()
        return transactions

    def get_portfolio(self, portfolio_id: str) -> Portfolio:
        portfolio = self.repo.get(portfolio_id)
        return portfolio

    def portfolio_exists(self, portfolio_id: str) -> bool:
        return self.repo.exists(portfolio_id)
