from .stock import Stock


def evaluate_magic_formula_data(stock: Stock) -> dict:
    income_stmt = stock.income_statements.latest
    balance_sheet = stock.balance_sheets.latest
    if not (income_stmt and balance_sheet):
        return
    ebit = stock.income_statements.latest.ebit
    current_assets = balance_sheet.current_assets
    current_liabilities = balance_sheet.current_liabilities
    net_working_capital = current_assets - current_liabilities
    net_fixed_assets = balance_sheet.net_fixed_assets

    ev = stock.info.get("enterpriseValue")
    if not ev:
        ev = float(stock.info["marketCap"]) + balance_sheet.total_assets - balance_sheet.current_liabilities

    return {
        "Ticker": stock.symbol,
        "MarketCap": float(stock.info["marketCap"]),
        "EBIT": float(ebit),
        "EnterpriseValue": float(ev),
        "NetWorkingCapital": float(net_working_capital),
        "NetFixedAssets": float(net_fixed_assets),
    }

