import requests
from bs4 import BeautifulSoup
import re

def obtener_tasa_usura():
    """
    Extrae la tasa de usura de La República
    """
    url = "https://www.larepublica.co/indicadores-economicos/bancos/tasa-de-usura"
    
    try:
        # Hacer la solicitud
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse del HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar la tasa (puede variar según la estructura de la página)
        # Opción 1: Buscar por clase o id específico
        tasa_element = soup.find('div', class_='value') or soup.find('span', class_='indicator-value')
        
        if tasa_element:
            tasa_texto = tasa_element.get_text(strip=True)
            # Extraer solo el número
            tasa = float(re.findall(r'\d+[,.]?\d*', tasa_texto.replace(',', '.'))[0])
            return tasa
        else:
            # Opción 2: Buscar por patrón de texto
            texto_completo = soup.get_text()
            match = re.search(r'(\d+[,.]?\d*)\s*%', texto_completo)
            if match:
                tasa = float(match.group(1).replace(',', '.'))
                return tasa
                
    except Exception as e:
        print(f"Error al obtener la tasa: {e}")
        return None

# Usar la función
tasa_usura = obtener_tasa_usura()
print(f"Tasa de usura: {tasa_usura}%")