from dataset.functions_list import FUNCTIONS
import subprocess
import resource
from concurrent.futures import ProcessPoolExecutor, as_completed

MAX_WORKERS = 20  # Set your desired maximum number of parallel processes

def run_func(func):
    # add here additional limits if needed
    def set_limits():
        # Limit memory, CPU time, etc.
        resource.setrlimit(resource.RLIMIT_AS, (12*1024*1024*1024, 12*1024*1024*1024))  # 12GB
        
    result = subprocess.run(
        ["python", "dummy_wrapper.py", func["name"]],
        capture_output=True, text=True, #preexec_fn=set_limits
    )
    return func["name"], result.stdout, result.stderr, result.returncode

if __name__ == "__main__":
    results = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(run_func, func) for func in FUNCTIONS]
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