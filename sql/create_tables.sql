-- Tabelas
CREATE TABLE Medico (
    crm VARCHAR(15) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(50) NOT NULL,
    telefone VARCHAR(15),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE Paciente (
    id_paciente INTEGER PRIMARY KEY DEFAULT nextval('paciente_id_seq'),
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(15)
);

CREATE TABLE Consulta (
    id_consulta INTEGER PRIMARY KEY DEFAULT nextval('consulta_id_seq'),
    crm_medico VARCHAR(15) NOT NULL,
    id_paciente INTEGER NOT NULL,   
    data_hora TIMESTAMP NOT NULL,
    observacoes TEXT,
    
    CONSTRAINT fk_medico
        FOREIGN KEY (crm_medico)
        REFERENCES Medico (crm)
        ON DELETE RESTRICT, 
        
    CONSTRAINT fk_paciente
        FOREIGN KEY (id_paciente)
        REFERENCES Paciente (id_paciente)
        ON DELETE RESTRICT 
);

-- Sequences
CREATE SEQUENCE paciente_id_seq INCREMENT BY 1 START WITH 1;
CREATE SEQUENCE consulta_id_seq INCREMENT BY 1 START WITH 1;


-- 4. Criação de índices para otimizar consultas por especialidade e paciente
CREATE INDEX idx_medico_especialidade ON Medico (especialidade);
CREATE INDEX idx_consulta_paciente ON Consulta (id_paciente);