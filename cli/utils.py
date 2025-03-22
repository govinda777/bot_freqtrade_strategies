"""
Utilitários gerais para a CLI.
"""
import os
import json
from datetime import datetime
import click

def format_date(timestamp):
    """Formata um timestamp em data legível."""
    if not timestamp:
        return "N/A"
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError, AttributeError):
            return str(timestamp)

def save_json(data, filename=None):
    """Salva dados em um arquivo JSON."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True, filename
    except Exception as e:
        return False, str(e)

def confirm_action(message="Deseja continuar?", default=False):
    """Solicita confirmação do usuário."""
    return click.confirm(message, default=default)

def format_currency(amount, currency="USDT", decimals=2):
    """Formata um valor monetário."""
    if amount is None:
        return "N/A"
    return f"{float(amount):.{decimals}f} {currency}"

def parse_timerange(timerange):
    """Valida e formata o intervalo de tempo."""
    if not timerange:
        return None
        
    # Aceita formatos como: 20230101-20230201 ou 2023-01-01-2023-02-01
    if "-" in timerange:
        parts = timerange.split("-")
        if len(parts) != 2:
            raise ValueError("Formato de timerange inválido. Use: YYYYMMDD-YYYYMMDD")
            
        # Formatar partes para garantir que estejam no formato YYYYMMDD
        formatted_parts = []
        for part in parts:
            if len(part) == 10 and part.count("-") == 2:  # formato: YYYY-MM-DD
                formatted_parts.append(part.replace("-", ""))
            elif len(part) == 8:  # formato: YYYYMMDD
                formatted_parts.append(part)
            else:
                raise ValueError(f"Formato de data inválido: {part}. Use: YYYYMMDD ou YYYY-MM-DD")
                
        return f"{formatted_parts[0]}-{formatted_parts[1]}"
    else:
        raise ValueError("Formato de timerange inválido. Use: YYYYMMDD-YYYYMMDD")
