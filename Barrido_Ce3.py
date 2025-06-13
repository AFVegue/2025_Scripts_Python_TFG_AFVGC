# Librerias
import numpy as np
import win32com.client
import csv
import pandas as pd
import matplotlib.pyplot as plt


# Enlaza con mediante la API de python
awrde = win32com.client.Dispatch('MWOApp.MWOffice')

# Establezco las frecuencias
freqs = np.linspace(0.1e9, 10e9, 9901, endpoint=True)
awrde.Project.Frequencies.Clear()
awrde.Project.Frequencies.AddMultiple(freqs)

# Empiezo el proyecto
# Elimina el esquema si ya existe con ese nombre
if awrde.Project.Schematics.Exists("active_feedback_ampli"):
    awrde.Project.Schematics.Remove("active_feedback_ampli")

# Copiar el esquema "SUB" como nuevo esquema de trabajo
awrde.Project.Schematics.Copy("SUB", "active_feedback_ampli")

# Accedemos a la copia
s = awrde.Project.Schematics("active_feedback_ampli")



# Añadir elementos al esquematico
p1 = s.Elements.Add("PORT", 0, 0, 0, False)
p2 = s.Elements.Add("PORT", 6000, 400, 0, False)
c4 = s.Elements.Add("CAP", 0, 0, 0, False)
c6 = s.Elements.Add("CAP", 1000, 0, -90, False)
c3 = s.Elements.Add("CAP", 1400, -1600, 0, False)
c8 = s.Elements.Add("CAP", 6000, -600, -90, False)
c7 = s.Elements.Add("CAP", 7100, -600, -90, False)
c2 = s.Elements.Add("CAP", 1000, 3200, -90, False)
c1 = s.Elements.Add("CAP", 5800, 3200, -90, False)
l2 = s.Elements.Add("IND", 3900, -1600, 0, False)
l3 = s.Elements.Add("IND", 2700, 700, -90, True)
l1 = s.Elements.Add("IND", 4700, 900, -90, True)
r1 = s.Elements.Add("RES", 2700, 3200, -90, False)
r2 = s.Elements.Add("RES", 1900, 3200, -90, False)
rl2 = s.Elements.Add("RES", 4700, 3200, -90, False)
gnd1 = s.Elements.Add("GND", 1000, 1000, 0, False)
gnd2 = s.Elements.Add("GND", 7100, 400, 0, False)
gnd3 = s.Elements.Add("GND", 1000, 4200, 0, False)
gnd4 = s.Elements.Add("GND", 1900, 4200, 0, False)
gnd5 = s.Elements.Add("GND", 5800, 4200, 0, False)
gndSUB1 = s.Elements.Add("GND", 4200, -400, 0, True)
gnd2SUB2 = s.Elements.Add("GND", 4200, 400, 0, False)
gndDC = s.Elements.Add("GND", 4700, 5700, 0, False)
DC = s.Elements.Add("DCVS", 4700, 4700, 0, False)
node_vb = s.Elements.Add("PORT_NAME", 3500, 0, -270, False)
node_vc = s.Elements.Add("PORT_NAME", 4700, 0, -180, False)

# Cableado
s.Wires.Add(c3.Nodes.Item(2).x, c3.Nodes.Item(2).y, l2.Nodes.Item(1).x, l2.Nodes.Item(1).y)
s.Wires.Add(1000, 0, 1000, -1600)
s.Wires.Add(1000, -1600, 1400, -1600)
s.Wires.Add(1000, 0, 3700, 0)
s.Wires.Add(2700, 0, 2700, 700)
s.Wires.Add(2700, 1700, 2700, 3200)
s.Wires.Add(1000, 3200, 1000, 2700)
s.Wires.Add(1900, 3200, 1900, 2700)
s.Wires.Add(1000, 2700, 1900, 2700)
s.Wires.Add(1900, 2700, 2700, 2700)
s.Wires.Add(2700, 4200, 2700, 4700)
s.Wires.Add(4700, 4200, 4700, 4700)
s.Wires.Add(2700, 4700, 4700, 4700)
s.Wires.Add(4900, -1600, 6000, -1600)
s.Wires.Add(6000, -1600, 6000, -600)
s.Wires.Add(6000, -900, 7100, -900)
s.Wires.Add(7100, -900, 7100, -600)
s.Wires.Add(6000, -900, 4700, -900)
s.Wires.Add(4700, -900, 4700, 900)
s.Wires.Add(4700, 1900, 4700, 3200)
s.Wires.Add(4700, 2700, 5800, 2700)
s.Wires.Add(5800, 2700, 5800, 3200)

