DC Permanent Magnet Motor Electromagnetic Calculation Program
This program is designed for the electromagnetic design and analysis of DC permanent magnet motors. It calculates key performance metrics, material selections, and operating characteristics under various load conditions and special operating scenarios. The program features a graphical user interface (GUI) built with Python, utilizing tkinter, numpy, and scipy for user input and result visualization.

Note: The program interface and comments are currently in Chinese to support its initial use by a Chinese company. An English version is planned for future updates.

Table of Contents

Symbol Conventions
Assumptions and Empirical Coefficients
Variable Naming Clarifications
Material and Slot Type Definitions
Special Operating Scenarios
Input Data Handling
Array Definitions
Subroutine Descriptions
Dependencies
Future Updates

Symbol Conventions
The program uses specific symbol mappings to align with computational notation, replacing special characters from handwritten calculations. Below is a list of single-character replacements:



Handwritten Symbol
Program Symbol
Description



*
BN
Multiplication or placeholder


'
1
Prime or index


μ
MU
Magnetic permeability


δ
g
Air gap


α
ALFA
Angle or coefficient


σ
SIGMA
Conductivity or coefficient


τ
TAO
Pole pitch


θ
SITA
Angle


Φ
FI
Magnetic flux


Λ
NUMDA
Permeance coefficient


ρ
ROU
Resistivity


Σ
SUM
Summation


β
BETA
Angle or coefficient


Δ
DELT
Difference or change


η
eff
Efficiency


Note: For combined symbols (e.g., ΔU_b → DELTUb), the order remains consistent with handwritten notation. Only single-character replacements are listed above.
Assumptions and Empirical Coefficients
The program uses the following assumptions and empirical coefficients for determining primary dimensions:

Assumed Data:

P' = PJS (Calculated power)
B'_δ/B_R = XSBGR (Air gap flux density to remanence ratio)
H_M/δ = XSHMG (Magnet thickness to air gap ratio)
L_M/L_A = XSLMA (Magnet length to armature length ratio)
L_J/L_A = XSLJA (Frame length to armature length ratio)


Empirical Coefficients:

λ_E calculation coefficient: XSDB
P_Fe (iron loss) calculation coefficient: XSTH



Variable Naming Clarifications
To avoid ambiguity, the following variables are distinguished in the program:



Handwritten Variable
Program Variable
Description



A
A / AX
Parameter A / Armature reaction


D_0
D0 / DJ
Core inner diameter / Stator outer diameter


H_T2
ht / H2J
Slot height / Armature yoke height


B_T2
Vbt2
Average tooth flux density


H_J2
H2J
Armature yoke magnetic field strength


P_B
NPB
Number of brush pairs


A_MAX
AXMAX
Maximum armature reaction


N
RPM
Rotational speed


T
TEMP
Temperature


P_s
PBP
Brush pressure per unit area


For rectangular slots:

Narrow side length: ABX
Wide side length: BBX

Material and Slot Type Definitions
The program supports the following material and slot type options:

Permanent Magnet Material (YCCL):

1: NdFeB
2: Ferrite


Frame Material (JZCL):

1: Cast Steel
2: Cast Iron


Winding Material (RZCL):

1: Brass
2: Copper


Insulation Class (INSC):

1: A
2: E
3: B
4: F
5: H


Armature Material (DSCL):

1: DR510-50
2: DR420-50
3: DR490-50
4: DR550-50
5: DW315-50


Slot Type (CX):

1: Pear-shaped slot
2: Semi-pear-shaped slot
3: Circular slot
4: Slanted circular slot



Special Operating Scenarios
The program supports analysis under the following special operating scenarios, controlled by checkboxes in the GUI:



Scenario
Variable
Value
Description



Sudden Start
TSGK1
1/0
Enabled (1) / Disabled (0)


Instantaneous Stall
TSGK2
1/0
Enabled (1) / Disabled (0)


Sudden Stop
TSGK3
1/0
Enabled (1) / Disabled (0)


Sudden Reversal
TSGK4
1/0
Enabled (1) / Disabled (0)


Input Data Handling
Descriptive strings in the input data file are assigned to the variable TERM and are not used in calculations.
Array Definitions
The program uses arrays to store discrete data points for magnetization and loss curves, as well as other parameters. Below is a summary:



Array Name
Size
Description
Correspondence



HW10
150
H values for DW315-50 magnetization curve
HW10 ↔ BW10


BW10
150
B values for DW315-50 magnetization curve
HW10 ↔ BW10, PW10 ↔ BW10


