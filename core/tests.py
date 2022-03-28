# manual tests

from algohack import find_seq_path, find_sequence


def test1():
    matrix = [['55', '1C', '55', '55', '1C'], ['E9', '55', 'BD', 'E9', 'E9'], ['55', 'E9', 'BD', '55', '1C'],
     ['55', 'E9', '1C', 'E9', '1C'], ['1C', 'E9', '55', '55', '1C']]
    #['1C BD 1C E9 1C 55 E9', '1C 55 E9 1C BD 1C E9', 'BD 1C E9 1C 55 E9 1C 1C BD', 'BD 1C E9 1C 1C BD 1C 55 E9', '1C 1C BD 1C 55 E9 BD 1C E9', '1C 55 E9 BD 1C E9 1C 1C BD']
    seq = '1C 55 E9 1C BD 1C E9'.split(' ')
    path = find_seq_path(seq, matrix)
    print(seq)
    print(path)


def test2():
    sequences = [['1C', '1C'],
                 ['1C', '1C', 'E9'],
                 ['E9', '1C', 'BD']]
    a_seqs = ['1C E9 1C BD', '1C E9 1C BD 1C 1C', 'E9 1C BD 1C 1C E9', '1C 1C E9 1C 1C E9 1C BD', 'E9 1C BD 1C 1C E9 1C 1C', '1C 1C E9 1C BD 1C 1C E9']

    seqs = find_sequence(sequences)
    print(a_seqs)
    print(seqs)


def test21():
    sequences = [['1C', '2C'],
                 ['1C', '2C', 'E9'],
                 ['E9', '1C', 'BD']]
    seqs = find_sequence(sequences, print)
    print(seqs)
    assert seqs == [['1C', '2C', 'E9', '1C', 'BD'],
                    ['1C', '2C', 'E9', '1C', 'BD', '1C', '2C', 'E9'],
                    ['1C', '2C', 'E9', '1C', '2C', 'E9', '1C', 'BD'],
                    ['1C', '2C', 'E9', '1C', 'BD', '1C', '2C'],
                    ['E9', '1C', 'BD', '1C', '2C', 'E9'],
                    ['E9', '1C', 'BD', '1C', '2C', 'E9', '1C', '2C']]


def test22():
    sequences = [['E9', '55'],
                 ['1C', '1C', '55'],
                 ['55', '55', '1C']]
    seqs = find_sequence(sequences, print)
    print(seqs)
    assert seqs == [['E9', '55', '1C', '1C', '55', '55', '1C'],
                    ['E9', '55', '55', '1C', '1C', '55'],
                    ['1C', '1C', '55', 'E9', '55', '55', '1C'],
                    ['1C', '1C', '55', '55', '1C', 'E9', '55'],
                    ['55', '55', '1C', 'E9', '55', '1C', '1C', '55'],
                    ['55', '55', '1C', '1C', '55', 'E9', '55']]


def test3():
    matrix = [['55', 'E9', 'E9', 'E9', '55'], ['E9', 'BD', '1C', 'BD', 'BD'], ['55', '1C', '55', '55', '1C'], ['E9', '1C', 'E9', '1C', '55'], ['1C', 'E9', '1C', '1C', 'BD']]
    #['1C BD 1C E9 1C 55 E9', '1C 55 E9 1C BD 1C E9', 'BD 1C E9 1C 55 E9 1C 1C BD', 'BD 1C E9 1C 1C BD 1C 55 E9', '1C 1C BD 1C 55 E9 BD 1C E9', '1C 55 E9 BD 1C E9 1C 1C BD']
    seq = '1C 1C E9 1C BD'.split(' ')
    path = find_seq_path(seq, matrix)
    print(seq)
    print(path)


def test_no_entry_point_in_matrix():
    matrix = [['55', 'BD', 'E9', 'BD', '55'],
              ['1C', '1C', '55', '55', '1C'],
              ['1C', '55', '55', '1C', '1C'],
              ['E9', '1C', 'E9', '1C', 'BD'],
              ['55', '55', '1C', '55', '55']]
    seq = ['1C', '1C', '1C', '55']
    path = find_seq_path(seq, matrix)
    print(seq)
    print(path)
    assert path == [[0, 0], [1, 0], [1, 4], [2, 4], [2, 1]]


test_no_entry_point_in_matrix()
