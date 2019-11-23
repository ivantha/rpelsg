import os
import sys

# Path hack.

sys.path.insert(0, os.path.abspath('..'))

from google_drive_downloader import GoogleDriveDownloader as gdd

from common.utils import get_txt_files

parent_dir = '../datasets/unicorn_wget'

files = (
    ('benign_base', '1-rmP2_vOgIU56husFP0AhHK3O3HjPi0d'),
    ('benign_streaming', '1-urTwbWoqmeI-Y4Blhq1Xi_qnh2zDUhR'),
    ('attack_base', '1-jcapoEm0lEri9sBHn5RvTkrnDvSo0QG'),
    ('attack_streaming', '1-nZMkgFLfRPXCGKX2yo62ykSn2FGAh6X'),
)

if __name__ == '__main__':
    os.makedirs(parent_dir, exist_ok=True)

    for file_base, drive_id in files:
        gdd.download_file_from_google_drive(file_id=drive_id,
                                            dest_path='{}/{}.zip'.format(parent_dir, file_base),
                                            unzip=True, showsize=True)

        data_files = get_txt_files('{}/{}/'.format(parent_dir, file_base))

        new_f_counter = 0
        line_counter = 0
        new_f = open('{}/{}/{}.txt'.format(parent_dir, file_base, new_f_counter), 'w')

        for data_file in data_files:
            with open(data_file) as file:
                for line in file.readlines():
                    try:
                        source_id, target_id, _ = line.split()

                        line_counter += 1
                        new_f.write('{},{}\n'.format(source_id, target_id))

                        # start writing to a new file
                        if line_counter == 100000:
                            new_f.close()

                            new_f_counter += 1
                            line_counter = 0
                            new_f = open('{}/{}/{}.txt'.format(parent_dir, file_base, new_f_counter), 'w')
                    except:
                        print('{} > {}'.format(data_file, line))

                os.remove(data_file)
