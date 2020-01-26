import os
import random
import shutil

from google_drive_downloader import GoogleDriveDownloader as gdd

from common.utils import get_txt_files

datasets = (
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
    ),
    (
        '../datasets/unicorn-wget',
        (
            ('benign_base', '1-rmP2_vOgIU56husFP0AhHK3O3HjPi0d'),
            ('benign_streaming', '1-urTwbWoqmeI-Y4Blhq1Xi_qnh2zDUhR'),
            ('attack_base', '1-jcapoEm0lEri9sBHn5RvTkrnDvSo0QG'),
            ('attack_streaming', '1-nZMkgFLfRPXCGKX2yo62ykSn2FGAh6X'),
        )
    ),
    (
        '../datasets/soc-Pokec',
        (
            ('soc-Pokec', '1I4eespCmdknZ0zlgy-PuZELv0RexHfuV'),
        )
    ),
    (
        '../datasets/soc-RedditHyperlinks',
        (
            ('soc-RedditHyperlinks', '1I7Q09n58X4DIxfK3SDaQ1noo4T_DS7wt'),
        )
    ),
    (
        '../datasets/ego-Gplus',
        (
            ('ego-Gplus', '1IF6JI64ENfQXRxAW1vIjDYPimTlrcoFZ'),
        )
    ),
    (
        '../datasets/ca-AstroPh',
        (
            ('ca-AstroPh', '1IPT-O9dGo2q3Knkof9Knzx_6t65KlpwL'),
        )
    ),
    (
        '../datasets/cit-HepPh',
        (
            ('cit-HepPh', '1IahaJH4FybYu31gJRcFK8b8fanl7604X'),
        )
    ),
    (
        '../datasets/roadNet-CA',
        (
            ('roadNet-CA', '1IusD9nbXRxZRpQhYg1xR5cLQdA6q7xWT'),
        )
    ),
    (
        '../datasets/web-Google',
        (
            ('web-Google', '1J-LRZzFiIoMp46I6hoM8C5J33gNhTjtQ'),
        )
    ),
    (
        '../datasets/gen-random-simple',
        (
            ('gen-random-simple', '1MjYNufhJVBFaQMm8w9nPWftvR4PtJQp3'),
        )
    ),
    (
        '../datasets/gen-scale-free',
        (
            ('gen-scale-free', '1MdGHmlDO9dNtcETvLqjriNCnhFgqLloY'),
        )
    ),
    (
        '../datasets/gen-small-world',
        (
            ('gen-small-world', '1MTwJOTCyuil_JXIqopp0asLkLfvEtIh8'),
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