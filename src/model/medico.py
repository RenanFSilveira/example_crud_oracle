class Medico:
    def __init__(self, crm, nome, especialidade, telefone, email):
        self._crm = crm
        self._nome = nome
        self._especialidade = especialidade
        self._telefone = telefone
        self._email = email

    # Getters
    def get_crm(self):
        return self._crm

    def get_nome(self):
        return self._nome

    def get_especialidade(self):
        return self._especialidade

    def get_telefone(self):
        return self._telefone
    
    def get_email(self):
        return self._email

    # Setters
    def set_nome(self, nome):
        self._nome = nome

    def set_especialidade(self, especialidade):
        self._especialidade = especialidade

    def set_telefone(self, telefone):
        self._telefone = telefone
    
    # crm e email não tem SET pois são imutáveis.
    
    # Método to_string
    def to_string(self):
        return f"CRM: {self.get_crm()} | Nome: {self.get_nome()} | Especialidade: {self.get_especialidade()}"