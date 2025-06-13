import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

########### NDF ###############

# --- 1. Cargar archivos ---
df_awr = pd.read_csv("ndf_awr.csv")
df_py = pd.read_csv("datos_ndf.csv")

# --- 2. Procesar archivo AWR ---
df_awr.columns = df_awr.columns.str.strip()
df_py.columns = df_py.columns.str.strip()

df_awr_clean = df_awr.iloc[1:].copy()
df_awr_clean = df_awr_clean.iloc[:, 0].str.split('\t', expand=True)
df_awr_clean.columns = ['Frecuencia (GHz)', 'NDF_Re', 'NDF_Im']
df_awr_clean = df_awr_clean.astype(float)

# --- 3. Procesar archivo Python ---
df_py['Frecuencia (GHz)'] = df_py['Frecuencia (Hz)'] / 1e9

# --- 4. Unir por frecuencia ---
df_interp = pd.merge(df_awr_clean[['Frecuencia (GHz)']], df_py, on='Frecuencia (GHz)', how='left')
df_interp['NDF_Re_real'] = df_awr_clean['NDF_Re']
df_interp['NDF_Im_real'] = df_awr_clean['NDF_Im']

# --- 5. Calcular NDF complejo ---
ndf_real = df_interp['NDF_Re_real'] + 1j * df_interp['NDF_Im_real']
ndf_sim = df_interp['NDF_Re'] + 1j * df_interp['NDF_Im']

# --- 6. Convertir a coordenadas polares ---
theta_real = np.angle(ndf_real)
r_real = np.abs(ndf_real)

theta_sim = np.angle(ndf_sim)
r_sim = np.abs(ndf_sim)

# --- 7. Calcular error absoluto medio ---
error_abs = np.abs(ndf_real - ndf_sim)
error_mean = error_abs.mean()
print(f"Error absoluto medio NDF: {error_mean:.5f}")

# --- 8. Graficar en coordenadas polares con colores contrastantes ---
plt.figure(figsize=(7, 7))
ax = plt.subplot(111, projection="polar")
ax.plot(theta_real, r_real, label='NDF real (AWR)', color='crimson', linewidth=2)
ax.plot(theta_sim, r_sim, label='NDF simulado (Python)', linestyle='--', color='navy', linewidth=2)
ax.set_title("Validacion NDF", va='bottom')
ax.grid(True)
ax.legend(loc='upper right')
plt.tight_layout()
plt.show()



############ S-Params #############

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Cargar archivos ---
df_awr = pd.read_csv("S_awr_1.csv")
df_py = pd.read_csv("datos_ce1.csv")

# --- 2. Limpiar nombres de columnas ---
df_awr.columns = df_awr.columns.str.strip()
df_py.columns = df_py.columns.str.strip()

# --- 3. Procesar datos de AWR ---
df_awr_clean = df_awr.iloc[:, 0].str.split('\t', expand=True)
df_awr_clean.columns = ['Frecuencia (GHz)', '|S11| (dB)', '|S12| (dB)', '|S22| (dB)', '|S21| (dB)']
df_awr_clean = df_awr_clean.astype(float)

# --- 4. Convertir frecuencia en Python y unir por GHz ---
df_py['Frecuencia (GHz)'] = df_py['Frecuencia (Hz)'] / 1e9
df_merged = pd.merge(df_awr_clean, df_py, on='Frecuencia (GHz)', how='left')

# --- 5. Renombrar columnas para claridad ---
df_merged = df_merged.rename(columns={
    '|S11| (dB)_x': 'S11_AWR',
    '|S12| (dB)_x': 'S12_AWR',
    '|S21| (dB)_x': 'S21_AWR',
    '|S22| (dB)_x': 'S22_AWR',
    '|S11| (dB)_y': 'S11_PY',
    '|S12| (dB)_y': 'S12_PY',
    '|S21| (dB)_y': 'S21_PY',
    '|S22| (dB)_y': 'S22_PY'
}) if any("_x" in col for col in df_merged.columns) else df_merged.rename(columns={
    '|S11| (dB)': 'S11_AWR',
    '|S12| (dB)': 'S12_AWR',
    '|S21| (dB)': 'S21_AWR',
    '|S22| (dB)': 'S22_AWR',
    '|S11| (dB).1': 'S11_PY',
    '|S12| (dB).1': 'S12_PY',
    '|S21| (dB).1': 'S21_PY',
    '|S22| (dB).1': 'S22_PY'
})

# --- 6. Calcular errores absolutos ---
df_merged['Error_S11'] = np.abs(df_merged['S11_AWR'] - df_merged['S11_PY'])
df_merged['Error_S12'] = np.abs(df_merged['S12_AWR'] - df_merged['S12_PY'])
df_merged['Error_S21'] = np.abs(df_merged['S21_AWR'] - df_merged['S21_PY'])
df_merged['Error_S22'] = np.abs(df_merged['S22_AWR'] - df_merged['S22_PY'])

