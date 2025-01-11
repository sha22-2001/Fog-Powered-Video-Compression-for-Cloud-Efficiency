import csv
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
import random
import shutil  # To copy the file to another location

# Read data from the TXT file
txt_file = "Analyse_Data()/detected_objects/D@ta/13-05-24.txt"  # Replace with the path to your TXT file
with open(txt_file, "r") as file:
    data = file.readlines()

# Split the date and time components
data = [line.strip().split(" - ") for line in data]

# Create a DataFrame with the data
df = pd.DataFrame(data, columns=["Class", "Number of Class", "Date", "Time"])

# Sort the DataFrame by 'Class' and 'Time'
df.sort_values(by=["Class", "Time"], inplace=True)

# Save the data to a CSV file
csv_file = 'Analyse_Data()/data_to_table.csv'
df.to_csv(csv_file, index=False)

# Read the CSV file
df_csv = pd.read_csv(csv_file)

# Create a line plot with separate colors for each group of classes
fig, ax = plt.subplots(figsize=(10, 6))

# Group the data by 'Class' and plot each group with a different color
for label, group in df_csv.groupby('Class'):
    ax.plot(group.index, group['Number of Class'], label=f'Class {label}')

# Set labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Number of Classes')

# Add descriptions to the graph
ax.set_title('Wildlife Activity Over Time', fontsize=14, fontweight='bold')
ax.set_xlabel('Time of Day', fontsize=12)
ax.set_ylabel('Number of Sightings', fontsize=12)

# Simplify the x-axis to show specific intervals
x_ticks = list(range(0, len(df_csv), len(df_csv) // 4))  # Set intervals as needed
x_tick_labels = [df_csv['Time'][i] for i in x_ticks]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_tick_labels, rotation=45, ha='right')

# Add a legend
ax.legend(title="Wildlife Classes")

# Save the graph as an image file (e.g., PNG)
graph_file = "Analyse_Data()/time_vs_number.png"
plt.tight_layout()  # Ensures the graph is not cut off
plt.savefig(graph_file)

# Create a PDF document
pdf_file = "Analyse_Data()/report.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)

# Create a list to store the elements of the PDF
elements = []

# Add the graph image to the PDF
elements.append(Paragraph('Graph:', getSampleStyleSheet()['Heading1']))
elements.append(Spacer(1, 12))
image = Image(graph_file, width=6*inch, height=3*inch)
elements.append(image)

# Create a table to show class changes and time intervals
elements.append(Spacer(1, 24))
elements.append(Paragraph('Class Changes:', getSampleStyleSheet()['Heading1']))
elements.append(Spacer(1, 12))

# Filter the DataFrame to find class changes
class_changes = df_csv[df_csv['Number of Class'] != df_csv['Number of Class'].shift(1)][['Class', 'Number of Class', 'Time']]

# Convert the DataFrame to a list of lists for the table
table_data = [class_changes.columns.tolist()] + class_changes.values.tolist()

# Create a table with colored headers
table = Table(table_data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

elements.append(table)

# Find the point where 'Number of Class' is maximum
max_point = df_csv[df_csv['Number of Class'] == df_csv['Number of Class'].max()][['Class', 'Number of Class', 'Time']]

# Find the point where 'Number of Class' is minimum
min_point = df_csv[df_csv['Number of Class'] == df_csv['Number of Class'].min()][['Class', 'Number of Class', 'Time']]

# Create separate tables for max and min points
elements.append(Spacer(1, 24))
elements.append(Paragraph('Point with Maximum Number of Classes:', getSampleStyleSheet()['Heading1']))
elements.append(Spacer(1, 12))
max_table_data = [max_point.columns.tolist()] + max_point.values.tolist()
max_table = Table(max_table_data)
max_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

elements.append(max_table)

elements.append(Spacer(1, 24))
elements.append(Paragraph('Point with Minimum Number of Classes:', getSampleStyleSheet()['Heading1']))
elements.append(Spacer(1, 12))
min_table_data = [min_point.columns.tolist()] + min_point.values.tolist()
min_table = Table(min_table_data)
min_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

elements.append(min_table)

# Add a PageBreak to start a new page for random images
elements.append(PageBreak())

# Get the unique class types from the CSV data
class_types = df_csv['Class'].unique()

# Create a title for the new page that includes class types
images_title = 'Images: ' + ', '.join(class_types)
elements.append(Paragraph(images_title, getSampleStyleSheet()['Heading1']))
elements.append(Spacer(1, 12))

# Get 20 random image paths from a folder
image_folder = "Analyse_Data()/detected_objects"  # Replace with the actual path to your image folder
random_image_paths = random.sample(os.listdir(image_folder), 20)

# Create a table to display the random images in a grid
image_table_data = []
image_row = []
for image_path in random_image_paths:
    image = Image(os.path.join(image_folder, image_path), width=1.5*inch, height=1.5*inch)
    image_row.append(image)
    if len(image_row) == 5:  # Display 5 images in a row
        image_table_data.append(image_row)
        image_row = []

if image_row:
    image_table_data.append(image_row)

image_table = Table(image_table_data)
elements.append(image_table)

# Build the PDF document
doc.build(elements)

# Copy the PDF to another location
additional_pdf_location = "E:/Wild_life/static/Research/report.pdf"
shutil.copy(pdf_file, additional_pdf_location)

# Display the graph
plt.show()

print(f"Data from {txt_file} has been saved to {csv_file}")
print(f"Graph has been saved to {graph_file}")
print(f"PDF report has been saved to {pdf_file} and {additional_pdf_location}")
