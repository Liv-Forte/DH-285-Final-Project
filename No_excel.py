import os
from collections import Counter
import numpy as np
from PIL import Image
from colorthief import ColorThief
import plotly.graph_objects as go
from bs4 import BeautifulSoup

# Function to calculate Euclidean distance between two RGB colors
def color_distance(color1, color2):
    return np.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))

# Function to determine if a color is "black" (within a small threshold)
def is_black(color, threshold=50):
    return all(c < threshold for c in color)

# Base directory containing subfolders of images
base_directory = "/Users/oliviaforte/DH 285 Final Project/Video Game Data"

# Get all subdirectories (folders) in the base directory
subfolders = [f.path for f in os.scandir(base_directory) if f.is_dir()]

# Initialize a dictionary to store color palettes for each folder
folder_color_palettes = {}

# Iterate through each folder (subdirectory) and extract the color palettes
for subfolder in subfolders:
    folder_name = os.path.basename(subfolder)
    print(f"Processing folder: {folder_name}")

    # List to store all colors from the current folder
    all_colors = []

    # Get all image files in the folder (assuming jpg or png)
    image_files = [f for f in os.listdir(subfolder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Process each image in the folder
    for image_file in image_files:
        image_path = os.path.join(subfolder, image_file)

        # Skip images that are too small
        try:
            with Image.open(image_path) as img:
                if img.size[0] < 100 or img.size[1] < 100:
                    print(f"Skipping image {image_file} due to small size.")
                    continue
        except Exception as e:
            print(f"Error opening image {image_file}: {e}")
            continue

        try:
            # Extract the color palette using ColorThief
            color_thief = ColorThief(image_path)
            palette = color_thief.get_palette(color_count=6)  # Change the count if you want more colors

            # Filter out black colors and add the rest to the all_colors list
            for color in palette:
                if not is_black(color):
                    all_colors.append(color)
        except Exception as e:
            print(f"Error processing image {image_file}: {e}")
            continue

    # Now, we want to select the top 50 distinct colors for this folder
    # First, count the occurrences of each color
    color_counts = Counter(all_colors)

    # Create a list to store the distinct colors
    distinct_colors = []

    # Iterate through the color counts and add colors to the distinct_colors list if they are far enough apart
    for color, count in color_counts.most_common():
        # Check if this color is distinct enough from the already selected colors
        if not any(color_distance(color, selected_color) < 60 for selected_color in distinct_colors):
            distinct_colors.append(color)
        # Stop if we have collected 50 distinct colors
        if len(distinct_colors) >= 50:
            break

    # Store the distinct colors (in hex format) for this folder
    hex_colors = ['rgb' + str(color) for color in distinct_colors]
    folder_color_palettes[folder_name] = hex_colors

# Now we create a Plotly visualization for each folder's color palette
fig = go.Figure()

# For each folder, create a trace in the figure
for i, (folder_name, hex_colors) in enumerate(folder_color_palettes.items()):
    fig.add_trace(go.Bar(
        x=[f"{folder_name} - Color {i+1}" for i in range(len(hex_colors))],  # Unique labels for each color
        y=[1] * len(hex_colors),  # All bars will have the same height
        marker=dict(color=hex_colors),
        width=1,
        name=folder_name  # Add a legend entry for each folder
    ))

# Update layout for a cleaner view
fig.update_layout(
    title="Top 50 Distinct Dominant Colors from Each Image Folder",
    xaxis_title="Color Index",
    yaxis_title="Palette Colors",
    barmode='stack',  # Stack the colors in the bar
    showlegend=True,  # Show the legend for each folder
    plot_bgcolor='white',
    height=600
)

# Show the interactive plot
fig.show()

# Get the HTML code for the figure
html_str = fig.to_html()

# Use BeautifulSoup to pretty-print the HTML
soup = BeautifulSoup(html_str, 'html.parser')
pretty_html = soup.prettify()

# Save the pretty-printed HTML to a file
with open("color_palettes_by_folder.html", "w") as file:
    file.write(pretty_html)