# Valores de componentes
Rb1 = 9700
Rb2 = 1000
Rc = 400
Vdc = 10
Lchoke = 32.48e-9
Cdc = 13e-12
Cb1 = 1e-12
Ce1 = 6e-12
Cc1 = 1e-12
Lc1 = 1e-9
c4.parameters("C").ValueAsDouble = Cdc
c6.parameters("C").ValueAsDouble = Cb1
#c3.parameters("C").ValueAsDouble = Cc1
l2.parameters("L").ValueAsDouble = Lc1
c8.parameters("C").ValueAsDouble = Cdc
c7.parameters("C").ValueAsDouble = Ce1
c2.parameters("C").ValueAsDouble = Cdc
r2.parameters("R").ValueAsDouble = Rb2
r1.parameters("R").ValueAsDouble = Rb1
rl2.parameters("R").ValueAsDouble = Rc
c1.parameters("C").ValueAsDouble = Cdc
l3.parameters("L").ValueAsDouble = Lchoke
l1.parameters("L").ValueAsDouble = Lchoke
DC.Parameters("V").ValueAsDouble = Vdc

# Barrido de valores de ce3
ce3_values = np.random.uniform(0.75e-12, 1.25e-12, 10)


################### Carta de Smith ce3 #####################

# Abrimos un archivo CSV para escritura y definimos el writer
with open("datos_ndf.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Escribimos la cabecera del archivo con los nombres de las columnas
    writer.writerow(["ce3 (F)", "Frecuencia (Hz)", "NDF_Re", "NDF_Im"])

    # Iteramos sobre todos los valores del condensador ce3
    for ce3_val in ce3_values:
        # Asignamos el valor actual al parámetro "C" del componente c3
        c3.parameters("C").ValueAsDouble = ce3_val

        try:
            # Accedemos a la colección de gráficos del proyecto de AWR
            graphs = awrde.Project.Graphs

            # Comprobamos si existe el gráfico requerido para medir NDF
            if not graphs.Exists("PYTHON_active_feedback_ndf"):
                print("Error: el gráfico no existe.")
                break  # Si no existe, salimos del bucle

            # Accedemos al gráfico donde se evaluará el NDF
            g = graphs("PYTHON_active_feedback_ndf")

            # Añadimos medidas para obtener la parte real e imaginaria del NDF
            m_re = g.Measurements.Add("active_feedback_ampli.AP", "Re(NDF())")
            m_im = g.Measurements.Add("active_feedback_ampli.AP", "Im(NDF())")

            # Ejecutamos la simulación para ambas medidas
            m_re.SimulateMeasurement()
            m_im.SimulateMeasurement()

            # Extraemos el eje X (frecuencia) y los valores simulados Y
            freqs = m_re.XValues
            vals_re = m_re.YValues(1)  # Parte real de NDF
            vals_im = m_im.YValues(1)  # Parte imaginaria de NDF

            # Guardamos los datos en el CSV: ce3, frecuencia, Re(NDF), Im(NDF)
            for f, re, im in zip(freqs, vals_re, vals_im):
                writer.writerow([ce3_val, f, re, im])

        except Exception as e:
            # Capturamos e imprimimos errores, por ejemplo si falla la simulación
            print(f"Error en ce3 = {ce3_val*1e12:.2f} pF: {e}")



# Cargamos el CSV generado a un DataFrame de pandas
df = pd.read_csv("datos_ndf.csv")

# Combinamos las columnas Re e Im en una nueva columna de tipo complejo
df["NDF"] = df["NDF_Re"] + 1j * df["NDF_Im"]

# Extraemos las frecuencias únicas y los valores únicos de ce3
frequencies = sorted(df["Frecuencia (Hz)"].unique())
ce3_vals = df["ce3 (F)"].unique()

# Inicializamos una figura polar (tipo carta de Smith modificada)
plt.figure(figsize=(7, 7))
ax = plt.subplot(111, projection="polar")

# Recorremos cada valor de ce3 y trazamos su trayectoria de NDF en el plano polar
for ce3 in ce3_vals:
    subset = df[df["ce3 (F)"] == ce3]  # Filtramos datos para este ce3
    ndf = subset["NDF"].values         # Obtenemos los valores complejos
    theta = np.angle(ndf)              # Ángulo de NDF (fase)
    r = np.abs(ndf)                    # Módulo de NDF
    ax.plot(theta, r, alpha=0.3, color='cornflowerblue', linewidth=0.8)  # Curva semitransparente

# Agrupamos los datos por frecuencia y calculamos el valor medio (promedio sobre ce3)
grouped = df.groupby("Frecuencia (Hz)")
mean_re = grouped["NDF_Re"].mean().values
mean_im = grouped["NDF_Im"].mean().values

# Construimos los valores complejos promedio
mean_ndf = mean_re + 1j * mean_im
theta_mean = np.angle(mean_ndf)
r_mean = np.abs(mean_ndf)

# Dibujamos la curva media en el gráfico polar
ax.plot(theta_mean, r_mean, label="Media NDF", color='blue', linewidth=2)

# Ajustamos detalles visuales del gráfico
ax.set_title("active_feedback_ndf", va='bottom')  # Título
ax.grid(True)         # Cuadrícula
plt.tight_layout()    # Ajuste automático del layout
plt.show()            # Mostramos el gráfico




########## AF-SPARAMS #############
# Archivo de salida
with open("datos_ce3.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ce3 (F)", "Frecuencia (Hz)", "|S11| (dB)", "|S12| (dB)", "|S21| (dB)", "|S22| (dB)"])

    for ce3_val in ce3_values:
        c3.parameters("C").ValueAsDouble = ce3_val

        # Simulación
        graphs = awrde.Project.Graphs
        if graphs.Exists("python_af_sparams"):
            graphs.Remove("python_af_sparams")
        g = graphs.Add("python_af_sparams", 3)

        m_s11 = g.Measurements.Add("active_feedback_ampli", "DB(|S(1,1)|)")
        m_s12 = g.Measurements.Add("active_feedback_ampli", "DB(|S(1,2)|)")
        m_s21 = g.Measurements.Add("active_feedback_ampli", "DB(|S(2,1)|)")
        m_s22 = g.Measurements.Add("active_feedback_ampli", "DB(|S(2,2)|)")

        m_s21.SimulateMeasurement()

        fs = m_s21.XValues
        s11 = m_s11.YValues(1)
        s12 = m_s12.YValues(1)
        s21 = m_s21.YValues(1)
        s22 = m_s22.YValues(1)

        for f, v11, v12, v21, v22 in zip(fs, s11, s12, s21, s22):
            writer.writerow([ce3_val, f, v11, v12, v21, v22])


