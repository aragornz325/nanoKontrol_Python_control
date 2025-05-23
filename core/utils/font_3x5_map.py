def transpose_and_flip(matrix):
    """
    Traspasa el matrix y lo voltea horizontalmente.
    no se porque no di vueltas las letras en vez de hacer la función XD

    Args:
        matriz (list of list): La matriz a transponer y voltear.

    Returns:
        la lista de letras dada vuelta
    """
    return [list(reversed(col)) for col in zip(*matrix)]


FONT_3x5 = {
    " ": [[0, 0, 0]],
    "A": transpose_and_flip([[1, 1, 1], [1, 0, 1], [1, 0, 1]]),
    "B": transpose_and_flip([[1, 1, 0], [1, 1, 1], [1, 1, 0]]),
    "C": transpose_and_flip([[1, 1, 1], [1, 0, 0], [1, 1, 1]]),
    "D": transpose_and_flip([[1, 1, 0], [1, 0, 1], [1, 1, 0]]),
    "E": transpose_and_flip([[1, 1, 1], [1, 1, 1], [1, 0, 1]]),
    "F": transpose_and_flip([[1, 1, 1], [1, 1, 0], [1, 0, 0]]),
    "G": transpose_and_flip([[1, 1, 1], [1, 0, 1], [1, 1, 1]]),
    "H": transpose_and_flip([[1, 0, 1], [1, 1, 1], [1, 0, 1]]),
    "I": transpose_and_flip([[1], [1], [1]]),
    "J": transpose_and_flip([[1, 1, 1], [0, 0, 1], [0, 0, 1]]),
    "K": transpose_and_flip([[1, 0, 1], [1, 1, 0], [1, 0, 1]]),
    "L": transpose_and_flip([[1, 0, 0], [1, 0, 0], [1, 1, 1]]),
    "M": transpose_and_flip([[1, 0, 1], [1, 1, 1], [1, 0, 1]]),
    "N": transpose_and_flip([[1, 0, 1], [1, 1, 1], [1, 1, 1]]),
    "O": transpose_and_flip([[1, 1, 1], [1, 0, 1], [1, 1, 1]]),
    "P": transpose_and_flip([[1, 1, 1], [1, 1, 0], [1, 0, 0]]),
    "Q": transpose_and_flip([[1, 1, 1], [1, 0, 1], [1, 1, 0]]),
    "R": transpose_and_flip([[1, 1, 1], [1, 1, 0], [1, 0, 1]]),
    "S": transpose_and_flip([[0, 1, 1], [1, 1, 1], [1, 1, 0]]),
    "T": transpose_and_flip([[0, 1, 0], [0, 1, 0], [1, 1, 1]]),
    "U": transpose_and_flip([[1, 0, 1], [1, 0, 1], [1, 1, 1]]),
    "V": transpose_and_flip([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    "W": transpose_and_flip([[1, 0, 1], [1, 1, 1], [1, 1, 1]]),
    "X": transpose_and_flip([[1, 0, 1], [0, 1, 0], [1, 0, 1]]),
    "Y": transpose_and_flip([[1, 0, 1], [0, 1, 0], [0, 1, 0]]),
    "Z": transpose_and_flip([[1, 1, 1], [0, 1, 0], [1, 1, 1]]),
}
