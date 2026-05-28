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
IK_DIR = Path(__file__).parent / 'Ergebnisse' / 'IK_Ergebnisse'
ANALOG_DIR = Path(__file__).parent / 'Ergebnisse' / 'CaseStudy_SS2026'

# Normalgang
file_n1_id = ID_DIR / 'Gait_normal_01_ID.sto'
file_n2_id = ID_DIR / 'Gait_normal_05_ID.sto'
file_n3_id = ID_DIR / 'Gait_normal_06_ID.sto'

file_n1_ik = IK_DIR / 'Gait_normal_01_IK.mot'
file_n2_ik = IK_DIR / 'Gait_normal_05_IK.mot'
file_n3_ik = IK_DIR / 'Gait_normal_06_IK.mot'

file_n1_analog = ANALOG_DIR / 'Gait_normal' / 'Gait_normal_01_analogdata.mot'
file_n2_analog = ANALOG_DIR / 'Gait_normal' / 'Gait_normal_05_analogdata.mot'
file_n3_analog = ANALOG_DIR / 'Gait_normal' / 'Gait_normal_06_analogdata.mot'


# Lateraler Gang
file_l1_id = ID_DIR / 'Gait_lateral_06_ID.sto'
file_l2_id = ID_DIR / 'Gait_lateral_09_ID.sto'
file_l3_id = ID_DIR / 'Gait_lateral_29_ID.sto'

file_l1_ik = IK_DIR / 'Gait_lateral_06_IK.mot'
file_l2_ik = IK_DIR / 'Gait_lateral_09_IK.mot'
file_l3_ik = IK_DIR / 'Gait_lateral_29_IK.mot'

file_l1_analog = ANALOG_DIR / 'Gait_lateral' / 'Gait_lateral_06_analogdata.mot'
file_l2_analog = ANALOG_DIR / 'Gait_lateral' / 'Gait_lateral_09_analogdata.mot'
file_l3_analog = ANALOG_DIR / 'Gait_lateral' / 'Gait_lateral_29_analogdata.mot'

# Medialer Gang
file_m1_id = ID_DIR / 'Gait_medial_04_ID.sto'
file_m2_id = ID_DIR / 'Gait_medial_07_ID.sto'
file_m3_id = ID_DIR / 'Gait_medial_08_ID.sto'

file_m1_ik = IK_DIR / 'Gait_medial_04_IK.mot'
file_m2_ik = IK_DIR / 'Gait_medial_07_IK.mot'
file_m3_ik = IK_DIR / 'Gait_medial_08_IK.mot'

file_m1_analog = ANALOG_DIR / 'Gait_medial' / 'Gait_medial_04_analogdata.mot'
file_m2_analog = ANALOG_DIR / 'Gait_medial' / 'Gait_medial_07_analogdata.mot'
file_m3_analog = ANALOG_DIR / 'Gait_medial' / 'Gait_medial_08_analogdata.mot'

# =====================================================================
# PLOT-FUNKTION (lädt + trimmt + glättet + plottet)
# =====================================================================
def plotGait(files, label, sigmas=None, colors=None,
             trial_names=None, title=None, show_mean=False, only_mean=False,
             ax=None, ylabel='Moment [Nm]'):

    n = len(files)
    sigmas      = sigmas      or [0] * n
    colors      = colors      or [f'C{i}' for i in range(n)]
    trial_names = trial_names or [f'Trial {i+1}' for i in range(n)]

    # Daten laden + auf kürzeste Länge trimmen
    signals = [getFromLabel(f, label)[1] for f in files]
    n_min   = min(len(s) for s in signals)
    signals = np.array([s[:n_min] for s in signals])
    time    = getFromLabel(files[0], 'time')[1][:n_min]

    # Falls kein ax übergeben -> neue Figure
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure

    for signal, c, sigma, name in zip(signals, colors, sigmas, trial_names):
        if sigma > 0:
            ax.plot(time, signal, color=c, alpha=0.25, linestyle='--')  # roh, blass
            signal = gaussian_filter1d(signal, sigma=sigma)
            name = f'{name} (σ={sigma})'
        if not only_mean:
            ax.plot(time, signal, color=c, alpha=0.9, label=name)

    if show_mean:
        mean = np.mean(signals, axis=0)
        std  = np.std(signals,  axis=0)
        ax.plot(time, mean, color='black', linewidth=2, label='Mean')
        ax.fill_between(time, mean - std, mean + std,
                        color='gray', alpha=0.2, label='Std Dev')

    ax.set_title(title or label)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig, ax


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

fix, axs = plt.subplots(1, 3, figsize=(12, 18))

fig3, ax3 = plotGait(
    files       = [file_n1_id, file_n3_id],
    label       = 'knee_rotation_r_moment',
    sigmas      = [0, 0], #Gauss filter zum Glätten der Kurven (0 = kein Filter)
    colors      = ['tab:blue', 'tab:green'],
    trial_names = ['Normal 1', 'Normal 3'],
    title       = 'Knee Rotation Moment — Normal Gait',
    show_mean   = False,
    only_mean   = False,
    ax          = axs[0],
    ylabel      = 'Moment in Nm', # Normalisiert auf Körpergewicht
)

fig4, ax4 = plotGait(
    files       = [file_m1_id, file_m2_id, file_m3_id],
    label       = 'knee_rotation_r_moment',
    sigmas      = [0, 0, 0], #Gauss filter zum Glätten der Kurven (0 = kein Filter)
    colors      = ['tab:blue', 'tab:orange', 'tab:green'],
    trial_names = ['Medial 1', 'Medial 2', 'Medial 3'],
    title       = 'Knee Rotation Moment — Medial Gait',
    show_mean   = False,
    ax          = axs[1],
    ylabel      = 'Moment in Nm', # Normalisiert auf Körpergewicht
)

fig5, ax5 = plotGait(
    files       = [file_l1_id, file_l2_id, file_l3_id],
    label       = 'knee_rotation_r_moment',
    sigmas      = [0]*3, #Gauss filter zum Glätten der Kurven (0 = kein Filter)
    colors      = ['tab:blue', 'tab:orange', 'tab:green'],
    trial_names = ['Lateral 1', 'Lateral 2', 'Lateral 3'],
    title       = 'Knee Rotation Moment — Lateral Gait',
    show_mean   = False,
    ax          = axs[2],
    ylabel      = 'Moment in Nm', # Normalisiert auf Körpergewicht
)

for ax in axs.flat:
    ax.set(xlabel='Zeit in s', ylabel='Moment in Nm')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.show()