# Cargar archivo CSV
df = pd.read_csv("datos_ce3.csv")

# Obtener todos los valores únicos de ce3
ce3_vals = df["ce3 (F)"].unique()

if len(ce3_vals) == 0:
    raise ValueError("No se encontraron valores de ce3 en el archivo.")

# Usar el primer valor disponible
ce3_target = ce3_vals[0]
subset = df[df["ce3 (F)"] == ce3_target]

# Graficar S11, S12, S21, S22 en la misma figura
plt.figure(figsize=(10, 6))
plt.plot(subset["Frecuencia (Hz)"] / 1e9, subset["|S11| (dB)"], label="S11", color="blue")
plt.plot(subset["Frecuencia (Hz)"] / 1e9, subset["|S12| (dB)"], label="S12", color="magenta")
plt.plot(subset["Frecuencia (Hz)"] / 1e9, subset["|S21| (dB)"], label="S21", color="orange")
plt.plot(subset["Frecuencia (Hz)"] / 1e9, subset["|S22| (dB)"], label="S22", color="red")

plt.title("af_sparams (barrido en ce3)")
plt.xlabel("Frecuencia (GHz)")
plt.ylabel("Magnitud (dB)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Cargar el archivo CSV
df = pd.read_csv("datos_ce3.csv")
df["Frecuencia (GHz)"] = df["Frecuencia (Hz)"] / 1e9

# Definir parámetros y colores
parametros = {
    "S11": "|S11| (dB)",
    "S12": "|S12| (dB)",
    "S21": "|S21| (dB)",
    "S22": "|S22| (dB)"
}
colores = {
    "S11": "red",
    "S12": "blue",
    "S21": "orange",
    "S22": "magenta"
}

ce3_vals = sorted(df["ce3 (F)"].unique())
grouped = df.groupby("Frecuencia (GHz)")

# Crear subplots
fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

for i, (param, columna) in enumerate(parametros.items()):
    ax = axs[i]

    for ce3 in ce3_vals:
        subset = df[df["ce3 (F)"] == ce3]
        ax.plot(subset["Frecuencia (GHz)"], subset[columna], color=colores[param], alpha=0.25)

    media = grouped[columna].mean()
    ax.plot(media.index, media.values, label=f"Media {param}", color=colores[param])
    ax.set_ylabel(f"{param} (dB)")
    ax.grid(True)
    ax.legend()

axs[-1].set_xlabel("Frecuencia (GHz)")
plt.suptitle("af_sparams (barrido en ce3)")
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()


################# Crear esquema af_polezero #######################
if awrde.Project.Schematics.Exists("af_polezero"):
    awrde.Project.Schematics.Remove("af_polezero")

awrde.Project.Schematics.Copy("active_ampli_tmp", "af_polezero")

pz = awrde.Project.Schematics("af_polezero")

#Creamos el diseño del esquematico
# Fuente de corriente ACCS
accs = pz.Elements.Add("ACCS", 0, 200)
accs.Parameters("Mag").ValueAsDouble = 1e-3  # 1 mA
gnd1 = pz.Elements.Add("GND", 0, 1200)

#conexion AC con Vc
pz.Wires.Add(accs.Nodes.Item(1).x, accs.Nodes.Item(1).y, accs.Nodes.Item(1).x, accs.Nodes.Item(1).y-500)
pz.Wires.Add(accs.Nodes.Item(2).x, accs.Nodes.Item(1).y-500, accs.Nodes.Item(1).x+500, accs.Nodes.Item(1).y-500)

# Añadir nodo Vb
node_vb = pz.Elements.Add("PORT_NAME", accs.Nodes.Item(1).x+500, accs.Nodes.Item(1).y-1500, -180, False)

# Añadir nodo Vc
node_vc = pz.Elements.Add("PORT_NAME", accs.Nodes.Item(1).x+500, accs.Nodes.Item(1).y-500, -180, False)

#puerto
port = pz.Elements.Add("PORT", accs.Nodes.Item(1).x+2500, accs.Nodes.Item(1).y-500, 0, False)
pz.Wires.Add(port.Nodes.Item(1).x, port.Nodes.Item(1).y, port.Nodes.Item(1).x+500, port.Nodes.Item(1).y)
pz.Wires.Add(port.Nodes.Item(1).x+1500, port.Nodes.Item(1).y, port.Nodes.Item(1).x+2000, port.Nodes.Item(1).y)

#resistencia
r1pz= pz.Elements.Add("RES", port.Nodes.Item(1).x+2000, port.Nodes.Item(1).y, -90, False)
r1pz.Parameters("R").ValueAsDouble = 50
gnd2= pz.Elements.Add("GND", r1pz.Nodes.Item(2).x, r1pz.Nodes.Item(2).y, 0, False)


# Archivo de salida
with open("datos_pz.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ce3 (F)", "Frecuencia (Hz)", "DB(|Vac(ACCS.I1)|)", "ANG(|Vac(ACCS.I1)|)"])

    for ce3_val in ce3_values:
        # Asignar valor a ce3
        c3.parameters("C").ValueAsDouble = ce3_val

        # Eliminar gráfico anterior si existe
        graphs = awrde.Project.Graphs
        if graphs.Exists("PYTHON_active_feedback_pc"):
            graphs.Remove("PYTHON_active_feedback_pc")

        # Crear nuevo gráfico
        g = graphs.Add("PYTHON_active_feedback_pc", 3)

        # Añadir mediciones sobre el análisis af_polezero.AP
        m_db = g.Measurements.Add("af_polezero.AP", "DB(|Vac(ACCS.I1)|)")
        m_ang = g.Measurements.Add("af_polezero.AP", "Ang(Vac(ACCS.I1))")

        # Ejecutar simulación (solo una llamada es suficiente)
        m_db.SimulateMeasurement()

        # Obtener datos
        fs = m_db.XValues  # frecuencias en Hz
        db = m_db.YValues(1)
        ang = m_ang.YValues(1)

        # Guardar en CSV
        for f, vdb, vang in zip(fs, db, ang):
            writer.writerow([ce3_val, f, vdb, vang])

