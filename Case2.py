#Exercício 2

import pandas as pd
import numpy as np

# Carregar dados da planilha Excel
file_path = 'C:\Users\E490\AppData\Local\Temp\0039eb07-fc1e-40ef-85aa-02be0c905f0c_Avaliação.zip.f0c\retorno_acoes.xlsx' #Coloque o caminho para sua planilha .xlsx
data = pd.read_excel(file_path)

# Converter a coluna de datas para o tipo datetime
data['date'] = pd.to_datetime(data['date'])

# Calcular retornos diários
returns = data.set_index('date').pct_change()

# Calcular retornos mensais
monthly_returns = returns.resample('M').sum()

# Implementar Estratégia 1 (trend)
def trend_strategy(monthly_returns):
    best_performers = monthly_returns.idxmax(axis=1)
    trend_portfolio = pd.DataFrame(index=monthly_returns.index, columns=monthly_returns.columns)
    
    for date in monthly_returns.index:
        trend_portfolio.loc[date, best_performers[date]] = 1
    
    trend_returns = (trend_portfolio.shift(1) * monthly_returns).sum(axis=1)
    return trend_returns

# Implementar Estratégia 2 (revert)
def revert_strategy(monthly_returns):
    worst_performers = monthly_returns.idxmin(axis=1)
    revert_portfolio = pd.DataFrame(index=monthly_returns.index, columns=monthly_returns.columns)
    
    for date in monthly_returns.index:
        revert_portfolio.loc[date, worst_performers[date]] = 1
    
    revert_returns = (revert_portfolio.shift(1) * monthly_returns).sum(axis=1)
    return revert_returns

# Calcular retornos das estratégias
trend_returns = trend_strategy(monthly_returns)
revert_returns = revert_strategy(monthly_returns)

# Avaliar as estratégias
def evaluate_strategy(strategy_returns):
    total_return = strategy_returns.sum()
    annualized_return = (1 + total_return) ** (12 / len(strategy_returns)) - 1
    volatility = strategy_returns.std() * np.sqrt(12)  # Anualizando a volatilidade
    sharpe_ratio = annualized_return / volatility
    
    return {
        'Total Return': total_return,
        'Annualized Return': annualized_return,
        'Volatility': volatility,
        'Sharpe Ratio': sharpe_ratio
    }

trend_evaluation = evaluate_strategy(trend_returns)
revert_evaluation = evaluate_strategy(revert_returns)

print("Trend Strategy Evaluation:", trend_evaluation)
print("Revert Strategy Evaluation:", revert_evaluation)

# Escolher estratégia preferida
preferred_strategy = 'Trend' if trend_evaluation['Sharpe Ratio'] > revert_evaluation['Sharpe Ratio'] else 'Revert'
print("Preferred Strategy:", preferred_strategy)