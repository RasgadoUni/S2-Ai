import streamlit as st
import pandas as pd
from datetime import datetime

# Inicialización del estado de la sesión
if 'transacciones' not in st.session_state:
    st.session_state.transacciones = []

if 'balances' not in st.session_state:
    st.session_state.balances = {
        "Activo": {
            "Caja": 0, "Bancos": 0, "Mercancías": 0, "Terrenos": 0, "Edificios": 0, 
            "Equipo de cómputo": 0, "Mobiliario y equipo": 0, "Muebles y enseres": 0, 
            "IVA pagado": 0, "Rentas Pagadas por Anticipado": 0, "Anticipo de clientes": 0, 
            "Papelería": 0, "Equipo de Reparto": 0, "Clientes": 0
        },
        "Pasivo": {
            "Acreedores": 0, "Documentos por pagar": 0, "IVA por acreditar": 0, 
            "IVA trasladado": 0, "IVA por trasladar": 0
        },
        "Capital": {
            "Capital Social": 0
        },
        "Depreciación": {
            "Depreciación Edificio": 0,
            "Depreciación Equipo Reparto": 0,
            "Depreciación Mobiliario y Equipo": 0,
            "Depreciación Muebles y Enseres": 0,
            "Depreciación Equipo de Cómputo": 0
        },
        "Ingresos": {
            "Ventas": 0
        },
        "Costos": {
            "Costo de lo Vendido": 0
        },
        "Gastos": {
            "Gastos Generales": 0
        }
    }

if 'libro_mayor' not in st.session_state:
    st.session_state.libro_mayor = {}

