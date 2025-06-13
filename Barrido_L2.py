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
c3.parameters("C").ValueAsDouble = Cc1
#l2.parameters("L").ValueAsDouble = Lc1
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

# Barrido de valores
l2_values = np.random.uniform(0.7e-9, 1.3e-9, 10)

################### Carta de Smith (barrido L2) #####################

# 1) Escribir el CSV
with open("datos_ndf_l2.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Cabecera adaptada: L2 en lugar de Ce1
    writer.writerow(["L2 (H)", "Frecuencia (Hz)", "NDF_Re", "NDF_Im"])

    # Barrido sobre l2_values
    for l2_val in l2_values:
        # Asigno el valor al parámetro L de tu componente L2
        l2.parameters("L").ValueAsDouble = l2_val

        try:
            graphs = awrde.Project.Graphs
            if not graphs.Exists("PYTHON_active_feedback_ndf"):
                print("Error: el gráfico no existe.")
                break

            g = graphs("PYTHON_active_feedback_ndf")

            # Medidas de Re y Im de NDF
            m_re = g.Measurements.Add("active_feedback_ampli.AP", "Re(NDF())")
            m_im = g.Measurements.Add("active_feedback_ampli.AP", "Im(NDF())")

            m_re.SimulateMeasurement()
            m_im.SimulateMeasurement()

            freqs   = m_re.XValues
            vals_re = m_re.YValues(1)
            vals_im = m_im.YValues(1)

            # Guardo L2, frecuencia, Re, Im
            for f, re, im in zip(freqs, vals_re, vals_im):
                writer.writerow([l2_val, f, re, im])

        except Exception as e:
            print(f"Error en L2 = {l2_val:.3e} H: {e}")

# 2) Leer el CSV y preparar DataFrame
df = pd.read_csv("datos_ndf_l2.csv")
df["NDF"] = df["NDF_Re"] + 1j * df["NDF_Im"]

# 3) Extraer frecuencias únicas y valores de L2
frequencies = sorted(df["Frecuencia (Hz)"].unique())
l2_vals     = df["L2 (H)"].unique()

# 4) Ploteo en carta polar
plt.figure(figsize=(7, 7))
ax = plt.subplot(111, projection="polar")

# Trazar cada trayectoria de NDF para cada L2
for l2_val in l2_vals:
    sub = df[df["L2 (H)"] == l2_val].sort_values("Frecuencia (Hz)")
    ndf   = sub["NDF"].values
    theta = np.angle(ndf)
    r     = np.abs(ndf)
    ax.plot(theta, r, alpha=0.3, color='cornflowerblue', linewidth=0.8)

# Curva media sobre L2
grouped = df.groupby("Frecuencia (Hz)")
mean_re = grouped["NDF_Re"].mean().values
mean_im = grouped["NDF_Im"].mean().values
mean_ndf = mean_re + 1j * mean_im

theta_m = np.angle(mean_ndf)
r_m     = np.abs(mean_ndf)
ax.plot(theta_m, r_m, label="Media NDF", color='blue', linewidth=2)

# Detalles estéticos
ax.set_title("active_feedback_ndf (barrido L2)", va='bottom')
ax.grid(True)
plt.tight_layout()
plt.show()



########## AF-SPARAMS (barrido L2) #############

# 1) Escribir el CSV
with open("datos_l2.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "L2 (H)", "Frecuencia (Hz)",
        "|S11| (dB)", "|S12| (dB)", "|S21| (dB)", "|S22| (dB)"
    ])

    for l2_val in l2_values:
        # Asigna el valor de inductancia
        l2.parameters("L").ValueAsDouble = l2_val

        graphs = awrde.Project.Graphs
        if graphs.Exists("python_af_sparams"):
            graphs.Remove("python_af_sparams")
        g = graphs.Add("python_af_sparams", 3)

        # Medidas S-params
        m_s11 = g.Measurements.Add("active_feedback_ampli", "DB(|S(1,1)|)")
        m_s12 = g.Measurements.Add("active_feedback_ampli", "DB(|S(1,2)|)")
        m_s21 = g.Measurements.Add("active_feedback_ampli", "DB(|S(2,1)|)")
        m_s22 = g.Measurements.Add("active_feedback_ampli", "DB(|S(2,2)|)")

        # Solo es necesario simular una de ellas
        m_s21.SimulateMeasurement()

        fs   = m_s21.XValues
        s11  = m_s11.YValues(1)
        s12  = m_s12.YValues(1)
        s21  = m_s21.YValues(1)
        s22  = m_s22.YValues(1)

        for f, v11, v12, v21, v22 in zip(fs, s11, s12, s21, s22):
            writer.writerow([l2_val, f, v11, v12, v21, v22])

