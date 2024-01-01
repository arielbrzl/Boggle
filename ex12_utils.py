
BOARD_SIZE = 4
BOUNDS = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
OUT_OF_BOUNDS = [(-1, j) for j in range(BOARD_SIZE + 1)] + \
                [(i, -1) for i in range(BOARD_SIZE + 1)] + \
                [(4, k) for k in range(BOARD_SIZE + 1)] + \
                [(m, 4) for m in range(BOARD_SIZE)] + [(-1, -1)]


def check_sequence(path):
    """
    this function assures that the path is composed of adjacent places only,
    and without repetitions
    """
    if len(path) != len(set(path)):  # one location appears twice
        return False
    for ind in range(len(path)):
        if ind == len(path) - 1:  # the last in sequence
            return True
        i, j = path[ind][0], path[ind][1]
        if path[ind + 1] not in [
            (i + 1, j), (i - 1, j), (i, j - 1),
            (i, j + 1), (i - 1, j - 1),
            (i - 1, j + 1), (i + 1, j - 1),
            (i + 1, j + 1)]:
            return False
    return True


def is_valid_path(board, path, words):
    """
    this function uses check_sequence function to verify if the path is valid
    then it composes the word and check if it is in the dictionary
    :return: None if a) path is not legal b) word not in dictionary
                    c)path is out of BOUNDS
             the string of the word if it is legal and in dictionary
    """
    if not check_sequence(path):
        return None
    cur_word = ""
    for tupl in path:
        if tupl not in BOUNDS:
            return None
        cur_word += board[tupl[0]][tupl[1]]
    if cur_word in words:
        return cur_word
    else:
        return None


def letters_filter(words, initials):
    """
    filters out words that dont share the first letters as given
    """
    filtered_words = []
    for word in words:
        if word[:len(initials)] == initials:
            filtered_words.append(word)
    return filtered_words


def recursive_length_n_paths(n, board, words, cur_location,
                             path, word, list_of_path=None):
    """
    this function is using recursion to look for all possible paths.
    the algo. can only move to adjacent location.
     each direction is named like a direction. e.g - S = south
    :param list_of_path:
    :param n: how many more letters do we left
    :param board: a list of lists repr. the board
    :param words: a list of words, previously filtered
    :param cur_location: a tuple indicating the current loc. (i,j)
    :param path: a list containing the tuples of all the locations we've been
    :param word: a string accumulating all the letters already visited
    param list_of_path: a list containing all the previous paths
    :return: when we get to a base case, if the word is valid, we return path
    """
    if list_of_path is None:
        list_of_path = []
    if n == 0:
        if word in words:
            if path not in list_of_path:
                return [path]
        return list_of_path
    x, y = cur_location[0], cur_location[1]
    if (x + 1, y) in BOUNDS and (x + 1, y) not in path:
        filtered_words = letters_filter(words, word + board[x + 1][y])
        if filtered_words:
            S = recursive_length_n_paths(n - 1, board, filtered_words,
                                         (x + 1, y),
                                         path + [(x + 1, y)],
                                         word + board[x + 1][y], list_of_path)
        else:
            S = []
    else:
        S = []
    if (x - 1, y) in BOUNDS and (x - 1, y) not in path:
        filtered_words = letters_filter(words, word + board[x - 1][y])
        if filtered_words:
            N = recursive_length_n_paths(n - 1, board, filtered_words,
                                         (x - 1, y),
                                         path + [(x - 1, y)],
                                         word + board[x - 1][y], list_of_path)
        else:
            N = []
    else:
        N = []
    if (x, y + 1) in BOUNDS and (x, y + 1) not in path:
        filtered_words = letters_filter(words, word + board[x][y + 1])
        if filtered_words:
            E = recursive_length_n_paths(n - 1, board, filtered_words,
                                         (x, y + 1),
                                         path + [(x, y + 1)],
                                         word + board[x][y + 1], list_of_path)
        else:
            E = []
    else:
        E = []
    if (x, y - 1) in BOUNDS and (x, y - 1) not in path:
        filtered_words = letters_filter(words, word + board[x][y - 1])
        if filtered_words:
            W = recursive_length_n_paths(n - 1, board, filtered_words,
                                         (x, y - 1),
                                         path + [(x, y - 1)],
                                         word + board[x][y - 1], list_of_path)
        else:
            W = []
    else:
        W = []
    if (x + 1, y + 1) in BOUNDS and (x + 1, y + 1) not in path:
        filtered_words = letters_filter(words, word + board[x + 1][y + 1])
        if filtered_words:
            SE = recursive_length_n_paths(n - 1, board, filtered_words,
                                          (x + 1, y + 1),
                                          path + [(x + 1, y + 1)],
                                          word + board[x + 1][y + 1],
                                          list_of_path)
        else:
            SE = []
    else:
        SE = []
    if (x + 1, y - 1) in BOUNDS and (x + 1, y - 1) not in path:
        filtered_words = letters_filter(words, word + board[x + 1][y - 1])
        if filtered_words:
            SW = recursive_length_n_paths(n - 1, board, filtered_words,
                                          (x + 1, y - 1),
                                          path + [(x + 1, y - 1)],
                                          word + board[x + 1][y - 1],
                                          list_of_path)
        else:
            SW = []
    else:
        SW = []
    if (x - 1, y + 1) in BOUNDS and (x - 1, y + 1) not in path:
        filtered_words = letters_filter(words, word + board[x - 1][y + 1])
        if filtered_words:
            NE = recursive_length_n_paths(n - 1, board, filtered_words,
                                          (x - 1, y + 1),
                                          path + [(x - 1, y + 1)],
                                          word + board[x - 1][y + 1],
                                          list_of_path)
        else:
            NE = []
    else:
        NE = []
    if (x - 1, y - 1) in BOUNDS and (x - 1, y - 1) not in path:
        filtered_words = letters_filter(words, word + board[x - 1][y - 1])
        if filtered_words:
            NW = recursive_length_n_paths(n - 1, board, filtered_words,
                                          (x - 1, y - 1),
                                          path + [(x - 1, y - 1)],
                                          word + board[x - 1][y - 1],
                                          list_of_path)
        else:
            NW = []
    else:
        NW = []
    return E + S + W + N + SW + SE + NE + NW


