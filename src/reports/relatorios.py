import os
from conexion.oracle_queries import OracleQueries

SQL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sql")

class Relatorio:
    def __init__(self):
        self.oracle = OracleQueries(can_write=False)
        self.oracle.connect()

    def _read_sql(self, filename: str) -> str:
        path = os.path.join(SQL_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"SQL não encontrado: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _run(self, filename: str):
        sql = self._read_sql(filename)
        df = self.oracle.sqlToDataFrame(sql)
        if df.empty:
            print("\n[Relatório] Sem resultados.\n")
        else:
            print("\n[Relatório] Resultados:\n")
            try:
                print(df.to_string(index=False))
            except Exception:
                print(df)
        return df

    def get_relatorio_consultas_por_medico(self):    
        return self._run("relatorio_consultas_por_medico.sql")

    def get_relatorio_consultas_detalhado(self):     
        return self._run("relatorio_consultas_detalhado.sql")