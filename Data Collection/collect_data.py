#!/usr/bin/env python3

import multiprocessing as mp
import subprocess as sub
import sys
from functools import partial
import os

bench_arr = [1, 2, 3, 4]
benches = ["deepsjeng_r", "imagick_r", "nab_r", "xz_r"]

# OOO Benchmark
def run_bench_ooo(bench_num, config):
    command = f'./run_gem5_single {config} {bench_num}'
    try:
        dir_name = config.split(".")[0]
        output = sub.check_output([command], stderr=sub.PIPE, shell=True).decode("utf-8")
        print(output, file=sys.stderr)
        with open(f"output/{dir_name}/{benches[bench_num-1]}/stats.txt") as handle:
            for line in handle.readlines():
                if "system.cpu.numCycles" in line:
                    for s in line.split(' ')[1:]:
                        if s != "":
                            print(f"Found cycles: {s}", file=sys.stderr)
                            return s
                    break

    except sub.CalledProcessError as e:
        print('exit code: {}'.format(e.returncode))
        print('stdout: {}'.format(e.output.decode(sys.getfilesystemencoding())))
        print('stderr: {}'.format(e.stderr.decode(sys.getfilesystemencoding())))

# Main Code Starts here

# Variables
num_rob_entries = [16, 32, 64, 128, 256, 512, 1024]
num_iq_entries = [16, 32, 64, 128, 256, 512, 1024]
num_lq_entries = [16, 64, 128, 256, 512, 1024]
num_sq_entries = [16, 64, 128, 256, 512, 1024]
num_phys_reg = [64, 128, 256, 512, 1024, 2048]
cpu_width = [2, 4, 6, 8]

# Hardcode config files
config_files = []
for i in range(len(num_phys_reg)):
    for j in range(len(cpu_width)):
        config_files.append(f"test_{i}_{j}.cfg")

def execute_sim_config(i):
    try:
        # Get cycle count
        res = int(run_bench_ooo(4, config_files[i]))

        # Get power numbers
        config_file_name = config_files[i].split(".")[0]
        config_file_location = f"output/{config_file_name}/xz_r"
        print(config_file_location)
        sub.run(["./run_mcpat", config_file_location])

        # Parse power numbers
        power_file_loc = config_file_location + "/mcpat.txt"
        power_file = open(power_file_loc)
        content = power_file.readlines()
        power = float(content[12].strip().split(" ")[3])
        #print(power)

    except:
        res = 99999999999999
        power = 99999999999999.0

    return res, power

for rob in num_rob_entries:
    for iq in num_iq_entries:
        for lq in num_lq_entries:
            for sq in num_sq_entries:

                # We execute num_phys_reg and cpu width in parallel

                # Create Config Files
                for i in range(len(num_phys_reg)):
                    for j in range(len(cpu_width)):
                        with open(f"test_{i}_{j}.cfg", "w") as file:
                            file.write(f"--numROBEntries={rob} --numIQEntries={iq} --numLQEntries={lq} --numSQEntries={sq} --numPhysIntRegs={num_phys_reg[i]} --cpuWidth={cpu_width[j]}")

                # Run parallel
                with mp.Pool(len(num_phys_reg) * len(cpu_width)) as p:
                    # Run gem5 simulation
                    res = p.map(execute_sim_config, range(len(num_phys_reg) * len(cpu_width)))
                    print(res)

                    # Print results
                    for i in range(len(num_phys_reg)):
                        for j in range(len(cpu_width)):
                            perf = res[i * len(cpu_width) + j][0]
                            power = res[i * len(cpu_width) + j][1]
                            res_string = f"{rob},{iq},{lq},{sq},{num_phys_reg[i]},{cpu_width[j]},{perf},{power}\n"
                            print(res_string)
                            with open("param_sweep.txt", "a") as file:
                                file.write(res_string)
