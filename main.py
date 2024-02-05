import pandas as pd
from flask import Flask, request, jsonify

# Leitura do arquivo Excel
excel_file = 'contratos.xlsx'
df = pd.read_excel(excel_file)

# Criar uma aplicação Flask
app = Flask(__name__)

# Rota para buscar por parâmetro
@app.route('/api-pgs', methods=['GET'])
def buscar_contrato():
    # Obter parâmetros da requisição
    descricao_situacao = request.args.get('descricao_situacao')
    codigo = request.args.get('codigo')
    num_contrato = request.args.get('num_contrato')

    # Inicializar resultado com o DataFrame original
    resultado = df.copy()

    # Renomear a coluna para torná-la mais amigável para URL
    resultado = resultado.rename(columns={'Descr.Sit.item cont.(enumerado)': 'situacao'})

    # Filtrar com base nos parâmetros fornecidos
    if descricao_situacao is not None and 'situacao' in resultado.columns:
        resultado = resultado[resultado['situacao'].str.lower() == descricao_situacao.lower()]
    else:
        resultado['situacao'] = ''

    # Filtrar por Cód, se o parâmetro for fornecido
    if codigo is not None and codigo != '' and 'Cód' in resultado.columns:
        resultado = resultado[resultado['Cód'] == int(codigo)]
    else:
        resultado['Cód'] = resultado['Cód'].astype(str)

    # Substituir NaN por vazio ou null
    resultado.replace({pd.NA: None, pd.NaT: None}, inplace=True)

    # Garantir que a coluna 'CNPJ/CPF' esteja sempre presente no resultado JSON
    resultado['CNPJ/CPF'] = resultado['CNPJ/CPF'].fillna('')

    # Filtrar por Núm.contrato, se o parâmetro for fornecido
    if num_contrato is not None and num_contrato != '' and 'Núm.contrato' in resultado.columns:
        resultado = resultado[resultado['Núm.contrato'] == int(num_contrato)]
    else:
        resultado['Núm.contrato'] = resultado['Núm.contrato'].astype(str)

    # Retornar o resultado em formato JSON
    return jsonify(resultado.to_dict(orient='records'))

# Executar a aplicação Flask
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
