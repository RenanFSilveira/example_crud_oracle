from model.consulta import Consulta
from model.medico import Medico
from model.paciente import Paciente
from conexion.oracle_queries import OracleQueries
from datetime import datetime
import pandas as pd

from controller.controller_medico import ControllerMedico
from controller.controller_paciente import ControllerPaciente


class ControllerConsulta:
    """
    Classe responsável por controlar as operações de CRUD (Create, Read, Update, Delete)
    para a entidade Consulta.
    """

    def __init__(self):
        # Instancia os controllers de Medico e Paciente para buscar os objetos FK
        self.ctrl_medico = ControllerMedico()
        self.ctrl_paciente = ControllerPaciente()
        pass

    def recuperar_dados_medico(self, oracle:OracleQueries, crm: str) -> Medico:
        """
        Busca o objeto Medico completo no banco de dados.
        Retorna o objeto Medico ou None se não encontrado.
        """
        df_medico = oracle.sqlToDataFrame(f"SELECT crm, nome, especialidade, telefone, email FROM Medico WHERE crm = '{crm}'")
        
        if df_medico.empty:
            return None
        
        return Medico(
            df_medico.crm.values[0], 
            df_medico.nome.values[0], 
            df_medico.especialidade.values[0],
            df_medico.telefone.values[0],
            df_medico.email.values[0]
        )

    def recuperar_dados_paciente(self, oracle:OracleQueries, cpf: str) -> Paciente:
        """
        Busca o objeto Paciente completo no banco de dados (usando CPF como chave).
        Retorna o objeto Paciente ou None se não encontrado.
        """
        df_paciente = oracle.sqlToDataFrame(f"SELECT id_paciente, nome, data_nascimento, cpf, telefone FROM Paciente WHERE cpf = '{cpf}'")
        
        if df_paciente.empty:
            return None
        
        return Paciente(
            df_paciente.id_paciente.values[0], 
            df_paciente.nome.values[0], 
            df_paciente.data_nascimento.values[0],
            df_paciente.cpf.values[0],
            df_paciente.telefone.values[0]
        )
        
    def inserir_consulta(self) -> Consulta:
        """
        Insere uma nova Consulta. Requer a existência prévia de Médico e Paciente.
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        print("\n--- AGENDAMENTO DE NOVA CONSULTA ---")
        
        # 1. Busca e valida o Paciente
        cpf_paciente = input("CPF do Paciente: ")
        paciente = self.recuperar_dados_paciente(oracle, cpf_paciente)
        
        if paciente is None:
            print(f"\nPaciente com CPF {cpf_paciente} não encontrado. Abortando Consulta.")
            return None

        # 2. Busca e valida o Médico
        crm_medico = input("CRM do Médico: ")
        medico = self.recuperar_dados_medico(oracle, crm_medico)
        
        if medico is None:
            print(f"\nMédico com CRM {crm_medico} não encontrado. Abortando Consulta.")
            return None
            
        # 3. Solicita a data e hora da consulta
        data_hora_str = input("Data e Hora da Consulta (DD/MM/AAAA HH:MM): ")
        try:
            # Converte a string para objeto datetime (necessário para TIMESTAMP)
            data_hora = datetime.strptime(data_hora_str, '%d/%m/%Y %H:%M')
        except ValueError:
            print("Formato de data/hora inválido. Abortando Consulta.")
            return None

        observacoes = input("Observações (Opcional): ")
        
        # 4. Obtém o próximo ID da SEQUENCE
        id_consulta_temp = oracle.sqlToDataFrame("SELECT consulta_id_seq.NEXTVAL AS novo_id FROM DUAL").iloc[0,0]

        # 5. Insere a Consulta (Concatenação de Query SQL)
        # Atenção: Passa o ID do Paciente e o CRM do Médico, não os objetos.
        query = f"INSERT INTO Consulta (id_consulta, crm_medico, id_paciente, data_hora, observacoes) VALUES ("
        query += f"{id_consulta_temp}, '{medico.get_crm()}', {paciente.get_id_paciente()}, "
        query += f"TO_TIMESTAMP('{data_hora_str}', 'DD/MM/YYYY HH24:MI'), '{observacoes}')"

        oracle.write(query)
        
        # 6. Cria e retorna o objeto Consulta (Usando as instâncias de objeto recuperadas)
        nova_consulta = Consulta(
            id_consulta_temp, 
            paciente, # Objeto Paciente
            data_hora, 
            medico,   # Objeto Medico
            observacoes
        )
        
        print("\n--- Consulta Agendada com Sucesso ---")
        print(nova_consulta.to_string())
        return nova_consulta

    def atualizar_consulta(self) -> Consulta:
        """
        Atualiza os dados de uma Consulta existente.
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # 1. Solicita o ID da consulta
        id_consulta = input("ID da Consulta que deseja alterar: ")

        # 2. Verifica se a Consulta existe
        consulta_existente = self.verifica_existencia_consulta(oracle, id_consulta)
        
        if consulta_existente is None:
            print(f"\nConsulta com ID {id_consulta} não encontrada. Abortando Atualização.")
            return None

        # 3. Solicita campos mutáveis
        print(f"\n--- ATUALIZANDO CONSULTA (ID: {id_consulta}) ---")
        
        # Apenas data/hora e observações são mutáveis. As FKs (Médico e Paciente) não devem ser alteradas aqui.
        nova_data_hora_str = input("Nova Data e Hora da Consulta (DD/MM/AAAA HH:MM): ")
        try:
            nova_data_hora = datetime.strptime(nova_data_hora_str, '%d/%m/%Y %H:%M')
        except ValueError:
            print("Formato de data/hora inválido. Abortando Atualização.")
            return None

        novas_observacoes = input("Novas Observações: ")

        # 4. Atualiza a Consulta existente (Concatenação de Query SQL)
        query = f"UPDATE Consulta SET data_hora = TO_TIMESTAMP('{nova_data_hora_str}', 'DD/MM/YYYY HH24:MI'), "
        query += f"observacoes = '{novas_observacoes}' WHERE id_consulta = {id_consulta}"
        
        oracle.write(query)
        
        # 5. Cria o objeto atualizado (reutilizando os objetos Médico e Paciente originais)
        consulta_atualizada = Consulta(
            id_consulta, 
            consulta_existente.get_paciente(),
            nova_data_hora, 
            consulta_existente.get_medico(),
            novas_observacoes
        )
        
        print("\n--- Consulta Atualizada com Sucesso ---")
        print(consulta_atualizada.to_string())
        return consulta_atualizada


    def excluir_consulta(self):
        """
        Exclui um registro de Consulta pelo ID.
        """
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_consulta_excluir = input("ID da Consulta que irá excluir: ") 
        
        # 1. Verifica se a Consulta existe e recupera o objeto para exibir no final
        consulta_existente = self.verifica_existencia_consulta(oracle, id_consulta_excluir)
        
        if consulta_existente is None:
            print(f"\nConsulta com ID {id_consulta_excluir} não encontrada. Abortando Exclusão.")
            return None

        # 2. Remove a Consulta
        oracle.write(f"DELETE FROM Consulta WHERE id_consulta = {id_consulta_excluir}")            
        
        print("\n--- Consulta Removida com Sucesso ---")
        print(consulta_existente.to_string())
        return consulta_existente


    def verifica_existencia_consulta(self, oracle:OracleQueries, id_consulta:str=None) -> Consulta:
        """
        Verifica se uma Consulta existe na base de dados dado o ID.
        Retorna o objeto Consulta se EXISTE, ou None se NÃO EXISTE.
        """
        df_consulta = oracle.sqlToDataFrame(f"SELECT c.id_consulta, c.data_hora, c.observacoes, c.crm_medico, c.id_paciente FROM Consulta c WHERE c.id_consulta = {id_consulta}")
        
        if df_consulta.empty:
            return None

        # Se existe, recupera os IDs FK
        crm_medico = df_consulta.crm_medico.values[0]
        id_paciente = df_consulta.id_paciente.values[0]

        # Nota: Precisamos buscar o CPF do paciente para então buscar o objeto, 
        # pois o recuperar_dados_paciente usa o CPF como chave de busca principal (definido antes).

        df_paciente = oracle.sqlToDataFrame(f"SELECT cpf FROM Paciente WHERE id_paciente = {id_paciente}")
        cpf_paciente = df_paciente.cpf.values[0]

        # Recupera os OBJETOS FK completos
        medico_obj = self.recuperar_dados_medico(oracle, crm_medico)
        paciente_obj = self.recuperar_dados_paciente(oracle, cpf_paciente)

        # Cria e retorna o objeto Consulta
        return Consulta(
            df_consulta.id_consulta.values[0], 
            paciente_obj, 
            df_consulta.data_hora.values[0],
            medico_obj,
            df_consulta.observacoes.values[0]
        )