import os

import requests

from utils import get_txt_files, get_lines

dir = '../datasets/unicorn_wget'
files = [
    'attack_base',
    'attack_streaming',
    'benign_base',
    'benign_streaming'
]

if __name__ == '__main__':
    os.makedirs(dir, exist_ok=True)

    for file_base in files:
        # r = requests.get('https://ivantha.github.io/rpelsg-unicorn-wget-dataset/' + file_base)
        # f = open('{}/{}.zip'.format(dir, file_base), 'wb')
        # f.write(r.content)

        # TODO : unzip files

        data_files = get_txt_files('{}/{}/'.format(dir, file_base))

        new_f_counter = 0
        line_counter = 0
        new_f = open('{}/{}/{}.txt'.format(dir, file_base, new_f_counter), 'w')

        for data_file in data_files:
            for line in get_lines(data_file):
                try:
                    source_id, target_id, _ = line.split()

                    line_counter += 1
                    new_f.write('{},{}\n'.format(source_id, target_id))

                    # start writing to a new file
                    if line_counter == 10000:
                        new_f.close()

                        new_f_counter += 1
                        line_counter = 0
                        new_f = open('{}/{}/{}.txt'.format(dir, file_base, new_f_counter), 'w')
                except:
                    print('{} > {}'.format(data_file, line))

            os.remove(data_file)