# Función para actualizar los balances
def actualizar_balances(transaccion):
    for cuenta, monto in transaccion["deber"].items():
        if cuenta in st.session_state.balances["Activo"]:
            st.session_state.balances["Activo"][cuenta] += monto
        elif cuenta in st.session_state.balances["Pasivo"]:
            st.session_state.balances["Pasivo"][cuenta] += monto
        elif cuenta in st.session_state.balances["Capital"]:
            st.session_state.balances["Capital"][cuenta] += monto
        elif cuenta in st.session_state.balances["Depreciación"]:
            st.session_state.balances["Depreciación"][cuenta] += monto
        elif cuenta in st.session_state.balances["Ingresos"]:
            st.session_state.balances["Ingresos"][cuenta] += monto
        elif cuenta in st.session_state.balances["Costos"]:
            st.session_state.balances["Costos"][cuenta] += monto
        elif cuenta in st.session_state.balances["Gastos"]:
            st.session_state.balances["Gastos"][cuenta] += monto

        if cuenta not in st.session_state.libro_mayor:
            st.session_state.libro_mayor[cuenta] = {"Debe": [], "Haber": []}
        st.session_state.libro_mayor[cuenta]["Debe"].append(monto)

    for cuenta, monto in transaccion["haber"].items():
        if cuenta in st.session_state.balances["Activo"]:
            st.session_state.balances["Activo"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Pasivo"]:
            st.session_state.balances["Pasivo"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Capital"]:
            st.session_state.balances["Capital"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Depreciación"]:
            st.session_state.balances["Depreciación"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Ingresos"]:
            st.session_state.balances["Ingresos"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Costos"]:
            st.session_state.balances["Costos"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Gastos"]:
            st.session_state.balances["Gastos"][cuenta] -= monto

        if cuenta not in st.session_state.libro_mayor:
            st.session_state.libro_mayor[cuenta] = {"Debe": [], "Haber": []}
        st.session_state.libro_mayor[cuenta]["Haber"].append(monto)

# Función para registrar transacciones
def registrar_transaccion(transaccion):
    transaccion["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.transacciones.append(transaccion)
    actualizar_balances(transaccion)
    st.success("✅ Transacción registrada correctamente.")

# Configuración de la página
st.set_page_config(page_title="Sistema Contable", layout="wide", page_icon="💰")

# Título principal con estilo
st.markdown(
    """
    <style>
    .title {
        font-size: 45px;
        font-weight: bold;
        color: #326273;
        text-align: center;
        padding: 20px;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    <div class="title">💰 Sistema de Registro Contable</div>
    """,
    unsafe_allow_html=True
)

# Selección del tipo de transacción
tipo_transaccion = st.selectbox(
    'Tipo de Transacción',
    ['Asiento de apertura', 'Compra en efectivo', 'Compra a crédito', 'Compra combinada', 
     'Pago de rentas anticipadas','Anticipo de clientes', 'Compra de papelería',  
     'Primera Venta', 'Adelanto de Rentas', 'Segunda Venta', 'Depreciación']
)

# Campos del formulario según el tipo de transacción
if tipo_transaccion == 'Asiento de apertura':
    caja = st.number_input("Caja", value=50000)
    bancos = st.number_input("Bancos", value=500000)
    mercancias = st.number_input("Mercancías", value=500000)
    terrenos = st.number_input("Terrenos", value=1000000)
    edificios = st.number_input("Edificios", value=500000)
    eq_computo = st.number_input("Equipo de cómputo", value=50000)
    mob_equipo = st.number_input("Mobiliario y equipo", value=30000)
    muebles_enseres = st.number_input("Muebles y enseres", value=120000)
    capital_social = st.number_input("Capital Social", value=2750000)

elif tipo_transaccion == 'Compra en efectivo':
    mercancias = st.number_input("Mercancías", value=15000)
    iva = st.number_input("IVA", value=mercancias * 0.16)
    caja = st.number_input("Caja", value=mercancias + iva)

elif tipo_transaccion == 'Compra a crédito':
    eq_reparto = st.number_input("Equipo de Reparto", value=300000)
    iva = st.number_input("IVA", value=eq_reparto * 0.16)
    acreedores = st.number_input("Acreedores", value=eq_reparto + iva)

elif tipo_transaccion == 'Compra combinada':
    mercancias = st.number_input("Mercancías", value=20000)
    iva = st.number_input("IVA", value=(mercancias / 2) * 0.16)
    ivaA = st.number_input("IVA por acreditar", value=(mercancias / 2) * 0.16)
    caja = st.number_input("Caja (pago en efectivo)", value=(mercancias / 2) + iva)
    documentos_por_pagar = st.number_input("Documentos por pagar (crédito)", value=(mercancias / 2) + ivaA)

elif tipo_transaccion == 'Anticipo de clientes':
    anticipo = st.number_input("Anticipo de clientes", value=1500)
    iva_trasladado = st.number_input("IVA", value=anticipo * 0.16)
    caja = st.number_input("Caja", value=anticipo + iva_trasladado)

elif tipo_transaccion == 'Compra de papelería':
    papelería = st.number_input("Papelería", value=800)
    iva = st.number_input("IVA", value=papelería * 0.16)
    caja = st.number_input("Caja", value=papelería + iva)

elif tipo_transaccion == 'Pago de rentas anticipadas':
    rentas = st.number_input("Rentas pagadas por anticipado", value=12000)
    iva = st.number_input("IVA", value=rentas * 0.16)
    caja = st.number_input("Caja", value=rentas + iva)

elif tipo_transaccion == 'Primera Venta':
    venta = st.number_input("Ventas", value=50000)
    iva_trasladado = st.number_input("IVA Trasladado", value=venta * 0.16)
    costo_lo_vendido = st.number_input("Costo de lo Vendido", value=venta / 2)
    bancos = st.number_input("Bancos", value=venta + iva_trasladado)
    mercancias = st.number_input("Mercancías", value=costo_lo_vendido)

elif tipo_transaccion == 'Adelanto de Rentas':
    gastos_generales = st.number_input("Gastos Generales", value=6000)
    rentas_pagadas = st.number_input("Rentas Pagadas por Anticipado", value=gastos_generales)

elif tipo_transaccion == 'Segunda Venta':
    venta = st.number_input("Ventas", value=3000)
    anticipo_clientes = st.number_input("Anticipo de clientes (50% de la venta)", value=venta/2)
    iva_trasladado = st.number_input("IVA Trasladado (16% del anticipo)", value=anticipo_clientes*0.16)
    clientes = st.number_input("Clientes (Anticipo + IVA)", value=anticipo_clientes + iva_trasladado)
    iva_por_trasladar = st.number_input("IVA por trasladar", value=iva_trasladado)
    costo_vendido = st.number_input("Costo de lo Vendido (50% de la venta)", value=venta/2)
    inventario = st.number_input("Inventario (Mercancías)", value=venta/2)

elif tipo_transaccion == 'Depreciación':
    st.write("### Ajuste por Depreciación Mensual")
    st.write("|------------------------|------------|---------|--------------------|----------------------|")

# Botón para registrar la transacción
if st.button("Registrar Transacción"):
    if tipo_transaccion == 'Asiento de apertura':
        transaccion = {
            "tipo": "Asiento de apertura",
            "deber": {
                "Caja": caja,
                "Bancos": bancos,
                "Mercancías": mercancias,
                "Terrenos": terrenos,
                "Edificios": edificios,
                "Equipo de cómputo": eq_computo,
                "Mobiliario y equipo": mob_equipo,
                "Muebles y enseres": muebles_enseres
            },
            "haber": {
                "Capital Social": capital_social
            }
        }
    elif tipo_transaccion == 'Compra en efectivo':
        transaccion = {
            "tipo": "Compra en efectivo",
            "deber": {
                "Mercancías": mercancias,
                "IVA pagado": iva
            },
            "haber": {
                "Caja": caja
            }
        }
    elif tipo_transaccion == 'Compra a crédito':
        transaccion = {
            "tipo": "Compra a crédito",
            "deber": {
                "Equipo de Reparto": eq_reparto,
                "IVA por acreditar": iva
            },
            "haber": {
                "Acreedores": acreedores
            }
        }
    elif tipo_transaccion == 'Compra combinada':
        transaccion = {
            "tipo": "Compra combinada",
            "deber": {
                "Mercancías": mercancias,
                "IVA pagado": iva,
                "IVA por acreditar": ivaA
            },
            "haber": {
                "Caja": caja,
                "Documentos por pagar": documentos_por_pagar
            }
        }
    elif tipo_transaccion == 'Anticipo de clientes':
        transaccion = {
            "tipo": "Anticipo de clientes",
            "deber": {
                "Caja": caja
            },
            "haber": {
                "Anticipo de clientes": anticipo,
                "IVA trasladado": iva_trasladado
            }
        }
    elif tipo_transaccion == 'Compra de papelería':
        transaccion = {
            "tipo": "Compra de papelería",
            "deber": {
                "Papelería": papelería,
                "IVA pagado": iva
            },
            "haber": {
                "Caja": caja
            }
        }
    elif tipo_transaccion == 'Pago de rentas anticipadas':
        transaccion = {
            "tipo": "Pago de rentas anticipadas",
            "deber": {
                
                "IVA pagado": iva
            },
            "haber": {
                "Caja": caja,
                "Rentas pagadas por anticipado": rentas,
            }
        }
    elif tipo_transaccion == 'Depreciación':
        transaccion = {
            "tipo": "Depreciación",
            "deber": {
                "Gastos Generales": 10833.33
            },
            "haber": {
                "Depreciación Edificio": 2083.33,
                "Depreciación Equipo Reparto": 1250.00,
                "Depreciación Mobiliario y Equipo": 250.00,
                "Depreciación Muebles y Enseres": 1000.00,
                "Depreciación Equipo de Cómputo": 6250.00,
            }
        }
    elif tipo_transaccion == 'Primera Venta':
        transaccion = {
            "tipo": "Primera Venta",
            "deber": {
                "Bancos": bancos,
                "Costo de lo Vendido": costo_lo_vendido
            },
            "haber": {
                "Ventas": venta,
                "IVA Trasladado": iva_trasladado,
                "Mercancías": mercancias
            }
        }
    elif tipo_transaccion == 'Adelanto de Rentas':
        transaccion = {
            "tipo": "Adelanto de Rentas",
            "deber": {
                "Gastos Generales": gastos_generales
            },
            "haber": {
                "Rentas Pagadas por Anticipado": rentas_pagadas
            }
        }
    elif tipo_transaccion == 'Segunda Venta':
        transaccion = {
            "tipo": "Segunda Venta",
            "deber": {
                "Clientes": clientes,
                "Costo de lo Vendido": costo_vendido,
                "Anticipo de clientes": anticipo_clientes,
                "IVA trasladado": iva_trasladado
            },
            "haber": {
                "IVA Trasladado a credito": iva_trasladado,
                "IVA por trasladar": iva_por_trasladar,
                "Ventas": venta,
                "Mercancías": inventario
            }
        }
    registrar_transaccion(transaccion)

# Mostrar transacciones registradas
st.markdown("### 📋 Transacciones Registradas")
if st.session_state.transacciones:
    st.dataframe(pd.DataFrame(st.session_state.transacciones), use_container_width=True)
else:
    st.info("No hay transacciones registradas.")

# Mostrar balance general
st.markdown("### 📊 Balance General")
activo_df = pd.DataFrame.from_dict(st.session_state.balances["Activo"], orient="index", columns=["Monto"])
pasivo_df = pd.DataFrame.from_dict(st.session_state.balances["Pasivo"], orient="index", columns=["Monto"])
capital_df = pd.DataFrame.from_dict(st.session_state.balances["Capital"], orient="index", columns=["Monto"])
depreciacion_df = pd.DataFrame.from_dict(st.session_state.balances["Depreciación"], orient="index", columns=["Monto"])
ingresos_df = pd.DataFrame.from_dict(st.session_state.balances["Ingresos"], orient="index", columns=["Monto"])
costos_df = pd.DataFrame.from_dict(st.session_state.balances["Costos"], orient="index", columns=["Monto"])
gastos_df = pd.DataFrame.from_dict(st.session_state.balances["Gastos"], orient="index", columns=["Monto"])

st.write("### Activo")
st.dataframe(activo_df)

st.write("### Pasivo")
st.dataframe(pasivo_df)

st.write("### Capital")
st.dataframe(capital_df)

st.write("### Depreciación")
st.dataframe(depreciacion_df)

st.write("### Ingresos")
st.dataframe(ingresos_df)

st.write("### Costos")
st.dataframe(costos_df)

st.write("### Gastos")
st.dataframe(gastos_df)

# Mostrar balanza de comprobación corregida
st.markdown("### ⚖️ Balanza de Comprobación")

# Crear listas para la balanza
cuentas = []
debe = []
haber = []

# Recopilar todos los saldos de las cuentas
for categoria, cuentas_categoria in st.session_state.balances.items():
    for cuenta, saldo in cuentas_categoria.items():
        if saldo > 0:  # Saldo deudor (Debe)
            cuentas.append(cuenta)
            debe.append(abs(saldo))
            haber.append(0)
        elif saldo < 0:  # Saldo acreedor (Haber)
            cuentas.append(cuenta)
            debe.append(0)
            haber.append(abs(saldo))
        # No mostramos cuentas con saldo cero

# Crear DataFrame para la balanza
balanza_df = pd.DataFrame({
    "Cuenta": cuentas,
    "Debe": debe,
    "Haber": haber
})

# Calcular totales
total_debe = balanza_df["Debe"].sum()
total_haber = balanza_df["Haber"].sum()

# Mostrar la balanza
st.dataframe(
    balanza_df.style.format({
        "Debe": "${:,.2f}",
        "Haber": "${:,.2f}"
    }),
    use_container_width=True
)

# Mostrar totales
st.write(f"**Total Debe:** ${total_debe:,.2f}")
st.write(f"**Total Haber:** ${total_haber:,.2f}")

# Título del Estado de Resultados
st.markdown("### 📈 Estado de Resultados")

# Verificar si las cuentas existen en session_state
if "balances" in st.session_state:
    # Obtener los valores de las cuentas relevantes
    ventas = st.session_state.balances["Ingresos"].get("Ventas", 0)
    costo_ventas = st.session_state.balances["Costos"].get("Costo de lo Vendido", 0)
    gastos_generales = st.session_state.balances["Gastos"].get("Gastos Generales", 0)

    # Calcular las utilidades
    utilidad_bruta = ventas + costo_ventas
    utilidad_periodo = utilidad_bruta + gastos_generales

    # Crear el DataFrame para el Estado de Resultados
    estado_resultados = pd.DataFrame({
        "Concepto": ["Ventas", "Costo de lo Vendido", "Utilidad Bruta", 
                     "Gastos Generales", "Utilidad del Período"],
        "Monto": [-ventas, costo_ventas, -utilidad_bruta, 
                  gastos_generales, -utilidad_periodo]
    })

    # Mostrar el Estado de Resultados con formato
    st.dataframe(
        estado_resultados.style.format({"Monto": "${:,.2f}"}),
        use_container_width=True
    )

    # Mostrar resumen con métricas y colores
    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas Totales", f"${-ventas:,.2f}")
    col2.metric("Utilidad Bruta", f"${-utilidad_bruta:,.2f}", 
                delta=f"{(utilidad_bruta/ventas*100 if ventas !=0 else 0):.1f}%")
    col3.metric("Utilidad Neta", f"${-utilidad_periodo:,.2f}", 
                delta=f"{(utilidad_periodo/ventas*100 if ventas !=0 else 0):.1f}%", 
                delta_color="inverse" if utilidad_periodo < 0 else "normal")

else:
    st.error("No hay datos en balances. Asegúrate de registrar transacciones primero.")
    
# Mostrar libro mayor
st.markdown("### 📚 Libro Mayor")
for cuenta, movimientos in st.session_state.libro_mayor.items():
    st.write(f"Cuenta: {cuenta}")

    debe_mov = [abs(monto) for monto in movimientos["Debe"]]
    haber_mov = [abs(monto) for monto in movimientos["Haber"]]

    data = []

    for i, monto_debe in enumerate(debe_mov):
        data.append({"Movimiento": f"Debe {i+1}", "Monto": monto_debe, "Tipo": "Debe"})

    for i, monto_haber in enumerate(haber_mov):
        data.append({"Movimiento": f"Haber {i+1}", "Monto": monto_haber, "Tipo": "Haber"})

    df_cuenta = pd.DataFrame(data)

    total_debe_mov = sum(debe_mov)
    total_haber_mov = sum(haber_mov)
    diferencia = total_debe_mov - total_haber_mov
    if diferencia > 0:
        mayor = "Debe"
    elif diferencia < 0:
        mayor = "Haber"
    else:
        mayor = "Iguales"

    df_totales = pd.DataFrame({
        "Movimiento": ["Totales"],
        "Monto": [abs(diferencia)],
        "Tipo": [mayor]
    })

    df_final = pd.concat([df_cuenta, df_totales], ignore_index=True)

    st.dataframe(df_final)
    st.write("---")
