#Exercício 3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar dados do arquivo CSV
file_path = 'UNRATE.csv'
data = pd.read_csv(file_path)

# Converter a coluna de datas para o tipo datetime
data['DATE'] = pd.to_datetime(data['DATE'])

# Filtrar dados a partir do ano 2000
data = data[data['DATE'].dt.year >= 2000]

# Calcular a média móvel de três meses da taxa de desemprego
data['UNRATE_3MA'] = data['UNRATE'].rolling(window=3).mean()

# Calcular o Indicador de Sahm
data['Sahm_Indicator'] = np.nan

for i in range(len(data)):
    # Considerar os últimos 12 meses para o cálculo
    if i >= 11:
        # Encontrar o valor mínimo das médias móveis de três meses dos últimos 12 meses
        min_3ma_last_12_months = data['UNRATE_3MA'].iloc[i-11:i+1].min()
        # Calcular o indicador
        data.loc[data.index[i], 'Sahm_Indicator'] = data['UNRATE_3MA'].iloc[i] - min_3ma_last_12_months

# Gerar o gráfico
plt.figure(figsize=(14, 7))
plt.plot(data['DATE'], data['Sahm_Indicator'], label='Indicador de Sahm', color='blue')

# Preencher áreas onde o indicador é ativado (valor > 0.50)
plt.fill_between(data['DATE'], 0, data['Sahm_Indicator'], where=(data['Sahm_Indicator'] > 0.50), 
                 color='darkgray', alpha=0.5, label='Recessão Indicada')

plt.axhline(0.50, color='red', linestyle='--', linewidth=1, label='Limite de Recessão')
plt.title('Indicador de Recessão da Regra de Sahm')
plt.xlabel('Ano')
plt.ylabel('Indicador de Sahm')
plt.ylim(0, 10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()