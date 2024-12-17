import pandas as pd
import plotly.graph_objects as go
import os
import plotly.io as pio

pio.renderers.default = "browser"

# Define the path to the Excel file
file_path = "data/radar_DoE_RSM.xlsx"
# Define the figure size in cm
figure_width_cm = 20  # Set desired figure width in cm
figure_height_cm = 15  # Set desired figure height in cm
# Convert figure size from cm to inches (1 inch = 2.54 cm)
figure_width_inch = figure_width_cm / 2.54
figure_height_inch = figure_height_cm / 2.54

# Load the Excel file
data = pd.read_excel(file_path, header=None)

# Extract the title of the radar chart
title = data.iloc[0, 1]

# Extract the categories (from the first column, skipping the title row)
categories = data.iloc[2:, 0].tolist()

# Extract the series of data (columns B onwards)
series_names = data.iloc[1, 1:].tolist()  # Series names in the second row
values = data.iloc[2:, 1:].values  # Values starting from the third row

# Create the radar chart
fig = go.Figure()

# Add a trace for each series of data
for i, series_name in enumerate(series_names):
    fig.add_trace(
        go.Scatterpolar(
            r=values[:, i], theta=categories, fill="toself", name=series_name
        )
    )

# Update layout for better visualization
fig.update_layout(
    title=title,
    polar=dict(
        radialaxis=dict(
            visible=True, range=[0, max(map(max, values)) + 1]  # Auto-scaling the range
        )
    ),
    showlegend=True,
    legend=dict(
        # orientation="h",  # Horizontal legend
        # x=0.5,  # Center the legend horizontally
        # xanchor="center",
        # y=-0.15,  # Move the legend below the plot
        # yanchor="bottom",
        # tracegroupgap=2,  # Gap between legend groups
        # font=dict(size=12),  # Font size of the legend
        bgcolor="rgba(255, 255, 255, 0)",  # Transparent background for legend
        bordercolor="Black",  # Border color of the legend
        borderwidth=1,
        itemsizing="constant",
        # Make the legend 2-column
        itemclick="toggleothers",
    ),
    width=figure_width_inch * 100,  # Set the figure width (in pixels)
    height=figure_height_inch * 100,  # Set the figure height (in pixels)
)

# Generate the PDF file path by replacing '.xlsx' with '.pdf'
output_file = os.path.splitext(file_path)[0]

# Save the figure to a PDF file
fig.write_image(output_file + ".pdf", format="pdf")
fig.write_image(output_file + ".png", format="png")


# Show the radar chart
fig.show()

print(f"Figure saved as: {output_file}")
