from model.medico import Medico
from conexion.oracle_queries import OracleQueries

class ControllerMedico:
    """
    Classe responsável por controlar as operações de CRUD (Create, Read, Update, Delete)
    para a entidade Medico, utilizando JDBC puro.
    """

    def __init__(self):
        pass
        
    def inserir_medico(self) -> Medico:
        """
        Insere um novo registro de Medico.
        O CRM é a chave primária e é informado pelo usuário.
        """
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        print("\n--- INSERÇÃO DE NOVO MÉDICO ---")
        
        # 1. Solicita as chaves (CRM e Email)
        crm = input("CRM (Chave Primária): ")
        email = input("E-mail (Chave Única): ")

        # 2. Verifica se o CRM JÁ está cadastrado
        if self.verifica_existencia_medico(oracle, crm):
            print(f"\nO CRM {crm} já está cadastrado. Abortando Inserção.")
            return None
        
        # 3. Verifica se o Email JÁ está cadastrado (Garante a restrição UNIQUE)
        if self.verifica_existencia_email(oracle, email):
            print(f"\nO E-mail {email} já está cadastrado. Abortando Inserção.")
            return None
        
        # 4. Solicita os dados restantes
        nome = input("Nome Completo: ")
        especialidade = input("Especialidade (Ex: Cardiologia): ")
        telefone = input("Telefone (Ex: 99999-9999): ")

        # 5. Insere e persiste o novo Medico (Concatenação de Query SQL)
        query = f"INSERT INTO Medico (crm, nome, especialidade, telefone, email) VALUES ("
        query += f"'{crm}', '{nome}', '{especialidade}', '{telefone}', '{email}')"

        oracle.write(query)
        
        # 6. Recupera os dados do Medico criado para criar o Objeto
        df_medico = oracle.sqlToDataFrame(f"SELECT crm, nome, especialidade, telefone, email FROM Medico WHERE crm = '{crm}'")
        
        # 7. Cria e retorna o objeto Medico
        novo_medico = Medico(
            df_medico.crm.values[0], 
            df_medico.nome.values[0], 
            df_medico.especialidade.values[0],
            df_medico.telefone.values[0],
            df_medico.email.values[0]
        )
        
        print("\n--- Médico Inserido com Sucesso ---")
        print(novo_medico.to_string())
        return novo_medico
        
    def atualizar_medico(self) -> Medico:
        """
        Atualiza os atributos mutáveis de um Medico existente (nome, especialidade, telefone).
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita a chave de alteração (CRM)
        crm_atual = input("CRM do Médico que deseja alterar os dados: ")

        # 1. Verifica se o Médico EXISTE na base de dados
        if self.verifica_existencia_medico(oracle, crm_atual):
            
            # 2. Solicita os campos mutáveis (nome, especialidade, telefone)
            print(f"\n--- ATUALIZANDO MÉDICO (CRM: {crm_atual}) ---")
            novo_nome = input("Novo Nome Completo: ")
            nova_especialidade = input("Nova Especialidade: ")
            novo_telefone = input("Novo Telefone: ")

            # 3. Atualiza o Medico existente (Concatenação de Query SQL)
            query = f"UPDATE Medico SET nome = '{novo_nome}', "
            query += f"especialidade = '{nova_especialidade}', "
            query += f"telefone = '{novo_telefone}' WHERE crm = '{crm_atual}'"
            
            oracle.write(query)
            
            # 4. Recupera os dados atualizados
            df_medico = oracle.sqlToDataFrame(f"SELECT crm, nome, especialidade, telefone, email FROM Medico WHERE crm = '{crm_atual}'")
            
            # 5. Cria o objeto atualizado
            medico_atualizado = Medico(
                df_medico.crm.values[0], 
                df_medico.nome.values[0], 
                df_medico.especialidade.values[0],
                df_medico.telefone.values[0],
                df_medico.email.values[0]
            )
            
            print("\n--- Médico Atualizado com Sucesso ---")
            print(medico_atualizado.to_string())
            return medico_atualizado
        else:
            print(f"\nO CRM {crm_atual} não está cadastrado. Abortando Atualização.")
            return None


    def excluir_medico(self):
        """
        Exclui um registro de Medico pelo CRM.
        Verifica a existência de FK (Consultas) para evitar erros.
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        crm_excluir = input("CRM do Médico que irá excluir: ") 
        
        # 1. Verifica se o Médico EXISTE na base de dados
        if not self.verifica_existencia_medico(oracle, crm_excluir):
            print(f"\nO CRM {crm_excluir} não está cadastrado. Abortando Exclusão.")
            return None

        # 2. Verifica se o Médico tem consultas agendadas (Restrição FK)
        # O CRM está ligado à tabela Consulta
        df_consultas = oracle.sqlToDataFrame(f"SELECT COUNT(1) AS total FROM Consulta WHERE crm_medico = '{crm_excluir}'")
        
        if df_consultas.total.values[0] > 0:
            print(f"\nATENÇÃO: Este médico possui {df_consultas.total.values[0]} consultas agendadas.")
            print("A exclusão falhará devido à Chave Estrangeira (FK).")
            # ON DELETE RESTRICT no seu script SQL impede a exclusão.
            return None

        # 3. Recupera os dados do médico antes de remover (para exibir o objeto excluído)
        df_medico = oracle.sqlToDataFrame(f"SELECT crm, nome, especialidade, telefone, email FROM Medico WHERE crm = '{crm_excluir}'")
        
        # 4. Remove o Medico
        oracle.write(f"DELETE FROM Medico WHERE crm = '{crm_excluir}'")            
        
        # 5. Cria um novo objeto Medico para informar que foi removido
        medico_excluido = Medico(
            df_medico.crm.values[0], 
            df_medico.nome.values[0], 
            df_medico.especialidade.values[0],
            df_medico.telefone.values[0],
            df_medico.email.values[0]
        )
        
        print("\n--- Médico Removido com Sucesso ---")
        print(medico_excluido.to_string())
        return medico_excluido


    def verifica_existencia_medico(self, oracle:OracleQueries, crm:str=None) -> bool:
        """
        Verifica se um Médico existe na base de dados dado um CRM.
        Retorna True se EXISTE, False se NÃO EXISTE.
        """
        # Recupera os dados do Medico transformando em um DataFrame
        df_medico = oracle.sqlToDataFrame(f"SELECT crm FROM Medico WHERE crm = '{crm}'")
        
        # Retorna True se o DataFrame NÃO estiver vazio (ou seja, se o médico existe)
        return not df_medico.empty
        
    def verifica_existencia_email(self, oracle:OracleQueries, email:str=None) -> bool:
        """
        Verifica se um E-mail já está cadastrado para qualquer Medico.
        Retorna True se EXISTE, False se NÃO EXISTE.
        """
        # Recupera os dados do Medico transformando em um DataFrame
        df_medico = oracle.sqlToDataFrame(f"SELECT email FROM Medico WHERE email = '{email}'")
        
        # Retorna True se o DataFrame NÃO estiver vazio (ou seja, o email já está em uso)
        return not df_medico.empty