import os
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Set a professional style for the plots
sns.set_theme(style="whitegrid")

def generate_count_bool_plots(results_dir: str = "../results"):
    """
    Generate plots specifically for count_bool test cases.
    
    Args:
        results_dir: Path to the results directory containing test case folders
    """
    # Filter only count_bool test cases
    count_bool_data = {}
    
    for testcase in os.listdir(results_dir):
        if not testcase.startswith("count_bool"):
            continue
            
        testcase_path = os.path.join(results_dir, testcase)
        if not os.path.isdir(testcase_path):
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
            data["normalized_step"] = data["step"] / data["step"].max()
            strategies_data[strategy] = data
        
        if skip_testcase or len(strategies_data) == 0:
            continue
        
        count_bool_data[testcase] = strategies_data
        
        # Generate individual progressive plot for this test case
        plt.figure(figsize=(12, 8))
        colors = sns.color_palette("husl", len(strategies_data))
        for idx, (strategy, data) in enumerate(strategies_data.items()):
            plt.plot(data["normalized_step"], data["score"], label=strategy, linewidth=2, color=colors[idx])
        plt.xlabel("Normalized Step", fontsize=14)
        plt.ylabel("Coverage Percentage", fontsize=14)
        plt.title(f"Progressive Coverage for {testcase}", fontsize=16)
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(testcase_path, "progressive.png"), dpi=300)
        plt.close()
        print(f"Generated progressive plot for {testcase}")
        
        # Generate individual final coverage bar plot for this test case
        plt.figure(figsize=(12, 8))
        final_scores = {strategy: data["score"].iloc[-1] for strategy, data in strategies_data.items()}
        sns.barplot(x=list(final_scores.keys()), y=list(final_scores.values()), 
                   hue=list(final_scores.keys()), palette="viridis", legend=False)
        plt.xlabel("Fuzzing Strategy", fontsize=14)
        plt.ylabel("Final Coverage Percentage", fontsize=14)
        plt.title(f"Final Coverage for {testcase}", fontsize=16)
        plt.ylim(0, 1.0)
        plt.savefig(os.path.join(testcase_path, "final.png"), dpi=300)
        plt.close()
        print(f"Generated final coverage plot for {testcase}")
    
    if len(count_bool_data) == 0:
        print("No count_bool test cases found with valid results.")
        return
    
    # Generate combined progressive plot for all count_bool cases
    plt.figure(figsize=(14, 10))
    
    # Get total number of lines to plot
    total_lines = sum(len(strategies_data) for strategies_data in count_bool_data.values())
    colors = sns.color_palette("husl", total_lines)
    color_idx = 0
    
    for idx, (testcase, strategies_data) in enumerate(sorted(count_bool_data.items())):
        for strategy, data in strategies_data.items():
            plt.plot(data["normalized_step"], data["score"], 
                    label=f"{testcase} - {strategy}", linewidth=2, alpha=0.7, color=colors[color_idx])
            color_idx += 1
    
    plt.xlabel("Normalized Step", fontsize=14)
    plt.ylabel("Coverage Percentage", fontsize=14)
    plt.title("Progressive Coverage for All count_bool Test Cases", fontsize=16)
    plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "count_bool_combined_progressive.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated combined progressive plot for all count_bool cases")
    
    # Generate comparison plot: final coverage across different count_bool sizes
    plt.figure(figsize=(14, 8))
    
    # Organize data by strategy across different test cases
    strategy_names = set()
    for strategies_data in count_bool_data.values():
        strategy_names.update(strategies_data.keys())
    
    testcase_names = sorted(count_bool_data.keys())
    x_positions = np.arange(len(testcase_names))
    bar_width = 0.8 / len(strategy_names)
    colors = sns.color_palette("viridis", len(strategy_names))
    
    for idx, strategy in enumerate(sorted(strategy_names)):
        final_scores = []
        for testcase in testcase_names:
            if strategy in count_bool_data[testcase]:
                final_scores.append(count_bool_data[testcase][strategy]["score"].iloc[-1])
            else:
                final_scores.append(0)
        
        plt.bar(x_positions + idx * bar_width, final_scores, bar_width, 
               label=strategy, alpha=0.8, color=colors[idx])
    
    plt.xlabel("Test Case", fontsize=14)
    plt.ylabel("Final Coverage Percentage", fontsize=14)
    plt.title("Final Coverage Comparison Across count_bool Test Cases", fontsize=16)
    plt.xticks(x_positions + bar_width * (len(strategy_names) - 1) / 2, testcase_names, rotation=45, ha='right')
    plt.legend(fontsize=12)
    plt.ylim(0, 1.0)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "count_bool_final_comparison.png"), dpi=300)
    plt.close()
    print("Generated final coverage comparison plot")
    
    # Generate average progressive plot for count_bool cases
    plt.figure(figsize=(12, 8))
    
    strategies_aggregated = {}
    for testcase, strategies_data in count_bool_data.items():
        for strategy, data in strategies_data.items():
            if strategy not in strategies_aggregated:
                strategies_aggregated[strategy] = []
            strategies_aggregated[strategy].append(data)
    
    all_normalized_steps = np.linspace(0, 1, 100)
    colors = sns.color_palette("husl", len(strategies_aggregated))
    for idx, (strategy, data_list) in enumerate(strategies_aggregated.items()):
        interpolated_scores = []
        for data in data_list:
            interpolated_score = np.interp(all_normalized_steps, data["normalized_step"], data["score"])
            interpolated_scores.append(interpolated_score)
        
        average_scores = np.mean(interpolated_scores, axis=0)
        std_scores = np.std(interpolated_scores, axis=0)
        
        plt.plot(all_normalized_steps, average_scores, label=strategy, linewidth=2, color=colors[idx])
        plt.fill_between(all_normalized_steps, 
                        average_scores - std_scores, 
                        average_scores + std_scores, 
                        alpha=0.2, color=colors[idx])
    
    plt.xlabel("Normalized Step", fontsize=14)
    plt.ylabel("Average Coverage Percentage", fontsize=14)
    plt.title("Average Progressive Coverage for count_bool Test Cases", fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(results_dir, "count_bool_average_progressive.png"), dpi=300)
    plt.close()
    print("Generated average progressive plot for count_bool cases")
    
    # Generate summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS FOR count_bool TEST CASES")
    print("="*60)
    
    for testcase in sorted(count_bool_data.keys()):
        print(f"\n{testcase}:")
        strategies_data = count_bool_data[testcase]
        for strategy in sorted(strategies_data.keys()):
            data = strategies_data[strategy]
            final_coverage = data["score"].iloc[-1]
            max_coverage = data["score"].max()
            avg_coverage = data["score"].mean()
            print(f"  {strategy:20s} - Final: {final_coverage:.4f}, Max: {max_coverage:.4f}, Avg: {avg_coverage:.4f}")
    
    print("\n" + "="*60)
    print("All plots generated successfully!")
    print("="*60)

if __name__ == "__main__":
    generate_count_bool_plots()
