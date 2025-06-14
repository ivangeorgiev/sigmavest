import os
from typing import Optional

from ..domain import Transaction
from .db import TrackDb


class TransactionRepository:
    def __init__(self, db: Optional[TrackDb] = None):
        self.db: TrackDb = db or TrackDb.get_instance()

    @classmethod
    def get_instance(cls, db=None):
        """
        Factory method to get an instance of PortfolioRepository.
        """
        return cls(db)
    
    @property
    def table_name(self):
        table_name = "transactions"
        return table_name

    def list_transactions(self, select_fields: Optional[str|list] = None):
        select_fields = select_fields or "*"
        if isinstance(select_fields, list):
            select_fields = ",".join(select_fields)
        for row in self.db.execute(f"SELECT {select_fields} FROM {self.table_name}"):
            yield Transaction(*row)

    def add(self, transaction: Transaction) -> Transaction:
        last_id = self.get_last_id() or 0
        transaction.id = last_id + 1
        field_names = transaction.get_field_names()
        values = [str(getattr(transaction, n)) for n in field_names]
        query = f"INSERT INTO {self.table_name} ({','.join(field_names)}) VALUES ({','.join(['?']*len(field_names))})"
        self.db.execute(query, values)
        data_file = self.table_name + ".csv"
        self.db.db.execute(f"COPY {self.table_name} TO '{os.path.join(self.db.data_path, data_file)}' (HEADER true, DELIMITER ',')")
        return transaction

    def get_last_id(self):
        id = self.db.db.execute(f"SELECT MAX(id) FROM {self.table_name}").fetchone()[0] # type: ignore
        return id
