from conexion.oracle_queries import OracleQueries
from utils import config
from datetime import datetime

class SplashScreen:
    """
    Classe responsável por gerar e exibir a tela de abertura (Splash Screen) da aplicação, 
    incluindo a contagem de registros e informações do projeto.
    """

    def __init__(self):
        # Consultas de contagem de registros (Item 5.c do Edital)
        self.qry_total_medico = config.QUERY_COUNT.format(tabela="Medico")
        self.qry_total_paciente = config.QUERY_COUNT.format(tabela="Paciente")
        self.qry_total_consulta = config.QUERY_COUNT.format(tabela="Consulta")
        # Note: A QUERY_COUNT deve ser ajustada no config.py para o nome da coluna correto (ex: total_medico)

        # Nome(s) do(s) criador(es) - Coloque os nomes dos membros do grupo aqui [cite: 27]
        self.created_by = "Renan Fortunato Silveira e Colaboradores do Grupo" 
        
        # Informações do Professor e Disciplina (Preservar conforme o edital )
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2024/2" # Ajustar para o seu semestre atual [cite: 4]
        self.nome_aplicacao = "SISTEMA DE CONTROLE DE CONSULTAS MÉDICAS"

    # --- Métodos para Contagem de Registros ---

    def get_total_medico(self):
        # Cria uma nova conexão com o banco (somente leitura)
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros
        # Atenção: O nome da coluna (total_medico) depende do alias usado na QUERY_COUNT
        return oracle.sqlToDataFrame(self.qry_total_medico)["total_medico"].values[0]

    def get_total_paciente(self):
        oracle = OracleQueries()
        oracle.connect()
        return oracle.sqlToDataFrame(self.qry_total_paciente)["total_paciente"].values[0]

    def get_total_consulta(self):
        oracle = OracleQueries()
        oracle.connect()
        return oracle.sqlToDataFrame(self.qry_total_consulta)["total_consulta"].values[0]

    # --- Método de Exibição da Tela ---

    def get_updated_screen(self):
        """
        Retorna a string formatada para a tela de abertura.
        """
        # Formata a data e hora atual
        data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        return f"""
########################################################
# {self.nome_aplicacao}          
#                             
# TOTAL DE REGISTROS EXISTENTES:            
#   1 - MÉDICOS:        {str(self.get_total_medico()).rjust(5)}
#   2 - PACIENTES:       {str(self.get_total_paciente()).rjust(5)}
#   3 - CONSULTAS:       {str(self.get_total_consulta()).rjust(5)}
#
# CRIADO POR: {self.created_by}
#
# DISCIPLINA: {self.disciplina}
# PROFESSOR: {self.professor}
# SEMESTRE:  {self.semestre}
# Data:    {data_hora_atual}
########################################################
"""