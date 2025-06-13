# Librerias
import numpy as np
import win32com.client
import csv
import pandas as pd
import matplotlib.pyplot as plt


# Enlaza con mediante la API de python
awrde = win32com.client.Dispatch('MWOApp.MWOffice')

# Establezco las frecuencias
freqs = np.linspace(0.1e9, 10e9, 1000, endpoint=True)
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
c6 = s.Elements.Add("CAP", 1000, 0, -90, False)#C1
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
#Ce1 = 6e-12
Cc1 = 1e-12
Lc1 = 1e-9
c4.parameters("C").ValueAsDouble = Cdc
#c6.parameters("C").ValueAsDouble = Cb1  ##C1
#c3.parameters("C").ValueAsDouble = Cc1  ##Variar
#l2.parameters("L").ValueAsDouble = Lc1
c8.parameters("C").ValueAsDouble = Cdc
#c7.parameters("C").ValueAsDouble = Ce1
c2.parameters("C").ValueAsDouble = Cdc
r2.parameters("R").ValueAsDouble = Rb2
r1.parameters("R").ValueAsDouble = Rb1
rl2.parameters("R").ValueAsDouble = Rc
c1.parameters("C").ValueAsDouble = Cdc
l3.parameters("L").ValueAsDouble = Lchoke
l1.parameters("L").ValueAsDouble = Lchoke
DC.Parameters("V").ValueAsDouble = Vdc

# Barrido de valores de Ce1
ce1_values = np.random.uniform(5.5e-12, 6.5e-12, 3)
ce3_values = np.random.uniform(0.75e-12, 1.25e-12, 3)
ce6_values = np.random.uniform(0.75e-12, 1.25e-12, 3)
l2_values = np.random.uniform(0.7e-9, 1.3e-9, 3)



################### Carta de Smith  #####################

# Abrimos un archivo CSV para escritura y definimos el writer
with open("datos_ndf_multi.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Escribimos la cabecera del archivo con los nombres de las columnas
    writer.writerow(["Ce1 (F)", "Ce3 (F)", "Ce6 (F)", "L2 (H)", "Frecuencia (Hz)", "NDF_Re", "NDF_Im"])

    # Barridos de parámetros
    for ce1_val in ce1_values:
        for ce3_val in ce3_values:
            for ce6_val in ce6_values:
                for l2_val in l2_values:
                    # Asignamos los valores a cada componente correspondiente
                    c7.parameters("C").ValueAsDouble = ce1_val
                    c3.parameters("C").ValueAsDouble = ce3_val
                    c6.parameters("C").ValueAsDouble = ce6_val
                    l2.parameters("L").ValueAsDouble = l2_val

                    try:
                        graphs = awrde.Project.Graphs
                        if not graphs.Exists("PYTHON_active_feedback_ndf"):
                            print("Error: el gráfico no existe.")
                            break

                        g = graphs("PYTHON_active_feedback_ndf")

                        m_re = g.Measurements.Add("active_feedback_ampli.AP", "Re(NDF())")
                        m_im = g.Measurements.Add("active_feedback_ampli.AP", "Im(NDF())")

                        m_re.SimulateMeasurement()
                        m_im.SimulateMeasurement()

                        freqs = m_re.XValues
                        vals_re = m_re.YValues(1)
                        vals_im = m_im.YValues(1)

                        for f, re, im in zip(freqs, vals_re, vals_im):
                            writer.writerow([ce1_val, ce3_val, ce6_val, l2_val, f, re, im])

                    except Exception as e:
                        print(f"Error en Ce1={ce1_val}, Ce2={ce3_val}, Ce5={ce6_val}, L1={l2_val}: {e}")



# 1) Carga el CSV con todas las simulaciones
df = pd.read_csv("datos_ndf_multi.csv")
df["NDF"] = df["NDF_Re"] + 1j * df["NDF_Im"]

# 2) Extrae las combinaciones únicas de componentes
combos = df[["Ce1 (F)", "Ce3 (F)", "Ce6 (F)", "L2 (H)"]].drop_duplicates()

# 3) Selecciona al azar 10 de esas combinaciones
#    Fija random_state si quieres reproducibilidad
selected_combos = combos.sample(n=10, random_state=42)

# 4) Prepara la figura polar
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection="polar")

