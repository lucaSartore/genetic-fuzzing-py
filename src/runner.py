from dataset.functions_list import FUNCTIONS, FunctionType
import subprocess
import resource
import os
import shutil
import pathlib
from itertools import product
from typing import get_args, cast

from concurrent.futures import ProcessPoolExecutor, as_completed

from strategy.strategy import StrategyEnum

MAX_WORKERS = 20  # Set your desired maximum number of parallel processes

def main():
    results = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(run_func, func["name"], strategy, True)
            for strategy, func in 
            # product(list[StrategyEnum](["random"]), FUNCTIONS[:2] ) # only random strategy for quick test
            product(get_args(StrategyEnum), FUNCTIONS[:2] ) # all strategies for full tests
        ]
        for future in as_completed(futures):
            func_name, stdout, stderr, returncode = future.result()
            results.append({
                "name": func_name,
                "stdout": stdout,
                "stderr": stderr,
                "returncode": returncode
            })
            print(f"Function: {func_name}, Return code: {returncode}")
            if returncode != 0:
                print(f"Error in function {func_name}:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
            #if stdout:
            #    print(f"STDOUT:\n{stdout}")
            #if stderr:
            #    print(f"STDERR:\n{stderr}")

def run_func(func: str, strategy: StrategyEnum, overwrite: bool = False):
    # add here additional limits if needed
    def set_limits():
        # Limit memory, CPU time, etc.
        resource.setrlimit(resource.RLIMIT_AS, (12*1024*1024*1024, 12*1024*1024*1024))  # 12GB
        
    log_dir = f"./results/{func}/{strategy}"

        
    if os.path.exists(log_dir) and overwrite:
        shutil.rmtree(log_dir)

    if not os.path.exists(log_dir):
        pathlib.Path(log_dir).mkdir(parents=True, exist_ok=True)
        
    result = subprocess.run(
        [
            "python",
            "dummy_wrapper.py",
            "--function",
            func,
            "--strategy",
            strategy,
            "--logdir",
            log_dir
        ],
        capture_output=True, text=True, #preexec_fn=set_limits
    )

    with open(f"{log_dir}/stderr.log", "w") as f:
        f.write(result.stderr)
    with open(f"{log_dir}/stdout.log", "w") as f:
        f.write(result.stdout)
    with open(f"{log_dir}/returncode.txt", "w") as f:
        f.write(str(result.returncode))

    return func, result.stdout, result.stderr, result.returncode

if __name__ == "__main__":
    main()
