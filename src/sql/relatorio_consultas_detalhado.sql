SELECT
  c.id_consulta,
  TO_CHAR(c.data_hora, 'DD/MM/YYYY HH24:MI') AS data_hora,
  p.id_paciente,
  p.nome       AS paciente,
  p.cpf        AS cpf_paciente,
  m.crm,
  m.nome       AS medico,
  m.especialidade,
  c.observacoes
FROM Consulta c
JOIN Paciente p ON p.id_paciente = c.id_paciente
JOIN Medico   m ON m.crm         = c.crm
ORDER BY c.data_hora DESC;