# 5) Para cada combinación seleccionada, filtra y traza
for _, params in selected_combos.iterrows():
    mask = (
        (df["Ce1 (F)"] == params["Ce1 (F)"]) &
        (df["Ce3 (F)"] == params["Ce3 (F)"]) &
        (df["Ce6 (F)"] == params["Ce6 (F)"]) &
        (df["L2 (H)"] == params["L2 (H)"])
    )
    sub = df[mask]
    ndf = sub["NDF"].values
    theta = np.angle(ndf)
    r = np.abs(ndf)
    ax.plot(theta, r, alpha=0.6, linewidth=1)

# 6) Trazar también la curva media sobre todas las simulaciones
grouped = df.groupby("Frecuencia (Hz)")
mean_ndf = grouped["NDF_Re"].mean().values + 1j * grouped["NDF_Im"].mean().values
theta_mean = np.angle(mean_ndf)
r_mean = np.abs(mean_ndf)
ax.plot(theta_mean, r_mean, label="Media NDF", linewidth=2, color="blue")

# 7) Ajustes estéticos
ax.set_title("Analisis tolerancia NDF ", va="bottom")
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()

########## AF-SPARAMS MULTICOMPO ##########

# Archivo de salida
with open("datos_multi_ce1ce3ce6l2.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Ce1 (F)", "Ce3 (F)", "Ce6 (F)", "L2 (H)", "Frecuencia (Hz)", "|S11| (dB)", "|S12| (dB)", "|S21| (dB)", "|S22| (dB)"])

    for ce1_val in ce1_values:
        for ce3_val in ce3_values:
            for ce6_val in ce6_values:
                for l2_val in l2_values:
                    # Asignar valores
                    c7.parameters("C").ValueAsDouble = ce1_val
                    c3.parameters("C").ValueAsDouble = ce3_val
                    c6.parameters("C").ValueAsDouble = ce6_val
                    l2.parameters("L").ValueAsDouble = l2_val

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
                        writer.writerow([ce1_val, ce3_val, ce6_val, l2_val, f, v11, v12, v21, v22])

# 1) Carga el CSV con todas las simulaciones de S-params
df = pd.read_csv("datos_multi_ce1ce3ce6l2.csv")

# 2) Extrae las combinaciones únicas de parámetros
combos = df[["Ce1 (F)", "Ce3 (F)", "Ce6 (F)", "L2 (H)"]].drop_duplicates()

# 3) Muestra aleatoriamente 10 de esas combinaciones
selected_combos = combos.sample(n=10, random_state=123)

# 4) Prepara una figura con 4 subplots para S11, S12, S21, S22
fig, axes = plt.subplots(2, 2, figsize=(12, 10), sharex=True)
ax11, ax12, ax21, ax22 = axes.flatten()

# 5) Para cada combinación seleccionada, filtra y plotea sus curvas
for _, params in selected_combos.iterrows():
    # máscara para esta combinación
    mask = (
        (df["Ce1 (F)"] == params["Ce1 (F)"]) &
        (df["Ce3 (F)"] == params["Ce3 (F)"]) &
        (df["Ce6 (F)"] == params["Ce6 (F)"]) &
        (df["L2 (H)"]  == params["L2 (H)"])
    )
    sub = df[mask]
    f = sub["Frecuencia (Hz)"].values
    ax11.plot(f, sub["|S11| (dB)"], alpha=0.6, linewidth=1)
    ax12.plot(f, sub["|S12| (dB)"], alpha=0.6, linewidth=1)
    ax21.plot(f, sub["|S21| (dB)"], alpha=0.6, linewidth=1)
    ax22.plot(f, sub["|S22| (dB)"], alpha=0.6, linewidth=1)

# 6) Añadir curva media de todas las simulaciones
grouped = df.groupby("Frecuencia (Hz)")
f_med = np.array(grouped["|S11| (dB)"].mean().index)

med_s11 = grouped["|S11| (dB)"].mean().values
med_s12 = grouped["|S12| (dB)"].mean().values
med_s21 = grouped["|S21| (dB)"].mean().values
med_s22 = grouped["|S22| (dB)"].mean().values

