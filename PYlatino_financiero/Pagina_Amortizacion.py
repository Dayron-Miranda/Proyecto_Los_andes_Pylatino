import streamlit as st
import pandas as pd
import numpy_financial as npf
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Amortización Proyecto PYlatino",
    page_icon="💰",
    layout="wide"
)

def calcular_amortizacion(tasa_interes, monto_prestamo, plazo_meses):
    """Calcula el plan de amortización del préstamo"""
    tasa_mensual = (1 + tasa_interes / 100) ** (1/12) - 1
    pago_mensual = npf.pmt(tasa_mensual, plazo_meses, -monto_prestamo)
    
    tabla = []
    saldo = monto_prestamo
    
    for mes in range(1, plazo_meses + 1):
        interes = saldo * tasa_mensual
        abono_capital = pago_mensual - interes
        saldo -= abono_capital
        
        tabla.append({
            "Mes": mes,
            "Pago Mensual": round(pago_mensual, 2),
            "Interés": round(interes, 2),
            "Abono a Capital": round(abono_capital, 2),
            "Saldo Restante": round(max(saldo, 0), 2)
        })
    
    df = pd.DataFrame(tabla)
    return df, pago_mensual, tasa_mensual

def crear_excel(df):
    """Genera archivo Excel en memoria"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Amortización')
    output.seek(0)
    return output.getvalue()

# Título principal
st.title("💰 Calculadora de Amortización Proyecto PYlatino")
st.markdown("---")

# Sección de entrada de datos
st.subheader("📝 Ingresa los datos de tu préstamo en caso de no saber la tasa de interes anual consulte la tasa de usura del día")

col1, col2, col3 = st.columns(3)

with col1:
    tasa_interes = st.number_input(
        "Tasa de interés anual (%)",
        min_value=0.01,
        max_value=100.0,
        value=12.5,
        step=0.1,
        format="%.2f",
        help="Ingresa la tasa de interés anual en porcentaje"
    )

with col2:
    monto_prestamo = st.number_input(
        "Monto del préstamo ($)",
        min_value=1.0,
        value=10000.0,
        step=100.0,
        format="%.2f",
        help="Ingresa el monto total del préstamo"
    )

with col3:
    plazo_meses = st.number_input(
        "Plazo (meses)",
        min_value=1,
        max_value=360,
        value=12,
        step=1,
        help="Ingresa el plazo del préstamo en meses"
    )

st.markdown("---")

# Botón para calcular
if st.button("🔢 Calcular Plan de Amortización", type="primary", use_container_width=True):
    try:
        # Calcular amortización
        df_amortizacion, pago_mensual, tasa_mensual = calcular_amortizacion(
            tasa_interes, monto_prestamo, plazo_meses
        )
        
        # Resumen del préstamo
        st.subheader("📊 Resumen del Préstamo")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Monto del Préstamo", f"${monto_prestamo:,.2f}")
        with col2:
            st.metric("Pago Mensual", f"${pago_mensual:,.2f}")
        with col3:
            st.metric("Tasa Anual", f"{tasa_interes}%")
        with col4:
            st.metric("Tasa Mensual", f"{tasa_mensual*100:.4f}%")
        
        # Totales
        total_pagado = pago_mensual * plazo_meses
        total_intereses = total_pagado - monto_prestamo
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total a Pagar", f"${total_pagado:,.2f}")
        with col2:
            st.metric("Total de Intereses", f"${total_intereses:,.2f}")
        with col3:
            st.metric("Plazo", f"{plazo_meses} meses")
        
        st.markdown("---")
        
        # Tabla de amortización
        st.subheader("📋 Tabla de Amortización")
        
        # Formatear para visualización
        df_display = df_amortizacion.copy()
        for col in ['Pago Mensual', 'Interés', 'Abono a Capital', 'Saldo Restante']:
            df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(
            df_display,
            use_container_width=True,
            height=400
        )
        
        # Botón de descarga
        excel_data = crear_excel(df_amortizacion)
        st.download_button(
            label="📥 Descargar Plan en Excel",
            data=excel_data,
            file_name="Plan_Amortizacion.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"❌ Error al calcular: {str(e)}")
        st.info("Por favor verifica que todos los datos sean correctos.")

else:
    st.info("👆 Ingresa los datos y presiona el botón para calcular tu plan de amortización")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Calculadora de Amortización de Préstamos v1.0</p>",
    unsafe_allow_html=True
)