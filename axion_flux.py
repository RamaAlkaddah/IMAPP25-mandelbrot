"""
axion_flux.py
=============
Compute and plot the differential solar axion flux from the Primakoff process
for three axion masses: ma = 0, 10, and 130 keV.

Physical basis
--------------
Reference: Giannotti et al., JCAP 2017 / PRD 2019
(see also the parametric fit in the CAST/IAXO analysis papers that cite Giannotti)

The Primakoff process converts a solar photon (γ) into an axion (a) via its
coupling to two photons:
        γ  +  Ze  →  a  +  Ze        (photon ↔ axion conversion in Coulomb field)

The coupling constant is g_aγ  [GeV^-1].

Massless axion flux (Giannotti parametric fit to solar model AGSS09)
---------------------------------------------------------------------
The integral over the solar interior has been performed numerically for the
standard solar model. The result is well-described by:

    dΦ/dω  =  A · (g_aγ / g_ref)²  ·  ω^α · exp(−ω / ω₀)

with best-fit parameters:
    A      = 6.02 × 10^10   [cm^-2 s^-1 keV^-1]
    g_ref  = 1 × 10^-10     [GeV^-1]  (reference coupling for normalisation)
    α      = 2.481           (spectral power-law index)
    ω₀     = 1.205           [keV]    (related to solar core temperature T_core ~ 1.3 keV)

Massive axion modification (kinematic suppression)
--------------------------------------------------
When the axion has a non-zero rest mass ma, two effects enter:

1. Kinematic threshold  (energy conservation)
        ω  ≥  ma
   Below this energy the process is forbidden; the flux is exactly zero.

2. Phase-space / momentum suppression
   The massless formula implicitly assumes the axion momentum equals its energy
   (p = ω, ultra-relativistic limit). For a massive axion,
        p  =  √(ω² − ma²)
   The Primakoff cross section is proportional to p/ω, so the flux picks up
   a suppression factor:
        suppression(ω, ma)  =  √(1 − (ma/ω)²)   for ω > ma
                             =  0                  for ω ≤ ma

Combined formula for massive axion:
    dΦ(ma)/dω  =  [dΦ(0)/dω]  ×  suppression(ω, ma)

Note on ma = 130 keV
--------------------
The peak of the solar Primakoff spectrum is around ω_peak ~ 3 keV (set by the
solar core temperature). For ma = 130 keV the threshold lies far above the
peak, so essentially all of the flux is kinematically forbidden, giving a
result that is effectively zero across the plotted energy range (up to 20 keV).
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# ─────────────────────────────────────────────────────────────────────────────
# Physical parameters
# ─────────────────────────────────────────────────────────────────────────────

# Photon coupling constant (example / benchmark value)
# The flux scales as g_aγ²; change this to study different couplings.
G_AGAMMA = 1.0e-10   # [GeV^-1]  (CAST upper limit: 6.6e-11 GeV^-1)

# Giannotti parametric-fit coefficients for the massless Primakoff flux
A_FIT     = 6.02e10   # normalisation  [cm^-2 s^-1 keV^-1]
G_REF     = 1.0e-10   # reference coupling [GeV^-1]
ALPHA     = 2.481     # spectral index
OMEGA_0   = 1.205     # characteristic energy [keV]  (≈ core temperature scale)

# Axion masses to evaluate [keV]
MASSES_KEV = [0.0, 10.0, 130.0]

# Energy grid [keV]
OMEGA_MIN   = 0.05     # lower bound (avoid numerical issues at ω → 0)
OMEGA_MAX   = 20.0     # upper bound (flux negligible above ~15 keV)
N_POINTS    = 500      # number of energy steps


# ─────────────────────────────────────────────────────────────────────────────
# Flux functions
# ─────────────────────────────────────────────────────────────────────────────

def primakoff_flux_massless(omega, g_agamma):
    """
    Differential Primakoff solar axion flux for a MASSLESS axion.

    Implements the Giannotti parametric formula:
        dΦ/dω  =  A · (g_aγ / g_ref)²  ·  ω^α · exp(−ω / ω₀)

    Parameters
    ----------
    omega     : array_like, photon / axion energy [keV]
    g_agamma  : float, axion-photon coupling [GeV^-1]

    Returns
    -------
    ndarray, differential flux dΦ/dω  [cm^-2 s^-1 keV^-1]
    """
    coupling_ratio_sq = (g_agamma / G_REF) ** 2
    return A_FIT * coupling_ratio_sq * omega**ALPHA * np.exp(-omega / OMEGA_0)


def primakoff_flux_massive(omega, g_agamma, ma_keV):
    """
    Differential Primakoff solar axion flux for a MASSIVE axion (mass ma_keV).

    Applies kinematic threshold and phase-space suppression to the massless
    result:
        dΦ(ma)/dω  =  dΦ(0)/dω  ×  √(1 − (ma/ω)²)   if ω > ma
                    =  0                                if ω ≤ ma

    Parameters
    ----------
    omega     : array_like, photon / axion energy [keV]
    g_agamma  : float, axion-photon coupling [GeV^-1]
    ma_keV    : float, axion mass [keV]

    Returns
    -------
    ndarray, differential flux dΦ/dω  [cm^-2 s^-1 keV^-1]
    """
    # Base (massless) flux at all energy points
    flux0 = primakoff_flux_massless(omega, g_agamma)

    if ma_keV == 0.0:
        # No suppression needed for the massless case
        return flux0

    # Kinematic suppression factor:
    #   √(1 − (ma/ω)²)  where ω > ma, else 0
    # np.clip ensures the argument of sqrt never goes negative due to floating-
    # point rounding; np.where applies the threshold mask without any warning.
    ratio_sq = np.clip(1.0 - (ma_keV / omega) ** 2, 0.0, None)
    suppression = np.where(omega > ma_keV, np.sqrt(ratio_sq), 0.0)

    return flux0 * suppression


# ─────────────────────────────────────────────────────────────────────────────
# Build the energy grid and compute fluxes
# ─────────────────────────────────────────────────────────────────────────────

omega = np.linspace(OMEGA_MIN, OMEGA_MAX, N_POINTS)   # energy axis [keV]

# Dictionary: mass (keV) → flux array [cm^-2 s^-1 keV^-1]
fluxes = {}
for ma in MASSES_KEV:
    fluxes[ma] = primakoff_flux_massive(omega, G_AGAMMA, ma)


# ─────────────────────────────────────────────────────────────────────────────
# Write tabulated results to CSV
# ─────────────────────────────────────────────────────────────────────────────

csv_path = os.path.join(os.path.dirname(__file__), "axion_flux_table.csv")

with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)

    # Header row: energy column + one column per mass
    header = ["omega_keV"] + [f"dPhi_dw_ma{int(ma)}keV_cm2_s_keV" for ma in MASSES_KEV]
    writer.writerow(header)

    # One row per energy point
    for i, w in enumerate(omega):
        row = [f"{w:.4f}"] + [f"{fluxes[ma][i]:.6e}" for ma in MASSES_KEV]
        writer.writerow(row)

print(f"[OK] Flux table written to: {csv_path}")

# Print a short preview of the table (every 50th row)
print()
print(f"{'omega [keV]':>12}  " +
      "  ".join(f"{'dΦ/dω (ma='+str(int(ma))+'keV) [cm⁻²s⁻¹keV⁻¹]':>30}" for ma in MASSES_KEV))
print("-" * 110)
for i in range(0, N_POINTS, N_POINTS // 20):
    w = omega[i]
    cols = "  ".join(f"{fluxes[ma][i]:>30.4e}" for ma in MASSES_KEV)
    print(f"{w:>12.3f}  {cols}")


# ─────────────────────────────────────────────────────────────────────────────
# Plot dΦ/dω vs ω for each mass
# ─────────────────────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(9, 6))

# Colour and style choices for the three masses
styles = {
    0.0:   {"color": "steelblue",  "ls": "-",  "label": r"$m_a = 0$ keV (massless)"},
    10.0:  {"color": "darkorange", "ls": "--", "label": r"$m_a = 10$ keV"},
    130.0: {"color": "crimson",    "ls": ":",  "label": r"$m_a = 130$ keV (essentially zero)"},
}

for ma, style in styles.items():
    ax.plot(omega, fluxes[ma],
            color=style["color"],
            linestyle=style["ls"],
            linewidth=2,
            label=style["label"])

    # Mark the kinematic threshold with a vertical dashed line (if within plot range)
    if 0.0 < ma <= OMEGA_MAX:
        ax.axvline(x=ma, color=style["color"], linestyle=":", alpha=0.5, linewidth=1)
        ax.text(ma + 0.1, ax.get_ylim()[1] * 0.5,
                f"threshold\n$\\omega = m_a$\n= {ma} keV",
                color=style["color"], fontsize=8, va="top")

# Axis labels and formatting
ax.set_xlabel(r"Axion energy $\omega$ [keV]", fontsize=13)
ax.set_ylabel(r"$d\Phi/d\omega$ [cm$^{-2}$ s$^{-1}$ keV$^{-1}$]", fontsize=13)
ax.set_title(
    "Solar Primakoff Axion Flux  (Giannotti parametric fit)\n"
    r"$g_{a\gamma} = 10^{-10}$ GeV$^{-1}$",
    fontsize=13
)
ax.legend(fontsize=11)
ax.set_xlim(OMEGA_MIN, OMEGA_MAX)
ax.set_ylim(bottom=0)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plot_path = os.path.join(os.path.dirname(__file__), "axion_flux_plot.png")
plt.savefig(plot_path, dpi=150)
print(f"\n[OK] Plot saved to: {plot_path}")
plt.show()
