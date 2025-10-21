SELECT
  m.crm,
  m.nome AS medico,
  m.especialidade,
  COUNT(c.id_consulta)            AS total_consultas,
  MIN(c.data_hora)                AS primeira_consulta,
  MAX(c.data_hora)                AS ultima_consulta
FROM Medico m
LEFT JOIN Consulta c
       ON c.crm = m.crm
GROUP BY
  m.crm, m.nome, m.especialidade
ORDER BY
  total_consultas DESC, m.nome;