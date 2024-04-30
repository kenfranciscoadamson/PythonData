import pandas as pd
import os

def validate_data(source_file_name, target_file_name, output_file_name):
    # Get the path of the current script
    script_path = os.path.dirname(os.path.abspath(__file__))
    
    # Construct full file paths
    source_file = os.path.join(script_path, source_file_name)
    target_file = os.path.join(script_path, target_file_name)
    output_file = os.path.join(script_path, output_file_name)
    
    # Read Excel tables into pandas DataFrames
    source_df = pd.read_excel(source_file)
    target_df = pd.read_excel(target_file)
    
    # Use the first column as the primary key
    source_df['Key'] = source_df.iloc[:, 0].astype(str)
    target_df['Key'] = target_df.iloc[:, 0].astype(str)
    
    # Merge Source and Target DataFrames on the key column
    merged_df = pd.merge(target_df, source_df, on='Key', suffixes=('_target', '_source'), how='left')
    
    # Find rows with discrepancies
    discrepancies_rows = []
    for col in source_df.columns:
        if col != 'Key':  # Exclude the key column from comparison
            source_col = col + '_source'
            target_col = col + '_target'
            discrepancies_rows.append(merged_df[merged_df[source_col].fillna('').astype(str) != merged_df[target_col].fillna('').astype(str)])
    
    # Concatenate rows with discrepancies into a single DataFrame
    discrepancies_df = pd.concat(discrepancies_rows)
    
    # Drop duplicates to avoid repeating rows
    discrepancies_df.drop_duplicates(inplace=True)
    
    # Print the number of rows with discrepancies
    num_discrepancies = len(discrepancies_df)
    print(f"Number of rows with discrepancies: {num_discrepancies}\n")
    
    # Save rows with discrepancies to an output Excel file
    if num_discrepancies > 0:
        discrepancies_df.to_excel(output_file, index=False)
        print(f"Rows with discrepancies saved to {output_file}")
    else:
        print("No discrepancies found.")

# Example file names, adjust as necessary
source_file_name = 'Source.xlsx'
target_file_name = 'Target.xlsx'
output_file_name = 'Discrepancies.xlsx'

validate_data(source_file_name, target_file_name, output_file_name)
