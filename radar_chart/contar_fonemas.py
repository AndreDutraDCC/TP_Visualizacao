import json
from collections import Counter
import sys

if len(sys.argv) < 2:
    print("Por favor, forneça o nome do arquivo JSON como argumento.")
    sys.exit(1)

# Obtém o nome do arquivo a partir do argumento
nome_arquivo = sys.argv[1]

# Abre o arquivo JSON
with open(nome_arquivo, 'r') as file:
    data = json.load(file)

# Cria um único string com todos os fonemas
fonemas = ''.join(data.values())

# Conta a ocorrência de cada fonema
contador_fonemas = Counter(fonemas)

# Converte o resultado em um array de tuplas (fonema, quantidade)
resultado = [(fonema, quantidade) for fonema, quantidade in contador_fonemas.items()]
resultado_ordenado = sorted(resultado, key=lambda x: x[1], reverse=True)
# Exibe o resultado
for fonema, quantidade in resultado_ordenado:
    print(f"O fonema '{fonema}' aparece {quantidade} vezes.")