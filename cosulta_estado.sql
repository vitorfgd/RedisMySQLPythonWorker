SELECT * FROM logradouro lo 
INNER JOIN bairros ba ON(lo.bairros_cd_bairro = ba.cd_bairro)
INNER JOIN cidades ci ON (ba.cidade_cd_cidade = ci.cd_cidade)
INNER JOIN uf ON (ci.uf_cd_uf = cd_uf)
WHERE ds_uf_sigla = "SC"