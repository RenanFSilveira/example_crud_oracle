-- Sequences
CREATE SEQUENCE paciente_id_seq INCREMENT BY 1 START WITH 1;
CREATE SEQUENCE consulta_id_seq INCREMENT BY 1 START WITH 1;

-- Tabelas
CREATE TABLE Medico (
    crm VARCHAR(15) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(50) NOT NULL,
    telefone VARCHAR(15),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE Paciente (
    id_paciente INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(15)
);

CREATE TABLE Consulta (
    id_consulta INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    crm_medico VARCHAR(15) NOT NULL,
    id_paciente INTEGER NOT NULL,   
    data_hora TIMESTAMP NOT NULL,
    observacoes VARCHAR2(3000),
    
    CONSTRAINT fk_medico
        FOREIGN KEY (crm_medico)
        REFERENCES Medico (crm),
        
    CONSTRAINT fk_paciente
        FOREIGN KEY (id_paciente)
        REFERENCES Paciente (id_paciente)
);




-- 4. Criação de índices para otimizar consultas por especialidade e paciente
CREATE INDEX idx_medico_especialidade ON Medico (especialidade);
CREATE INDEX idx_consulta_paciente ON Consulta (id_paciente);