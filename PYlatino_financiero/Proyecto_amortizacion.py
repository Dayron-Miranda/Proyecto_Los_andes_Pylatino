import pandas as pd
import numpy as np
import os

#Tasa_interes = 

#def main



def pedir_info():
    print ("Proyecto de Amortización de Préstamos")
    print ("-------------------------------------")
    print ("Acontinuacion tendremos una serie de preguntas las cuales nos ayudaran a calcular tu credito y te dara una perspectiva de tus pagos mensuales")
    Tasa_interes = float(input("Por favor ingresa la tasa de interes anual (en porcentaje, por ejemplo 12.5): "))
    Monto_prestamo = float(input("Por favor ingresa el monto del préstamo: "))
    Plazo_meses = int(input("Por favor ingresa el plazo del préstamo en meses": "))
    print("\nCalculando el plan de amortización...\n") 
    

pedir_info()