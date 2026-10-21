"""Calculate and visualize a normalized electric field from point charges.

The original assignment defines the Coulomb constant as ``k = 1``. Charge
values, distances, and electric-field results are therefore expressed in
assignment-defined normalized units rather than SI units.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import hypot, isfinite

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


NORMALIZED_COULOMB_CONSTANT: float = 1.0
FIELD_ARROW_LENGTH: float = 2.0

Vector = tuple[float, float]


@dataclass(frozen=True, slots=True)
class Point:
    """Represent a point in the two-dimensional coordinate plane."""

    x: float
    y: float

    def is_within(self, coordinate_min: int, coordinate_max: int) -> bool:
        """Return whether the point lies inside the inclusive square grid."""

        return (
            coordinate_min <= self.x <= coordinate_max
            and coordinate_min <= self.y <= coordinate_max
        )


@dataclass(frozen=True, slots=True)
class Charge:
    """Represent an ideal point charge in normalized assignment units."""

    x: float
    y: float
    q: float


def electric_field(
    charge: Charge,
    field_point: Point,
    *,
    coulomb_constant: float = NORMALIZED_COULOMB_CONSTANT,
) -> Vector:
    """Return one point charge's electric-field vector at ``field_point``.

    The displacement vector points from the source charge to the field point.
    A positive charge therefore produces a field pointing away from the source,
    while a negative charge produces a field pointing toward it.

    Raises:
        ValueError: If an input is non-finite, the normalized Coulomb constant
            is not positive, or the field point coincides with the charge.
    """

    values = {
        "charge.x": charge.x,
        "charge.y": charge.y,
        "charge.q": charge.q,
        "field_point.x": field_point.x,
        "field_point.y": field_point.y,
        "coulomb_constant": coulomb_constant,
    }
    for name, value in values.items():
        if not isfinite(value):
            raise ValueError(f"{name} must be finite.")

    if coulomb_constant <= 0.0:
        raise ValueError("coulomb_constant must be greater than zero.")

    displacement_x = field_point.x - charge.x
    displacement_y = field_point.y - charge.y
    distance = hypot(displacement_x, displacement_y)

    if distance == 0.0:
        raise ValueError("The field point cannot coincide with a point charge.")

    scale = coulomb_constant * charge.q / (distance * distance * distance)
    return scale * displacement_x, scale * displacement_y


def total_electric_field(
    charges: Sequence[Charge],
    field_point: Point,
    *,
    coulomb_constant: float = NORMALIZED_COULOMB_CONSTANT,
) -> Vector:
    """Return the vector sum of all charge contributions at ``field_point``."""

    total_x = 0.0
    total_y = 0.0

    for charge in charges:
        field_x, field_y = electric_field(
            charge,
            field_point,
            coulomb_constant=coulomb_constant,
        )
        total_x += field_x
        total_y += field_y

    return total_x, total_y


def generate_random_charges(
    count: int,
    control_point: Point,
    coordinate_min: int,
    coordinate_max: int,
    charge_min: int,
    charge_max: int,
    *,
    rng: np.random.Generator | None = None,
) -> list[Charge]:
    """Generate nonzero charges at unique grid positions.

    Supplying a seeded NumPy generator makes the result deterministic for tests
    or reproducible examples.

    Raises:
        ValueError: If a range is invalid, the control point is outside the
            grid, no nonzero charge value is available, or ``count`` cannot be
            placed on the available positions.
    """

    if coordinate_min > coordinate_max:
        raise ValueError("coordinate_min cannot be greater than coordinate_max.")

    if not control_point.is_within(coordinate_min, coordinate_max):
        raise ValueError("The control point must lie inside the coordinate grid.")

    if count <= 0:
        raise ValueError("count must be a positive integer.")

    if charge_min > charge_max:
        raise ValueError("charge_min cannot be greater than charge_max.")

    charge_values = [
        charge_value
        for charge_value in range(charge_min, charge_max + 1)
        if charge_value != 0
    ]
    if not charge_values:
        raise ValueError("The charge range must contain a nonzero integer.")

    available_positions = [
        (x, y)
        for x in range(coordinate_min, coordinate_max + 1)
        for y in range(coordinate_min, coordinate_max + 1)
        if (x, y) != (control_point.x, control_point.y)
    ]

    if count > len(available_positions):
        raise ValueError(
            "Too many charges for the available unique grid positions: "
            f"requested {count}, maximum {len(available_positions)}."
        )

    generator = rng if rng is not None else np.random.default_rng()
    position_indices = generator.choice(
        len(available_positions),
        size=count,
        replace=False,
    )
    generated_values = generator.choice(charge_values, size=count, replace=True)

    return [
        Charge(
            x=available_positions[int(position_index)][0],
            y=available_positions[int(position_index)][1],
            q=int(charge_value),
        )
        for position_index, charge_value in zip(
            position_indices,
            generated_values,
            strict=True,
        )
    ]


def normalize_field_for_plot(
    field: Vector,
    *,
    arrow_length: float = FIELD_ARROW_LENGTH,
) -> Vector:
    """Scale a field vector to a fixed plotting length while preserving direction."""

    if not isfinite(arrow_length) or arrow_length <= 0.0:
        raise ValueError("arrow_length must be a positive finite number.")

    field_x, field_y = field
    magnitude = hypot(field_x, field_y)
    if magnitude == 0.0:
        return 0.0, 0.0

    scale = arrow_length / magnitude
    return field_x * scale, field_y * scale


def plot_configuration(
    control_point: Point,
    charges: Sequence[Charge],
    total_field: Vector,
    coordinate_min: int,
    coordinate_max: int,
    *,
    show: bool = True,
) -> Figure:
    """Plot the charges, control point, and normalized total-field direction."""

    if coordinate_min > coordinate_max:
        raise ValueError("coordinate_min cannot be greater than coordinate_max.")

    figure, axis = plt.subplots(figsize=(8, 8))

    positive_charges = [charge for charge in charges if charge.q > 0]
    negative_charges = [charge for charge in charges if charge.q < 0]

    if positive_charges:
        axis.scatter(
            [charge.x for charge in positive_charges],
            [charge.y for charge in positive_charges],
            color="tab:red",
            label="Positive charge",
            zorder=3,
        )

    if negative_charges:
        axis.scatter(
            [charge.x for charge in negative_charges],
            [charge.y for charge in negative_charges],
            color="tab:blue",
            label="Negative charge",
            zorder=3,
        )

    for charge in charges:
        axis.annotate(
            f"{charge.q:+g}",
            (charge.x, charge.y),
            xytext=(6, 6),
            textcoords="offset points",
        )

    axis.scatter(
        [control_point.x],
        [control_point.y],
        color="black",
        marker="x",
        s=70,
        linewidths=2.0,
        label="Control point P",
        zorder=4,
    )

    arrow_x, arrow_y = normalize_field_for_plot(total_field)
    if arrow_x != 0.0 or arrow_y != 0.0:
        axis.quiver(
            control_point.x,
            control_point.y,
            arrow_x,
            arrow_y,
            angles="xy",
            scale_units="xy",
            scale=1,
            color="tab:green",
            width=0.007,
            label="Normalized field direction",
            zorder=2,
        )
    else:
        axis.annotate(
            "Resultant field is zero",
            (control_point.x, control_point.y),
            xytext=(8, -18),
            textcoords="offset points",
            color="tab:green",
        )

    margin = 1.0
    axis.set_xlim(coordinate_min - margin, coordinate_max + margin)
    axis.set_ylim(coordinate_min - margin, coordinate_max + margin)
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlabel("x [normalized distance]")
    axis.set_ylabel("y [normalized distance]")
    axis.set_title(
        "Electric field at control point P\n"
        "Arrow length is normalized and does not represent field magnitude"
    )
    axis.grid(True, alpha=0.4)
    axis.legend(loc="best")
    figure.tight_layout()

    if show:
        plt.show()

    return figure


def read_interactive_configuration() -> tuple[Point, list[Charge], int, int]:
    """Read and validate one random-charge configuration from standard input."""

    grid_radius = int(
        input("Enter maximum coordinate range (from center to each side): ")
    )
    if grid_radius < 1:
        raise ValueError("The maximum coordinate range must be at least 1.")

    coordinate_min = -grid_radius
    coordinate_max = grid_radius

    control_point = Point(
        x=int(input("Enter x coordinate of the control point: ")),
        y=int(input("Enter y coordinate of the control point: ")),
    )
    if not control_point.is_within(coordinate_min, coordinate_max):
        raise ValueError("The control point must lie inside the coordinate grid.")

    maximum_count = (2 * grid_radius + 1) ** 2 - 1
    count = int(input(f"Enter number of charges (max: {maximum_count}): "))
    charge_min = int(input("Enter minimum charge value: "))
    charge_max = int(input("Enter maximum charge value: "))

    charges = generate_random_charges(
        count,
        control_point,
        coordinate_min,
        coordinate_max,
        charge_min,
        charge_max,
    )
    return control_point, charges, coordinate_min, coordinate_max


def print_field_report(charges: Sequence[Charge], control_point: Point) -> Vector:
    """Print individual contributions and return the total normalized field."""

    for charge in charges:
        field_x, field_y = electric_field(charge, control_point)
        magnitude = hypot(field_x, field_y)
        print(
            f"{charge}: E_x = {field_x:.6f}, E_y = {field_y:.6f}, "
            f"|E| = {magnitude:.6f}"
        )

    total_field = total_electric_field(charges, control_point)
    total_magnitude = hypot(*total_field)
    print(
        "\nRESULT IN NORMALIZED ASSIGNMENT UNITS: "
        f"E_x = {total_field[0]:.6f}, E_y = {total_field[1]:.6f}, "
        f"|E| = {total_magnitude:.6f}\n"
        "The plotted arrow shows direction only; its length is normalized."
    )
    return total_field


def main() -> int:
    """Run the interactive command-line application."""

    try:
        control_point, charges, coordinate_min, coordinate_max = (
            read_interactive_configuration()
        )
    except (EOFError, ValueError) as error:
        print(f"Input error: {error}")
        return 1

    print(f"\n{control_point}")
    for charge in charges:
        print(charge)

    total_field = print_field_report(charges, control_point)
    plot_configuration(
        control_point,
        charges,
        total_field,
        coordinate_min,
        coordinate_max,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
