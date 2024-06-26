import pandas as pd
import os
import zipfile
import time

def convert_excel_to_dat_zip(excel_file_path):
    # Start time
    start_time = time.time()
    
    # Read Excel file
    xls = pd.ExcelFile(excel_file_path)
    
    # Output file paths
    dat_file_path = os.path.join(os.path.dirname(excel_file_path), "Worker.dat")
    zip_file_path = os.path.join(os.path.dirname(excel_file_path), "Worker.zip")
    
    # Initialize data size variables
    excel_data_size = os.path.getsize(excel_file_path)
    dat_data_size = 0
    
    # Open .dat file in write mode
    with open(dat_file_path, 'w', encoding='utf-8') as dat_file:
        # Iterate through each sheet
        for sheet_name in xls.sheet_names:
            # Read sheet into DataFrame
            df = xls.parse(sheet_name)
            
            # Convert DataFrame to pipe-delimited string
            dat_content = df.to_csv(index=False, sep='|', na_rep='')  # Removed terminator to avoid errors
            
            # Write sheet content to .dat file
            dat_file.write(dat_content)
            
            # Update data size
            dat_data_size += len(dat_content.encode('utf-8'))
    
    # Compress .dat file into a .zip file
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(dat_file_path, os.path.basename(dat_file_path))
    
    # End time
    end_time = time.time()
    
    # Output text file with relevant information
    output_text = f"""Conversion Summary:
    - Excel File Size: {excel_data_size} bytes
    - .dat File Size: {dat_data_size} bytes
    - .zip File Size: {os.path.getsize(zip_file_path)} bytes
    - Runtime: {end_time - start_time:.2f} seconds"""
    
    output_text_path = os.path.join(os.path.dirname(excel_file_path), "Conversion_Summary.txt")
    with open(output_text_path, 'w') as text_file:
        text_file.write(output_text)

# Example usage
if __name__ == "__main__":
    excel_file_path = r"Your excel file path.xlsx"
    convert_excel_to_dat_zip(excel_file_path)
