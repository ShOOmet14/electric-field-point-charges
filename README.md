# Electric Field - Point Charges

This project simulates the **electric field vector** **E** at a chosen control point **P**, produced by multiple **point charges** randomly placed on a 2D grid.

The program:

- generates **unique** charge positions (no duplicates),
- prevents placing any charge at the control point coordinates,
- computes the electric field using the **superposition principle**,
- visualizes charges, the control point, and the **electric field vector** on a plot.

---

## Screenshots

### Example plot 1

<img src="Figures/Figure_1.png" alt="Example plot 1" width="800"/>

### Example plot 2

<img src="Figures/Figure_2.png" alt="Example plot 2" width="800"/>

### Console output example

<img src="Figures/Figure_3.png" alt="Console output example" width="900"/>

---

## Project structure

- `charges.py` — **English version** (main script)
- `ladunki.py` — **Polish version** (original script kept for reference)
- `figures/` — screenshots and equation images used in this README

---

## Equations used in the project

### Electric field from a single point charge

<img src="Figures/equation.jpg" alt="Electric field from single charge" width="260"/>

### Position vector from the charge to the control point

<img src="Figures/equation1.jpg" alt="Position vector" width="260"/>

### Constant used in the assignment

According to the assignment requirement:

<img src="Figures/equation2.jpg" alt="k constant" width="260"/>

In the code we use: **k = 1**

### Distance between charge and control point

<img src="Figures/equation3.jpg" alt="Distance r" width="220"/>

---

## Features

- Random generation of **N unique** point charges on a 2D grid
- Charges never appear at the control point `(xP, yP)`
- Charge values are random integers in range `[q_min, q_max]` excluding `0`
- Visualization with Matplotlib:
  - `q > 0` → blue
  - `q < 0` → red
  - control point `P` → green
  - electric field vector at `P` → green arrow (**scaled for visibility**)

---

## Requirements

- Python 3
- NumPy
- Matplotlib

Install dependencies:

```bash
pip install numpy matplotlib
```