def path_organiser(list_of_possible_words):
    """
    takes all the sublists returned from the recursive func and turns them
     to a single list
    :param list_of_possible_words:
    :return:
    """
    final_paths = []
    for sub_list in list_of_possible_words:
        if sub_list:
            for path in sub_list:
                final_paths.append(path)
    return final_paths


def possible_word_length(n, board):
    """
    this function returns the possible range of length of words
    according to the cubes on the board
    :param n: int, how many cubes our path is
    :param board: list of lists
    :return: minimal and maximal length of a word
    """
    length_list = []
    for lst in board:
        for cube in lst:
            length_list.append(len(cube))
    sorted_lst = sorted(length_list)[::-1]
    return sum(sorted_lst[-n:]), sum(sorted_lst[:n])


def word_minimizer_path(n, board, words):
    """
    this function filters out words not of a possible length
    :return: a list of possible words
    """
    minimized_words_list = []
    min_length, max_length = possible_word_length(n, board)
    possible_length = [min_length + i for i in
                       range(max_length - min_length + 1)]
    for word in words:
        if len(word) in possible_length:
            minimized_words_list.append(word)
    return minimized_words_list


def find_length_n_paths(n, board, words):
    """
    returns all the possible paths in length n
    calls a recursive function that appends possible paths to a list
    """
    if n <= 0 or n > 16 or type(n) != int:
        return []
    list_of_possible_paths = []
    minimized_words_list = word_minimizer_path(n, board, words)
    for i in range(len(board)):
        for j in range(len(board)):
            filtered_words = letters_filter(minimized_words_list, board[i][j])
            list_of_possible_paths.append(
                recursive_length_n_paths(n - 1, board, filtered_words,
                                         (i, j), [(i, j)], board[i][j]))
    final_paths = path_organiser(list_of_possible_paths)
    return final_paths