# Cargar el CSV
df = pd.read_csv("datos_pz.csv")
df["Frecuencia (GHz)"] = df["Frecuencia (Hz)"] / 1e9

# Obtener valores únicos de ce3
ce3_vals = sorted(df["ce3 (F)"].unique())

# Agrupar para estadísticas
grouped = df.groupby("Frecuencia (GHz)")
frequencies = sorted(grouped.groups.keys())

# === CREAR SUBPLOTS COMPARTIENDO EJE X ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# === MAGNITUD ===
for ce3 in ce3_vals:
    subset = df[df["ce3 (F)"] == ce3]
    ax1.plot(subset["Frecuencia (GHz)"],
             subset["DB(|Vac(ACCS.I1)|)"],
             color='cornflowerblue', alpha=0.3, linewidth=0.8)

# Estadísticas
mean_db = grouped["DB(|Vac(ACCS.I1)|)"].mean().values
std_db = grouped["DB(|Vac(ACCS.I1)|)"].std().values

ax1.plot(frequencies, mean_db, label="DB(|Vac(ACCS.I1)|)", color='blue')
ax1.fill_between(frequencies, mean_db - std_db, mean_db + std_db,
                 color='blue', alpha=0.2)
ax1.set_ylabel("Mag (dB)")
ax1.set_title("Active Feedback (barrido en ce3)")
ax1.grid(True)
ax1.legend()

# === FASE ===
for ce3 in ce3_vals:
    subset = df[df["ce3 (F)"] == ce3]
    ax2.plot(subset["Frecuencia (GHz)"],
             np.degrees(subset["ANG(|Vac(ACCS.I1)|)"]),
             color='mediumvioletred', alpha=0.3, linewidth=0.8)