# --- 7. Mostrar errores absolutos medios ---
mean_errors = {
    'S11': df_merged['Error_S11'].mean(),
    'S12': df_merged['Error_S12'].mean(),
    'S21': df_merged['Error_S21'].mean(),
    'S22': df_merged['Error_S22'].mean()
}

print("Errores absolutos medios Parametros S:")
for s, e in mean_errors.items():
    print(f"{s}: {e:.6e} dB")

# --- 8. Graficar subplots comparativos ---
fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
fig.suptitle('Validacion simulacion AF_SPARAMS', fontsize=16)

# S11
axs[0, 0].plot(df_merged['Frecuencia (GHz)'], df_merged['S11_AWR'], label='AWR', color='black')
axs[0, 0].plot(df_merged['Frecuencia (GHz)'], df_merged['S11_PY'], '--', label='Python', color='red')
axs[0, 0].set_title('|S11| (dB)')
axs[0, 0].legend()
axs[0, 0].grid(True)

# S12
axs[0, 1].plot(df_merged['Frecuencia (GHz)'], df_merged['S12_AWR'], label='AWR', color='black')
axs[0, 1].plot(df_merged['Frecuencia (GHz)'], df_merged['S12_PY'], '--', label='Python', color='blue')
axs[0, 1].set_title('|S12| (dB)')
axs[0, 1].legend()
axs[0, 1].grid(True)

# S21
axs[1, 0].plot(df_merged['Frecuencia (GHz)'], df_merged['S21_AWR'], label='AWR', color='black')
axs[1, 0].plot(df_merged['Frecuencia (GHz)'], df_merged['S21_PY'], '--', label='Python', color='green')
axs[1, 0].set_title('|S21| (dB)')
axs[1, 0].legend()
axs[1, 0].grid(True)
axs[1, 0].set_xlabel('Frecuencia (GHz)')

# S22
axs[1, 1].plot(df_merged['Frecuencia (GHz)'], df_merged['S22_AWR'], label='AWR', color='black')
axs[1, 1].plot(df_merged['Frecuencia (GHz)'], df_merged['S22_PY'], '--', label='Python', color='purple')
axs[1, 1].set_title('|S22| (dB)')
axs[1, 1].legend()
axs[1, 1].grid(True)
axs[1, 1].set_xlabel('Frecuencia (GHz)')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


######### TX ##############

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Cargar archivos ---
df_tx_awr = pd.read_csv("tx_awr_1.csv")
df_tx_py = pd.read_csv("datos_tx.csv")

# --- 2. Limpiar nombres de columnas ---
df_tx_awr.columns = df_tx_awr.columns.str.strip()
df_tx_py.columns = df_tx_py.columns.str.strip()

# --- 3. Procesar datos AWR (columna tabulada) ---
df_tx_awr_clean = df_tx_awr.iloc[:, 0].str.split('\t', expand=True)
df_tx_awr_clean.columns = ['Frecuencia (GHz)', 'S21_active_sensor_txon', 'S21_csrr_txon']
df_tx_awr_clean = df_tx_awr_clean.astype(float)

# --- 4. Convertir frecuencia en datos Python ---
df_tx_py['Frecuencia (GHz)'] = df_tx_py['Frecuencia (Hz)'] / 1e9

# --- 5. Unir por frecuencia ---
df_tx_merged = pd.merge(df_tx_awr_clean, df_tx_py, on='Frecuencia (GHz)', how='left')

# --- 6. Renombrar columnas para claridad ---
df_tx_merged = df_tx_merged.rename(columns={
    '|S21| (dB)': 'S21_active_python',
    'CSRR_txon:|S21| (dB)': 'S21_csrr_python'
})

# --- 7. Calcular errores absolutos ---
df_tx_merged['Error_S21_active'] = np.abs(df_tx_merged['S21_active_sensor_txon'] - df_tx_merged['S21_active_python'])
df_tx_merged['Error_S21_csrr'] = np.abs(df_tx_merged['S21_csrr_txon'] - df_tx_merged['S21_csrr_python'])

# --- 8. Mostrar errores medios ---
mean_errors_tx = {
    'S21_active': df_tx_merged['Error_S21_active'].mean(),
    'S21_csrr': df_tx_merged['Error_S21_csrr'].mean()
}

print("Errores absolutos medios TX:")
for key, val in mean_errors_tx.items():
    print(f"{key}: {val:.6e} dB")

# --- 9. Graficar comparación en subplots ---
fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
fig.suptitle('Validacion - TX ON', fontsize=15)