# 2) Leer CSV
df = pd.read_csv("datos_l2.csv")
df["Frecuencia (GHz)"] = df["Frecuencia (Hz)"] / 1e9

# 3) Valores únicos de L2
l2_vals = sorted(df["L2 (H)"].unique())
grouped = df.groupby("Frecuencia (GHz)")

# 4) Gráfico para un L2 concreto (ej. el primero)
l2_target = l2_vals[0]
sub0 = df[df["L2 (H)"] == l2_target]
plt.figure(figsize=(10, 6))
plt.plot(sub0["Frecuencia (GHz)"], sub0["|S11| (dB)"], label="S11")
plt.plot(sub0["Frecuencia (GHz)"], sub0["|S12| (dB)"], label="S12")
plt.plot(sub0["Frecuencia (GHz)"], sub0["|S21| (dB)"], label="S21")
plt.plot(sub0["Frecuencia (GHz)"], sub0["|S22| (dB)"], label="S22")
plt.title(f"AF-Sparams para L2 = {l2_target:.2e} H")
plt.xlabel("Frecuencia (GHz)")
plt.ylabel("Magnitud (dB)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# 5) Todos los L2, media ±1σ en 4 subplots
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

fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
for i, (tag, col) in enumerate(parametros.items()):
    ax = axs[i]
    # todas las trayectorias
    for l2_val in l2_vals:
        sub = df[df["L2 (H)"] == l2_val]
        ax.plot(sub["Frecuencia (GHz)"], sub[col], color=colores[tag], alpha=0.25)
    # curva media
    media = grouped[col].mean()
    ax.plot(media.index, media.values, label=f"Media {tag}", color=colores[tag])
    ax.set_ylabel(f"{tag} (dB)")
    ax.grid(True)
    ax.legend()

axs[-1].set_xlabel("Frecuencia (GHz)")
plt.suptitle("Variación de parámetros S con barrido de L2", y=0.97)
plt.tight_layout(rect=[0,0,1,0.96])
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
with open("datos_pz_l2.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "L2 (H)", "Frecuencia (Hz)",
        "DB(|Vac(ACCS.I1)|)", "ANG(|Vac(ACCS.I1)|)"
    ])

    for l2_val in l2_values:
        # Asignar valor a la inductancia L2
        l2.parameters("L").ValueAsDouble = l2_val

        graphs = awrde.Project.Graphs
        if graphs.Exists("PYTHON_active_feedback_pc"):
            graphs.Remove("PYTHON_active_feedback_pc")
        g = graphs.Add("PYTHON_active_feedback_pc", 3)

        # Mediciones de magnitud y fase
        m_db  = g.Measurements.Add("af_polezero.AP", "DB(|Vac(ACCS.I1)|)")
        m_ang = g.Measurements.Add("af_polezero.AP", "Ang(Vac(ACCS.I1))")

        m_db.SimulateMeasurement()  # una simulación basta

        freqs = m_db.XValues
        db    = m_db.YValues(1)
        ang   = m_ang.YValues(1)

        for f, vdb, vang in zip(freqs, db, ang):
            writer.writerow([l2_val, f, vdb, vang])

# Leer CSV y preparar DataFrame
df = pd.read_csv("datos_pz_l2.csv")
df["Frecuencia (GHz)"] = df["Frecuencia (Hz)"] / 1e9

# Valores únicos de L2 y estadísticas por frecuencia
l2_vals    = sorted(df["L2 (H)"].unique())
grouped    = df.groupby("Frecuencia (GHz)")
frequencies = sorted(grouped.groups.keys())

