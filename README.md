# Electric Field - Point Charges

This project simulates the **electric field vector** **E** at a chosen control point **P**, produced by multiple **point charges** randomly placed on a 2D grid.

The program:
- generates **unique** charge positions (no duplicates),
- prevents placing any charge at the control point coordinates,
- computes the electric field using **superposition**,
- visualizes charges, the control point, and the **electric field vector** on a plot.

According to the assignment requirement:

\[
\frac{1}{4\pi\epsilon_0} = 1
\]

---

## Project files

- `charges.py` — **English version** (main script)
- `ladunki.py` — **Polish version** (original script, kept for reference)
- `Figure_1.png` — example plot (charges + control point + electric field vector)
- `Figure_2.png` — example plot (different random configuration)
- `Figure_3.png` — example console output

---

## Features

- Random generation of **N unique** point charges on a 2D grid
- Charges never appear at the control point `(xP, yP)`
- Charge values are random integers in range `[q_min, q_max]` excluding `0`
- Electric field calculation:

\[
\vec{E} = \sum_i q_i \frac{\vec{r_i}}{|\vec{r_i}|^3}
\]

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
