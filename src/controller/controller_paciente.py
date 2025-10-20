from model.paciente import Paciente
from conexion.oracle_queries import OracleQueries
from datetime import date, datetime

class Controller_Paciente:
    # Classe responsável por controlar as operações de CRUD
    def __init__(self):
        pass
        
    def inserir_paciente(self) -> Paciente:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        print("\n--- INSERÇÃO DE NOVO PACIENTE ---")
        # 1. Solicita ao usuario o novo cpf
        cpf = input("CPF (Novo): ")

        # 2. Verifica se o CPF JÁ está cadastrado
        if self.verifica_existencia_paciente(oracle, cpf):
            print(f"\nO CPF {cpf} já está cadastrado. Abortando Inserção.")
            return None
        else: 
            # 3. Solicita os dados restantes
            nome = input("Nome completo (Novo): ")
            
            # Tratamento da data de nascimento (exigido no modelo)
            data_nascimento_str = input("Data de Nascimento (DD/MM/AAAA): ")
            try:
                # Converte a string para objeto date/datetime (depende da sua classe Paciente)
                data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y').date()
            except ValueError:
                print("Formato de data inválido. Abortando Inserção.")
                return None
            
            # Telefone
            telefone = input("Telefone (Ex: 99999-9999): ")

            # 4. Obtém o próximo ID da SEQUENCE (Para Oracle, a sintaxe de SEQUENCE é usada)
            # Sintaxe: SELECT NOME_DA_SEQUENCE.NEXTVAL FROM DUAL
            
            # NOTE: Assumindo que a sequence se chama paciente_id_seq e a tabela é Paciente
            # Uso de iloc[0,0] para obter o valor da primeira célula do DataFrame
            id_paciente_temp = oracle.sqlToDataFrame("SELECT paciente_id_seq.NEXTVAL AS novo_id FROM DUAL").iloc[0,0]

            # 5. Insere e persiste o novo Paciente (Conforme o edital, usando concatenação)
            # Todos os campos são inseridos, exceto o id_paciente, que usa o valor da sequence.
            query = f"INSERT INTO Paciente (id_paciente, nome, data_nascimento, cpf, telefone) VALUES ("
            query += f"{id_paciente_temp}, '{nome}', TO_DATE('{data_nascimento_str}', 'DD/MM/YYYY'), '{cpf}', '{telefone}')"

            oracle.write(query)
            
            # 6. Recupera os dados do Paciente criado para criar o Objeto
            df_paciente = oracle.sqlToDataFrame(f"SELECT id_paciente, nome, data_nascimento, cpf, telefone FROM Paciente WHERE id_paciente = {id_paciente_temp}")
            
            # 7. Cria e retorna o objeto Paciente
            # OBS: O DataFrame pode retornar o tipo de dado original, ajustar a criação do objeto
            novo_paciente = Paciente(
                df_paciente.id_paciente.values[0], 
                df_paciente.nome.values[0], 
                df_paciente.data_nascimento.values[0], # Já deve vir como date/datetime
                df_paciente.cpf.values[0],
                df_paciente.telefone.values[0]
            )
            
            print("\n--- Paciente Inserido com Sucesso ---")
            print(novo_paciente.to_string())
            return novo_paciente

    def atualizar_paciente(self) -> Paciente:
        # Atualiza os atributos de um Paciente existente, exceto o ID e CPF.
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o cpf do Paciente a ser alterado
        cpf_atual = input("CPF do Paciente que deseja alterar os dados: ")

        # 1. Verifica se o Paciente EXISTE na base de dados
        if self.verifica_existencia_paciente(oracle, cpf_atual): # CORRIGIDO: Lógica invertida. Se EXISTE...
            
            # 2. Solicita todos os campos mutáveis (nome, data_nascimento, telefone)
            print(f"\n--- ATUALIZANDO PACIENTE (CPF: {cpf_atual}) ---")
            novo_nome = input("Novo Nome Completo: ")
            
            data_nascimento_str = input("Nova Data de Nascimento (DD/MM/AAAA): ")
            try:
                data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y').date()
            except ValueError:
                print("Formato de data inválido. Abortando Atualização.")
                return None
                
            novo_telefone = input("Novo Telefone: ")

            # 3. Atualiza o Paciente existente (Concatenação de Query SQL)
            query = f"UPDATE Paciente SET nome = '{novo_nome}', "
            query += f"data_nascimento = TO_DATE('{data_nascimento_str}', 'DD/MM/YYYY'), "
            query += f"telefone = '{novo_telefone}' WHERE cpf = '{cpf_atual}'"
            
            oracle.write(query)
            
            # 4. Recupera os dados atualizados
            df_paciente = oracle.sqlToDataFrame(f"SELECT id_paciente, nome, data_nascimento, cpf, telefone FROM Paciente WHERE cpf = '{cpf_atual}'")
            
            # 5. Cria o objeto atualizado
            paciente_atualizado = Paciente(
                df_paciente.id_paciente.values[0], 
                df_paciente.nome.values[0], 
                df_paciente.data_nascimento.values[0],
                df_paciente.cpf.values[0],
                df_paciente.telefone.values[0]
            )
            
            print("\n--- Paciente Atualizado com Sucesso ---")
            print(paciente_atualizado.to_string())
            return paciente_atualizado
        else:
            print(f"\nO CPF {cpf_atual} não está cadastrado. Abortando Atualização.")
            return None

    def excluir_paciente(self):
        # Exclui um registro de Paciente pelo CPF, verificando a existência de FK (Requisito 6.c.5.i)
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cpf_excluir = input("CPF do Paciente que irá excluir: ") 
        
        # 1. Verifica se o Paciente EXISTE na base de dados
        if self.verifica_existencia_paciente(oracle, cpf_excluir):

            # 2. Verifica se o Paciente tem consultas agendadas (Restrição FK)
            df_consultas = oracle.sqlToDataFrame(f"SELECT COUNT(1) AS total FROM Consulta c JOIN Paciente p ON c.id_paciente = p.id_paciente WHERE p.cpf = '{cpf_excluir}'")
            
            if df_consultas.total.values[0] > 0:
                print(f"\nATENÇÃO: Este paciente possui {df_consultas.total.values[0]} consultas agendadas.")
                print("A exclusão falhará devido à Chave Estrangeira (FK).")
                # Conforme o edital, informar que o registro não pode ser excluído
                # (pois definimos ON DELETE RESTRICT no script SQL).
                return None

            # 3. Recupera os dados do paciente antes de remover (para exibir o objeto excluído)
            df_paciente = oracle.sqlToDataFrame(f"SELECT id_paciente, nome, data_nascimento, cpf, telefone FROM Paciente WHERE cpf = '{cpf_excluir}'")
            
            # 4. Remove o Paciente
            oracle.write(f"DELETE FROM Paciente WHERE cpf = '{cpf_excluir}'")
            
            # 5. Cria um novo objeto Paciente para informar que foi removido
            paciente_excluido = Paciente(
                df_paciente.id_paciente.values[0], 
                df_paciente.nome.values[0], 
                df_paciente.data_nascimento.values[0],
                df_paciente.cpf.values[0],
                df_paciente.telefone.values[0]
            )
            
            print("\n--- Paciente Removido com Sucesso ---")
            print(paciente_excluido.to_string())
            return paciente_excluido
        else:
            print(f"\nO CPF {cpf_excluir} não está cadastrado. Abortando Exclusão.")
            return None

    def verifica_existencia_paciente(self, oracle:OracleQueries, cpf:str=None) -> bool:
        """
        Verifica se um Paciente existe na base de dados dado um CPF.
        Retorna True se EXISTE, False se NÃO EXISTE.
        """
        # Recupera os dados do Paciente transformando em um DataFrame
        df_paciente = oracle.sqlToDataFrame(f"SELECT cpf FROM Paciente WHERE cpf = '{cpf}'")
        
        # df_paciente.empty retorna True se NÃO houver registros (paciente não existe)
        # Invertemos a lógica para retornar True se EXISTE
        return not df_paciente.empty