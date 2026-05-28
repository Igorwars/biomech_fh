# =====================================================================
# IMPORTS
# =====================================================================
import re
from pathlib import Path
import matplotlib.pyplot as plt
from read import (plotGait, setAxLabels,
                  normal1, normal2, normal3,
                  lateral1, lateral2, lateral3,
                  medial1, medial2, medial3)

# Plots speichern unter <SAVE_DIR>/<slug>.png. Auf None setzen zum Deaktivieren.
SAVE_DIR = Path(__file__).parent / 'plots_out'

def saveFig(fig, name):
    if SAVE_DIR is None or not name:
        return
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r'[^\w]+', '_', name).strip('_').lower()
    fig.savefig(SAVE_DIR / f'{slug}.png', dpi=150, bbox_inches='tight')




# =====================================================================
# MAIN
# =====================================================================
def main():
    #Kniegelenkmomente Flexion/ extension  normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 3 Graphen)
    compareToOverlayPlots('knee_angle_l_moment', suptitle='Knee Angle Moment')
    overlayPlot('knee_angle_l_moment', title='Knee Angle Moment — Overlay')

    #Kniegelenkmomente Innen/ Außen Rotation    normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 3 Graphen)
    compareToOverlayPlots('knee_rotation_l_moment', suptitle='Knee Rotation Moment')
    overlayPlot('knee_rotation_l_moment', title='Knee Rotation Moment — Overlay')

    #Kniegelenkmomente Abbduktion/adduktion  normal, medial, lateral (mittelwerte  und Standardabweichung) (1 Abb & 3 Graphen)
    compareToOverlayPlots('knee_adduction_l_moment', suptitle='Knee Adduction Moment')
    overlayPlot('knee_adduction_l_moment', title='Knee Adduction Moment — Overlay')

    #Kniegelenkwinkel Flexion/ extension     normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 4 Graphen)
    compareToOverlayPlots('knee_angle_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Flexion Angle')
    overlayPlot('knee_angle_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Flexion Angle — Overlay')

    #Kniegelenkwinkel Innen/ Außen Rotation  normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 4 Graphen)
    compareToOverlayPlots('knee_rotation_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Rotation Angle')
    overlayPlot('knee_rotation_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Rotation Angle — Overlay')

    #Kniegelenkwinkel Abbduktion/adduktion   normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 4 Graphen)
    compareToOverlayPlots('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Adduction Angle')
    overlayPlot('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Adduction Angle — Overlay')


# =====================================================================
# LABEL-REFERENZ (zum Nachschlagen, nicht ausgeführt)
# =====================================================================
"""ALLE LABELS:

Inverse Dynamik:
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


Inverse Kinematik:
time	pelvis_tilt	pelvis_list	pelvis_rotation	pelvis_tx
pelvis_ty	pelvis_tz

hip_flexion_r	hip_adduction_r	hip_rotation_r

knee_angle_r	knee_rotation_r	knee_adduction_r

ankle_angle_r	subtalar_angle_r	mtp_angle_r	hip_flexion_l
hip_adduction_l	hip_rotation_l
knee_angle_l	knee_rotation_l	knee_adduction_l
ankle_angle_l	subtalar_angle_l	mtp_angle_l
lumbar_extension	lumbar_bending	lumbar_rotation
"""


# =====================================================================
# TRIAL-GRUPPEN
# =====================================================================
normals  = [normal1, normal3]
medials  = [medial1, medial2, medial3]
laterals = [lateral1, lateral2, lateral3]


# =====================================================================
# PLOT-HELPER
# =====================================================================
def overlayPlot(label, source='inverse_dynamic', ylabel='Moment in Nm', title=None):
    fig, ax = plt.subplots(figsize=(10, 5))
    plotGait(normals,  label, source=source, ax=ax, show_mean=True, only_mean=True, mean_color='tab:blue',  mean_label='Normal Gait',  std_label=None, legend=False)
    plotGait(medials,  label, source=source, ax=ax, show_mean=True, only_mean=True, mean_color='tab:green', mean_label='Medial Gait',  std_label=None, legend=False)
    plotGait(laterals, label, source=source, ax=ax, show_mean=True, only_mean=True, mean_color='tab:pink',  mean_label='Lateral Gait', std_label=None, legend=True)
    ax.set(xlabel='% Gangzyklus', ylabel=ylabel, title=title)
    saveFig(fig, title)
    plt.show()


def compareToOverlayPlots(label, source='inverse_dynamic', ylabel='Moment in Nm', suptitle=None):
    fig, axs = plt.subplots(1, 4, figsize=(20, 4), sharey=True)
    plotGait(normals,  label, source=source, title='Normal Gait',  ax=axs[0], show_mean=True, only_mean=True, mean_color='tab:blue',  mean_label='Normal Gait',  std_label=None, legend=False)
    plotGait(medials,  label, source=source, title='Medial Gait',  ax=axs[1], show_mean=True, only_mean=True, mean_color='tab:green', mean_label='Medial Gait',  std_label=None, legend=False)
    plotGait(laterals, label, source=source, title='Lateral Gait', ax=axs[2], show_mean=True, only_mean=True, mean_color='tab:pink',  mean_label='Lateral Gait', std_label=None, legend=False)

    plotGait(normals,  label, source=source, title='Overlay', ax=axs[3], show_mean=True, only_mean=True, mean_color='tab:blue',  mean_label='Normal Gait',  show_std=False, legend=False)
    plotGait(medials,  label, source=source, title='Overlay', ax=axs[3], show_mean=True, only_mean=True, mean_color='tab:green', mean_label='Medial Gait',  show_std=False, legend=False)
    plotGait(laterals, label, source=source, title='Overlay', ax=axs[3], show_mean=True, only_mean=True, mean_color='tab:pink',  mean_label='Lateral Gait', show_std=False, legend=False)
    setAxLabels(axs, xlabel='% Gangzyklus', ylabel=ylabel, suptitle=suptitle, legend=True)
    saveFig(fig, suptitle)
    plt.show()


# =====================================================================
# AUSFÜHRUNG
# =====================================================================
main()
