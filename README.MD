# Sistema de Gestão de Consultas Médicas - Python + Oracle
Disciplina: Banco de Dados
Professor: Howard Roatti
Instituição: FAESA
Última atualização: Outubro/2025
Vídeo de apresentação: https://youtu.be/wNuKxfriwNw

Integrantes:
Estevão Matos de Souza, Gabriel Araujo Ceruti Castro, Gabriel Araujo Valoni,
Heitor Lopes Trindade Fadlalah, Renan Fortunato Silveira, Thiago Rosetti Miranda
Turma: 4HC1A

---

Descrição do Projeto
O Sistema de Gestão de Consultas Médicas tem como objetivo registrar médicos, pacientes e consultas realizadas, permitindo o controle das informações essenciais de cada entidade e a geração de relatórios sobre atendimentos e produtividade.

Este projeto foi desenvolvido em Python, com integração direta ao banco de dados Oracle, simulando um sistema real de interface entre uma aplicação de backend e um banco de dados relacional.

O sistema implementa operações CRUD completas (Create, Read, Update, Delete) sobre as entidades Médico, Paciente e Consulta, além de dois relatórios obrigatórios:
1. Relatório com funções agregadas (GROUP BY);
2. Relatório com junção de tabelas (JOIN).

---

Requisitos do Ambiente
Software Necessário
• Python 3.10+ instalado no sistema
• Banco de Dados Oracle configurado e acessível
• Oracle Instant Client instalado (veja instruções abaixo)
• Dependências listadas no arquivo: src/requirements.txt

Instale as dependências com:
pip install -r src/requirements.txt

---
```text
Estrutura do Projeto
.
├── diagrams/
│   └── DIAGRAMA_RELACIONAL_PEDIDOS.pdf
├── sql/
│   └── create_tables.sql
├── src/
│   ├── conexion/
│   │   └── oracle_queries.py
│   ├── controller/
│   │   ├── controller_medico.py
│   │   ├── controller_paciente.py
│   │   └── controller_consulta.py
│   ├── model/
│   │   ├── medico.py
│   │   ├── paciente.py
│   │   └── consulta.py
│   ├── reports/
│   │   └── relatorios.py
│   ├── utils/
│   │   ├── config.py
│   │   └── splash_screen.py
│   ├── create_tables_and_records.py
│   ├── principal.py
│   ├── test.py
│   └── requirements.txt
└── README.md
---

Execução do Projeto no Linux
1. Clonar o repositório do GitHub:
   git clone https://github.com/RenanFSilveira/example_crud_oracle
   cd example_crud_oracle
2. Criar e ativar ambiente virtual (recomendado):
   python3 -m venv .venv
   source .venv/bin/activate
3. Instalar as dependências:
   pip install -r src/requirements.txt
4. Criar tabelas e inserir registros de exemplo:
   python src/create_tables_and_records.py
5. Executar o sistema principal (menu interativo):
   python src/principal.py
6. Encerrar o ambiente virtual:
   deactivate

---

Exemplos de Uso (Módulo OracleQueries)
Consulta:
from conexion.oracle_queries import OracleQueries

query = "SELECT id_medico, nome FROM medico ORDER BY nome"
oracle = OracleQueries()
oracle.connect()
df = oracle.sqlToDataFrame(query)
print(df)

Inserção:
oracle = OracleQueries(can_write=True)
oracle.connect()
oracle.write("INSERT INTO medico (id_medico, nome) VALUES (1, 'Dr. João')")

---

Relatórios Implementados
1. Relatório de Consultas por Médico (Agrupamento / GROUP BY):
   • Exibe a quantidade total de consultas realizadas por cada médico.
2. Relatório de Consultas Detalhadas (Junção / JOIN):
   • Mostra informações completas das consultas com o nome do médico e do paciente.

---

Instalação do Oracle Instant Client (Linux)
1. Baixe a versão compatível em:
   https://www.oracle.com/database/technologies/instant-client.html
2. Se o arquivo for .rpm, converta e instale:
   sudo apt install alien
   sudo alien --scripts oracle-instantclient18.5-basic-18.5.0.0.0-3.x86_64.rpm
3. Configure as variáveis de ambiente:
   sudo mkdir -p /usr/local/oracle/instantclient_18_5/
   sudo mv lib /usr/local/oracle/instantclient_18_5/
   echo 'export ORACLE_HOME=/usr/local/oracle/instantclient_18_5' >> ~/.bash_profile
   echo 'export LD_LIBRARY_PATH=$ORACLE_HOME/lib' >> ~/.bash_profile
   echo 'export PATH=$PATH:$ORACLE_HOME/bin' >> ~/.bash_profile
   source ~/.bash_profile

---

Solução de Problemas Comuns
Erro: ORA-28001: the password has expired
Execute os comandos abaixo no Oracle (como DBA):
ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
ALTER USER labdatabase IDENTIFIED BY "labDatabase2022";

---

Documentação de Execução (Ambiente MV - FAESA)
Esse procedimento foi feito usando a MV fornecida em aula.

1. Clonar o repositório:
   https://github.com/RenanFSilveira/example_crud_oracle
2. Subindo o container do banco de dados:
   cd database_services/
   docker compose up -d oracle
3. Abrindo a conexão no DBeaver:
   Usar a conexão 'LABDATABASE ORACLE' que vem criada por padrão na MV.
4. Ativando o ambiente virtual de desenvolvimento:
   cd ~
   source Workspace/.venv/bin/activate
5. Criação das tabelas e execução do sistema:
   cd example_crud_oracle/src/
   python create_tables_and_records.py
   python principal.py

A partir desse ponto, a aplicação faz o CRUD completo via terminal, e todas as alterações são salvas e persistem no banco de dados Oracle.

---

Observações Finais
Este projeto foi desenvolvido com o propósito de demonstrar a integração entre Python e Oracle Database, aplicando o modelo de entidades e relacionamentos do domínio médico-paciente-consulta.
A estrutura modular e o uso de operações CRUD completas permitem expandir facilmente o sistema para outros contextos de gestão de informações.