# Crear subplots para magnitud y fase
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# MAGNITUD (dB)
for l2 in l2_vals:
    sub = df[df["L2 (H)"] == l2]
    ax1.plot(
        sub["Frecuencia (GHz)"],
        sub["DB(|Vac(ACCS.I1)|)"],
        color='cornflowerblue', alpha=0.3, linewidth=0.8
    )

mean_db = grouped["DB(|Vac(ACCS.I1)|)"].mean().values
std_db  = grouped["DB(|Vac(ACCS.I1)|)"].std().values
ax1.plot(frequencies, mean_db, label="Mag (dB)", color='blue')
ax1.fill_between(
    frequencies,
    mean_db - std_db,
    mean_db + std_db,
    color='blue', alpha=0.2
)
ax1.set_ylabel("Mag (dB)")
ax1.set_title("Pole-Zero (barrido L2)")
ax1.grid(True)
ax1.legend()

# FASE (grados)
for l2 in l2_vals:
    sub = df[df["L2 (H)"] == l2]
    ax2.plot(
        sub["Frecuencia (GHz)"],
        np.degrees(sub["ANG(|Vac(ACCS.I1)|)"].values),
        color='mediumvioletred', alpha=0.3, linewidth=0.8
    )

mean_ang = np.degrees(grouped["ANG(|Vac(ACCS.I1)|)"].mean().values)
std_ang  = np.degrees(grouped["ANG(|Vac(ACCS.I1)|)"].std().values)
ax2.plot(frequencies, mean_ang, label="Ang (deg)", color='deeppink')
ax2.fill_between(
    frequencies,
    mean_ang - std_ang,
    mean_ang + std_ang,
    color='deeppink', alpha=0.2
)
ax2.set_xlabel("Frecuencia (GHz)")
ax2.set_ylabel("Ang (deg)")
ax2.set_ylim(-200, 100)
ax2.grid(True)
ax2.legend()

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

with open("datos_tx_l2.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "L2 (H)",
        "Frecuencia (Hz)",
        "|S21| (dB)",
        "CSRR_txon|S21| (dB)"
    ])

    for l2_val in l2_values:
        # Asignar el valor de inductancia a tu componente L2
        l2.parameters("L").ValueAsDouble = l2_val

        # Configurar/eliminar gráfico
        graphs = awrde.Project.Graphs
        if graphs.Exists("PYTHON_active_sensor_txon_sparams"):
            graphs.Remove("PYTHON_active_sensor_txon_sparams")
        g = graphs.Add("PYTHON_active_sensor_txon_sparams", 3)

        # Medidas
        m_s21      = g.Measurements.Add("active_sensor_txon", "DB(|S(2,1)|)")
        m_csrr_s21 = g.Measurements.Add("CSRR_txon",         "DB(|S(2,1)|)")

        # Simular ambas
        m_s21.SimulateMeasurement()
        m_csrr_s21.SimulateMeasurement()

        # Extraer datos
        fs        = m_s21.XValues
        s21_vals  = m_s21.YValues(1)
        csrr_vals = m_csrr_s21.YValues(1)

        # Guardar fila por fila
        for f, v21, vc in zip(fs, s21_vals, csrr_vals):
            writer.writerow([l2_val, f, v21, vc])

# 2) Leer el CSV y preparar DataFrame
df = pd.read_csv("datos_tx_l2.csv")
df["Frecuencia (GHz)"] = df["Frecuencia (Hz)"] / 1e9

# 3) Yield-plot: todas las trayectorias + media ±1σ
plt.figure(figsize=(10, 6))

# a) Cada trayectoria individual de |S21|
for l2_val in sorted(df["L2 (H)"].unique()):
    sub = df[df["L2 (H)"] == l2_val].sort_values("Frecuencia (GHz)")
    plt.plot(sub["Frecuencia (GHz)"],
             sub["|S21| (dB)"],
             color="cornflowerblue",
             alpha=0.3,
             linewidth=0.8)

# b) Estadísticas de |S21|
grouped = df.groupby("Frecuencia (GHz)")
freqs    = np.array(sorted(grouped.groups.keys()))
mean_s21 = grouped["|S21| (dB)"].mean().values
std_s21  = grouped["|S21| (dB)"].std().values

