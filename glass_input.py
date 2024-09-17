import pandas as pd
import subprocess
import os
import shutil

# Define the path to your Fortran executable and input file
fortran_executable = "./buck_modified_main_v5.6-lammps.x"
input_file = "./start.inp"
output_dir = "output_files"  # Directory to store all output folders

# Load the glass composition table from a CSV file
compositions_df = pd.read_csv('glass_compositions.csv')

def update_input_file(comp):
    """Update the composition, density, and nsize lines in start.inp file."""
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

    # Update the nsize line (assuming it's on line 20 in your input file)
    lines[16] = f"nsize {comp['nsize']}\n"

    # Update the density line (assuming it's on line 19 in your input file)
    lines[19] = f"density {comp['density']}\n"

    # Write the updated lines back to the input file
    with open(input_file, 'w') as file:
        file.writelines(lines)

def run_fortran_executable(glass_ID):
    """Run the Fortran executable and save output files in a new folder named with the glass ID."""
    # Create a directory named with the glass ID to store the output files
    run_folder = os.path.join(output_dir, f"{glass_ID}")
    os.makedirs(run_folder, exist_ok=True)
    
    # Run the Fortran executable
    subprocess.run([fortran_executable, input_file])
    
    # List of files to move
    output_files = ["in.lmp", "input.dat", "potential_B-O", "TABLE-lmp"]
    
    # Move generated output files to the run_folder
    for filename in output_files:
        if os.path.exists(filename):  # Check if file exists
            shutil.move(filename, os.path.join(run_folder, filename))

# Iterate over each row (glass composition) in the CSV file
for index, row in compositions_df.iterrows():
    glass_id = row[0]  # Assuming the first column contains the glass ID
    update_input_file(row)  # Update the input file with the current composition, density, and nsize
    run_fortran_executable(glass_id)  # Run the Fortran executable and save files in a folder named with the glass ID