# Estadísticas
mean_ang = np.degrees(grouped["ANG(|Vac(ACCS.I1)|)"].mean().values)
std_ang = np.degrees(grouped["ANG(|Vac(ACCS.I1)|)"].std().values)

ax2.plot(frequencies, mean_ang, label="ANG(|Vac(ACCS.I1)|)", color='deeppink')
ax2.fill_between(frequencies, mean_ang - std_ang, mean_ang + std_ang,
                 color='deeppink', alpha=0.2)

ax2.set_xlabel("Frecuencia (GHz)")
ax2.set_ylabel("Ang (deg)")
ax2.set_ylim(-200, 100)
ax2.grid(True)
ax2.legend()

# Layout limpio
plt.tight_layout()
plt.show()



################ Crear esquema af_nonlinear ###################
if awrde.Project.Schematics.Exists("af_nonlinear"):
    awrde.Project.Schematics.Remove("af_nonlinear")

awrde.Project.Schematics.Copy("active_ampli_tmp", "af_nonlinear")
nn = awrde.Project.Schematics("af_nonlinear")

# Fuente OSCAPROBE
osc = nn.Elements.Add("OSCAPROBE", 0, 200, -180, False)
osc.Parameters("Fstart").ValueAsDouble = 1*10e8
osc.Parameters("Fend").ValueAsDouble = 3*10e8
osc.Parameters("Fsteps").ValueAsDouble = 9991
osc.Parameters("Vsteps").ValueAsDouble = 20
osc.Parameters("Damp").ValueAsDouble = 1

gnd1 = nn.Elements.Add("GND", 0, 200)

#conexion AC con Vc
nn.Wires.Add(osc.Nodes.Item(2).x, osc.Nodes.Item(2).y, osc.Nodes.Item(2).x, osc.Nodes.Item(2).y-1500)
nn.Wires.Add(osc.Nodes.Item(2).x, osc.Nodes.Item(2).y-1500, osc.Nodes.Item(2).x+500, osc.Nodes.Item(2).y-1500)

# Añadir nodo Vc
node_vc_nn = nn.Elements.Add("PORT_NAME", osc.Nodes.Item(2).x+500, osc.Nodes.Item(2).y-500, -180, False) #PCONN1

# Añadir nodo Vb
node_vb_nn = nn.Elements.Add("PORT_NAME", osc.Nodes.Item(2).x+500, osc.Nodes.Item(2).y-1500, -180, False) #PCONN2

#puerto
port = nn.Elements.Add("PORT", accs.Nodes.Item(1).x+2500, accs.Nodes.Item(1).y-500, 0, False)
nn.Wires.Add(port.Nodes.Item(1).x, port.Nodes.Item(1).y, port.Nodes.Item(1).x+500, port.Nodes.Item(1).y)
nn.Wires.Add(port.Nodes.Item(1).x+1500, port.Nodes.Item(1).y, port.Nodes.Item(1).x+2000, port.Nodes.Item(1).y)

#resistencia
r1pz= nn.Elements.Add("RES", port.Nodes.Item(1).x+2000, port.Nodes.Item(1).y, -90, False)
r1pz.Parameters("R").ValueAsDouble = 50
gnd2= nn.Elements.Add("GND", r1pz.Nodes.Item(2).x, r1pz.Nodes.Item(2).y, 0, False)



################# Crear esquema active_sensor_txon #######################
if awrde.Project.Schematics.Exists("active_sensor_txon"):
    awrde.Project.Schematics.Remove("active_sensor_txon")

awrde.Project.Schematics.Copy("txon_tmp", "active_sensor_txon")
tx = awrde.Project.Schematics("active_sensor_txon")

port2 = tx.Elements.Add("PORT", 3000,0, -180, False)
port1 = tx.Elements.Add("PORT", 0,0, 0, False)


tx.Wires.Add(port1.Nodes.Item(1).x, port1.Nodes.Item(1).y, port1.Nodes.Item(1).x+900, port1.Nodes.Item(1).y)
tx.Wires.Add(port1.Nodes.Item(1).x+900, port1.Nodes.Item(1).y, port1.Nodes.Item(1).x+900, port1.Nodes.Item(1).y-1200)
tx.Wires.Add(port2.Nodes.Item(1).x, port2.Nodes.Item(1).y, port2.Nodes.Item(1).x-1100, port2.Nodes.Item(1).y)
tx.Wires.Add(port2.Nodes.Item(1).x-1100, port2.Nodes.Item(1).y, port2.Nodes.Item(1).x-1100, port2.Nodes.Item(1).y-1200)

