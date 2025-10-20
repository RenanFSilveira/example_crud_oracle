from model.medico import Medico
from model.paciente import Paciente

class Consulta:
    def __init__(self, id_consulta, paciente: Paciente, data_hora, medico: Medico, observacoes):
        self._id_consulta = id_consulta
        self._paciente = paciente
        self._data_hora = data_hora
        self._medico = medico
        self._observacoes = observacoes

    # Getters
    def get_id_consulta(self):
        return self._id_consulta

    def get_paciente(self):
        return self._paciente

    def get_data_hora(self):
        return self._data_hora
    
    def get_medico(self):
        return self._medico

    def get_observacoes(self):
        return self._observacoes

    # Setters
    def set_data_hora(self, data_hora):
        self._data_hora = data_hora

    def set_observacoes(self, observacoes):
        self._observacoes = observacoes
    
    # id_consulta, paciente e medico não tem SET pois são imutáveis.

    # Método to_string
    def to_string(self):
        return (f"id_consulta: {self.get_id_consulta()} | "
                f"Paciente: {self.get_paciente().get_nome()} (ID: {self.get_paciente().get_id_paciente()}) | "
                f"Médico: {self.get_medico().get_nome()} (CRM: {self.get_medico().get_crm()}) | "
                f"Data/Hora: {self.get_data_hora()}")