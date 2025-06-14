from collections import namedtuple
from typing import Optional

from sigmavest.settings import Settings
from sigmavest.dependency import resolve

DEFAULT_DB_PATH = ":memory:"
DEFAULT_DATA_PATH = "."


class TrackDb:
    def __init__(self, db_path: Optional[str] = None, data_path: Optional[str] = None):
        import duckdb

        settings: Settings = resolve(Settings)
        db_path = db_path or settings.DATABASE_PATH or DEFAULT_DB_PATH
        self.db = duckdb.connect(database=db_path, read_only=False)
        self.data_path = data_path or settings.DATABASE_DATA_PATH or DEFAULT_DATA_PATH
        self.import_data()
        self.create_views()

    def import_data(self):
        """
        Import data from CSV files into DuckDB tables.
        """
        import os

        if not os.path.exists(self.data_path):
            raise ValueError(f"Data path {self.data_path} does not exist.")

        # self._create_transactions_table()

        for file in os.listdir(self.data_path):
            if file.endswith(".csv"):
                table_name = file[:-4]

                self.db.execute(f"""
                    CREATE TABLE IF NOT EXISTS "{table_name}" AS
                    SELECT * FROM '{os.path.join(self.data_path, file)}'
                """)  # type: ignore
                # self.import_csv(os.path.join(self.data_path, file), table_name)

                # TODO: Move this to logging
                print(f"Imported {file} into DuckDB table '{table_name}'.")

        self.db.execute("""
                ALTER TABLE transactions ALTER date TYPE DATE;
                ALTER TABLE transactions ALTER quantity TYPE DECIMAL(20,8);
                ALTER TABLE transactions ALTER price TYPE DECIMAL(20,8);
                ALTER TABLE transactions ALTER fees TYPE DECIMAL(20,8);
                ALTER TABLE transactions ALTER amount_paid TYPE DECIMAL(20,8);
        """)

    def create_views(self):
        """
        Create views for easier access to data.
        """
        self.db.execute("""
            CREATE OR REPLACE VIEW holdings AS
            SELECT buys.ticker, 
                   CAST(SUM(buys.quantity - COALESCE(alloc.sold_quantity, 0)) AS DECIMAL(20,8)) AS quantity, 
                   CAST(SUM((buys.quantity - COALESCE(alloc.sold_quantity, 0))*buys.amount_paid/buys.quantity) AS DECIMAL(20,8)) AS cost
              FROM transactions buys
              LEFT JOIN (SELECT SUM(quantity) AS sold_quantity, buy_transaction_id FROM sell_allocations GROUP BY buy_transaction_id) alloc ON alloc.buy_transaction_id=buys.id
             WHERE buys.transaction_type = 'BUY'
             GROUP BY buys.ticker
            HAVING SUM(buys.quantity - COALESCE(alloc.sold_quantity, 0)) <> 0
        """)

    def import_csv(self, csv_path: str, table_name: str):
        conn = self.db

        # Get CSV columns
        summary = conn.execute(f"""
            SUMMARIZE SELECT * FROM read_csv('{csv_path}')
        """).fetchall()
        csv_columns = [row[0] for row in summary]

        # Get table columns
        table_columns = conn.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
        """).fetchall()
        table_columns = [c[0] for c in table_columns]

        # Find intersection
        common_columns = set(csv_columns) & set(table_columns)

        if not common_columns:
            raise ValueError(f"No matching columns between CSV ({csv_columns}) and table ({table_columns})")

        # Build dynamic query
        columns_str = ", ".join(common_columns)
        query = f"""
            INSERT INTO {table_name}({columns_str})
            SELECT {columns_str}
            FROM read_csv({repr(csv_path)})
        """

        conn.execute(query)

    def _create_transactions_table(self):
        """
        Create the transactions table if it does not exist.
        """
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                type VARCHAR,
                ticker VARCHAR,
                quantity DECIMAL(20, 8),
                ammount_paid DECIMAL(20, 8),
                date DATE
            )
        """)

        # Add more views as needed

    def execute(self, query: str, params=None):
        if params is None:
            return self.db.execute(query).fetchall()
        else:
            return self.db.execute(query, params).fetchall()

    def execute_ex(self, query: str, params=None) -> list | None:
        if params is None:
            result = self.db.execute(query)
        else:
            result = self.db.execute(query, params)
        if result:
            Row = namedtuple("Row", [col[0] for col in result.description])  # type: ignore
            return [Row(*row) for row in result.fetchall()]


    def exists(self, db, table: str, **kwargs) -> bool:
        """
        Check if a record exists in the specified table matching all conditions.
        
        Args:
            conn: DuckDB connection
            table: Table name
            kwargs: Dictionary of column=value pairs to match
            
        Returns:
            bool: True if record exists, False otherwise
        """
        where_clause = " AND ".join([f"{k} = ?" for k in kwargs.keys()])
        query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {where_clause})"
        
        result = self.db.execute(query, list(kwargs.values())).fetchone()
        return result[0] if result else False

    def close(self):
        self.db.close()

    @classmethod
    def get_instance(cls):
        """
        Factory method to get an instance of DuckDbDb.
        """
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance
