import numpy as np
import matplotlib.pyplot as plt

# Global constant (according to the assignment: 1/(4*pi*epsilon0) = 1).
# You can uncomment the real values for vacuum if you want.
# epsilon = 8.854e-12
# pi = np.pi
# k = 1 / (4 * pi * epsilon)

k = 1


# Charge object:
# Stores x, y coordinates and charge value q.
# Includes:
# - method for printing parameters
# - method for drawing a non-zero charge value
# - method for generating charges using all available unique grid positions
#   (each position can be used only once, and the control point position is forbidden)
class Charge:
    def __init__(self, x, y, q):
        self.x = x
        self.y = y
        self.q = q

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name} (x = {self.x}, y = {self.y}, q = {self.q})"

    @staticmethod
    def draw_charge_value(rng, q_min, q_max):
        q = 0
        while q == 0:
            q = int(rng.integers(q_min, q_max + 1))
        return q

    @classmethod
    def draw(cls, count, rng, coord_min, coord_max, q_min, q_max, control_point):
        possible_coordinates = [
            (x, y)
            for x in range(coord_min, coord_max + 1)
            for y in range(coord_min, coord_max + 1)
            if (x, y) != (control_point.x, control_point.y)
        ]

        if count > len(possible_coordinates):
            raise ValueError(
                f"Too many charges! The maximum number of unique charges for your grid is {len(possible_coordinates)}."
            )

        indices = rng.choice(len(possible_coordinates), size=count, replace=False)

        charges = []
        for i in indices:
            x, y = possible_coordinates[i]
            q = cls.draw_charge_value(rng, q_min, q_max)
            charges.append(cls(x, y, q))

        return charges


# Point object:
# Stores x and y coordinates.
# Includes:
# - method for printing parameters
# - method for checking coordinate validity (inside grid limits)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name} (x = {self.x}, y = {self.y})"

    def check(self, coord_min, coord_max):
        return coord_min <= self.x <= coord_max and coord_min <= self.y <= coord_max


# Function that generates charges (their coordinates and values) and allows choosing a control point
def generate_charges():
    # Reading coordinate limits and control point coordinates
    coord_max = int(input("Enter maximum coordinate range (from center to each side): "))
    coord_min = -coord_max

    x_point = int(input("Enter x coordinate of the control point: "))
    y_point = int(input("Enter y coordinate of the control point: "))

    control_point = Point(x_point, y_point)

    if not control_point.check(coord_min, coord_max):
        print("Control point coordinates are out of range.")
        return None

    print(repr(control_point))

    # Reading number of charges and charge value range
    max_count = (2 * coord_max + 1) ** 2 - 1
    count = int(input(f"Enter number of charges (max: {max_count}): "))

    if count <= 0:
        print("The number of charges must be a positive integer.")
        return None

    if count > max_count:
        print(f"Too many charges! Maximum allowed: {max_count}.")
        return None

    q_min = int(input("Enter minimum charge value: "))
    q_max = int(input("Enter maximum charge value: "))

    if q_min > q_max:
        print("Minimum value cannot be greater than maximum value.")
        return None

    if q_min == 0 and q_max == 0:
        print("You cannot draw only zero. Please choose a different range.")
        return None

    rng = np.random.default_rng()

    charges = Charge.draw(count, rng, coord_min, coord_max, q_min, q_max, control_point)

    for ch in charges:
        print(repr(ch))

    return control_point, charges, coord_min, coord_max


# Function that computes electric field vector components.
# Input: charge value and charge coordinates (x, y), and field point coordinates (x, y).
def electric_field(q, x_charge, y_charge, x_point, y_point):
    # Components and magnitude of displacement vector r
    r_x = x_point - x_charge
    r_y = y_point - y_charge
    r = np.sqrt(r_x * r_x + r_y * r_y)
    r = max(r, 1e-12)

    # Electric field vector components
    # Multiplication is slightly faster than exponentiation
    e_x = q * k * r_x / (r * r * r)
    e_y = q * k * r_y / (r * r * r)

    return e_x, e_y


# Function that calculates superposition of all electric fields
# and prints the field values for each charge
def superposition_fields(charges_data, control_point_data):
    e_total_x = 0.0
    e_total_y = 0.0

    for charge in charges_data:
        temp_x, temp_y = electric_field(
            charge.q, charge.x, charge.y, control_point_data.x, control_point_data.y
        )
        e_total_x += temp_x
        e_total_y += temp_y

        e_mag = np.sqrt(temp_x * temp_x + temp_y * temp_y)
        print(
            f"For charge {charge}  E_x = {temp_x:.6f}, E_y = {temp_y:.6f}, |E| = {e_mag:.6f}."
        )

    return e_total_x, e_total_y


def plot(control_point, charges, coord_min, coord_max):
    e_x, e_y = superposition_fields(charges, control_point)
    e_mag_total = np.sqrt(e_x * e_x + e_y * e_y)

    print(
        f"\nRESULT: E_x = {e_x:.6f}, E_y = {e_y:.6f}, |E| = {e_mag_total:.6f}\n"
        "Important: the arrow is scaled in the plot.\n"
    )

    # Normalize arrow length so it is always visible
    arrow_length = 2.0
    if e_mag_total > 0:
        e_x = (e_x / e_mag_total) * arrow_length
        e_y = (e_y / e_mag_total) * arrow_length
    else:
        e_x, e_y = 0, 0

    plt.quiver(
        control_point.x,
        control_point.y,
        e_x,
        e_y,
        angles="xy",
        scale_units="xy",
        scale=1,
        color="g",
    )
    plt.plot(control_point.x, control_point.y, "og")
    plt.text(control_point.x + 0.1, control_point.y + 0.1, "P")

    positive_label = False
    negative_label = False

    for charge in charges:
        if charge.q > 0:
            if not positive_label:
                plt.plot(charge.x, charge.y, "ob", label="q > 0")
                positive_label = True
            else:
                plt.plot(charge.x, charge.y, "ob")
        else:
            if not negative_label:
                plt.plot(charge.x, charge.y, "or", label="q < 0")
                negative_label = True
            else:
                plt.plot(charge.x, charge.y, "or")

        # '+' always shows the sign, 'd' means integer
        plt.text(charge.x + 0.15, charge.y + 0.15, f"{charge.q:+d}")

    margin = 1
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlim(coord_min - margin, coord_max + margin)
    plt.ylim(coord_min - margin, coord_max + margin)
    plt.title("Electric field vector at point P")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    result = generate_charges()
    if result is not None:
        control_point, charges, coord_min, coord_max = result
        plot(control_point, charges, coord_min, coord_max)

# TODO: upload to GitHub as a project
