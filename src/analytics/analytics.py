import os
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import glob
import shutil

# Set a professional style for the plots
sns.set_theme(style="whitegrid")

def generate_graphs(results_dir: str = "../results"):
    single_test_analytics(results_dir)
    test_average_analytics(results_dir)
    move_charts(results_dir)


def test_average_analytics(results_dir: str):
    strategies_data = {}

    for testcase in os.listdir(results_dir):
        testcase_path = os.path.join(results_dir, testcase)
        if not os.path.isdir(testcase_path):
            continue

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
            data["normalized_step"] = data["step"] / data["step"].max()

            if strategy not in strategies_data:
                strategies_data[strategy] = []

            strategies_data[strategy].append(data)

        if skip_testcase:
            continue

    # Generate average progressive.png
    plt.figure(figsize=(12, 8))
    for strategy, data_list in strategies_data.items():
        all_normalized_steps = np.linspace(0, 1, 100)
        interpolated_scores = []

        for data in data_list:
            interpolated_score = np.interp(all_normalized_steps, data["normalized_step"], data["score"])
            interpolated_scores.append(interpolated_score)

        average_scores = np.mean(interpolated_scores, axis=0)
        plt.plot(all_normalized_steps, average_scores, label=strategy, linewidth=2)

    plt.xlabel("Normalized Step", fontsize=14)
    plt.ylabel("Average Coverage Percentage", fontsize=14)
    plt.title("Average Progressive Coverage Across Test Cases", fontsize=16)
    plt.legend(fontsize=12)
    plt.savefig(os.path.join(results_dir, "average_progressive.png"), dpi=300)
    plt.close()

    # Generate average final.png
    plt.figure(figsize=(12, 8))
    final_scores = {strategy: np.mean([data["score"].iloc[-1] for data in data_list]) for strategy, data_list in strategies_data.items()}
    sns.barplot(x=list(final_scores.keys()), y=list(final_scores.values()), hue=list(final_scores.keys()), palette="viridis", legend=False)
    plt.xlabel("Fuzzing Strategy", fontsize=14)
    plt.ylabel("Average Final Coverage Percentage", fontsize=14)
    plt.title("Average Final Coverage Across Test Cases", fontsize=16)
    plt.savefig(os.path.join(results_dir, "average_final.png"), dpi=300)
    plt.close()

def single_test_analytics(results_dir: str):

    for testcase in os.listdir(results_dir):
        testcase_path = os.path.join(results_dir, testcase)
        if not os.path.isdir(testcase_path):
            continue

        strategies = {}
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
            data["normalized_step"] = data["step"] / data["step"].max()
            strategies[strategy] = data

        if skip_testcase or len(strategies) == 0:
            continue

        # Generate progressive.png
        plt.figure(figsize=(12, 8))
        for strategy, data in strategies.items():
            plt.plot(data["normalized_step"], data["score"], label=strategy, linewidth=2)
        plt.xlabel("Normalized Step", fontsize=14)
        plt.ylabel("Coverage Percentage", fontsize=14)
        plt.title(f"Progressive Coverage for {testcase}", fontsize=16)
        plt.legend(fontsize=12)
        plt.savefig(os.path.join(testcase_path, "progressive.png"), dpi=300)
        plt.close()

        # Generate final.png
        plt.figure(figsize=(12, 8))
        final_scores = {strategy: data["score"].iloc[-1] for strategy, data in strategies.items()}
        sns.barplot(x=list(final_scores.keys()), y=list(final_scores.values()), hue=list(final_scores.keys()), palette="viridis", legend=False)
        plt.xlabel("Fuzzing Strategy", fontsize=14)
        plt.ylabel("Final Coverage Percentage", fontsize=14)
        plt.title(f"Final Coverage for {testcase}", fontsize=16)
        plt.savefig(os.path.join(testcase_path, "final.png"), dpi=300)
        plt.close()

def move_charts(
    root_dir: str, 
):
    filenames = ['final.png', 'progressive.png']

    target_dir= os.path.join(root_dir, 'all')

    os.makedirs(target_dir, exist_ok=True)
    print(f"Target directory '{target_dir}' is ready.")

    for filename in filenames:
        print(f"\n--- Processing: {filename} ---")
        
        # Build the glob pattern: 
        # root_dir/*/<filename> matches any file inside any immediate subdirectory of root_dir
        pattern = os.path.join(root_dir, '*', filename)
        
        # glob.iglob is memory efficient for large numbers of files
        for src_path in glob.iglob(pattern):
            # src_path will look like 'path/to/root/ProjectA/final.png'

            # 3. Extract the <NAME> part (e.g., 'ProjectA')
            # Get the directory of the file: 'path/to/root/ProjectA'
            name_dir = os.path.dirname(src_path)
            # Get the last part of the path (the <NAME> folder): 'ProjectA'
            name = os.path.basename(name_dir)

            # 4. Define the new destination path
            # New filename format: <NAME>_<filename> (e.g., ProjectA_final.png)
            new_filename = f"{name}_{filename}"
            # Full destination path: target_dir/ProjectA_final.png
            dest_path = os.path.join(target_dir, new_filename)

            try:
                # 5. Copy the file
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")
            except Exception as e:
                print(f"ERROR copying {src_path}: {e}")

if __name__ == "__main__":
    generate_graphs()
