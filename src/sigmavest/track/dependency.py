from ..dependency.container import Container
from .repository import PortfolioRepository, TrackDb, TransactionRepository
from .service import PortfolioService, TransactionService


def register(c: Container):
    c.register_factory(TrackDb, lambda c: TrackDb.get_instance())

    # Register repositories
    c.register_factory(TransactionRepository, lambda c: TransactionRepository(c.resolve(TrackDb)))
    c.register_factory(PortfolioRepository, lambda c: PortfolioRepository(c.resolve(TrackDb)))

    # Register services
    c.register_factory(TransactionService, lambda c: TransactionService(c.resolve(TransactionRepository)))
    c.register_factory(PortfolioService, lambda c: PortfolioService(c.resolve(PortfolioRepository)))
