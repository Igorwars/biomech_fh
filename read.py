# =====================================================================
# IMPORTS
# =====================================================================
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# =====================================================================
# .sto FILE READER
# =====================================================================
def readMotionFile(filename):
    """ Reads OpenSim .sto files.
    Parameters
    ----------
    filename: absolute path to the .sto file
    Returns
    -------
    header: the header of the .sto
    labels: the labels of the columns
    data: an array of the data
    """

    if not os.path.exists(filename):
        print('file do not exists')
        return None, None, None

    file_id = open(filename, 'r')

    # read header
    next_line = file_id.readline()
    header = [next_line]
    nc = 0
    nr = 0
    while not 'endheader' in next_line:
        if 'datacolumns' in next_line:
            nc = int(next_line[next_line.index(' ') + 1:len(next_line)])
        elif 'datarows' in next_line:
            nr = int(next_line[next_line.index(' ') + 1:len(next_line)])
        elif 'nColumns' in next_line:
            nc = int(next_line[next_line.index('=') + 1:len(next_line)])
        elif 'nRows' in next_line:
            nr = int(next_line[next_line.index('=') + 1:len(next_line)])

        next_line = file_id.readline()
        header.append(next_line)

    # process column labels
    next_line = file_id.readline()
    if next_line.isspace() == True:
        next_line = file_id.readline()

    labels = next_line.split()

    # get data
    data = []
    for i in range(1, nr + 1):
        d = [float(x) for x in file_id.readline().split()]
        data.append(d)

    file_id.close()

    return header, labels, data



# =====================================================================
# HELPERS — Spalte aus .sto holen
# =====================================================================
def getFromIndex(file, index):
    head, label, dats = readMotionFile(file)
    dats = np.array(dats)
    return label[index], dats[:, index]

def getFromLabel(file, label):
    head, labels, dats = readMotionFile(file)
    dats = np.array(dats)
    index = labels.index(label)
    return label, dats[:, index]

# =====================================================================
# FILE PATHS
# =====================================================================
ID_DIR = Path(__file__).parent / 'Ergebnisse' / 'ID_Ergebnisse'

# Normalgang
file_n1 = ID_DIR / 'Gait_normal_01_ID.sto'
file_n2 = ID_DIR / 'Gait_normal_05_ID.sto'
file_n3 = ID_DIR / 'Gait_normal_06_ID.sto'

# Lateraler Gang
file_l1 = ID_DIR / 'Gait_lateral_06_ID.sto'
file_l2 = ID_DIR / 'Gait_lateral_09_ID.sto'
file_l3 = ID_DIR / 'Gait_lateral_29_ID.sto'

# Medialer Gang
file_m1 = ID_DIR / 'Gait_medial_04_ID.sto'
file_m2 = ID_DIR / 'Gait_medial_07_ID.sto'
file_m3 = ID_DIR / 'Gait_medial_08_ID.sto'


# =====================================================================
# PLOT-FUNKTION (lädt + trimmt + glättet + plottet)
# =====================================================================
def plotGait(files, label, sigmas=None, colors=None,
             trial_names=None, title=None, show_mean=False):

    n = len(files)
    sigmas      = sigmas      or [0] * n
    colors      = colors      or [f'C{i}' for i in range(n)]
    trial_names = trial_names or [f'Trial {i+1}' for i in range(n)]

    # Daten laden + auf kürzeste Länge trimmen
    signals = [getFromLabel(f, label)[1] for f in files]
    n_min   = min(len(s) for s in signals)
    signals = np.array([s[:n_min] for s in signals])
    time    = getFromLabel(files[0], 'time')[1][:n_min]

    # Plot
    plt.figure(figsize=(10, 6))
    for signal, c, sigma, name in zip(signals, colors, sigmas, trial_names):
        if sigma > 0:
            plt.plot(time, signal, color=c, alpha=0.25, linestyle='--')  # roh, blass
            signal = gaussian_filter1d(signal, sigma=sigma)
            name = f'{name} (σ={sigma})'
        plt.plot(time, signal, color=c, alpha=0.9, label=name)

    if show_mean:
        mean = np.mean(signals, axis=0)
        std  = np.std(signals,  axis=0)
        plt.plot(time, mean, color='black', linewidth=2, label='Mean')
        plt.fill_between(time, mean - std, mean + std,
                         color='gray', alpha=0.2, label='Std Dev')

    plt.title(title or label)
    plt.xlabel('Time [s]')
    plt.ylabel('Moment [Nm]')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


# =====================================================================
# LABEL-REFERENZ (zum Nachschlagen, nicht ausgeführt)
# =====================================================================
"""ALLE LABELS:
time	pelvis_tilt_moment	pelvis_list_moment	pelvis_rotation_moment	
pelvis_tx_force	pelvis_ty_force	pelvis_tz_force	

hip_flexion_r_moment	hip_adduction_r_moment	hip_rotation_r_moment	
hip_flexion_l_moment	hip_adduction_l_moment	hip_rotation_l_moment	

lumbar_extension_moment	lumbar_bending_moment	lumbar_rotation_moment	

knee_angle_r_moment	knee_rotation_r_moment	knee_adduction_r_moment	
knee_angle_l_moment	knee_rotation_l_moment	knee_adduction_l_moment	

ankle_angle_r_moment	ankle_angle_l_moment	

subtalar_angle_r_moment	subtalar_angle_l_moment	

mtp_angle_r_moment	mtp_angle_l_moment
"""

# =====================================================================
# AUFRUF
# =====================================================================
plotGait(
    files       = [file_n1, file_n2, file_n3],
    label       = 'knee_adduction_l_moment',
    sigmas      = [0, 1, 0], #Gauss filter zum Glätten der Kurven (0 = kein Filter)
    colors      = ['tab:blue', 'tab:orange', 'tab:green'],
    trial_names = ['Normal 1', 'Normal 2', 'Normal 3'],
    title       = 'Knee Adduction Moment — Normal Gait',
    show_mean   = False,
)

#Versuch bei Knee Angle Moment, da gait_normal_05_ID.sto Fehler hat - geprüft ob auch hier der Fehler ist (Antwort: Ja)
plotGait(
    files       = [file_n1, file_n2, file_n3],
    label       = 'knee_angle_l_moment',
    sigmas      = [0, 1, 0], #Gauss filter zum Glätten der Kurven (0 = kein Filter)
    colors      = ['tab:blue', 'tab:orange', 'tab:green'],
    trial_names = ['Normal 1', 'Normal 2', 'Normal 3'],
    title       = 'Knee Angle Moment — Normal Gait',
    show_mean   = False,
)