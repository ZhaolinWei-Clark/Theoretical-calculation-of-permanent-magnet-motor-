# Electromagnetic Calculation Program for DC Permanent Magnet Motors

## Overview

This software is designed for the electromagnetic design and performance analysis of DC permanent magnet motors. It allows users to compute and simulate key parameters under various working conditions. The program incorporates interpolation subroutines, predefined material data, and motor design assumptions.

---

## Table 1: Special Character Mapping in the Program

In the transition from manual calculations to Python programming, several characters are replaced for compatibility:

| Manual Symbol | Python Symbol |
|---------------|----------------|
| *             | BN             |
| ‘-1           | -1             |
| μ             | MU             |
| δ             | G              |
| α             | ALFA           |
| σ             | SIGMA          |
| τ             | TAO            |
| θ             | SITA           |
| Φ             | FI             |
| Λ             | NUMDA          |
| ρ             | ROU            |
| Σ             | SUM            |
| β             | BETA           |
| Δ             | DELT           |
| η             | EFF            |

**Note**: The replacement applies to individual characters. When characters are part of combined expressions (e.g., `ΔU_b`), the sequence remains unchanged, and the combination becomes `DELTUb`.

---

## Assumed Parameters for Motor Sizing

- `P' = PJS`
- `B'_δ / B_R = XSBGR`
- `H_M / δ = XSHMG`
- `L_M / L_A = XSLMA`
- `L_J / L_A = XSLJA`

### Empirical Coefficients

- Coefficient for λ_E formula: `XSDB`
- Coefficient for iron loss \( P_{Fe} \): `XSTH`

### Variable Renaming Notes

To avoid variable naming conflicts (case-insensitive), some variables are renamed:

| Original Name     | Program Variable |
|-------------------|------------------|
| A                 | AX               |
| D₀                | DJ               |
| H_(T2)            | HT               |
| B_(T2)            | V_BT2            |
| H_(J2)            | H2J              |
| Brush Pair Count  | NPB              |
| A_MAX             | AXMAX            |
| N (Speed)         | RPM              |
| T (Temperature)   | TEMP             |
| Brush Pressure    | PBP              |

### Slot Geometry and Material Codes

- **Flat wire narrow side**: `ABX`
- **Flat wire wide side**: `BBX`

#### Material Codes

- **Permanent Magnet (YCCL)**:
  - `1`: NdFeB
  - `2`: Ferrite

- **Housing Material (JZCL)**:
  - `1`: Cast Steel
  - `2`: Cast Iron

- **Winding Material (RZCL)**:
  - `1`: Brass
  - `2`: Copper

- **Insulation Class (INSC)**:
  - `1`: A
  - `2`: E
  - `3`: B
  - `4`: F
  - `5`: H

- **Armature Material (DSCL)**:
  - `1`: DR510-50
  - `2`: DR420-50
  - `3`: DR490-50
  - `4`: DR550-50
  - `5`: DW315-50

- **Slot Type (CX)**:
  - `1`: Pear-shaped
  - `2`: Semi-pear-shaped
  - `3`: Circular
  - `4`: Slanted shoulder circular

---

## Special Working Conditions

- **Sudden Start**: `TSGK1`
- **Instantaneous Locked Rotor**: `TSGK2` (1: Enabled, 0: Disabled)
- **Sudden Stop**: `TSGK3`
- **Sudden Reversal**: `TSGK4`

> Descriptive strings in input files are stored in the `TERM` variable and are ignored in calculations.

---

## Table 2: Array Descriptions

### Example Material Curve Arrays

| Array Name | Description |
|------------|-------------|
| `HW10(150)` | H values for DW315-50 |
| `BW10(150)` | B values for DW315-50 |
| `PW10(150)` | Loss (p) values for DW315-50 |
| `BD21`, `HD21`, `PD21`, `BPD21` | Magnetic & loss curves for DR550-50 |
| `BD23`, `HD23` | DR510-50 Magnetization |
| `BD24`, `HD24` | DR490-50 Magnetization |
| `PD234`, `BD234` | Loss curves for DR510-50/DR490-50 |
| `BD25`, `HD25`, `PD25`, `BPD25` | DR420-50 Magnetization and Loss |
| `BZG`, `HZG` | Cast Steel Magnetization |
| `BZT`, `HZT` | Cast Iron Magnetization |
| `DLX(45)` | Nominal diameters for enameled copper wire |
| `SZDLMB`, `SZHMG`, `SZGAP`, `SZDLAB` | Data for ΔLa* curve calculations |

---

## Table 3: Subroutine Descriptions

| Subroutine | Purpose | Parameters | Notes |
|------------|---------|------------|-------|
| `LAG` | Lagrange Linear Interpolation | `K`, `X`, `XXO`, `YYO`, `Y` | Base function for interpolation |
| `YYCZ` | 1D Linear Interpolation | `M`, `X`, `XX`, `YY`, `XLAG` | Uses `LAG` |
| `EYCZ` | 2D Linear Interpolation | `M`, `N`, `X1`, `X2`, `XX1`, `XX2`, `YY`, `XLAG`, `YY1–3` | Uses `LAG` |
| `SYCZ` | 3D Linear Interpolation | `L`, `M`, `N`, `X1–3`, `XX1–3`, `YY`, `XLAG`, `YY1–3` | Uses `LAG` |
| `CLCD` | Slot Leakage Permeance Calculation | `CX`, `bo2`, `ho2`, `d1`, `h2`, `d2`, `h22`, `LUMDAS` | |
| `XXG` | Auto Gauge Selection for Round Wire | `DLX`, `S`, `d`, `N` | Computes nominal wire diameter |

---

## Notes

- This version of the program uses Chinese for variable and interface descriptions, designed for use by Chinese companies.
- An English version will be released in the future.
