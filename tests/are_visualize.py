# Sketch construction time charts

import json
import os
from datetime import datetime as dtt

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from sketches import Sketches

if __name__ == '__main__':
    profiles = [
        (
            '512kb'
        ),
        (
            '2mb'
        ),
        (
            '8mb'
        ),
        (
            '32mb'
        )
    ]

    results = []

    for profile_id, sketches in profiles:
        os.makedirs(os.path.dirname('../output/are/{}.json'.format(profile_id)), exist_ok=True)
        with open('../output/are/{}.json'.format(profile_id)) as file:
            output = json.load(file)
            results.append(output)

    matplotlib.rcParams['figure.dpi'] = 500



    plt.savefig('../output/sketch_time/sketch_time.png')
    plt.show()
