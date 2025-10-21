# ===============================================
# QUERIES AUXILIARES GENÉRICAS
# ===============================================

# Consulta para contagem genérica de registros. 
# O format() é usado para substituir o {tabela} e o {alias_coluna} na SplashScreen.
# Ex: SELECT count(1) AS total_medico FROM Medico
QUERY_COUNT = "SELECT count(1) AS total_{tabela} FROM {tabela}"


# ===============================================
# MENUS DA APLICAÇÃO
# ===============================================

# Menu Principal (Item 5.a do Edital)
MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
5 - Sair
"""

# Menu de Relatórios (Item 6.a do Edital)
MENU_RELATORIOS = """Relatórios
1 - Consultas por Especialidade (Sumarização)
2 - Consultas Agendadas Detalhadas (Junção)
0 - Voltar ao Menu Principal
"""

# Menu de Entidades para CRUD (Item 5.b do Edital)
MENU_ENTIDADES = """Entidades CRUD
1 - PACIENTES
2 - MÉDICOS
3 - CONSULTAS
0 - Voltar ao Menu Principal
"""