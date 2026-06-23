with open(r'd:\AntiGravity\projeto_01\LP_ORCAMENTO_INTERNO\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('DL Ignis (ERRADO - deve ser 0)', html.count('DL Ignis'), 0),
    ('DL Alerta (CORRETO)', html.count('DL Alerta'), 1),
    ('DL GateKeeper (CORRETO)', html.count('DL GateKeeper'), 1),
    ('DL Suporte Grill', html.count("DL Suporte Grill"), 1),
    ('CAMPOS_TECNICOS_DL bug (deve ser 0)', html.count('CAMPOS_TECNICOS_DL'), 0),
    ('cl_cpf presente', html.count('cl_cpf'), 1),
    ('cl_cnpj presente', html.count('cl_cnpj'), 1),
    ('cl_em_shopping presente', html.count('cl_em_shopping'), 1),
    ('cl_tipo_imovel presente', html.count('cl_tipo_imovel'), 1),
    ('contatora', html.count('ontatora'), 1),
    ('resistencia inferior', html.count('inferior'), 1),
    ('resistencia superior', html.count('superior'), 1),
    ('termostato', html.count('ermostato'), 1),
    ('paca paca', html.count('paca paca'), 1),
    ('display', html.count('Display'), 1),
    ('seletora', html.count('eletora'), 1),
    ('suspensao de chapa', html.count('uspens'), 1),
    ('PVC de protecao', html.count('PVC de prote'), 1),
    ('chicote interno', html.count('chicote interno'), 1),
    ('chicote 127/220', html.count('127/220'), 1),
    ('chicote 220/380', html.count('220/380'), 1),
    ('POOL_CAMPOS.grills', html.count('grills'), 1),
    ('onTipoClienteChange', html.count('onTipoClienteChange'), 1),
    ('dyn-input no submit', html.count('dyn-input'), 1),
    ('Restaurante/Lanchonete', html.count('Restaurante/Lanchonete'), 1),
    ('Loja Comercial', html.count('Loja Comercial'), 1),
    ('Padaria', html.count('Padaria'), 1),
]

print('=== VALIDACAO COMPLETA ===')
ok = 0
fail = 0
for name, actual, min_expected in checks:
    if min_expected == 0:
        passed = actual == 0
    else:
        passed = actual >= min_expected
    status = 'OK' if passed else 'FALHA'
    if passed:
        ok += 1
    else:
        fail += 1
    print(f'  [{status}] {name} = {actual}')

print(f'\nResultado: {ok} OK / {fail} FALHA')
