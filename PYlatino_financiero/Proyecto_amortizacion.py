import pandas as pd
import numpy as np
import numpy_financial as npf
import os




def pedir_info():
    print("Proyecto de Amortización de Préstamos")
    print("-------------------------------------")
    print("A continuación tendremos una serie de preguntas las cuales nos ayudarán a calcular tu crédito y te dará una perspectiva de tus pagos mensuales\n")
    
    tasa_interes_anual = float(input("Por favor ingresa la tasa de interés anual (en porcentaje, por ejemplo 12.5): "))
    monto_prestamo = float(input("Por favor ingresa el monto del préstamo: "))
    plazo_meses = int(input("Por favor ingresa el plazo del préstamo en meses: "))
    
    print("\nCalculando el plan de amortización...\n")
    
    return tasa_interes_anual, monto_prestamo, plazo_meses

def calcular_amortizacion(Tasa_interes, Monto_prestamo, Plazo_meses):
    tasa_Mensual = (1 + Tasa_interes / 100) ** (1/12) - 1
    pago_mensual = npf.pmt(tasa_Mensual, Plazo_meses, -Monto_prestamo)


    tabla = [] 
    saldo = Monto_prestamo

    for mes in range(1, Plazo_meses + 1):
        interes = saldo * tasa_Mensual
        abono_capital = pago_mensual - interes
        saldo -= abono_capital

        tabla.append({
            "Mes": mes,
            "Pago Mensual": round(pago_mensual, 2),
            "Interés": round(interes, 2),
            "Abono a Capital": round(abono_capital, 2),
            "Saldo Restante": round(saldo if saldo > 0 else 0, 2)
        })

    df_amortizacion = pd.DataFrame(tabla)
    return df_amortizacion


def guardar_excel(df, nombre_archivo="Plan_Amortizacion.xlsx"):
    ruta_actual = os.getcwd()
    ruta_archivo = os.path.join(ruta_actual, nombre_archivo)
    df.to_excel(ruta_archivo, index=False)
    print(f"El plan de amortización ha sido guardado en: {ruta_archivo}")


def main():
    tasa_interes_anual, monto_prestamo, plazo_meses = pedir_info()
    tasa_Mensual = (1 + tasa_interes_anual / 100) ** (1/12) - 1
    tasa_Mensual = round(tasa_Mensual * 100, 4)
    df_amortizacion = calcular_amortizacion(tasa_interes_anual, monto_prestamo, plazo_meses)
    print(f"Plan de Amortización para un préstamo de {monto_prestamo} a una tasa anual de {tasa_interes_anual}% y en meses {tasa_Mensual}% a {plazo_meses} meses:\n")
    print(df_amortizacion)
    respuesta = input("desea guardar el plan de amortización en un archivo excel? Y/N: ")
    if respuesta.lower() == 'y':
        guardar_excel(df_amortizacion) 
    else:
        print("No se guardó el archivo.")





if __name__ == "__main__":
    main()