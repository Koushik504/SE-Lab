"""
collisions: frog-vs-vehicle collision detection.
"""

CELL_SIZE = 50


def check_collision(frog, vehicles):
    """
    Returns True if the frog's actual rectangle overlaps
    with any vehicle's actual rectangle.
    """

    # Get the frog's actual screen rectangle
    frog_rect = frog.get_rect(CELL_SIZE)

    # Check the frog against every vehicle
    for v in vehicles:
        # Get the vehicle's actual screen rectangle
        vehicle_rect = v.get_rect(CELL_SIZE)

        # Check whether the two rectangles overlap
        if frog_rect.colliderect(vehicle_rect):
            return True

    return False