PW10
150
P values for DW315-50 loss curve
PW10 ↔ BW10


BD21
150
B values for DR550-50 magnetization curve
HD21 ↔ BD21, PD21 ↔ BPD21


HD21
150
H values for DR550-50 magnetization curve
HD21 ↔ BD21


PD21
150
P values for DR550-50 loss curve
PD21 ↔ BPD21


BPD21
150
B values for DR550-50 loss curve
PD21 ↔ BPD21


BD23
150
B values for DR510-50 magnetization curve
HD23 ↔ BD23, PD234 ↔ BD234


HD23
150
H values for DR510-50 magnetization curve
HD23 ↔ BD23


BD24
150
B values for DR490-50 magnetization curve
HD24 ↔ BD24, PD234 ↔ BD234


HD24
150
H values for DR490-50 magnetization curve
HD24 ↔ BD24


PD234
150
P values for DR510-50 and DR490-50 loss curves
PD234 ↔ BD234


BD234
150
B values for DR510-50 and DR490-50 loss curves
PD234 ↔ BD234


BD25
21
B values for DR420-50 magnetization curve
HD25 ↔ BD25, PD25 ↔ BPD25


HD25
21
H values for DR420-50 magnetization curve
HD25 ↔ BD25


PD25
22
P values for DR420-50 loss curve
PD25 ↔ BPD25


BPD25
22
B values for DR420-50 loss curve
PD25 ↔ BPD25


BZG
160
B values for cast steel magnetization curve
HZG ↔ BZG


HZG
160
H values for cast steel magnetization curve
HZG ↔ BZG


BZT
77
B values for cast iron magnetization curve
HZT ↔ BZT


HZT
77
H values for cast iron magnetization curve
HZT ↔ BZT


DLX
45
Nominal diameters of enameled round copper wires
-


SZDLMB
12
ΔLm* values for ΔLa* curve
SZDLAB ↔ SZGAP, SZDLMB, SZHMG


SZHMG
3
hm/δ values for ΔLa* curve
SZDLAB ↔ SZGAP, SZDLMB, SZHMG


SZGAP
4
Gap values for ΔLa* curve
SZDLAB ↔ SZGAP, SZDLMB, SZHMG


SZDLAB
144
ΔLa* values for ΔLa* curve
SZDLAB ↔ SZGAP, SZDLMB, SZHMG


Subroutine Descriptions
The program includes several subroutines for interpolation and slot leakage calculations:



Subroutine
Function
Parameters
Notes



LAG
Lagrange Linear Interpolation
K: Number of discrete pointsX: Independent variable interpolation pointXX0: Independent variable arrayYY0: Function value arrayY: Interpolated function value
Core interpolation routine


YYCZ
Univariate Linear Interpolation
M: Number of discrete pointsX: Independent variable interpolation pointXX: Independent variable arrayYY: Function value arrayXLAG: Interpolated function value
Calls LAG


EYCZ
Bivariate Linear Interpolation
M: Number of first variable pointsN: Number of second variable pointsX1: First variable interpolation pointX2: Second variable interpolation pointXX1: First variable arrayXX2: Second variable arrayYY: Function value arrayXLAG: Interpolated function valueYY1, YY2, YY3: Intermediate arrays
Calls LAG


SYCZ
Trivariate Linear Interpolation
L: Number of first variable pointsM: Number of second variable pointsN: Number of third variable pointsX1: First variable interpolation pointX2: Second variable interpolation pointX3: Third variable interpolation pointXX1: First variable arrayXX2: Second variable arrayXX3: Third variable arrayYY: Function value arrayXLAG: Interpolated function valueYY1, YY2, YY3: Intermediate arrays
Calls LAG


CLCD
Slot Leakage Permeance Calculation
CX: Slot type codebo2: Slot opening widthho2: Slot opening heightd1: Slot upper widthh2: Slot upper heightd2: Slot lower widthh22: Slot lower heightLUMDAS: Slot leakage permeance
-


XXG
Round Conductor Auto-Selection
DLX: Standard wire gauge arrayS: Conductor cross-sectional aread: Selected nominal wire diameterN: Number of parallel wires
-


Dependencies

Python 3.x
Libraries:
tkinter (for GUI)
numpy (for numerical computations)
scipy (for interpolation)



Install dependencies using:
pip install numpy scipy

Future Updates

Translate the program interface and comments to English for broader accessibility.
Add support for additional motor types and configurations.
Enhance error handling and input validation in the GUI.
Include export functionality for calculation results (e.g., CSV, PDF).

For issues or contributions, please contact the project maintainer.
