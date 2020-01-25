import os
import random
import shutil

from google_drive_downloader import GoogleDriveDownloader as gdd

from common.utils import get_txt_files

datasets = (
    (
        '../datasets/ego-Twitter',
        (
            ('ego-Twitter', '1HTzRpeLLeSVZw0NdlFKecokXLtviXXla'),
        )
    ),
    (
        '../datasets/email-EuAll',
        (
            ('email-EuAll', '1HNw17l-PtdVgcMcWnCsZndGEWVjin3Oz'),
        )
    ),
    (
        '../datasets/ego-Facebook',
        (
            ('ego-Facebook', '1HcDGtLakSWbjOT4kfW2bOXWBHYTUk0np'),
        )
    ),
    (
        '../datasets/com-Youtube',
        (
            ('com-Youtube', '1HqNsOrAW-NMzwXMqBgxtMmDQJvHweUre'),
        )
    )
)


if __name__ == '__main__':
    for output_dir, files in datasets:
        os.makedirs(output_dir, exist_ok=True)

        for file_base, drive_id in files:
            gdd.download_file_from_google_drive(file_id=drive_id,
                                                dest_path='{}/{}.zip'.format(output_dir, file_base),
                                                unzip=True, showsize=True)

            data_files = get_txt_files('{}/{}/'.format(output_dir, file_base))

            # read lines
            lines = []
            for data_file in data_files:
                with open(data_file) as file:
                    lines += file.readlines()

            shutil.rmtree('{}/{}/'.format(output_dir, file_base))

            subsets = [
                (100.0, '100'),
                (75.0, '75'),
                (50.0, '50'),
                (25.0, '25'),
                (10.0, '10'),
                (5.0, '5'),
                (1.0, '1'),
                (0.1, '01'),
                (0.01, '001'),
            ]

            num_lines = len(lines)

            for percent, suffix in subsets:
                k = int(num_lines * percent / 100.0)

                i = 0
                reservoir = ['x'] * k

                for line in lines:
                    if i < k:
                        reservoir[i] = line
                    else:
                        j = random.randrange(i + 1)
                        if j < k:
                            reservoir[j] = line

                    i += 1

                os.makedirs('{}/{}_{}/'.format(output_dir, file_base, suffix), exist_ok=True)
                with open('{}/{}_{}/data.txt'.format(output_dir, file_base, suffix), 'w') as new_f:
                    for line in reservoir:
                        try:
                            source_id, target_id = line.split()
                            new_f.write('{},{}\n'.format(source_id, target_id))
                        except:
                            print('Error in line > {}'.format(line))