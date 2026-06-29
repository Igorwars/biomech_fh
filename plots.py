# =====================================================================
# IMPORTS
# =====================================================================
import re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import read
from read import (plotGait, setAxLabels, getFromLabel, integerTicks,
                  directionsFor, directionLabels,
                  normal1, normal2, normal3,
                  lateral1, lateral2, lateral3,
                  medial1, medial2, medial3)

# Plots speichern unter <SAVE_DIR>/<slug>.png. Auf None setzen zum Deaktivieren.
SAVE_DIR           = Path(__file__).parent / 'plots_out'
SAVE_DIR_SECONDARY = Path(__file__).parent / 'plots_secondary'
SAVE_DIR_MONO = Path(__file__).parent / 'plots_monocolor'

SAVE_DIR_FINAL = Path(__file__).parent / 'plots_final'
SAVE_DIR_FINAL_OVERLAYS = SAVE_DIR_FINAL / 'overlays'

def saveFig(fig, name, save_dir=None):
    target = save_dir if save_dir is not None else SAVE_DIR
    if target is None or not name:
        return
    target.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r'[^\w]+', '_', name).strip('_').lower()
    fig.savefig(target / f'{slug}.png', dpi=150, bbox_inches='tight')


"""
Ground reaction forces (6 Stück)
Ankle flexion angle / moment / mit mittelwert, alle trials -> 4 Images
subtalar angle / moment / mit mittelwert, alle trials -> 4 Images
Knee flexion angle / moment / mit mittelwert, alle trials -> 4 Images
Knee adduction angle / moment / mit mittelwert, alle trials  -> 4 Images
Knee rotation angle / moment / mit mittelwert, alle trials  -> 4 Images
Hip flexion angle / moment / mit mittelwert, alle trials -> 4 Images
Hip adduction angle / moment / mit mittelwert, alle trials -> 4 Images
Hip rotation angle / moment / mit mittelwert, alle trials -> 4 Images
"""
def mostImportantPlots():
    #Ground reaction forces (6 Stück)
    compareToOverlayPlots('1_ground_force_vy', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Superior/Inferior', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('1_ground_force_vy', source='analog', ylabel='Kraft in N', title='Bodenreaktionskraft Superior/Inferior', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('1_ground_force_vz', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Anterior/Posterior', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('1_ground_force_vz', source='analog', ylabel='Kraft in N', title='Bodenreaktionskraft Anterior/Posterior', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('1_ground_force_vx', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Medial/Lateral', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('1_ground_force_vx', source='analog', ylabel='Kraft in N', title='Bodenreaktionskraft Medial/Lateral', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    #Knee angles (3x4)
    compareToOverlayPlots('knee_angle_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Flexion Angle', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('knee_angle_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Flexion Angle', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('knee_rotation_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Rotation Angle', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('knee_rotation_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Rotation Angle', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Adduction Angle', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Adduction Angle', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('knee_angle_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', suptitle='Knee Flexion Moment', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('knee_angle_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', title='Knee Flexion Moment', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('knee_rotation_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', suptitle='Knee Rotation Moment', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('knee_rotation_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', title='Knee Rotation Moment', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('knee_adduction_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', suptitle='Knee Adduction Moment', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('knee_adduction_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', title='Knee Adduction Moment', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    
    #Ankle angles (2x4)
    compareToOverlayPlots('ankle_angle_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Ankle Flexion Angle', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('ankle_angle_l', source='inverse_kinematic', ylabel='Winkel in °', title='Ankle Flexion Angle', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('subtalar_angle_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Subtalar Angle', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('subtalar_angle_l', source='inverse_kinematic', ylabel='Winkel in °', title='Subtalar Angle', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('ankle_angle_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', suptitle='Ankle Flexion Moment', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('ankle_angle_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', title='Ankle Flexion Moment', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('subtalar_angle_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', suptitle='Subtalar Moment', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('subtalar_angle_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', title='Subtalar Moment', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    
    #Hip angles (3x4)
    compareToOverlayPlots('hip_flexion_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Flexion Angle', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('hip_flexion_l', source='inverse_kinematic', ylabel='Winkel in °', title='Hip Flexion Angle', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('hip_rotation_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Rotation Angle', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('hip_rotation_l', source='inverse_kinematic', ylabel='Winkel in °', title='Hip Rotation Angle', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('hip_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Adduction Angle', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('hip_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', title='Hip Adduction Angle', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('hip_flexion_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', suptitle='Hip Flexion Moment', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('hip_flexion_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', title='Hip Flexion Moment', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('hip_rotation_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', suptitle='Hip Rotation Moment', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('hip_rotation_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', title='Hip Rotation Moment', save_dir=SAVE_DIR_FINAL_OVERLAYS)
    compareToOverlayPlots('hip_adduction_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', suptitle='Hip Adduction Moment', save_dir=SAVE_DIR_FINAL)
    overlayPlot          ('hip_adduction_l_moment', source='inverse_dynamic', ylabel='Moment in Nm', title='Hip Adduction Moment', save_dir=SAVE_DIR_FINAL_OVERLAYS)


# =====================================================================
# MAIN
# =====================================================================
def main():
    # =================================================================
    # GRUPPIERTE OVERLAY-ABBILDUNGEN
    # Pro Gelenk je eine Abbildung fuer Winkel und eine fuer Momente,
    # Panels nebeneinander = die Freiheitsgrade (max 3). Jedes Panel ist
    # ein Overlay (Normal/Medial/Lateral-Mittel) wie overlayPlot.
    # =================================================================
    DEG = 'Winkel in °'
    NM  = 'Moment in Nm'
    N   = 'Kraft in N'

    # ---- Kniegelenk ----
    overlayRow([('knee_angle_l',     'Flexion/Extension'),
                ('knee_adduction_l', 'Adduktion/Abduktion'),
                ('knee_rotation_l',  'Innen-/Außenrotation')],
               source='inverse_kinematic', ylabel=DEG, suptitle='Knie — Winkel')
    overlayRow([('knee_angle_l_moment',     'Flexion/Extension'),
                ('knee_adduction_l_moment', 'Adduktion/Abduktion'),
                ('knee_rotation_l_moment',  'Innen-/Außenrotation')],
               source='inverse_dynamic', ylabel=NM, suptitle='Knie — Momente')

    # ---- Sprunggelenk ----
    overlayRow([('ankle_angle_l',    'Dorsal-/Plantarflexion'),
                ('subtalar_angle_l', 'Inversion/Eversion')],
               source='inverse_kinematic', ylabel=DEG, suptitle='Sprunggelenk — Winkel')
    overlayRow([('ankle_angle_l_moment',    'Dorsal-/Plantarflexion'),
                ('subtalar_angle_l_moment', 'Inversion/Eversion')],
               source='inverse_dynamic', ylabel=NM, suptitle='Sprunggelenk — Momente')

    # ---- Hüfte ----
    overlayRow([('hip_flexion_l',   'Flexion/Extension'),
                ('hip_adduction_l', 'Adduktion/Abduktion'),
                ('hip_rotation_l',  'Innen-/Außenrotation')],
               source='inverse_kinematic', ylabel=DEG, suptitle='Hüfte — Winkel')
    overlayRow([('hip_flexion_l_moment',   'Flexion/Extension'),
                ('hip_adduction_l_moment', 'Adduktion/Abduktion'),
                ('hip_rotation_l_moment',  'Innen-/Außenrotation')],
               source='inverse_dynamic', ylabel=NM, suptitle='Hüfte — Momente')

    # ---- Bodenreaktionskräfte ----
    overlayRow([('1_ground_force_vy', 'Superior/Inferior'),
                ('1_ground_force_vz', 'Anterior/Posterior'),
                ('1_ground_force_vx', 'Medial/Lateral')],
               source='analog', ylabel=N, suptitle='Bodenreaktionskräfte')

    #return  # ---- alter (ungenutzter) Plot-Block darunter bleibt erhalten ----

    #Kniegelenkmomente Flexion/ extension  normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 3 Graphen)
    compareToOverlayPlots('knee_angle_l_moment', suptitle='Knee Flexion Moment')
    overlayPlot('knee_angle_l_moment', title='Knee Flexion Moment')
    nineLinesOverlay('knee_angle_l_moment', title='Knee Flexion Moment — All Trials')

    #Kniegelenkmomente Innen/ Außen Rotation    normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 3 Graphen)
    compareToOverlayPlots('knee_rotation_l_moment', suptitle='Knee Rotation Moment')
    overlayPlot('knee_rotation_l_moment', title='Knee Rotation Moment')
    nineLinesOverlay('knee_rotation_l_moment', title='Knee Rotation Moment — All Trials')

    #Kniegelenkmomente Abbduktion/adduktion  normal, medial, lateral (mittelwerte  und Standardabweichung) (1 Abb & 3 Graphen)
    compareToOverlayPlots('knee_adduction_l_moment', suptitle='Knee Adduction Moment')
    overlayPlot('knee_adduction_l_moment', title='Knee Adduction Moment')
    nineLinesOverlay('knee_adduction_l_moment', title='Knee Adduction Moment — All Trials')

    #Kniegelenkwinkel Flexion/ extension     normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 4 Graphen)
    compareToOverlayPlots('knee_angle_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Flexion Angle')
    overlayPlot('knee_angle_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Flexion Angle')
    nineLinesOverlay('knee_angle_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Flexion Angle — All Trials')

    #Kniegelenkwinkel Innen/ Außen Rotation  normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 4 Graphen)
    compareToOverlayPlots('knee_rotation_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Rotation Angle')
    overlayPlot('knee_rotation_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Rotation Angle')
    nineLinesOverlay('knee_rotation_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Rotation Angle — All Trials')

    #Kniegelenkwinkel Abbduktion/adduktion   normal, medial, lateral (mittelwerte und Standardabweichung) (1 Abb & 4 Graphen)
    compareToOverlayPlots('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Adduction Angle')
    overlayPlot('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Adduction Angle')
    nineLinesOverlay('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Adduction Angle — All Trials')

    # ---- 3x3 Trial-Vergleich + 9-Trial-Overlay pro Metrik ----
    compareTrials3x1('knee_angle_l_moment',     suptitle='Knee Flexion Moment — Trials')
    nineLinesOverlay('knee_angle_l_moment',     title='Knee Flexion Moment — All Trials')

    compareTrials3x1('knee_rotation_l_moment',  suptitle='Knee Rotation Moment — Trials')
    nineLinesOverlay('knee_rotation_l_moment',  title='Knee Rotation Moment — All Trials')

    compareTrials3x1('knee_adduction_l_moment', suptitle='Knee Adduction Moment — Trials')
    nineLinesOverlay('knee_adduction_l_moment', title='Knee Adduction Moment — All Trials')

    compareTrials3x1('knee_angle_l',     source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Flexion Angle — Trials')
    nineLinesOverlay('knee_angle_l',     source='inverse_kinematic', ylabel='Winkel in °', title='Knee Flexion Angle — All Trials')

    compareTrials3x1('knee_rotation_l',  source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Rotation Angle — Trials')
    nineLinesOverlay('knee_rotation_l',  source='inverse_kinematic', ylabel='Winkel in °', title='Knee Rotation Angle — All Trials')

    compareTrials3x1('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Adduction Angle — Trials')
    nineLinesOverlay('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', title='Knee Adduction Angle — All Trials')
    

    # ---- Bodenreaktionskräfte: Mittelwerte + Std (4x1) und Overlay (1x1) ----
    compareToOverlayPlots('1_ground_force_vy', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Superior/Inferior')
    overlayPlot          ('1_ground_force_vy', source='analog', ylabel='Kraft in N', title='Bodenreaktionskraft Superior/Inferior')

    compareToOverlayPlots('1_ground_force_vz', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Anterior/Posterior')
    overlayPlot          ('1_ground_force_vz', source='analog', ylabel='Kraft in N', title='Bodenreaktionskraft Anterior/Posterior')

    compareToOverlayPlots('1_ground_force_vx', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Medial/Lateral')
    overlayPlot          ('1_ground_force_vx', source='analog', ylabel='Kraft in N', title='Bodenreaktionskraft Medial/Lateral')

    # ---- Bodenreaktionskräfte: Einzeltrials (3x1) und 9-Trial-Overlay (1x1) ----
    compareTrials3x1('1_ground_force_vy', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Superior/Inferior — Trials')
    nineLinesOverlay('1_ground_force_vy', source='analog', ylabel='Kraft in N', title='Bodenreaktionskraft Superior/Inferior — All Trials')

    compareTrials3x1('1_ground_force_vz', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Anterior/Posterior — Trials')
    nineLinesOverlay('1_ground_force_vz', source='analog', ylabel='Kraft in N', title='Bodenreaktionskraft Anterior/Posterior — All Trials')

    compareTrials3x1('1_ground_force_vx', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Medial/Lateral — Trials')
    nineLinesOverlay('1_ground_force_vx', source='analog', ylabel='Kraft in N', title='Bodenreaktionskraft Medial/Lateral — All Trials')
    
    # ====================================================================
    # SEKUNDÄR-PLOTS: Hüfte + Sprunggelenk → plots_secondary/
    # ====================================================================
    sec = SAVE_DIR_SECONDARY
    ""
    # ---- Hüftgelenkmomente Flexion/Extension ----
    compareToOverlayPlots('hip_flexion_l_moment',   suptitle='Hip Flexion Moment',   save_dir=sec)
    overlayPlot          ('hip_flexion_l_moment',   title='Hip Flexion Moment',   save_dir=sec)
    # ---- Hüftgelenkmomente Innen/Außen Rotation ----
    compareToOverlayPlots('hip_rotation_l_moment',  suptitle='Hip Rotation Moment',  save_dir=sec)
    overlayPlot          ('hip_rotation_l_moment',  title='Hip Rotation Moment',  save_dir=sec)
    # ---- Hüftgelenkmomente Abduktion/Adduktion ----
    compareToOverlayPlots('hip_adduction_l_moment', suptitle='Hip Adduction Moment', save_dir=sec)
    overlayPlot          ('hip_adduction_l_moment', title='Hip Adduction Moment', save_dir=sec)

    # ---- Hüftgelenkwinkel Flexion/Extension ----
    compareToOverlayPlots('hip_flexion_l',   source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Flexion Angle',   save_dir=sec)
    overlayPlot          ('hip_flexion_l',   source='inverse_kinematic', ylabel='Winkel in °', title='Hip Flexion Angle',   save_dir=sec)
    # ---- Hüftgelenkwinkel Innen/Außen Rotation ----
    compareToOverlayPlots('hip_rotation_l',  source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Rotation Angle',  save_dir=sec)
    overlayPlot          ('hip_rotation_l',  source='inverse_kinematic', ylabel='Winkel in °', title='Hip Rotation Angle',  save_dir=sec)
    # ---- Hüftgelenkwinkel Abduktion/Adduktion ----
    compareToOverlayPlots('hip_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Adduction Angle', save_dir=sec)
    overlayPlot          ('hip_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', title='Hip Adduction Angle', save_dir=sec)

    # ---- Hüfte: Einzeltrials (3x1 + 9-Trial-Overlay) ----
    compareTrials3x1('hip_flexion_l_moment',   suptitle='Hip Flexion Moment — Trials',   save_dir=sec)
    nineLinesOverlay('hip_flexion_l_moment',   title='Hip Flexion Moment — All Trials',  save_dir=sec)
    compareTrials3x1('hip_rotation_l_moment',  suptitle='Hip Rotation Moment — Trials',  save_dir=sec)
    nineLinesOverlay('hip_rotation_l_moment',  title='Hip Rotation Moment — All Trials', save_dir=sec)
    compareTrials3x1('hip_adduction_l_moment', suptitle='Hip Adduction Moment — Trials', save_dir=sec)
    nineLinesOverlay('hip_adduction_l_moment', title='Hip Adduction Moment — All Trials',save_dir=sec)

    compareTrials3x1('hip_flexion_l',   source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Flexion Angle — Trials',   save_dir=sec)
    nineLinesOverlay('hip_flexion_l',   source='inverse_kinematic', ylabel='Winkel in °', title='Hip Flexion Angle — All Trials',   save_dir=sec)
    compareTrials3x1('hip_rotation_l',  source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Rotation Angle — Trials',  save_dir=sec)
    nineLinesOverlay('hip_rotation_l',  source='inverse_kinematic', ylabel='Winkel in °', title='Hip Rotation Angle — All Trials',  save_dir=sec)
    compareTrials3x1('hip_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Adduction Angle — Trials', save_dir=sec)
    nineLinesOverlay('hip_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', title='Hip Adduction Angle — All Trials', save_dir=sec)

    # ---- Sprunggelenkmomente Plantar/Dorsiflexion ----
    compareToOverlayPlots('ankle_angle_l_moment',    suptitle='Ankle Flexion Moment',  save_dir=sec)
    overlayPlot          ('ankle_angle_l_moment',    title='Ankle Flexion Moment',  save_dir=sec)
    # ---- Sprunggelenkmomente Innen/Außen Rotation (Subtalar / Inv-Ev) ----
    compareToOverlayPlots('subtalar_angle_l_moment', suptitle='Subtalar Moment',       save_dir=sec)
    overlayPlot          ('subtalar_angle_l_moment', title='Subtalar Moment',       save_dir=sec)

    # ---- Sprunggelenkwinkel Plantar/Dorsiflexion ----
    compareToOverlayPlots('ankle_angle_l',    source='inverse_kinematic', ylabel='Winkel in °', suptitle='Ankle Flexion Angle',  save_dir=sec)
    overlayPlot          ('ankle_angle_l',    source='inverse_kinematic', ylabel='Winkel in °', title='Ankle Flexion Angle',  save_dir=sec)
    # ---- Sprunggelenkwinkel Innen/Außen Rotation (Subtalar) ----
    compareToOverlayPlots('subtalar_angle_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Subtalar Angle',       save_dir=sec)
    overlayPlot          ('subtalar_angle_l', source='inverse_kinematic', ylabel='Winkel in °', title='Subtalar Angle',       save_dir=sec)

    # ---- Sprunggelenk: Einzeltrials (3x1 + 9-Trial-Overlay) ----
    compareTrials3x1('ankle_angle_l_moment',    suptitle='Ankle Flexion Moment — Trials',  save_dir=sec)
    nineLinesOverlay('ankle_angle_l_moment',    title='Ankle Flexion Moment — All Trials', save_dir=sec)
    compareTrials3x1('subtalar_angle_l_moment', suptitle='Subtalar Moment — Trials',       save_dir=sec)
    nineLinesOverlay('subtalar_angle_l_moment', title='Subtalar Moment — All Trials',      save_dir=sec)

    compareTrials3x1('ankle_angle_l',    source='inverse_kinematic', ylabel='Winkel in °', suptitle='Ankle Flexion Angle — Trials',  save_dir=sec)
    nineLinesOverlay('ankle_angle_l',    source='inverse_kinematic', ylabel='Winkel in °', title='Ankle Flexion Angle — All Trials', save_dir=sec)
    compareTrials3x1('subtalar_angle_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Subtalar Angle — Trials',       save_dir=sec)
    nineLinesOverlay('subtalar_angle_l', source='inverse_kinematic', ylabel='Winkel in °', title='Subtalar Angle — All Trials',      save_dir=sec)
   
    sec = SAVE_DIR_MONO
    compareTrials3x1Monocolor('knee_angle_l_moment',     suptitle='Knee Flexion Moment — Trials',     save_dir=sec)
    compareTrials3x1Monocolor('knee_rotation_l_moment',  suptitle='Knee Rotation Moment — Trials',  save_dir=sec)
    compareTrials3x1Monocolor('knee_adduction_l_moment', suptitle='Knee Adduction Moment — Trials', save_dir=sec)
    compareTrials3x1Monocolor('knee_angle_l',     source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Flexion Angle — Trials',     save_dir=sec)
    compareTrials3x1Monocolor('knee_rotation_l',  source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Rotation Angle — Trials',  save_dir=sec)
    compareTrials3x1Monocolor('knee_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Knee Adduction Angle — Trials', save_dir=sec)
    compareTrials3x1Monocolor('1_ground_force_vy', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Vertikal — Trials', save_dir=sec)
    compareTrials3x1Monocolor('1_ground_force_vz', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Anterior/Posterior — Trials', save_dir=sec)
    compareTrials3x1Monocolor('1_ground_force_vx', source='analog', ylabel='Kraft in N', suptitle='Bodenreaktionskraft Medial/Lateral — Trials', save_dir=sec)
    compareTrials3x1Monocolor('hip_flexion_l_moment',   suptitle='Hip Flexion Moment — Trials',   save_dir=sec)
    compareTrials3x1Monocolor('hip_rotation_l_moment',  suptitle='Hip Rotation Moment — Trials',  save_dir=sec)
    compareTrials3x1Monocolor('hip_adduction_l_moment', suptitle='Hip Adduction Moment — Trials', save_dir=sec)
    compareTrials3x1Monocolor('hip_flexion_l',   source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Flexion Angle — Trials',   save_dir=sec)
    compareTrials3x1Monocolor('hip_rotation_l',  source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Rotation Angle — Trials',  save_dir=sec)
    compareTrials3x1Monocolor('hip_adduction_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Hip Adduction Angle — Trials', save_dir=sec)
    compareTrials3x1Monocolor('ankle_angle_l_moment',    suptitle='Ankle Flexion Moment — Trials',  save_dir=sec)
    compareTrials3x1Monocolor('subtalar_angle_l_moment', suptitle='Subtalar Moment — Trials',       save_dir=sec)
    compareTrials3x1Monocolor('ankle_angle_l',    source='inverse_kinematic', ylabel='Winkel in °', suptitle='Ankle Flexion Angle — Trials',  save_dir=sec)
    compareTrials3x1Monocolor('subtalar_angle_l', source='inverse_kinematic', ylabel='Winkel in °', suptitle='Subtalar Angle — Trials',       save_dir=sec)
    
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
normals  = [normal1, normal2, normal3]
medials  = [medial1, medial2, medial3]
laterals = [lateral1, lateral2, lateral3]


# =====================================================================
# PLOT-HELPER
# =====================================================================
def overlayPlot(label, source='inverse_dynamic', ylabel='Moment in Nm', title=None, save_dir=None):
    fig, ax = plt.subplots(figsize=(10, 5))
    plotGait(normals,  label, source=source, ax=ax, show_mean=True, only_mean=True, mean_color='black',  mean_label='Normal Gait',  std_label=None, legend=False)
    plotGait(medials,  label, source=source, ax=ax, show_mean=True, only_mean=True, mean_color='tab:cyan', mean_label='Medial Gait',  std_label=None, legend=False)
    plotGait(laterals, label, source=source, ax=ax, show_mean=True, only_mean=True, mean_color='tab:pink',  mean_label='Lateral Gait', std_label=None, legend=True)
    ax.set(xlabel='% Standphase', ylabel=ylabel, title=title)
    saveFig(fig, title, save_dir=save_dir)
    plt.show()


def overlayRow(metrics, source='inverse_dynamic', ylabel='Moment in Nm',
               suptitle=None, save_dir=None):
    """Mehrere Overlay-Plots (Normal/Medial/Lateral-Mittel) nebeneinander.

    metrics: Liste von (label, panel_title), max. 3 Panels.
    Jedes Panel ist ein Overlay genau wie overlayPlot, je Freiheitsgrad eines.
    """
    conditions = [
        (normals,  'black',    'Normal Gait'),
        (medials,  'tab:cyan', 'Medial Gait'),
        (laterals, 'tab:pink', 'Lateral Gait'),
    ]
    n = len(metrics)
    fig, axs = plt.subplots(1, n, figsize=(6.5 * n, 5), squeeze=False)
    axs = axs[0]
    for ax, (label, ptitle) in zip(axs, metrics):
        for trials, color, name in conditions:
            plotGait(trials, label, source=source, ax=ax,
                     show_mean=True, only_mean=True, mean_color=color,
                     mean_label=name, show_std=True, std_label=None,
                     legend=False, show_dir=False, ylabel='')
        ax.set(title=ptitle, xlabel='% Standphase')
        pair = directionsFor(label, source)
        if pair:
            directionLabels(ax, *pair, only_first_col=False)
    axs[0].set_ylabel(ylabel)
    axs[-1].legend(loc='best')
    if suptitle:
        fig.suptitle(suptitle, fontsize=14, fontweight='bold')
    fig.subplots_adjust(wspace=0.5)
    saveFig(fig, suptitle, save_dir=save_dir)
    plt.show()


def compareToOverlayPlots(label, source='inverse_dynamic', ylabel='Moment in Nm', suptitle=None, save_dir=None):
    fig, axs = plt.subplots(1, 4, figsize=(20, 4), sharey=True)
    plotGait(normals,  label, source=source, title='Normal Gait',  ax=axs[0], show_mean=True, only_mean=True, mean_color='black',  mean_label='Normal Gait',  std_label=None, legend=False)
    plotGait(medials,  label, source=source, title='Medial Gait',  ax=axs[1], show_mean=True, only_mean=True, mean_color='tab:cyan', mean_label='Medial Gait',  std_label=None, legend=False)
    plotGait(laterals, label, source=source, title='Lateral Gait', ax=axs[2], show_mean=True, only_mean=True, mean_color='tab:pink',  mean_label='Lateral Gait', std_label=None, legend=False)

    plotGait(normals,  label, source=source, title='Overlay', ax=axs[3], show_mean=True, only_mean=True, mean_color='black',  mean_label='Normal Gait',  show_std=False, legend=False)
    plotGait(medials,  label, source=source, title='Overlay', ax=axs[3], show_mean=True, only_mean=True, mean_color='tab:cyan', mean_label='Medial Gait',  show_std=False, legend=False)
    plotGait(laterals, label, source=source, title='Overlay', ax=axs[3], show_mean=True, only_mean=True, mean_color='tab:pink',  mean_label='Lateral Gait', show_std=False, legend=False)
    setAxLabels(axs, xlabel='% Standphase', ylabel=ylabel, suptitle=suptitle, legend=True)
    saveFig(fig, suptitle, save_dir=save_dir)
    plt.show()


def loadNormalized(trial, label, source='inverse_dynamic', n_points=101):
    t = getFromLabel(trial[source], 'time')[1]
    y = getFromLabel(trial[source], label)[1]
    t0, t1 = trial['window']
    mask = (t >= t0) & (t <= t1)
    t_sel, y_sel = t[mask], y[mask]
    pct = (t_sel - t_sel[0]) / (t_sel[-1] - t_sel[0]) * 100
    if read.MARKER_MODE:
        # native Stuetzpunkte -> kein Resampling, keine Interpolation
        return pct, y_sel
    x = np.linspace(0, 100, n_points)
    return x, np.interp(x, pct, y_sel)


def compareTrials3x1(label, source='inverse_dynamic', ylabel='Moment in Nm', suptitle=None, save_dir=None):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    conditions = [
        (normals,  'Normal Gait'),
        (medials,  'Medial Gait'),
        (laterals, 'Lateral Gait'),
    ]
    for col, (trials, name) in enumerate(conditions):
        plotGait(trials, label, source=source, title=name, ax=axs[col])
    setAxLabels(axs, xlabel='% Standphase', ylabel=ylabel, suptitle=suptitle)
    saveFig(fig, suptitle, save_dir=save_dir)
    plt.show()
    
def compareTrials3x1Monocolor(label, source='inverse_dynamic', ylabel='Moment in Nm', suptitle=None, save_dir=None):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    conditions = [
        (normals,  'Normal Gait'),
        (medials,  'Medial Gait'),
        (laterals, 'Lateral Gait'),
    ]
    i = 0
    farben = [["black", "black", "black"], ["tab:cyan", "tab:cyan", "tab:cyan"], ["tab:pink", "tab:pink", "tab:pink"]]
    for col, (trials, name) in enumerate(conditions):
        i = i + 1
        plotGait(trials, label, source=source, title=name, ax=axs[col], linestyles=['-', '--', ':'], colors=farben[i-1])
    setAxLabels(axs, xlabel='% Standphase', ylabel=ylabel, suptitle=suptitle)
    saveFig(fig, suptitle, save_dir=save_dir)
    plt.show()


def nineLinesOverlay(label, source='inverse_dynamic', ylabel='Moment in Nm', title=None, save_dir=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    conditions = [
        (normals,  'black'),
        (medials,  'tab:cyan'),
        (laterals, 'tab:pink'),
    ]
    linestyles = ['-', '--', ':']
    for trials, color in conditions:
        for trial, ls in zip(trials, linestyles):
            x, y = loadNormalized(trial, label, source)
            if read.MARKER_MODE:
                ax.plot(x, y, color=color, label=trial['name'], **read.MARKER_KW)
            else:
                ax.plot(x, y, color=color, linestyle=ls, label=trial['name'])
    ax.set(xlabel='% Standphase', ylabel=ylabel, title=title, xlim=(0, 100))
    ax.legend(ncol=3, loc='best')
    ax.grid(True, alpha=0.3)
    integerTicks(ax)
    pair = directionsFor(label, source)
    if pair:
        directionLabels(ax, *pair)
    saveFig(fig, title, save_dir=save_dir)
    plt.show()


def runRaw():
    """Alle Plots nochmal als reine Messpunkte (keine lineare Interpolation)
    in nicht-interpoliert/<unterordner>. Mittelwerte bleiben technisch
    resampled, werden aber als Marker gezeichnet."""
    global SAVE_DIR, SAVE_DIR_SECONDARY, SAVE_DIR_MONO
    base  = Path(__file__).parent / 'nicht-interpoliert'
    saved = (SAVE_DIR, SAVE_DIR_SECONDARY, SAVE_DIR_MONO)
    SAVE_DIR           = base / 'plots_out'
    SAVE_DIR_SECONDARY = base / 'plots_secondary'
    SAVE_DIR_MONO      = base / 'plots_monocolor'
    read.MARKER_MODE = True
    try:
        main()
    finally:
        read.MARKER_MODE = False
        SAVE_DIR, SAVE_DIR_SECONDARY, SAVE_DIR_MONO = saved


# =====================================================================
# AUSFÜHRUNG
# =====================================================================
main()       # normal (linear interpoliert) -> plots_out / plots_secondary / plots_monocolor
runRaw()     # nicht interpoliert (Messpunkte) -> nicht-interpoliert/<unterordner>
mostImportantPlots()
