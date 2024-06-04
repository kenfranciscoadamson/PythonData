import pandas as pd
import os
import time
import configparser
import re

def validate_data(config_file):
    # Start timing the execution
    start_time = time.time()

    # Load configuration settings
    config = configparser.ConfigParser()
    config.read(config_file)
    source_file_name = config.get('FILES', 'source_file_name')
    target_file_name = config.get('FILES', 'target_file_name')
    primary_keys = config.get('COLUMNS', 'primary_keys').split(',')

    # Define columns to exclude from validation using wildcard pattern
    exclude_columns_pattern = r'(?i)(LAST_UPDATE|LAST_UPDATED_BY|CREATED_BY|CREATION_DATE|CreatedBy|CreationDate|LastUpdatedBy|LastUpdateDate|SourceSystemId|SourceSystemOwner|SOURCE_SYSTEM_ID|SOURCE_SYSTEM_OWNER)'
    exclude_columns = [col for col in pd.read_excel(source_file_name, nrows=0).columns if re.search(exclude_columns_pattern, col)]

    # Get the path of the current script
    script_path = os.path.dirname(os.path.abspath(__file__))
    
    # Construct full file paths
    source_file = os.path.join(script_path, source_file_name)
    target_file = os.path.join(script_path, target_file_name)
    
    # Read Excel tables into pandas DataFrames excluding specified columns
    source_df = pd.read_excel(source_file, usecols=lambda col: col not in exclude_columns)
    target_df = pd.read_excel(target_file, usecols=lambda col: col not in exclude_columns)
    
    # Use specified columns as the primary keys
    source_df['Key'] = source_df[primary_keys].astype(str).agg('-'.join, axis=1)
    target_df['Key'] = target_df[primary_keys].astype(str).agg('-'.join, axis=1)
    
    # Merge Source and Target DataFrames on the key column using an outer join
    merged_df = pd.merge(target_df, source_df, on='Key', suffixes=('_target', '_source'), how='outer')
    
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
    
    # Validate the presence of expected columns and prepare the final column list
    available_columns = discrepancies_df.columns.tolist()
    
    # Ensure primary keys are actually in the DataFrame
    primary_key_columns = ['Key'] + [pk for pk in primary_keys if pk in available_columns]
    
    # Prepare non-excluded columns ensuring they exist in the DataFrame
    main_columns = sorted([col for col in available_columns if col != 'Key' and ('_source' in col or '_target' in col)],
                          key=lambda x: x[:-7])  # Strip suffix to sort by base column name
    
    # Prepare excluded columns ensuring they exist in the DataFrame
    excluded_columns_sorted = sorted([col for col in available_columns if col in exclude_columns],
                                     key=lambda x: x.rsplit('_', 1)[0])
    
    # Combine them to form the final columns
    final_columns = primary_key_columns + main_columns + excluded_columns_sorted
    
    # Now reorder the DataFrame based on these columns
    discrepancies_df = discrepancies_df[final_columns]

    # Print the number of rows with discrepancies
    num_discrepancies = len(discrepancies_df)
    print(f"Number of rows with discrepancies: {num_discrepancies}\n")
    
    # Save rows with discrepancies to an output Excel file
    if num_discrepancies > 0:
        output_file_name = f"{os.path.splitext(source_file_name)[0]}_vs_{os.path.splitext(target_file_name)[0]}_Discrepancies.xlsx"
        output_file = os.path.join(script_path, output_file_name)
        discrepancies_df.to_excel(output_file, index=False)
        print(f"Rows with discrepancies saved to {output_file}")
    else:
        print("No discrepancies found.")
    
    # Print runtime
    end_time = time.time()
    print(f"Validation completed in {end_time - start_time:.2f} seconds")

# Config file path, adjust as necessary
config_file = 'Config.txt'

validate_data(config_file)