ax11.plot(f_med, med_s11, color="black", lw=2, label="Media")
ax12.plot(f_med, med_s12, color="black", lw=2, label="Media")
ax21.plot(f_med, med_s21, color="black", lw=2, label="Media")
ax22.plot(f_med, med_s22, color="black", lw=2, label="Media")

# 7) Ajustes estéticos
for ax, title in zip([ax11, ax12, ax21, ax22],
                     ["|S11| (dB)", "|S12| (dB)", "|S21| (dB)", "|S22| (dB)"]):
    ax.set_title(title)
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Magnitud (dB)")
    ax.grid(True)
    ax.legend()

fig.suptitle("Analisis tolerancias S-parameters", y=1.02, fontsize=16)
plt.tight_layout()
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
with open("datos_pz_multi.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Ce1 (F)", "Ce3 (F)", "Ce6 (F)", "L2 (H)",
        "Frecuencia (Hz)", "Mag dB", "Ang (rad)"
    ])

    for ce1 in ce1_values:
      for ce3 in ce3_values:
        for ce6 in ce6_values:
          for l2_valor in l2_values:
            # Asigna los valores en AWR
            c7.parameters("C").ValueAsDouble = ce1
            c3.parameters("C").ValueAsDouble = ce3
            c6.parameters("C").ValueAsDouble = ce6
            l2.parameters("L").ValueAsDouble = l2_valor

            graphs = awrde.Project.Graphs
            # Limpia/añade el gráfico
            if graphs.Exists("PYTHON_active_feedback_pc"):
                graphs.Remove("PYTHON_active_feedback_pc")
            g = graphs.Add("PYTHON_active_feedback_pc", 3)

            # Mediciones de magnitud y ángulo
            m_db  = g.Measurements.Add("af_polezero.AP", "DB(|Vac(ACCS.I1)|)")
            m_ang = g.Measurements.Add("af_polezero.AP", "Ang(Vac(ACCS.I1))")

            # Simula (con una sola llamada basta)
            m_db.SimulateMeasurement()
            # m_ang no necesita SimulateMeasurement() extra porque comparte datos X

            freqs = m_db.XValues
            mags   = m_db.YValues(1)
            angs   = m_ang.YValues(1)

            # Escribe filas
            for f, db, ang in zip(freqs, mags, angs):
                writer.writerow([ce1, ce3, ce6, l2_valor, f, db, ang])

# --- 3) Leer el CSV y transformar ---
df = pd.read_csv("datos_pz_multi.csv")

# 4 columnas de parámetros + f + mag + ang
# Extraer combinaciones únicas
combos = df[["Ce1 (F)", "Ce3 (F)", "Ce6 (F)", "L2 (H)"]].drop_duplicates()

# --- 4) Muestrear 10 combinaciones ---
selected = combos.sample(n=10, random_state=0)

# --- 5) Plot: una figura con dos subplots (magnitud y fase) ---
fig, (axm, axp) = plt.subplots(2, 1, figsize=(8, 10), sharex=True)

for _, params in selected.iterrows():
    mask = (
        (df["Ce1 (F)"] == params["Ce1 (F)"]) &
        (df["Ce3 (F)"] == params["Ce3 (F)"]) &
        (df["Ce6 (F)"] == params["Ce6 (F)"]) &
        (df["L2 (H)"]  == params["L2 (H)"])
    )
    sub = df[mask].sort_values("Frecuencia (Hz)")   # <- aquí ordenas

    f   = sub["Frecuencia (Hz)"].values
    mag = sub["Mag dB"].values
    ang = sub["Ang (rad)"].values

    # Trazar magnitud y fase ya sin saltos
    axm.plot(f,   mag, alpha=0.6, linewidth=1)
    axp.plot(f,   ang, alpha=0.6, linewidth=1)


# --- 6) Curvas medias sobre todas las simulaciones ---
grp = df.groupby("Frecuencia (Hz)")
f_med   = np.array(grp["Mag dB"].mean().index)
mag_med = grp["Mag dB"].mean().values
ang_med = grp["Ang (rad)"].mean().values