# Subplot sensor activo
axs[0].plot(df_tx_merged['Frecuencia (GHz)'], df_tx_merged['S21_active_sensor_txon'], label='AWR', color='black')
axs[0].plot(df_tx_merged['Frecuencia (GHz)'], df_tx_merged['S21_active_python'], '--', label='Python', color='red')
axs[0].set_title('|S21| (dB) - active_sensor_txon')
axs[0].legend()
axs[0].grid(True)

# Subplot CSRR
axs[1].plot(df_tx_merged['Frecuencia (GHz)'], df_tx_merged['S21_csrr_txon'], label='AWR', color='black')
axs[1].plot(df_tx_merged['Frecuencia (GHz)'], df_tx_merged['S21_csrr_python'], '--', label='Python', color='blue')
axs[1].set_title('|S21| (dB) - CSRR_txon')
axs[1].legend()
axs[1].grid(True)
axs[1].set_xlabel('Frecuencia (GHz)')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


############# RX #################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Cargar archivos ---
df_rx_awr = pd.read_csv("rx_awr.csv")
df_rx_py = pd.read_csv("datos_rx.csv")

# --- 2. Limpiar columnas ---
df_rx_awr.columns = df_rx_awr.columns.str.strip()
df_rx_py.columns = df_rx_py.columns.str.strip()

# --- 3. Procesar AWR (columna tabulada) ---
df_rx_awr_clean = df_rx_awr.iloc[:, 0].str.split('\t', expand=True)
df_rx_awr_clean.columns = ['Frecuencia (GHz)', 'S11_active_rxon', 'S11_csrr_rxon']
df_rx_awr_clean = df_rx_awr_clean.astype(float)

# --- 4. Procesar Python ---
df_rx_py['Frecuencia (GHz)'] = df_rx_py['Frecuencia (Hz)'] / 1e9

# --- 5. Merge por frecuencia ---
df_rx_merged = pd.merge(df_rx_awr_clean, df_rx_py, on='Frecuencia (GHz)', how='left')

# --- 6. Renombrar columnas ---
df_rx_merged = df_rx_merged.rename(columns={
    '|S11| (dB)': 'S11_active_python',
    'CSRR_rxon:|S11| (dB)': 'S11_csrr_python'
})

# --- 7. Calcular errores ---
df_rx_merged['Error_S11_active'] = np.abs(df_rx_merged['S11_active_rxon'] - df_rx_merged['S11_active_python'])
df_rx_merged['Error_S11_csrr'] = np.abs(df_rx_merged['S11_csrr_rxon'] - df_rx_merged['S11_csrr_python'])

mean_errors_rx = {
    'S11_active': df_rx_merged['Error_S11_active'].mean(),
    'S11_csrr': df_rx_merged['Error_S11_csrr'].mean()
}
print("Errores absolutos medios RX:")
for key, val in mean_errors_rx.items():
    print(f"{key}: {val:.6e}")

# --- 8. Gráfica ---
fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
fig.suptitle('Validacion - RX ON', fontsize=15)

axs[0].plot(df_rx_merged['Frecuencia (GHz)'], df_rx_merged['S11_active_rxon'], label='AWR', color='black')
axs[0].plot(df_rx_merged['Frecuencia (GHz)'], df_rx_merged['S11_active_python'], '--', label='Python', color='red')
axs[0].set_title('|S11| (dB) - active_sensor_rxon')
axs[0].legend()
axs[0].grid(True)

axs[1].plot(df_rx_merged['Frecuencia (GHz)'], df_rx_merged['S11_csrr_rxon'], label='AWR', color='black')
axs[1].plot(df_rx_merged['Frecuencia (GHz)'], df_rx_merged['S11_csrr_python'], '--', label='Python', color='blue')
axs[1].set_title('|S11| (dB) - CSRR_rxon')
axs[1].legend()
axs[1].grid(True)
axs[1].set_xlabel('Frecuencia (GHz)')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


############# PC #############

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Cargar archivos ---
df_pz_awr = pd.read_csv("pz_awr.csv")
df_pz_py = pd.read_csv("datos_pz.csv")

# --- 2. Limpiar columnas ---
df_pz_awr.columns = df_pz_awr.columns.str.strip()
df_pz_py.columns = df_pz_py.columns.str.strip()

# --- 3. Procesar datos AWR (columna tabulada) ---
df_pz_awr_clean = df_pz_awr.iloc[:, 0].str.split('\t', expand=True)
df_pz_awr_clean.columns = ['Frecuencia (GHz)', 'Magnitude (dB)', 'Phase (Deg)']
df_pz_awr_clean = df_pz_awr_clean.astype(float)

# --- 4. Procesar datos Python ---
df_pz_py['Frecuencia (GHz)'] = df_pz_py['Frecuencia (Hz)'] / 1e9

