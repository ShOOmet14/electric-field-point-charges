from math import hypot

import numpy as np
import pytest

from charges import (
    Charge,
    Point,
    electric_field,
    generate_random_charges,
    normalize_field_for_plot,
    total_electric_field,
)


def test_positive_charge_field_points_away_from_source() -> None:
    field = electric_field(Charge(0.0, 0.0, 2.0), Point(2.0, 0.0))

    assert field == pytest.approx((0.5, 0.0))


def test_negative_charge_field_points_toward_source() -> None:
    field = electric_field(Charge(0.0, 0.0, -2.0), Point(2.0, 0.0))

    assert field == pytest.approx((-0.5, 0.0))


def test_field_magnitude_obeys_inverse_square_law() -> None:
    charge = Charge(0.0, 0.0, 1.0)

    near_magnitude = hypot(*electric_field(charge, Point(1.0, 0.0)))
    far_magnitude = hypot(*electric_field(charge, Point(2.0, 0.0)))

    assert far_magnitude == pytest.approx(near_magnitude / 4.0)


def test_superposition_adds_vector_components() -> None:
    charges = [
        Charge(-1.0, 0.0, 1.0),
        Charge(0.0, -1.0, 1.0),
    ]

    assert total_electric_field(charges, Point(0.0, 0.0)) == pytest.approx(
        (1.0, 1.0)
    )


def test_symmetric_charges_cancel_horizontal_component() -> None:
    charges = [
        Charge(-1.0, 0.0, 1.0),
        Charge(1.0, 0.0, 1.0),
    ]

    field_x, field_y = total_electric_field(charges, Point(0.0, 2.0))

    assert field_x == pytest.approx(0.0, abs=1.0e-15)
    assert field_y > 0.0


def test_equal_symmetric_charges_cancel_completely_at_midpoint() -> None:
    charges = [
        Charge(-1.0, 0.0, 1.0),
        Charge(1.0, 0.0, 1.0),
    ]

    assert total_electric_field(charges, Point(0.0, 0.0)) == pytest.approx(
        (0.0, 0.0),
        abs=1.0e-15,
    )


def test_zero_distance_is_rejected() -> None:
    with pytest.raises(ValueError, match="cannot coincide"):
        electric_field(Charge(1.0, -2.0, 3.0), Point(1.0, -2.0))


def test_custom_coulomb_constant_scales_field() -> None:
    charge = Charge(0.0, 0.0, 1.0)
    point = Point(1.0, 0.0)

    normalized = electric_field(charge, point)
    scaled = electric_field(charge, point, coulomb_constant=3.5)

    assert scaled == pytest.approx(tuple(3.5 * component for component in normalized))


@pytest.mark.parametrize("bad_constant", [0.0, -1.0, np.inf, np.nan])
def test_invalid_coulomb_constant_is_rejected(bad_constant: float) -> None:
    with pytest.raises(ValueError, match="coulomb_constant"):
        electric_field(
            Charge(0.0, 0.0, 1.0),
            Point(1.0, 0.0),
            coulomb_constant=bad_constant,
        )


def test_random_generation_is_deterministic_unique_and_excludes_invalid_values(
) -> None:
    control_point = Point(0.0, 0.0)

    first = generate_random_charges(
        12,
        control_point,
        -2,
        2,
        -3,
        3,
        rng=np.random.default_rng(2026),
    )
    second = generate_random_charges(
        12,
        control_point,
        -2,
        2,
        -3,
        3,
        rng=np.random.default_rng(2026),
    )

    positions = {(charge.x, charge.y) for charge in first}
    assert first == second
    assert len(positions) == len(first)
    assert (control_point.x, control_point.y) not in positions
    assert all(charge.q != 0 for charge in first)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"count": 0}, "positive integer"),
        ({"coordinate_min": 2, "coordinate_max": -2}, "coordinate_min"),
        ({"charge_min": 2, "charge_max": -2}, "charge_min"),
        ({"charge_min": 0, "charge_max": 0}, "nonzero integer"),
        ({"count": 9, "coordinate_min": -1, "coordinate_max": 1}, "Too many"),
    ],
)
def test_random_generation_rejects_invalid_configuration(
    kwargs: dict[str, int],
    message: str,
) -> None:
    arguments = {
        "count": 1,
        "coordinate_min": -1,
        "coordinate_max": 1,
        "charge_min": -1,
        "charge_max": 1,
    }
    arguments.update(kwargs)

    with pytest.raises(ValueError, match=message):
        generate_random_charges(
            control_point=Point(0.0, 0.0),
            rng=np.random.default_rng(1),
            **arguments,
        )


def test_random_generation_rejects_control_point_outside_grid() -> None:
    with pytest.raises(ValueError, match="control point"):
        generate_random_charges(
            1,
            Point(2.0, 0.0),
            -1,
            1,
            -1,
            1,
        )


def test_normalized_plot_vector_preserves_direction_and_uses_fixed_length() -> None:
    normalized = normalize_field_for_plot((3.0, 4.0), arrow_length=2.0)

    assert normalized == pytest.approx((1.2, 1.6))
    assert hypot(*normalized) == pytest.approx(2.0)
    assert normalize_field_for_plot((0.0, 0.0)) == (0.0, 0.0)