# Archivo de salida
with open("datos_tx.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ce3 (F)", "Frecuencia (Hz)", "|S21| (dB)", "CSRR_txon:|S21| (dB)"])

    for ce3_val in ce3_values:
        c3.parameters("C").ValueAsDouble = ce3_val

        # Simulación
        graphs = awrde.Project.Graphs
        if graphs.Exists("PYTHON_active_sensor_txon_sparams"):
            graphs.Remove("PYTHON_active_sensor_txon_sparams")
        g = graphs.Add("PYTHON_active_sensor_txon_sparams", 3)


        m_s21 = g.Measurements.Add("active_sensor_txon", "DB(|S(2,1)|)")
        m_CSRR_s21 = g.Measurements.Add("CSRR_txon", "DB(|S(2,1)|)")

        m_s21.SimulateMeasurement()
        m_CSRR_s21.SimulateMeasurement()

        fs = m_s21.XValues
        s21 = m_s21.YValues(1)
        CSRR_s21 = m_CSRR_s21.YValues(1)

        for f, v21, CSRR_s21 in zip(fs, s21, CSRR_s21):
            writer.writerow([ce3_val, f, v21, CSRR_s21])


import pandas as pd
import matplotlib.pyplot as plt

# Cargar el CSV generado previamente
df = pd.read_csv("datos_tx.csv")

# Agrupar por las simulaciones distintas (supongo ce3 como la variable barrida)
ce3_vals = sorted(df["ce3 (F)"].unique())

# Crear gráfico de tipo Yield con sombreado
plt.figure(figsize=(10, 6))

# Graficar todas las curvas individuales en azul claro (simulaciones)
for ce3 in ce3_vals:
    subset = df[df["ce3 (F)"] == ce3]
    plt.plot(subset["Frecuencia (Hz)"] * 1e-9,  # GHz
             subset["|S21| (dB)"],
             color='cornflowerblue', alpha=0.3, linewidth=0.8)

# Calcular media y desviación típica por frecuencia
grouped = df.groupby("Frecuencia (Hz)")
frequencies = sorted(grouped.groups.keys())
mean_vals = grouped["|S21| (dB)"].mean().values
std_vals = grouped["|S21| (dB)"].std().values

# Graficar la media y sombrear ±1σ
plt.plot([f * 1e-9 for f in frequencies], mean_vals, label="Media", color='blue')
plt.fill_between([f * 1e-9 for f in frequencies],
                 mean_vals - std_vals,
                 mean_vals + std_vals,
                 color='blue', alpha=0.2)

# --- Añadir curva de Yield para CSRR_txon ---
mean_csrr = grouped["CSRR_txon:|S21| (dB)"].mean().values
std_csrr = grouped["CSRR_txon:|S21| (dB)"].std().values

plt.plot([f * 1e-9 for f in frequencies], mean_csrr,
         label="CSRR", color='orange', linestyle='--')

plt.fill_between([f * 1e-9 for f in frequencies],
                 mean_csrr - std_csrr,
                 mean_csrr + std_csrr,
                 color='orange', alpha=0.2)

# Personalización del gráfico
plt.xlabel("Frecuencia (GHz)")
plt.ylabel("|S21| (dB)")
plt.title("active_sensor_txon_sparams (barrido en ce3)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()





################# Crear esquema active_sensor_rxon #######################
if awrde.Project.Schematics.Exists("active_sensor_rxon"):
    awrde.Project.Schematics.Remove("active_sensor_rxon")

awrde.Project.Schematics.Copy("rxon_tmp", "active_sensor_rxon")
rx = awrde.Project.Schematics("active_sensor_rxon")

port1 = rx.Elements.Add("PORT", 0,0, 0, False)
port2 = rx.Elements.Add("PORT", 3000,0, -180, False)

rx.Wires.Add(port1.Nodes.Item(1).x, port1.Nodes.Item(1).y, port1.Nodes.Item(1).x+300, port1.Nodes.Item(1).y)
rx.Wires.Add(port1.Nodes.Item(1).x+1300, port1.Nodes.Item(1).y, port1.Nodes.Item(1).x+1400, port1.Nodes.Item(1).y)
rx.Wires.Add(port2.Nodes.Item(1).x, port2.Nodes.Item(1).y, port2.Nodes.Item(1).x-600, port2.Nodes.Item(1).y)



# Archivo de salida
with open("datos_rx.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ce3 (F)", "Frecuencia (Hz)", "|S11| (dB)", "CSRR_rxon:|S11| (dB)"])

    for ce3_val in ce3_values:
        c3.parameters("C").ValueAsDouble = ce3_val

        # Simulación
        graphs = awrde.Project.Graphs
        if graphs.Exists("PYTHON_active_sensor_rxon_sparams"):
            graphs.Remove("PYTHON_active_sensor_rxon_sparams")
        g = graphs.Add("PYTHON_active_sensor_rxon_sparams", 3)


        m_s11 = g.Measurements.Add("active_sensor_rxon", "DB(|S(1,1)|)")
        m_CSRR_s11 = g.Measurements.Add("CSRR_rxon", "DB(|S(1,1)|)")

        m_s11.SimulateMeasurement()
        m_CSRR_s11.SimulateMeasurement()

        fs = m_s11.XValues
        s11 = m_s11.YValues(1)
        CSRR_s11 = m_CSRR_s11.YValues(1)

        for f, v11, CSRR_s11 in zip(fs, s11, CSRR_s11):
            writer.writerow([ce3_val, f, v11, CSRR_s11])



