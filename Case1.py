#Exercício 1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar dados da planilha Excel, assumindo que a primeira coluna é a data
file_path = 'C:\Users\E490\AppData\Local\Temp\0039eb07-fc1e-40ef-85aa-02be0c905f0c_Avaliação.zip.f0c\retorno_acoes.xlsx' #Coloque o caminho para sua planilha .xlsx
df = pd.read_excel(file_path, parse_dates=['date'], index_col='date')

# Calcular retornos diários
returns = df.pct_change().dropna()

# Calcular retorno médio diário da carteira (igualmente ponderada)
portfolio_returns = returns.iloc[:, :-1].mean(axis=1)

# Calcular métricas
annualized_return = (1 + portfolio_returns.mean()) ** 252 - 1
annualized_volatility = portfolio_returns.std() * np.sqrt(252)
risk_free_rate = 0.05  # Suponha uma taxa livre de risco de 5%
sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility

# Calcular máximo drawdown
cumulative_returns = (1 + portfolio_returns).cumprod()
rolling_max = cumulative_returns.cummax()
drawdown = (cumulative_returns - rolling_max) / rolling_max
max_drawdown = drawdown.min()

# Calcular beta da carteira com o índice
cov_matrix = returns.cov()
beta = cov_matrix.iloc[:-1, -1].mean() / returns['IBOV'].var()

# Gráfico de Retorno Acumulado
plt.figure(figsize=(12, 6))
cumulative_returns.plot(title='Retorno Acumulado da Carteira', legend=False)
plt.xlabel('Data')
plt.ylabel('Retorno Acumulado')
plt.grid(True)
plt.show()

# Gráfico de Barras de Ganhos Anuais
annual_returns = portfolio_returns.resample('Y').apply(lambda x: (1 + x).prod() - 1)
ibov_annual_returns = returns['IBOV'].resample('Y').apply(lambda x: (1 + x).prod() - 1)

annual_comparison = pd.DataFrame({
    'Carteira': annual_returns,
    'Ibovespa': ibov_annual_returns
})

annual_comparison.plot(kind='bar', figsize=(12, 6))
plt.title('Comparação de Ganhos Anuais: Carteira vs Ibovespa')
plt.xlabel('Ano')
plt.ylabel('Retorno Anual')
plt.grid(True)
plt.show()

# Exibir métricas calculadas
print(f'Retorno Anualizado: {annualized_return:.2%}')
print(f'Volatilidade Anualizada: {annualized_volatility:.2%}')
print(f'Índice de Sharpe: {sharpe_ratio:.2f}')
print(f'Máximo Drawdown: {max_drawdown:.2%}')
print(f'Beta da Carteira: {beta:.2f}')