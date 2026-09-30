"""
click_detection: figures out whether a click landed on a balloon.
"""


def check_pop(balloons, click_pos):
    """
    Returns the balloon that was clicked, or None if the click missed
    every balloon. Iterates in reverse so top-drawn balloons are clicked first.
    """
    for balloon in reversed(balloons):
        dx = click_pos[0] - balloon.x
        dy = click_pos[1] - balloon.y
        distance_squared = dx * dx + dy * dy
        # Compare squared distance to squared radius
        if distance_squared <= balloon.radius ** 2:
            return balloon
    return None