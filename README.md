# Electric Field - Point Charges

This project simulates the **electric field vector** **E** at a chosen control point **P**, produced by multiple **point charges** randomly placed on a 2D grid.

The program:

- generates **unique** charge positions (no duplicates),
- prevents placing any charge at the control point coordinates,
- computes the electric field using **superposition**,
- visualizes charges, the control point, and the **electric field vector** on a plot.

---

## Project files

- `charges.py` — **English version** (main script)
- `ladunki.py` — **Polish version** (original script kept for reference)
- `Figure_1.png` — example plot (charges + control point + electric field vector)
- `Figure_2.png` — example plot (different random configuration)
- `Figure_3.png` — example console output
- `README.md` — project description
- `.gitignore` — ignored files list

---

## Electric Field Formula

The electric field at point **P** is computed using superposition:

![equation](https://latex.codecogs.com/svg.image?\vec{E}=\sum_i%20q_i\frac{\vec{r_i}}{|\vec{r_i}|^3})

where:

- **r** = (xP − xi, yP − yi)
- **|r|** = sqrt((xP − xi)² + (yP − yi)²)

According to the assignment requirement:

**1 / (4π ε₀) = 1**, so the constant **k = 1**.

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
