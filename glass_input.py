import pandas as pd
import subprocess
import os
import shutil

# Define the path to your Fortran executable and input file
fortran_executable = "path_to_your_executable"
input_file = 'start.inp'
output_dir = "output_files"  # Directory to store all output folders

# Load the glass composition table from a CSV file
# The CSV should now include a "density" column
compositions_df = pd.read_csv('glass_compositions.csv')

def update_input_file(comp):
    """Update the composition and density lines in start.inp file."""
    # Read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Update the composition lines
    lines[2] = f"SiO2    {comp['SiO2']}\n"
    lines[3] = f"Al2O3   {comp['Al2O3']}\n"
    lines[4] = f"B2O3    {comp['B2O3']}\n"
    lines[5] = f"P2O5    {comp['P2O5']}\n"
    lines[6] = f"ZrO2    {comp['ZrO2']}\n"
    lines[7] = f"Na2O    {comp['Na2O']}\n"
    lines[8] = f"CaO     {comp['CaO']}\n"
    lines[9] = f"SrO     {comp['SrO']}\n"
    lines[10] = f"Li2O    {comp['Li2O']}\n"
    lines[11] = f"K2O     {comp['K2O']}\n"
    lines[12] = f"MgO     {comp['MgO']}\n"
    lines[13] = f"BaO     {comp['BaO']}\n"
    lines[14] = f"ZnO     {comp['ZnO']}\n"
    lines[15] = f"Y2O3    {comp['Y2O3']}\n"

    # Update the density line (assuming it's on line 19 in your input file)
    lines[19] = f"density {comp['density']}\n"
    
    # Write the updated lines back to the input file
    with open(input_file, 'w') as file:
        file.writelines(lines)

def run_fortran_executable(run_index):
    """Run the Fortran executable and save output files in a new folder."""
    # Create a unique directory to store the output files
    run_folder = os.path.join(output_dir, f"run_{run_index}")
    os.makedirs(run_folder, exist_ok=True)
    
    # Run the Fortran executable
    subprocess.run([fortran_executable, input_file])
    
    # Move generated output files to the run_folder (customize based on output file names)
    for filename in os.listdir():
        if filename.startswith("output"):  # Replace with actual output filename pattern
            shutil.move(filename, os.path.join(run_folder, filename))

# Iterate over each row (glass composition) in the CSV file
for index, row in compositions_df.iterrows():
    update_input_file(row)  # Update the input file with the current composition and density
    run_fortran_executable(index)  # Run the Fortran executable and save files in a unique folder
