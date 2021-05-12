import os
import random
import zipfile

if __name__ == '__main__':
    for dataset_dir in os.listdir('../datasets'):
        dataset_dir_path = os.path.join('../datasets', dataset_dir)
        ext_dir_path = '{}/ext'.format(dataset_dir_path)
        if os.path.isdir(dataset_dir_path):
            # extract zip
            with zipfile.ZipFile('{}/data.zip'.format(dataset_dir_path), 'r') as zip_ref:
                zip_ref.extractall(ext_dir_path)

            # read lines
            lines = []
            for data_file in os.listdir(ext_dir_path):
                if data_file.startswith('data'):
                    with open('{}/{}'.format(ext_dir_path, data_file)) as file:
                        lines += file.readlines()

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

                with open('{}/{}.txt'.format(dataset_dir_path, suffix), 'w') as new_f:
                    for line in reservoir:
                        try:
                            parts = line.split()
                            source_id, target_id = int(parts[0]), int(parts[1])
                            new_f.write('{},{}\n'.format(source_id, target_id))
                        except:
                            print('Error in line > {}'.format(line))