# Cargar el CSV
df = pd.read_csv("datos_rx.csv")

# Convertir a GHz
df["Frecuencia (GHz)"] = df["Frecuencia (Hz)"] / 1e9

# Obtener los valores de ce3 únicos
ce3_vals = sorted(df["ce3 (F)"].unique())

# Crear figura
plt.figure(figsize=(10, 6))

# Dibujar todas las simulaciones individuales (|S11|)
for ce3 in ce3_vals:
    subset = df[df["ce3 (F)"] == ce3]
    plt.plot(subset["Frecuencia (GHz)"], subset["|S11| (dB)"],
             color='cornflowerblue', alpha=0.3, linewidth=0.8)

# Agrupar por frecuencia para estadísticas
grouped = df.groupby("Frecuencia (GHz)")
frequencies = sorted(grouped.groups.keys())

# Calcular media y desviación de |S11|
mean_s11 = grouped["|S11| (dB)"].mean().values
std_s11 = grouped["|S11| (dB)"].std().values

# Calcular media y desviación de CSRR_rxon:|S11|
mean_csrr = grouped["CSRR_rxon:|S11| (dB)"].mean().values
std_csrr = grouped["CSRR_rxon:|S11| (dB)"].std().values

# Añadir curva de media y banda ±1σ para |S11|
plt.plot(frequencies, mean_s11, label="S11", color='blue')
plt.fill_between(frequencies, mean_s11 - std_s11, mean_s11 + std_s11,
                 color='blue', alpha=0.2)

# Añadir curva de media y banda ±1σ para CSRR_rxon
plt.plot(frequencies, mean_csrr, label="CSRR", color='orange', linestyle='--')
plt.fill_between(frequencies, mean_csrr - std_csrr, mean_csrr + std_csrr,
                 color='orange', alpha=0.2)

