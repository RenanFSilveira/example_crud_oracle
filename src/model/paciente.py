class Paciente:
    def __init__(self, id_paciente, nome, data_nascimento, cpf, telefone):
        self._id_paciente = id_paciente
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf
        self._telefone = telefone

    # Getters
    def get_id_paciente(self):
        return self._id_paciente

    def get_nome(self):
        return self._nome

    def get_data_nascimento(self):
        return self._data_nascimento

    def get_cpf(self):
        return self._cpf
    
    def get_telefone(self):
        return self._telefone

    # Setters
    def set_nome(self, nome):
        self._nome = nome

    def set_data_nascimento(self, data_nascimento):
        self._data_nascimento = data_nascimento

    def set_telefone(self, telefone):
        self._telefone = telefone

    # id_paciente e cpf não tem um SET pois são imutáveis.
    
    # Método to_string
    def to_string(self):   
        return (f"id_paciente: {self.get_id_paciente()} | Nome: {self.get_nome()} | "
                f"data_nascimento: {self.get_data_nascimento()}")