axm.plot(f_med, mag_med, color="black", lw=2, label="Media")
axp.plot(f_med, ang_med, color="black", lw=2, label="Media")

# --- 7) Ajustes estéticos ---
axm.set_ylabel("Magnitud |Vac| (dB)")
axm.set_title("Analisis tolerancias Pole-Zero")
axm.grid(True)
axm.legend()

axp.set_xlabel("Frecuencia (Hz)")
axp.set_ylabel("Fase (rad)")
axp.grid(True)
axp.legend()

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
with open("datos_tx_multi.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Ce1 (F)", "Ce3 (F)", "Ce6 (F)", "L2 (H)",
        "Frecuencia (Hz)", "|S21| (dB)", "CSRR_txon|S21| (dB)"
    ])

    for ce1 in ce1_values:
        for ce3 in ce3_values:
            for ce6 in ce6_values:
                for l2_valor in l2_values:
                    # Asigna los valores en AWR
                    c7.parameters("C").ValueAsDouble = ce1
                    c3.parameters("C").ValueAsDouble = ce3
                    c6.parameters("C").ValueAsDouble = ce6
                    l2.parameters("L").ValueAsDouble = l2_valor

                    graphs = awrde.Project.Graphs
                    if graphs.Exists("PYTHON_active_sensor_txon_sparams"):
                        graphs.Remove("PYTHON_active_sensor_txon_sparams")
                    g = graphs.Add("PYTHON_active_sensor_txon_sparams", 3)

                    # Medidas
                    m_s21      = g.Measurements.Add("active_sensor_txon", "DB(|S(2,1)|)")
                    m_csrr_s21 = g.Measurements.Add("CSRR_txon",         "DB(|S(2,1)|)")

                    # Simula ambas
                    m_s21.SimulateMeasurement()
                    m_csrr_s21.SimulateMeasurement()

                    fs       = m_s21.XValues
                    s21_vals = m_s21.YValues(1)
                    csrr_vals= m_csrr_s21.YValues(1)

                    for f, v21, vc in zip(fs, s21_vals, csrr_vals):
                        writer.writerow([ce1, ce3, ce6, l2_valor, f, v21, vc])


# 1) Leer CSV ya corregido
df = pd.read_csv("datos_tx_multi.csv")

# 2) Extraer sample de 10 combos de (Ce1,Ce3,Ce6,L2)
combos = df[["Ce1 (F)","Ce3 (F)","Ce6 (F)","L2 (H)"]].drop_duplicates()
sampled = combos.sample(10, random_state=0)

# 3) Prepara gráfico
plt.figure(figsize=(10,6))

# 4) Dibuja las 10 trayectorias muestreadas
for _, params in sampled.iterrows():
    sel = (
      (df["Ce1 (F)"]==params["Ce1 (F)"]) &
      (df["Ce3 (F)"]==params["Ce3 (F)"]) &
      (df["Ce6 (F)"]==params["Ce6 (F)"]) &
      (df["L2 (H)"] ==params["L2 (H)"])
    )
    sub = df[sel].sort_values("Frecuencia (Hz)")
    f_GHz = sub["Frecuencia (Hz)"].values * 1e-9
    plt.plot(f_GHz, sub["|S21| (dB)"],
             color="cornflowerblue", alpha=0.4, linewidth=1)

# 5) Calcula media y σ sólo de las dos columnas numéricas
grp      = df.groupby("Frecuencia (Hz)")
freqs_G  = np.array(sorted(grp.groups.keys())) * 1e-9
mean_s21 = grp["|S21| (dB)"].mean().values
std_s21  = grp["|S21| (dB)"].std().values
mean_cs  = grp["CSRR_txon|S21| (dB)"].mean().values
std_cs   = grp["CSRR_txon|S21| (dB)"].std().values

# 6) Dibuja media ±1σ
plt.plot(freqs_G, mean_s21, color="blue", lw=2, label="|S21|")
plt.fill_between(freqs_G,
                 mean_s21-std_s21,
                 mean_s21+std_s21,
                 color="blue", alpha=0.2,)


