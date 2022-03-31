import logging
import os
import time

import mss
import numpy as np

from algohack import find_sequence, find_seq_path
from screen_area import matrix_rect_factor, sequences_rect_factor, buffer_rect_factor, box_size_factor, text_pos_factor, \
    id_rect_factor
from rcognize import get_matrix_from_image, get_id, get_buffer_size, back_scaling_factor


# game render commands file
cmd_file_name = os.getenv('CMDS_FILENAME')

# timeouts for screenshots
hack_mode_timeout = 0.1
fps_mode_timeout = 1.0

# params of screen
monitor_number = int(os.getenv('MON_NUMBER', '2'))
screen = mss.mss()
monitor_info = screen.monitors[monitor_number]
screen_width = monitor_info["width"]
screen_height = monitor_info["height"]
full_screen_rect = {
    "top": monitor_info["top"],
    "left": monitor_info["left"],
    "width": screen_width,
    "height": screen_height,
    "mon": monitor_number,
}
# params for grab TECH area
id_rect = id_rect_factor.scaled(screen_width, screen_height)
id_screen_rect = {
    "top": int(id_rect.top),
    "left": int(id_rect.left),
    "width": int(id_rect.right),
    "height": int(id_rect.bottom),
    "mon": monitor_number,
}


# returns commands for game render and the best path found
def analyze_screen():
    # cleanup cmds file
    save_data([])

    # wait for game render clean frame
    time.sleep(0.2)

    # grab part of screen for check TECH area
    image = np.array(screen.grab(id_screen_rect))
    if get_id(image) != 'TECH':
        logging.debug('TECH check failed')
        return [], []

    # grab full screen
    image = np.array(screen.grab(full_screen_rect))

    matrix_rect = matrix_rect_factor.scaled(screen_width, screen_height)
    sequences_rect = sequences_rect_factor.scaled(screen_width, screen_height)
    buffer_rect = buffer_rect_factor.scaled(screen_width, screen_height)

    matrix_img = matrix_rect.crop(image)
    sequences_img = sequences_rect.crop(image)
    buffer_img = buffer_rect.crop(image)

    buffer_size = get_buffer_size(buffer_img, box_size=screen_width * box_size_factor)

    m_matrix, coord_map = get_matrix_from_image(matrix_img)
    sequences, _ = get_matrix_from_image(sequences_img)

    logging.debug('matrix', m_matrix)
    logging.debug('sequences', sequences)

    rows = len(m_matrix)
    if 0 < rows < 10 and 0 < len(sequences) < 4:
        cols = len(m_matrix[0])

        for row in m_matrix:
            if cols != len(row):
                logging.error('Matrix aspect error', cols, len(row))
                return [], []

    # find and arrange sequences
    unique_seqs = set()
    for seq in find_sequence(sequences):
        unique_seqs.add(' '.join(seq))

    sorted_seq = sorted(unique_seqs, key=lambda s: len(s))
    logging.debug('sorted_seq', sorted_seq)

    # found sequence start pos (by y)
    text_pos = text_pos_factor * screen_height

    # viewing commands
    cmds = []
    best_seq = None
    best_path = None
    ex_seq = False
    for seq_str in sorted_seq:
        seq = seq_str.split(' ')
        path, s_seq = find_seq_path(seq, m_matrix)
        if s_seq:
            seq_str = ' '.join(s_seq)
        size_diff = len(path) - len(seq) if path else -1
        valid_path = path and size_diff >= 0

        if best_path and valid_path:
            cmds.append(f'text;{seq_str};{sequences_rect.left};{text_pos};{0xff00ffff if size_diff == 0 else 0xffffffaa}')
        elif valid_path:
            best_path = path
            best_seq = s_seq
            ex_seq = size_diff > 0
            cmds.append(f'text;{seq_str};{sequences_rect.left};{text_pos};{0xff00ff00 if size_diff == 0 else 0xffffaaaa}')
        elif path:
            cmds.append(f'text;{seq_str};{sequences_rect.left};{text_pos};0xffaaaaaa')
        else:
            cmds.append(f'text;{seq_str};{sequences_rect.left};{text_pos};0xff0000ff')
        text_pos += 30

    logging.info('sequences:  ', sorted_seq, len(unique_seqs))
    logging.info('best seq:   ', best_seq)
    logging.info('best path:  ', best_path)
    logging.info('buffer size:', buffer_size)

    if best_path:
        arr_color = '0xaa00ff00' if len(best_path) <= buffer_size else '0xaa0000ff'
        number = 1
        for coord_index in best_path:
            coord = coord_map[coord_index[0]][coord_index[1]]
            x = int(matrix_rect.left + coord[0] * back_scaling_factor)
            y = int(matrix_rect.top + coord[1] * back_scaling_factor)
            color = arr_color
            if number == 1 and ex_seq:
                color = '0xaaffaaaa'
            cmds.append(f'hit;{number};{x};{y};{color}')
            number += 1

    return cmds, best_path


# writes cmds info game commands file
def save_data(cmds):
    logging.info(f'cmds:{cmds}')
    f = open(cmd_file_name, "w")
    f.write('\n'.join(cmds))
    f.close()


# find and display path
def update_path():
    # render clean frame
    save_data([])
    time.sleep(0.2)

    # wait for successful recognition
    path = None
    while path is None:
        cmds, path = analyze_screen()
        save_data(cmds)
        time.sleep(0.5)


# returns true if TECH title found on id screen area
def is_hackmode():
    # grab part of screen for check TECH area
    image = np.array(screen.grab(id_screen_rect))
    return get_id(image) == 'TECH'


def main():
    logging.info('Running cyberhack...')

    if not cmd_file_name:
        raise Exception('Env variable CMDS_FILENAME is not set')

    logging.info(f'cmd file:{cmd_file_name}')

    last_mode = None
    while True:
        is_hack_mode_enabled = is_hackmode()
        if is_hack_mode_enabled == last_mode:
            time.sleep(hack_mode_timeout if is_hack_mode_enabled else fps_mode_timeout)
            continue

        last_mode = is_hack_mode_enabled

        logging.info(f'mode changed {is_hack_mode_enabled}')
        if is_hack_mode_enabled:
            update_path()
        else:
            save_data([])


if __name__ == '__main__':
    logging.root.setLevel(logging.INFO)
    main()
