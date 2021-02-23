from fractions import gcd


def solution(m):
    """Return the probablities for each terminal state.

    First the inputs are re-ordered so that the last rows all are terminal
    states. This is done by re-ordering the original matrix so that we have
    distinct transition and terminal row regions in the matrix. The ordering of
    the rows within these sub-regions will stay the same as with the original
    matrix.

    This will result in the answer for the absorbing Markov chain for the re-ordered
    matrix to be the same as the original matrix.
    """
    # Trivial case, only 1 state.
    if len(m) == 1:
        return [1, 1]

    # Re-order.
    m_modified = _reorder(m)
    # Solve.
    return _solve(m_modified)

def _reorder(m):
    """Re-order the matrix 'm' so that the last rows are all zeroes and the top
    rows are non-zeroes. Ordering of rows within the non-zeros is the same relatively
    as with the original matrix.
    """
    # Find which rows are zero's and non-zeroes.
    row_sums = [sum(x) for x in m]
    zero_rows = []
    other_rows = []
    for index, x in enumerate(row_sums):
        if x:
            other_rows.append(index)
        else:
            zero_rows.append(index)

    # Assert condition from the question, row 0 is the start state.
    assert(other_rows[0] == 0)

    # Construct the transformation matrix to switch rows that aren't zeroed
    # to the top.
    transform = get_zero_matrix(len(m))
    for row, column in enumerate(other_rows+zero_rows):
        transform[row][column] = 1

    # Apply row transfrom.
    m_modified = multiply(transform, m)
    # Apply column transform to ensure columnns match the switched states.
    return multiply(m_modified, transpose(transform))

