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
# TRIAL-DEFINITIONEN (Fenster + Files + Darstellung pro Aufnahme)
# =====================================================================
normal1 = {'name': 'Normal 1',  'window': (0.18, 0.86), 'color': 'black',
           'inverse_dynamic': file_n1_id, 'inverse_kinematic': file_n1_ik, 'analog': file_n1_analog}
normal2 = {'name': 'Normal 2',  'window': (0.13, 0.84), 'color': 'tab:cyan',
           'inverse_dynamic': file_n2_id, 'inverse_kinematic': file_n2_ik, 'analog': file_n2_analog}
normal3 = {'name': 'Normal 3',  'window': (0.15, 0.85), 'color': 'tab:pink',
           'inverse_dynamic': file_n3_id, 'inverse_kinematic': file_n3_ik, 'analog': file_n3_analog}

lateral1 = {'name': 'Lateral 1', 'window': (0.16, 0.87), 'color': 'black',
            'inverse_dynamic': file_l1_id, 'inverse_kinematic': file_l1_ik, 'analog': file_l1_analog}
lateral2 = {'name': 'Lateral 2', 'window': (0.09, 0.79), 'color': 'tab:cyan',
            'inverse_dynamic': file_l2_id, 'inverse_kinematic': file_l2_ik, 'analog': file_l2_analog}
lateral3 = {'name': 'Lateral 3', 'window': (0.11, 0.81), 'color': 'tab:pink',
            'inverse_dynamic': file_l3_id, 'inverse_kinematic': file_l3_ik, 'analog': file_l3_analog}

medial1 = {'name': 'Medial 1',  'window': (0.13, 0.84), 'color': 'black',
           'inverse_dynamic': file_m1_id, 'inverse_kinematic': file_m1_ik, 'analog': file_m1_analog}
medial2 = {'name': 'Medial 2',  'window': (0.14, 0.85), 'color': 'tab:cyan',
           'inverse_dynamic': file_m2_id, 'inverse_kinematic': file_m2_ik, 'analog': file_m2_analog}
medial3 = {'name': 'Medial 3',  'window': (0.15, 0.87), 'color': 'tab:pink',
           'inverse_dynamic': file_m3_id, 'inverse_kinematic': file_m3_ik, 'analog': file_m3_analog}

# =====================================================================
# PLOT-FUNKTION (lädt + fenstert + normalisiert + glättet + plottet)
# =====================================================================
def plotGait(trials, label, source='inverse_dynamic', title=None,
             show_mean=False, only_mean=False, ax=None,
             ylabel='Moment [Nm]', n_points=101,
             mean_color='black', mean_label='Mean',
             show_std=True, std_color=None, std_label='Std',
             legend=True):

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure

    x = np.linspace(0, 100, n_points)
    signals = []

    for trial in trials:
        file   = trial[source]
        t0, t1 = trial['window']
        sigma  = trial.get('sigma', 0)
        color  = trial.get('color')
        name   = trial['name']

        t = getFromLabel(file, 'time')[1]
        y = getFromLabel(file, label)[1]

        mask  = (t >= t0) & (t <= t1)
        t_sel = t[mask]
        y_sel = y[mask]

        # Zeit auf 0-100 % Gangzyklus normalisieren + auf gemeinsame Achse resamplen
        pct    = (t_sel - t_sel[0]) / (t_sel[-1] - t_sel[0]) * 100
        y_norm = np.interp(x, pct, y_sel)
        signals.append(y_norm)

        if sigma > 0:
            ax.plot(x, y_norm, color=color, alpha=0.25, linestyle='--')
            y_plot = gaussian_filter1d(y_norm, sigma=sigma)
            label_name = f'{name} (σ={sigma})'
        else:
            y_plot = y_norm
            label_name = name

        if not only_mean:
            ax.plot(x, y_plot, color=color, alpha=0.9, label=label_name)

    if show_mean:
        signals = np.array(signals)
        mean = np.mean(signals, axis=0)
        ax.plot(x, mean, color=mean_color, linewidth=2, label=mean_label)
        if show_std:
            std = np.std(signals, axis=0)
            ax.fill_between(x, mean - std, mean + std,
                            color=std_color or mean_color, alpha=0.2,
                            label=std_label or None)

    ax.set_title(title or label)
    ax.set_xlabel('% Gangzyklus')
    ax.set_ylabel(ylabel)
    if legend:
        ax.legend()
    ax.grid(True, alpha=0.3)

    return fig, ax

def setAxLabels(axs, xlabel="", ylabel="", suptitle=None,
                legend=False, legend_anchor=(0.5, -0.02), legend_bottom=0.22):
    for ax in axs.flat:
        ax.set(xlabel=xlabel, ylabel=ylabel)

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    fig = axs.flat[0].figure
    if suptitle:
        fig.suptitle(suptitle, fontsize=14, fontweight='bold')

    if legend:
        handles, labels, seen = [], [], set()
        for ax in axs.flat:
            for h, l in zip(*ax.get_legend_handles_labels()):
                if l and l not in seen:
                    handles.append(h); labels.append(l); seen.add(l)
        if handles:
            fig.legend(handles, labels, loc='lower center',
                       ncol=len(labels), bbox_to_anchor=legend_anchor)
            fig.subplots_adjust(bottom=legend_bottom)


