from typing import Optional

from ...dependency import resolve
from ..repository import TransactionRepository
from .requests.transaction import ListTransactionsRequest, ListTransactionsResponse, BuySecurityRequest, BuySecurityResponse


class TransactionService:
    def __init__(self, repo: Optional[TransactionRepository]):
        self.repo: TransactionRepository = repo or resolve(TransactionRepository)

    def list_transactions(self, request: ListTransactionsRequest) -> ListTransactionsResponse:
        transactions = self.repo.list_transactions()
        response = ListTransactionsResponse(transactions=transactions)
        return response

    def buy_serucity(self, request: BuySecurityRequest) -> BuySecurityResponse:
        transaction = request.to_domain_model()
        transaction = self.repo.add(transaction)
        response = BuySecurityResponse(transactions=[transaction])
        return response