def _solve(m):
    """
    Calculate by solving the absorbing Markov chain.
    https://en.wikipedia.org/wiki/Absorbing_Markov_chain
    """
    # Step 1.
    # Normalize the input matrix and create the matrix 'Q', this is the transistion
    # matrix between non-terminal states. Using this we can calculate the fundamental
    # matrix.

    # Calculate denominator to normalize to.
    row_sums = [sum(x) for x in m]
    main_denominator = lcm_common(row_sums)

    # Calculate the zero pivot, in the matrix 'm' the submatrix to the top
    # left of this pivot is the sqaure transition matrix 'Q'. To the top right the
    # absorbtion matrix 'R'. To the bottom left will be 0's. The bottom right will
    # _should_ be an identity matrix of the absorbing states. However in our use
    # case these are all zeroes.
    zero_pivot = row_sums.index(0)

    # Create the normalized Q matrix.
    q_matrix = get_zero_matrix(zero_pivot)
    for i in range(0, zero_pivot):
        for j in range(0, zero_pivot):
            q_matrix[i][j] = int(m[i][j] * main_denominator / row_sums[i])

    # Step 2.
    # Calculate the fundamental matrix 'N = (I-Q)^-1'
    # Step 2a; calculate (I-Q).
    fundamental_matrix = []
    for index, row in enumerate(q_matrix):
        # -Q.
        next_row = [-x for x in row]
        # -Q + I, I is normalized to the main denominator.
        next_row[index] = next_row[index] + main_denominator
        fundamental_matrix.append(next_row)

    # NOTE: we are missing a normalization scalar value here that is needed
    # since we normalized the identity matrix by multiplying it with the 'main_denominator'.
    # In the next step when inverting this would give us a 'nominator' that would be
    # equal to the value of the 'main_denominator'.
    #
    # Later in the algorithm this will be cancelled out by a division by the same
    # value so we can explicitly omit it.

    # Step 2b; calculate the inverse using 'Cramers Rule'.
    # https://en.wikipedia.org/wiki/Invertible_matrix#Methods_of_matrix_inversion
    # A^-1 = (1/det(A)) * Adj(A)
    fundamental_denominator = determinant_laplace(fundamental_matrix)
    fundamental_matrix = adjugate_matrix(fundamental_matrix)

    # Step 3.
    # Calculate the absorbing probability matrix, 'B=NR'.
    # Step 3a; calculate the normalized 'R' matrix.
    # NOTE; since R is normalized we should multiple this with 1/'main_denominator',
    # however in the next step this will cancel out with what would be the nominator
    # in front of the fundamental matrix.
    r_matrix = get_zero_matrix(zero_pivot, len(m)-zero_pivot)
    for i in range(0, zero_pivot):
        for j in range(0,  len(m)-zero_pivot):
            r_matrix[i][j] = int(
                m[i][j+zero_pivot] * main_denominator // row_sums[i]
            )

    # Step 3b; calculate 'NR' but only calculate using the first row of 'R' as asked.
    # Store intermediate values in 'R' and the final result in the first row of 'R'
    # Multiplication step.
    for i in range(0, len(fundamental_matrix[0])):
        for j in range(0, len(r_matrix[i])):
            r_matrix[i][j] *= fundamental_matrix[0][i]
    # Sum step.
    for j in range(0, len(r_matrix[0])):
        for i in range(1, len(r_matrix)):
            r_matrix[0][j] += r_matrix[i][j]

    answer = r_matrix[0] + [fundamental_denominator]

    # Step 4; normalize answer.
    common = 0
    for x in answer:
        common = gcd(common, x)

    return [x // common for x in answer]


# Math utilities #


def lcm(a, b):
    """Lowest common multiple."""
    return abs(a*b) // gcd(a, b)


def lcm_common(numbers):
    common = 1
    for x in numbers:
        if x:
            common = lcm(common, x)
    return common


# Matrix constructors #


def get_identity_matrix(size):
    """
    Args:
        size (int): matrix size (rows/columns)
    Returns:
        list(list(int))
    """
    matrix = []
    for x in range(0, size):
        row = [0]*size
        row[x] = 1
        matrix.append(row)
    return matrix


def get_zero_matrix(rows, columns=None):
    """
    Args:
        rows (int): amount of rows
        columns (int, optional): amounts of columns. Defaults to rows.
    Returns:
        list(list(int))
    """
    if not columns:
        columns = rows
    matrix = [[0]*columns for _ in range(0, rows)]
    return matrix


# Matrix Algorithms #


def multiply(m, n):
    """Matrix multiple 2 square matrices."""
    a = get_zero_matrix(len(m))

    for i in range(0, len(a)):
        for j in range(0, len(a)):
            a[i][j] = sum([
                x*y for x,y in zip(
                    m[i], [n[k][j] for k in range(0, len(n))]
                )
            ])

    return a


def transpose(m):
    """Transpose a square matrix."""
    a = get_zero_matrix(len(m))

    for i in range(0, len(m)):
        for j in range(0, len(m)):
            a[j][i] = m[i][j]

    return a


def determinant_laplace(matrix):
    """Determinant of a square matrix using Laplace expansion along the first row.
    The algorithm below was implemented by adapting and studying:
    https://en.wikipedia.org/wiki/Laplace_expansion
    """
    if len(matrix) == 1:
        return matrix[0][0]

    total = 0
    for index, value in enumerate(matrix[0]):
        submatrix = [row[:index] + row[index+1:] for row in matrix[1:]]
        sign = -1 if index % 2 == 1 else 1
        total += int(sign * value * determinant_laplace(submatrix))

    return total


def adjugate_matrix(matrix):
    """Calculate the adjugate matrix of a square matrix.
    https://en.wikipedia.org/wiki/Adjugate_matrix
    """
    if len(matrix) == 1:
        return [[1]]

    adjugate = get_zero_matrix(len(matrix))

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):

            # Construct the matrix 'M' which is the input matrix without
            # a given row and column.
            m_matrix = []
            for index, row in enumerate(matrix):
                # This calculate M_ji (remove row j and column i) as to get C_transpose.
                if index == j:
                    continue
                m_matrix.append(
                    row[:i] + row[i+1:]
                )

            sign = pow(-1, i+j)
            adjugate[i][j] = int(sign * determinant_laplace(m_matrix))

    return adjugate
