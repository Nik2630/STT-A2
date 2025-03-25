import matplotlib.pyplot as plt

# Data from the Speedup Ratios table in the report
speedup_data = {
    'Sequential': 1.00,
    'run-parallel\nauto threads': 0.04,
    'run-parallel\n1 thread': 0.66,
    'xdist\nauto processes\nload dist': 0.55,
    'xdist\nauto processes\nno dist': 0.56,
    'xdist\n1 process\nload dist': 0.57,
    'xdist\n1 process\nno dist': 0.60,
    'Combined\nauto processes+\nauto threads': 0.06,
}

configurations = list(speedup_data.keys())
speedup_ratios = list(speedup_data.values())

# Create a bar chart
plt.figure(figsize=(10, 6))  # Adjust figure size as needed
plt.bar(configurations, speedup_ratios, color='skyblue')

# Add labels and title
plt.xlabel('Parallelization Configuration')
plt.ylabel('Speedup Ratio (Tseq / Tpar)')
plt.title('Speedup Ratios for Different Parallelization Modes')
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability
plt.axhline(y=1.0, color='r', linestyle='--', linewidth=0.8, label='Sequential Baseline (Speedup = 1.0)') # Baseline

# Add value labels on top of bars (optional, for better readability)
for i, ratio in enumerate(speedup_ratios):
    plt.text(i, ratio + 0.01, f'{ratio:.2f}', ha='center', va='bottom') # Adjust vertical offset (0.01) as needed

plt.legend()
plt.tight_layout()  # Adjust layout to prevent labels from being cut off
plt.grid(axis='y', linestyle='--', alpha=0.7) # Add horizontal grid lines
plt.ylim(0, 1.2) # Set y-axis limit to start from 0 and have some space above 1.0

# Show the plot
plt.show()

# To save the plot to a file (e.g., PNG)
plt.savefig('speedup_ratios_plot.png')