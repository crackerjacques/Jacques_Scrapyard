import numpy as np
import soundfile as sf
import argparse
from scipy.signal import resample


# This script is audio interface jitter simulator
# python -i your_file.wav -o your_result.wav -d 0.1 -p 0.1 -j 0.1


def apply_jitter(input_file, output_file, jitter_random_microsec=0, jitter_deterministic_microsec=0, jitter_periodic_microsec=0):

    data, rate = sf.read(input_file, always_2d=True)

    file_info = sf.info(input_file)
    file_subtype = file_info.subtype

    upsample_factor = 16 
    upsampled_rate = rate * upsample_factor
    upsampled_data = resample(data, len(data) * upsample_factor, axis=0)

    jitter_random_samples = jitter_random_microsec * upsampled_rate / 1e6 
    jitter_deterministic_samples = jitter_deterministic_microsec * upsampled_rate / 1e6  
    jitter_periodic_samples = jitter_periodic_microsec * upsampled_rate / 1e6  

    jitter_random = np.random.normal(0, jitter_random_samples, len(upsampled_data))
    jitter_deterministic = np.full(len(upsampled_data), jitter_deterministic_samples)
    jitter_periodic = jitter_periodic_samples * np.sin(2 * np.pi * np.arange(len(upsampled_data)) / len(upsampled_data))

    jittered_data = np.zeros_like(upsampled_data)
    for i in range(len(upsampled_data)):
        jitter_total = jitter_random[i] + jitter_deterministic[i] + jitter_periodic[i]
        if i + jitter_total < len(upsampled_data) and i + jitter_total > 0:
            jittered_data[i] = upsampled_data[int(i + jitter_total)]

    downsampled_data = resample(jittered_data, len(data), axis=0)
    sf.write(output_file, downsampled_data, rate, subtype=file_subtype)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply jitter to an audio file.")
    parser.add_argument("-i", "--input", help="The input wav file.", required=True)
    parser.add_argument("-o", "--output", help="The output wav file.", required=True)
    parser.add_argument("-j", "--jitter", type=float, help="The strength of the random jitter in microseconds.", default=0)
    parser.add_argument("-d", "--deterministic", type=float, help="The strength of the deterministic jitter in microseconds.", default=0)
    parser.add_argument("-p", "--periodic", type=float, help="The strength of the periodic jitter in microseconds.", default=0)

    args = parser.parse_args()

    apply_jitter(args.input, args.output, args.jitter, args.deterministic, args.periodic)
