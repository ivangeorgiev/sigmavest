from typing import Optional

from ..domain.portfolio import Portfolio
from ..exceptions import DoesNotExist
from .db import TrackDb


class PortfolioRepository:
    def __init__(self, db: Optional[TrackDb] = None):
        self.db = db or TrackDb.get_instance()

    @classmethod
    def get_instance(cls, db=None):
        """
        Factory method to get an instance of PortfolioRepository.
        """
        return cls(db)

    @property
    def table_name(self):
        table_name = f"{self.db.data_path}/portfolios.csv"
        return table_name

    def list_portfolios(self, select_fields: Optional[str | list] = None):
        select_fields = select_fields or Portfolio.get_field_names()
        if isinstance(select_fields, list):
            select_fields = ",".join(select_fields)
        for row in self.db.execute(f"SELECT {select_fields} FROM '{self.table_name}'"):
            yield Portfolio(*row)

    def get(self, portfolio_id: str) -> Portfolio:
        select_fields = ",".join(Portfolio.get_field_names())

        rows = self.db.execute(f"SELECT {select_fields} FROM '{self.table_name}' WHERE id=?", [portfolio_id])
        if not rows:
            msg = f"Portfolio with ID '{portfolio_id}' does not exist"
            raise DoesNotExist(msg)
        return Portfolio(*rows[0])

    def exists(self, portfolio_id) -> bool:
        try:
            self.get(portfolio_id)
            return True
        except DoesNotExist:
            return False
