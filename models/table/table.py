class Table:
    
    def __init__(self, table_name: str) -> None:
        self._table_name = table_name
        
    @property
    def tableName(self) -> str:
        return self._table_name