plt.plot(freqs, mean_s21, label="Media |S21|", color="blue")
plt.fill_between(freqs,
                 mean_s21 - std_s21,
                 mean_s21 + std_s21,
                 color="blue", alpha=0.2, label="±1σ |S21|")

# c) Estadísticas de CSRR_txon|S21|
mean_csrr = grouped["CSRR_txon|S21| (dB)"].mean().values
std_csrr  = grouped["CSRR_txon|S21| (dB)"].std().values

plt.plot(freqs, mean_csrr, label="Media CSRR", color="orange", linestyle="--")
plt.fill_between(freqs,
                 mean_csrr - std_csrr,
                 mean_csrr + std_csrr,
                 color="orange", alpha=0.2, label="±1σ CSRR")

# 4) Ajustes estéticos
plt.xlabel("Frecuencia (GHz)")
plt.ylabel("|S21| y CSRR (dB)")
plt.title("active_sensor_txon_sparams\n(barrido en L2)")
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



with open("datos_rx_l2.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "L2 (H)",
        "Frecuencia (Hz)",
        "|S11| (dB)",
        "CSRR_rxon|S11| (dB)"
    ])

    for l2_val in l2_values:
        # Asigna el valor de L2 en tu esquema AWR
        l2.parameters("L").ValueAsDouble = l2_val

        graphs = awrde.Project.Graphs
        if graphs.Exists("PYTHON_active_sensor_rxon_sparams"):
            graphs.Remove("PYTHON_active_sensor_rxon_sparams")
        g = graphs.Add("PYTHON_active_sensor_rxon_sparams", 3)

        # Medidas de RX-On
        m_s11      = g.Measurements.Add("active_sensor_rxon", "DB(|S(1,1)|)")
        m_csrr_s11 = g.Measurements.Add("CSRR_rxon",         "DB(|S(1,1)|)")

        m_s11.SimulateMeasurement()
        m_csrr_s11.SimulateMeasurement()

        fs        = m_s11.XValues
        s11_vals  = m_s11.YValues(1)
        csrr_vals = m_csrr_s11.YValues(1)

        for f, v11, cs in zip(fs, s11_vals, csrr_vals):
            writer.writerow([l2_val, f, v11, cs])


# --- 2) Carga y prepara el DataFrame ---
df = pd.read_csv("datos_rx_l2.csv")
df["Frecuencia (GHz)"] = df["Frecuencia (Hz)"] / 1e9

# --- 3) Plot “yield” de |S11| + media±1σ con CSRR ---
plt.figure(figsize=(10,6))

# a) Todas las trayectorias individuales de |S11|
for l2_val in sorted(df["L2 (H)"].unique()):
    sub = df[df["L2 (H)"] == l2_val].sort_values("Frecuencia (GHz)")
    plt.plot(sub["Frecuencia (GHz)"],
             sub["|S11| (dB)"],
             color="cornflowerblue",
             alpha=0.3,
             linewidth=0.8)

# b) Estadísticas de |S11|
grouped  = df.groupby("Frecuencia (GHz)")
freqs    = np.array(sorted(grouped.groups.keys()))
mean_s11 = grouped["|S11| (dB)"].mean().values
std_s11  = grouped["|S11| (dB)"].std().values

plt.plot(freqs, mean_s11, label="|S11|", color="blue")
plt.fill_between(freqs,
                 mean_s11 - std_s11,
                 mean_s11 + std_s11,
                 color="blue", alpha=0.2)

# c) Estadísticas de CSRR_rxon|S11|
mean_csrr = grouped["CSRR_rxon|S11| (dB)"].mean().values
std_csrr  = grouped["CSRR_rxon|S11| (dB)"].std().values

plt.plot(freqs, mean_csrr, label="CSRR", color="orange", linestyle="--")
plt.fill_between(freqs,
                 mean_csrr - std_csrr,
                 mean_csrr + std_csrr,
                 color="orange", alpha=0.2)

# --- 4) Ajustes estéticos ---
plt.xlabel("Frecuencia (GHz)")
plt.ylabel("|S11| y CSRR (dB)")
plt.title("active_sensor_rxon_sparams\n(barrido en L2)")
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