# --- 5. Unir por frecuencia ---
df_pz_merged = pd.merge(df_pz_awr_clean, df_pz_py, on='Frecuencia (GHz)', how='left')

# --- 6. Calcular errores absolutos ---
df_pz_merged['Error_dB'] = np.abs(df_pz_merged['Magnitude (dB)'] - df_pz_merged['DB(|Vac(ACCS.I1)|)'])
df_pz_merged['Error_Phase'] = np.abs(df_pz_merged['Phase (Deg)'] - df_pz_merged['ANG(|Vac(ACCS.I1)|)'] * 180 / np.pi)

# --- 7. Calcular errores medios ---
mean_errors_pz = {
    'Magnitud (dB)': df_pz_merged['Error_dB'].mean(),
    'Fase (Deg)': df_pz_merged['Error_Phase'].mean()
}
print("Errores absolutos medios PZ:")
for key, val in mean_errors_pz.items():
    print(f"{key}: {val:.6e}")

# --- 8. Graficar comparación ---
fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
fig.suptitle('Validacion Active Feedback', fontsize=15)

axs[0].plot(df_pz_merged['Frecuencia (GHz)'], df_pz_merged['Magnitude (dB)'], label='AWR', color='black')
axs[0].plot(df_pz_merged['Frecuencia (GHz)'], df_pz_merged['DB(|Vac(ACCS.I1)|)'], '--', label='Python', color='darkorange')
axs[0].set_title('Magnitud de Vac (dB)')
axs[0].legend()
axs[0].grid(True)

axs[1].plot(df_pz_merged['Frecuencia (GHz)'], df_pz_merged['Phase (Deg)'], label='AWR', color='black')
axs[1].plot(df_pz_merged['Frecuencia (GHz)'], df_pz_merged['ANG(|Vac(ACCS.I1)|)'] * 180 / np.pi, '--', label='Python', color='blue')
axs[1].set_title('Fase de Vac (grados)')
axs[1].legend()
axs[1].grid(True)
axs[1].set_xlabel('Frecuencia (GHz)')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


############# Pout ####################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Cargar archivos ---
df_awr = pd.read_csv("Pout_awr.csv")
df_py = pd.read_csv("datos_pout.csv")

# --- 2. Limpiar columnas ---
df_awr.columns = df_awr.columns.str.strip()
df_py.columns = df_py.columns.str.strip()

# --- 3. Procesar AWR ---
df_awr_clean = df_awr.iloc[:, 0].str.split('\t', expand=True)
df_awr_clean.columns = ['Frecuencia (GHz)', 'Pout_AWR (dBm)']
df_awr_clean = df_awr_clean.astype(float)

# --- 4. Preparar Python ---
df_py = df_py.rename(columns={
    'Frequency (GHz)': 'Frecuencia (GHz)',
    'Power (dBm)': 'Pout_Python (dBm)'
})

# --- 5. Unir por frecuencia ---
df_merged = pd.merge(df_awr_clean, df_py, on='Frecuencia (GHz)', how='left')

# --- 6. Calcular error absoluto ---
df_merged['Error_abs_dBm'] = np.abs(df_merged['Pout_AWR (dBm)'] - df_merged['Pout_Python (dBm)'])
mean_error = df_merged['Error_abs_dBm'].mean()

# --- 7. Graficar estilo personalizado ---
plt.figure(figsize=(10, 6))

# Python
plt.vlines(df_merged["Frecuencia (GHz)"], ymin=-20, ymax=df_merged["Pout_Python (dBm)"],
           colors='#66b3ff', linewidth=2)
plt.plot(df_merged["Frecuencia (GHz)"], df_merged["Pout_Python (dBm)"],
         marker='^', linestyle='None', markerfacecolor='none', markeredgecolor='#66b3ff',
         markersize=8, label="Python")

# AWR
plt.vlines(df_merged["Frecuencia (GHz)"], ymin=-20, ymax=df_merged["Pout_AWR (dBm)"],
           colors='darkorange', linewidth=2)
plt.plot(df_merged["Frecuencia (GHz)"], df_merged["Pout_AWR (dBm)"],
         marker='o', linestyle='None', markerfacecolor='none', markeredgecolor='darkorange',
         markersize=8, label="AWR")

# --- 8. Estilo del gráfico ---
plt.xlabel("Frequency (GHz)", fontsize=14)
plt.ylabel("Power (dBm)", fontsize=14)
plt.title(f"Comparación de Pout (Python vs AWR) - Error medio: {mean_error:.2e} dB",
          fontsize=16, fontweight='bold')
plt.grid(True, linestyle='-', linewidth=0.5)
plt.ylim(-20, 10)
plt.xlim(0, df_merged["Frecuencia (GHz)"].max() + 1)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig("comparacion_pout_estilo_custom.png", dpi=300)
plt.show()


