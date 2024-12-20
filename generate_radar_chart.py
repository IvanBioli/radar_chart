import pandas as pd
import plotly.graph_objects as go
import os
import plotly.io as pio
import numpy as np

pio.renderers.default = "browser"

# List of file paths for multiple Excel files
file_paths = ["data/radar_DoE_FFT.xlsx", "data/radar_DoE_RSM.xlsx"]

# Define the figure size in cm
figure_width_cm = 17  # Set desired figure width in cm
figure_height_cm = 12  # Set desired figure height in cm
# Convert figure size from cm to inches (1 inch = 2.54 cm)
figure_width_inch = figure_width_cm / 2.54
figure_height_inch = figure_height_cm / 2.54

# Initialize a global list for categories to maintain consistent order
global_categories = []

# First pass: Collect all unique categories in their global order
for file_path in file_paths:
    data = pd.read_excel(file_path, header=None)
    categories = data.iloc[2:, 0].tolist()
    for cat in categories:
        if cat not in global_categories:
            global_categories.append(cat)
global_theta = list(np.linspace(0, 360, len(global_categories) + 1))
global_theta = global_theta[:-1]

# Step 2: Adjust positions for the first file's categories
data_first = pd.read_excel(file_paths[0], header=None)
first_file_categories = data_first.iloc[2:, 0].tolist()

# Determine positions for the first file's categories using only the initial `global_theta`
adjusted_theta = [None] * len(global_categories)

# Assign angles for categories in the first file
for i, cat in enumerate(first_file_categories):
    idx = global_categories.index(cat)
    adjusted_theta[idx] = global_theta[i]

# Fill remaining angles for other categories, preserving order and using remaining angles from `global_theta`
remaining_categories = [
    cat for cat in global_categories if cat not in first_file_categories
]
remaining_angles = [angle for angle in global_theta if angle not in adjusted_theta]

for cat in remaining_categories:
    idx = global_categories.index(cat)
    adjusted_theta[idx] = remaining_angles.pop(0)

# Final `global_theta` after adjustment
global_theta = adjusted_theta

# Process each file path
for file_path in file_paths:
    # Load the Excel file
    data = pd.read_excel(file_path, header=None)

    # Extract the title of the radar chart
    title = data.iloc[0, 1]

    # Extract the categories and their corresponding values
    file_categories = data.iloc[2:, 0].tolist()
    series_names = data.iloc[1, 1:].tolist()  # Series names in the second row
    values = data.iloc[2:, 1:].values  # Values starting from the third row

    # Align categories and values to the global order
    aligned_values = []
    theta_vec = []
    labels = []
    for i, global_cat in enumerate(global_categories):
        if global_cat in file_categories:
            idx = file_categories.index(global_cat)
            aligned_values.append(values[idx, :])
            theta_vec.append(global_theta[i])
            labels.append(global_cat)

    aligned_values = pd.DataFrame(aligned_values).values  # Convert to numpy array

    # Create the radar chart
    fig = go.Figure()

    # Add a trace for each series of data
    for i, series_name in enumerate(series_names):
        fig.add_trace(
            go.Scatterpolar(
                r=aligned_values[:, i],
                theta=theta_vec,
                fill="toself",
                name=series_name,
            )
        )

    # Update layout for better visualization
    fig.update_layout(
        title=title,
        polar=dict(
            angularaxis=dict(
                tickmode="array",  # Custom tick mode
                tickvals=theta_vec,  # Use angles for tick positions
                ticktext=labels,  # Use category names as tick labels
            ),
            radialaxis=dict(
                visible=True,
                range=[0, max(map(max, aligned_values)) + 1],  # Auto-scaling the range
            ),
        ),
        showlegend=True,
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0)",  # Transparent background for legend
            bordercolor="Black",  # Border color of the legend
            borderwidth=1,
        ),
        width=figure_width_inch * 100,  # Set the figure width (in pixels)
        height=figure_height_inch * 100,  # Set the figure height (in pixels)
    )

    # Generate the output file paths by replacing '.xlsx' with '.pdf'
    output_file = os.path.splitext(file_path)[0]

    # Save the figure to multiple file formats
    fig.write_image(output_file + ".pdf", format="pdf")
    fig.write_image(output_file + ".png", format="png")
    fig.write_image(output_file + ".jpg", format="jpg")
    fig.write_image(output_file + ".jpeg", format="jpeg")

    # Show the radar chart
    fig.show()

    print(f"Figure saved as: {output_file}")
