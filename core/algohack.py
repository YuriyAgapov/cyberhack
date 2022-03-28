from copy import deepcopy


def dummy(*_):
    pass


class Node:
    def __init__(self, symbol: str = None, parent=None):
        self.symbol = symbol
        self.parent = parent
        self.children = []
        self.closed = []
        if parent:
            parent.children.append(self)

    def __str__(self):
        return str(self.symbol)


def get_next_sequence(sequences: []):
    for sequence in sequences:
        if len(sequence) == 0:
            continue
        return sequence.pop(0)
    return None


def find_sequence(seqs: [], debug=lambda *args: dummy(args)):
    # print('find_sequence_2:', seqs)
    size = len(seqs)
    mixs = []
    # print('# size:', size)

    if size == 1:
        mixs = [seqs]
    elif size == 2:
        mixs = [[deepcopy(seqs[0]), deepcopy(seqs[1])], [deepcopy(seqs[1]), deepcopy(seqs[0])]]
    elif size == 3:
        mixs = [[deepcopy(seqs[0]), deepcopy(seqs[1]), deepcopy(seqs[2])],
                [deepcopy(seqs[0]), deepcopy(seqs[2]), deepcopy(seqs[1])],
                [deepcopy(seqs[1]), deepcopy(seqs[0]), deepcopy(seqs[2])],
                [deepcopy(seqs[1]), deepcopy(seqs[2]), deepcopy(seqs[0])],
                [deepcopy(seqs[2]), deepcopy(seqs[0]), deepcopy(seqs[1])],
                [deepcopy(seqs[2]), deepcopy(seqs[1]), deepcopy(seqs[0])]]

    # for x in range(size):
    #     l = deepcopy(seqs[x])
    #     mix = [l]
    #     for y in range(size):
    #         if x == y:
    #             continue
    #         r = deepcopy(seqs[y])
    #         mix.append(r)
    #
    #     mixs.append(mix)
    #print('# mixs:', mixs)

    for mix in mixs:
        prev = None
        debug('mix:', mix)
        for s in mix:
            if prev is not None:
                prev_size = len(prev)
                min_size = min(len(s), prev_size)
                debug('  p vs s:', prev, s)
                debug('  min_size:', min_size)
                for i in range(min_size - 1, -1, -1):
                    debug('   i:', i, s[0:i+1], prev[-1-i:len(prev)])
                    if s[0:i+1] == prev[-1-i:len(prev)]:
                        debug('    del ', prev[-1-i:len(prev)])
                        del prev[-1-i:len(prev)]
                        break

                    # if prev[-1] == s[0]:
                    #     debug('    del ', prev[-1])
                    #     del prev[prev_size-i-1]
                    #     debug('    prev ', prev)
                    # else:
                    #     break
                # a b c
                # b c d e
            prev = s
        debug(' mix res', mix)

    #return mixs

    result = []
    for mix in mixs:
        short_seq = []
        for s in mix:
            short_seq += s
        result.append(short_seq)
    return result


#res1 = find_sequence_2([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#print(res1)

# res2 = find_sequence_2([[1, 2, 3], [3, 4, 5], [5, 6, 7]])
# print(res2)
# exit(0)


def print_tree(node: Node, prefix=''):
    print(f'{prefix}{node.symbol}')
    for child in node.children:
        print_tree(child, prefix + '.')


def foreach_sequences(node: Node, callback):
    if len(node.children) == 0:
        sequence = []
        while node and node.symbol:
            sequence.insert(0, node.symbol)
            node = node.parent
        callback(sequence)
    else:
        for child in node.children:
            foreach_sequences(child, callback)


def print_sequences(node: Node):
    foreach_sequences(node, lambda seq: print(seq))


def find_in_matrix_row(symbol, matrix, row, cols):
    #print(f'find_in_matrix_row {symbol} in row {row}')
    res = []
    for c in range(cols):
        #print('  ', matrix[row][c])
        if matrix[row][c] == symbol:
            res.append(c)
    #print('  found at', res)
    return res


def find_in_matrix_col(symbol, matrix, col, rows):
    #print(f'find_in_matrix_col {symbol} in col {col}, rows {rows}')
    res = []
    for r in range(rows):
        #print('  ', matrix[r][col])
        if matrix[r][col] == symbol:
            #print('  found at', r)
            res.append(r)
    #print('  found at', res)
    return res


def is_path_contains(path, pos):
    #print('is_path_contains', path, pos)
    for path_pos in path:
        if path_pos == pos:
            return True
    return False


def find_seq_in_matrix(path, seq, pos, matrix, c_row, c_col, is_row, rows, cols, debug=dummy):
    debug('* find_seq_in_matrix add', path, [c_row, c_col])
    path.append([c_row, c_col])
    if len(seq) == pos:
        debug('  ret end')
        return path

    sym = seq[pos]
    #print(f'find_seq_in_matrix {sym} from {seq}')
    if is_row:
        found = find_in_matrix_row(sym, matrix, c_row, cols)
        if len(found) == 0:
            debug('  ret row failed')
            return []

        for col in found:
            if is_path_contains(path, [c_row, col]):
                debug('  skip col', col)
                continue

            npath = find_seq_in_matrix(deepcopy(path), seq, pos + 1, matrix, int(c_row), int(col), bool(not is_row), rows, cols, debug)
            if npath:
                #print('p1', path)
                return npath
    else:
        found = find_in_matrix_col(sym, matrix, c_col, rows)
        if len(found) == 0:
            debug('  ret col failed')
            return []

        for row in found:
            if is_path_contains(path, [row, c_col]):
                debug('  skip row', row)
                continue

            npath = find_seq_in_matrix(deepcopy(path), seq, pos + 1, matrix, int(row), int(c_col), bool(not is_row), rows, cols, debug)
            if npath:
                #print('p2', path)
                return npath

    debug('  ret enexpected')
    return []


def find_seq_path(seq, matrix, depth=0):
    rows = len(matrix)
    if rows == 0:
        return None, None
    cols = len(matrix[0])
    if cols == 0:
        return None, None

    found_cols = find_in_matrix_row(seq[0], matrix, 0, cols)
    #print('* found_cols', found_cols)

    for col in found_cols:
        res = find_seq_in_matrix([], seq, 1, matrix, 0, col, False, rows, cols)
        if res:
            return res, seq

    if depth == 0:
        for sym in matrix[0]:
            s_seq = deepcopy(seq)
            s_seq.insert(0, sym)
            res, _ = find_seq_path(s_seq, matrix, 1)
            if res:
                return res, s_seq

    return None, None
