def solution(x, y):
    """Calculates the "block" surface of the triangle to the top left, bottom right and
    the rectangle formed by the coordinates.
    """

    def blocky_triangle_plus(a):
        # Calculates the block surface of a same-sided-triangle.
        # Blocks which are "split" are added from the surface value.
        return (a * a + a) // 2

    def blocky_triangle_min(a):
        # Calculates the block surface of a same-sided-triangle.
        # Blocks which are "split" are removed from the surface value.
        return (a * a - a) // 2

    upper_triangle = blocky_triangle_plus(x - 1)
    rectangle = x * y
    lower_triangle = blocky_triangle_min(y - 1)

    val = upper_triangle + rectangle + lower_triangle

    return str(val)


def solution_recursive(x, y):
    """Pure recursive solution by traversing the bunnies back to start."""

    def solution_inner(x, y):
        if x != 1:
            # Move upwards diagonally.
            return solution_inner(x-1, y+1) + 1
        else:
            # (1,1) is trivially 1.
            if y == 1:
                return 1
            # Hit the wall, drop down to floor level and move to the end of the
            # x line we need to traverse.
            return solution_inner(y-1, 1) + 1
        return 1

    return str(solution_inner(x,y))


def solution_iteration(x, y):
    """Adaption of the recursive solution to a loop to prevent hitting the max
    recursion limit.
    """

    count = 1

    while x != 1 or y != 1:
        if x != 1:
            x = x - 1
            y = y + 1
        else:
            x = y - 1
            y = 1

        count = count + 1

    return str(count)
