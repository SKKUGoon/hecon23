class SqlTable:
    def __init__(self, name: str, database: str = None):
        self.name = name
        self.database = database

    def to_string(self) -> str:
        ls = [self.database, self.name]
        return ".".join(filter(None, ls))


class SqlColumns:
    def __init__(self, column_setup: dict):
        """
        Manipulate human friendly column structures
        :param column_setup: { column name: column type }
        """
        self.hcol = column_setup

    @property
    def typewise(self):
        result = dict()
        for k, v in self.hcol.items():
            if v.lower() in result.keys():
                result[v.lower()].add(k)
            else:
                result[v.lower()] = {k}
        return result