def recursive_length_n_words(n, board, words, cur_location, path, word,
                             list_of_path=None):
    """
    the helper function, recursively goes over all direction and minimizes
    the possible words
    :param n: number of letters yet to find
    :param board: game board
    :param words: legal words
    :param cur_location: a tuple (i,j) indicating our current location
    :param path: a list of all our previous locations
    :param word: a string accumulating the data of the previous locations
    :param list_of_path: a list containing all previous paths
    :return:
    """
    if list_of_path is None:
        list_of_path = []
    if n == 0:
        if word in words:
            # if path not in list_of_path:
            return [path]
        return list_of_path
    x, y = cur_location[0], cur_location[1]
    if (x + 1, y) in BOUNDS and (x + 1, y) not in path:
        filtered_words = letters_filter(words, word + board[x + 1][y])
        if filtered_words:
            S = recursive_length_n_words(n - len(board[x + 1][y]), board,
                                         filtered_words,
                                         (x + 1, y),
                                         path + [(x + 1, y)],
                                         word + board[x + 1][y], list_of_path)
        else:
            S = []
    else:
        S = []
    if (x - 1, y) in BOUNDS and (x - 1, y) not in path:
        filtered_words = letters_filter(words, word + board[x - 1][y])
        if filtered_words:
            N = recursive_length_n_words(n - len(board[x - 1][y]), board,
                                         filtered_words,
                                         (x - 1, y),
                                         path + [(x - 1, y)],
                                         word + board[x - 1][y], list_of_path)
        else:
            N = []
    else:
        N = []
    if (x, y + 1) in BOUNDS and (x, y + 1) not in path:
        filtered_words = letters_filter(words, word + board[x][y + 1])
        if filtered_words:
            E = recursive_length_n_words(n - len(board[x][y + 1]), board,
                                         filtered_words,
                                         (x, y + 1),
                                         path + [(x, y + 1)],
                                         word + board[x][y + 1], list_of_path)
        else:
            E = []
    else:
        E = []
    if (x, y - 1) in BOUNDS and (x, y - 1) not in path:
        filtered_words = letters_filter(words, word + board[x][y - 1])
        if filtered_words:
            W = recursive_length_n_words(n - len(board[x][y - 1]), board,
                                         filtered_words,
                                         (x, y - 1),
                                         path + [(x, y - 1)],
                                         word + board[x][y - 1], list_of_path)
        else:
            W = []
    else:
        W = []
    if (x + 1, y + 1) in BOUNDS and (x + 1, y + 1) not in path:
        filtered_words = letters_filter(words, word + board[x + 1][y + 1])
        if filtered_words:
            SE = recursive_length_n_words(n - len(board[x + 1][y + 1]), board,
                                          filtered_words, (x + 1, y + 1),
                                          path + [(x + 1, y + 1)],
                                          word + board[x + 1][y + 1],
                                          list_of_path)
        else:
            SE = []
    else:
        SE = []
    if (x + 1, y - 1) in BOUNDS and (x + 1, y - 1) not in path:
        filtered_words = letters_filter(words, word + board[x + 1][y - 1])
        if filtered_words:
            SW = recursive_length_n_words(n - len(board[x + 1][y - 1]), board,
                                          filtered_words, (x + 1, y - 1),
                                          path + [(x + 1, y - 1)],
                                          word + board[x + 1][y - 1],
                                          list_of_path)
        else:
            SW = []
    else:
        SW = []
    if (x - 1, y + 1) in BOUNDS and (x - 1, y + 1) not in path:
        filtered_words = letters_filter(words, word + board[x - 1][y + 1])
        if filtered_words:
            NE = recursive_length_n_words(n - len(board[x - 1][y + 1]), board,
                                          filtered_words, (x - 1, y + 1),
                                          path + [(x - 1, y + 1)],
                                          word + board[x - 1][y + 1],
                                          list_of_path)
        else:
            NE = []
    else:
        NE = []
    if (x - 1, y - 1) in BOUNDS and (x - 1, y - 1) not in path:
        filtered_words = letters_filter(words, word + board[x - 1][y - 1])
        if filtered_words:
            NW = recursive_length_n_words(n - len(board[x - 1][y - 1]), board,
                                          filtered_words, (x - 1, y - 1),
                                          path + [(x - 1, y - 1)],
                                          word + board[x - 1][y - 1],
                                          list_of_path)
        else:
            NW = []
    else:
        NW = []
    return E + S + W + N + SW + SE + NE + NW


def words_minimizer_by_length(words, n):
    """
    keeps only words with a specific length
    """
    minimized_words_list = []
    for word in words:
        if len(word) == n:
            minimized_words_list.append(word)
    return minimized_words_list


def find_length_n_words(n, board, words):
    """
    finds words with length n on board
    :param n: an int
    :param board: the game board
    :param words: a list of legal words
    :return:
    """
    if n <= 0 or type(n) is not int:
        return []
    list_of_possible_words = []
    minimized_words_list = words_minimizer_by_length(words, n)
    if not minimized_words_list:
        return []
    for i in range(len(board)):
        for j in range(len(board)):
            filtered_words = letters_filter(minimized_words_list, board[i][j])
            if filtered_words:
                list_of_possible_words.append(
                    recursive_length_n_words(n - len(board[i][j]), board,
                                             filtered_words,
                                             (i, j), [(i, j)], board[i][j]))
            else:
                continue
    final_path = path_organiser(list_of_possible_words)
    return final_path


def max_score_paths(board, words):
    list_of_words, list_of_paths = [], []
    for n in range(16):
        if find_length_n_paths(16 - n, board, words):
            for path in find_length_n_paths(16 - n, board, words):
                word = is_valid_path(board, path, words)
                if word not in list_of_words:
                    list_of_words.append(word)
                    list_of_paths.append(path)
    return list_of_paths
