import os
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Set a professional style for the plots
sns.set_theme(style="whitegrid")

def generate_combined_bar_plot(results_dir: str, testcases: list, output_filename: str = "combined_final.png"):
    """
    Generate a combined bar plot for multiple test cases.
    
    Args:
        results_dir: Path to the results directory containing test case folders
        testcases: List of test case names to include in the plot
        output_filename: Name of the output file
    """
    testcase_data = {}
    
    for testcase in testcases:
        testcase_path = os.path.join(results_dir, testcase)
        if not os.path.isdir(testcase_path):
            print(f"Warning: Test case directory not found: {testcase}")
            continue
        
        strategies_data = {}
        skip_testcase = False
        
        for strategy in os.listdir(testcase_path):
            strategy_path = os.path.join(testcase_path, strategy)
            if not os.path.isdir(strategy_path):
                continue
            
            returncode_path = os.path.join(strategy_path, "returncode.txt")
            log_path = os.path.join(strategy_path, "log.csv")
            
            if not os.path.exists(returncode_path) or not os.path.exists(log_path):
                continue
            
            with open(returncode_path, "r") as f:
                return_code = int(f.read().strip())
                if return_code != 0:
                    skip_testcase = True
                    break
            
            data = pd.read_csv(log_path, header=None, skiprows=1, names=["step", "score"], dtype={"step": int, "score": float})
            strategies_data[strategy] = data["score"].iloc[-1]  # Get final score
        
        if skip_testcase or len(strategies_data) == 0:
            print(f"Skipping test case: {testcase}")
            continue
        
        testcase_data[testcase] = strategies_data
    
    if len(testcase_data) == 0:
        print("No valid test cases found.")
        return
    
    # Collect all strategy names
    all_strategies = set()
    for strategies_data in testcase_data.values():
        all_strategies.update(strategies_data.keys())
    all_strategies = sorted(all_strategies)
    
    # Prepare data for plotting
    testcase_names = list(testcase_data.keys())
    x_positions = np.arange(len(testcase_names))
    bar_width = 0.8 / len(all_strategies)
    
    # Create figure
    plt.figure(figsize=(12, 8))
    colors = sns.color_palette("viridis", len(all_strategies))
    
    for idx, strategy in enumerate(all_strategies):
        final_scores = []
        for testcase in testcase_names:
            if strategy in testcase_data[testcase]:
                final_scores.append(testcase_data[testcase][strategy])
            else:
                final_scores.append(0)
        
        offset = idx * bar_width - (len(all_strategies) - 1) * bar_width / 2
        plt.bar(x_positions + offset, final_scores, bar_width, 
               label=strategy, alpha=0.8, color=colors[idx])
    
    plt.xlabel("Test Case", fontsize=14)
    plt.ylabel("Final Coverage Percentage", fontsize=14)
    plt.title("Final Coverage Comparison", fontsize=16)
    plt.xticks(x_positions, testcase_names, rotation=0, ha='center', fontsize=12)
    plt.legend(fontsize=12)
    plt.ylim(0, 1.0)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    output_path = os.path.join(results_dir, output_filename)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Generated combined bar plot: {output_path}")


if __name__ == "__main__":
    results_dir = "/data/universita/master/2-1/Bio inspired Artificial Intelligence/results_/results_function_call_parity"
    testcases = ["count_bool30", "is_odd_for_dummys"]
    generate_combined_bar_plot(results_dir, testcases, "combined_count_bool30_is_odd.png")
