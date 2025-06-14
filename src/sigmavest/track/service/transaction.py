from typing import Optional

from ...dependency import resolve
from ..domain import Transaction
from ..repository import TransactionRepository


class TransactionService:
    def __init__(self, repo: Optional[TransactionRepository]):
        self.repo: TransactionRepository = repo or resolve(TransactionRepository)

    def list_transactions(self):
        transactions = self.repo.list_transactions()
        return transactions

    def add_transaction(self, transaction: Transaction) -> Transaction:
        self.repo.add(transaction)
        return transaction