# 9) Ajustes estéticos
plt.xlabel("Frecuencia (GHz)")
plt.ylabel("|S21| (dB)")
plt.title("Analisis tolerancias modo TX-On")
plt.grid(True)
plt.legend(loc="upper right", fontsize="small")
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



# Archivo de salida multi-componente para RX-On\ nwith open("datos_rx_multi.csv", "w", newline='') as csvfile:
with open("datos_rx_multi.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Ce1 (F)", "Ce3 (F)", "Ce6 (F)", "L2 (H)",
        "Frecuencia (Hz)", "|S11| (dB)", "CSRR_rxon|S11| (dB)"
    ])


    for ce1 in ce1_values:
        for ce3 in ce3_values:
            for ce6 in ce6_values:
                for l2_val in l2_values:
                    # Asignar valores a componentes en AWR
                    c7.parameters("C").ValueAsDouble = ce1
                    c3.parameters("C").ValueAsDouble = ce3
                    c6.parameters("C").ValueAsDouble = ce6
                    l2.parameters("L").ValueAsDouble = l2_val

                    graphs = awrde.Project.Graphs
                    if graphs.Exists("PYTHON_active_sensor_rxon_sparams"):
                        graphs.Remove("PYTHON_active_sensor_rxon_sparams")
                    g = graphs.Add("PYTHON_active_sensor_rxon_sparams", 3)

                    # Mediciones de S11 y CSRR_rxon
                    m_s11      = g.Measurements.Add("active_sensor_rxon", "DB(|S(1,1)|)")
                    m_csrr_s11 = g.Measurements.Add("CSRR_rxon",         "DB(|S(1,1)|)")

                    # Simulaciones
                    m_s11.SimulateMeasurement()
                    m_csrr_s11.SimulateMeasurement()

                    freqs     = m_s11.XValues
                    s11_vals  = m_s11.YValues(1)
                    csrr_vals = m_csrr_s11.YValues(1)

                    # Escribir CSV
                    for f, s11, csrr in zip(freqs, s11_vals, csrr_vals):
                        writer.writerow([ce1, ce3, ce6, l2_val, f, s11, csrr])

# Leer CSV y preparar DataFrame
df = pd.read_csv("datos_rx_multi.csv")

# Muestreo de 10 combinaciones únicas
combos = df[["Ce1 (F)", "Ce3 (F)", "Ce6 (F)", "L2 (H)"]].drop_duplicates()
sampled = combos.sample(n=10, random_state=0)

# Crear plot
plt.figure(figsize=(10, 6))

# Trazar 10 trayectorias de |S11|
for _, params in sampled.iterrows():
 mask = (
     (df["Ce1 (F)"] == params["Ce1 (F)"]) &
     (df["Ce3 (F)"] == params["Ce3 (F)"]) &
     (df["Ce6 (F)"] == params["Ce6 (F)"]) &
     (df["L2 (H)"]  == params["L2 (H)"])
 )
 sub = df[mask].sort_values("Frecuencia (Hz)")
 f_ghz = sub["Frecuencia (Hz)"].values * 1e-9
 plt.plot(f_ghz, sub["|S11| (dB)"], color="cornflowerblue", alpha=0.4, linewidth=1)

# Estadísticas: media ±1σ para |S11| y CSRR
grp       = df.groupby("Frecuencia (Hz)")
freqs_ghz = np.array(sorted(grp.groups.keys())) * 1e-9
mean_s11  = grp["|S11| (dB)"].mean().values
std_s11   = grp["|S11| (dB)"].std().values
mean_csrr = grp["CSRR_rxon|S11| (dB)"].mean().values
std_csrr  = grp["CSRR_rxon|S11| (dB)"].std().values

# Dibujar media ±1σ
plt.plot(freqs_ghz, mean_s11, color="blue", lw=2, label="|S11|")
plt.fill_between(freqs_ghz,
              mean_s11 - std_s11,
              mean_s11 + std_s11,
              color="blue", alpha=0.2, )


# Estética
plt.xlabel("Frecuencia (GHz)")
plt.ylabel("Magnitudes |S11| y CSRR (dB)")
plt.title("Análisis tolerancias modo RX-On")
plt.grid(True)
plt.legend(loc="upper right", fontsize="small")
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