# Personalización
plt.xlabel("Frecuencia (GHz)")
plt.ylabel("|S11| (dB)")
plt.title("active_sensor_rxon_sparams (barrido en ce3)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


################# creo esquematico active_feedback_osci  #################

# Empiezo el proyecto
# Elimina el esquema si ya existe con ese nombre
if awrde.Project.Schematics.Exists("active_feedback_osci"):
    awrde.Project.Schematics.Remove("active_feedback_osci")

# Copiar el esquema "SUB" como nuevo esquema de trabajo
awrde.Project.Schematics.Copy("SUB", "active_feedback_osci")

# Accedemos a la copia
o = awrde.Project.Schematics("active_feedback_osci")



# Establezco los elementos
p1 = o.Elements.Add("PORT", 0, 0, 0, False)
p2 = o.Elements.Add("PORT", 6000, 400, 0, False)
c4= o.Elements.Add("CAP", 0, 0, 0, False)
c6= o.Elements.Add("CAP", 1000, 0, -90, False)
c3= o.Elements.Add("CAP", 1400, -1600, 0, False)
c8= o.Elements.Add("CAP", 6000, -600, -90, False)
c7= o.Elements.Add("CAP", 7100, -600, -90, False)
c2= o.Elements.Add("CAP", 1000, 3200, -90, False)
c1= o.Elements.Add("CAP", 5800, 3200, -90, False)
l2= o.Elements.Add("IND", 3900, -1600, 0, False) #l1
l3= o.Elements.Add("IND", 2700, 700, -90, True)
l1= o.Elements.Add("IND", 4700, 900, -90, True)
r1= o.Elements.Add("RES", 2700, 3200, -90, False)
r2= o.Elements.Add("RES", 1900, 3200, -90, False)
rl2= o.Elements.Add("RES", 4700, 3200, -90, False)
gnd1= o.Elements.Add("GND", 1000, 1000, 0, False)
gnd2= o.Elements.Add("GND", 7100, 400, 0, False)
gnd3= o.Elements.Add("GND", 1000, 4200, 0, False)
gnd4= o.Elements.Add("GND", 1900, 4200, 0, False)
gnd5= o.Elements.Add("GND", 5800, 4200, 0, False)
gndSUB1= o.Elements.Add("GND", 4200, -400, 0, True)
gnd2SUB2= o.Elements.Add("GND", 4200, 400, 0, False)
gndDC= o.Elements.Add("GND", 4700, 5700, 0, False)
DC= o.Elements.Add("DCVS", 4700, 4700, 0, False)

# Añadir nodo Vb
node_vb = o.Elements.Add("PORT_NAME", 3500, 0, -270, False)

# Añadir nodo Vc
node_vc = o.Elements.Add("PORT_NAME", 4700, 0, -180, False)




# Importar el Subcircuito basado en la Netlist
# Inserta el subcircuito BFP520 manualmente aquí.


#Cables
#s.Wires.Add(2400, -1600, 3900, -1600)
o.Wires.Add(c3.Nodes.Item(2).x, c3.Nodes.Item(2).y, l2.Nodes.Item(1).x, l2.Nodes.Item(1).y)
o.Wires.Add(1000, 0, 1000, -1600)
o.Wires.Add(1000, -1600, 1400, -1600)
o.Wires.Add(1000, 0, 3700, 0)
o.Wires.Add(2700, 0, 2700, 700)
o.Wires.Add(2700, 1700, 2700, 3200)
o.Wires.Add(1000, 3200, 1000, 2700)
o.Wires.Add(1900, 3200, 1900, 2700)
o.Wires.Add(1000, 2700, 1900, 2700)
o.Wires.Add(1900, 2700, 2700, 2700)
o.Wires.Add(2700, 4200, 2700, 4700)
o.Wires.Add(4700, 4200, 4700, 4700)
o.Wires.Add(2700, 4700, 4700, 4700)
o.Wires.Add(4900, -1600, 6000, -1600)
o.Wires.Add(6000, -1600, 6000, -600)
o.Wires.Add(6000, -900, 7100, -900)
o.Wires.Add(7100, -900, 7100, -600)
o.Wires.Add(6000, -900, 4700, -900)
o.Wires.Add(4700, -900, 4700, 900)
o.Wires.Add(4700, 1900, 4700, 3200)
o.Wires.Add(4700, 2700, 5800, 2700)
o.Wires.Add(5800, 2700, 5800, 3200)


# Establezco los valores de los elementos
Rb1=9700
Rb2=1000
Rc=400
Vdc=10
Lchoke=3.248*10e-9
Cdc=13*10e-13
Ce1=4.998*10e-13
Cb1=1.428*10e-13
Cc1=1.3*10e-13
Lc1=5.672*10e-10
c4.parameters("C").ValueAsDouble= Cdc
c6.parameters("C").ValueAsDouble= Cb1
c3.parameters("C").ValueAsDouble= Cc1
l2.parameters("L").ValueAsDouble= Lc1
c8.parameters("C").ValueAsDouble= Cdc
c7.parameters("C").ValueAsDouble= Ce1
l3.parameters("L").ValueAsDouble= Lchoke
l1.parameters("L").ValueAsDouble= Lchoke
c2.parameters("C").ValueAsDouble= Cdc
r2.parameters("R").ValueAsDouble= Rb2
r1.parameters("R").ValueAsDouble= Rb1
rl2.parameters("R").ValueAsDouble= Rc
c1.parameters("C").ValueAsDouble= Cdc
DC.Parameters("V").ValueAsDouble = Vdc





################ Crear esquema active_sensor_osci ###################
if awrde.Project.Schematics.Exists("active_sensor_osci"):
    awrde.Project.Schematics.Remove("active_sensor_osci")

awrde.Project.Schematics.Copy("osci_tmp", "active_sensor_osci")
osci = awrde.Project.Schematics("active_sensor_osci")


gnd1 = osci.Elements.Add("GND", 0, 200)

#conexion AC con Vc
osci.Wires.Add(gnd1.Nodes.Item(1).x, gnd1.Nodes.Item(1).y-1000, gnd1.Nodes.Item(1).x, gnd1.Nodes.Item(1).y-2700)
osci.Wires.Add(gnd1.Nodes.Item(1).x, gnd1.Nodes.Item(1).y-2700, gnd1.Nodes.Item(1).x+500, gnd1.Nodes.Item(1).y-2700)

# Añadir nodo Vc
node_vc_nn = osci.Elements.Add("PORT_NAME", gnd1.Nodes.Item(1).x+500, gnd1.Nodes.Item(1).y-1700, -180, False) #PCONN1

# Añadir nodo Vb
node_vb_osci = osci.Elements.Add("PORT_NAME", gnd1.Nodes.Item(1).x+500, gnd1.Nodes.Item(1).y-2700, -180, False) #PCONN2

#puerto
port = osci.Elements.Add("PORT", gnd1.Nodes.Item(1).x+2500, gnd1.Nodes.Item(1).y-500, 0, False)
osci.Wires.Add(port.Nodes.Item(1).x, port.Nodes.Item(1).y, port.Nodes.Item(1).x+100, port.Nodes.Item(1).y)
osci.Wires.Add(port.Nodes.Item(1).x+1100, port.Nodes.Item(1).y, port.Nodes.Item(1).x+1600, port.Nodes.Item(1).y)

