import os
import pandas as pd

def process_folder(folder_path):
    """
    Process all CSV files in the given folder by adding a 'Street' column.
    The 'Street' column is extracted from the 'Address' column by:
      - Taking the first part of the address before a comma.
      - Removing any extra spaces.
      - Removing any leading numbers and the spaces that follow them.
      
    The original CSV files are overwritten with the modified data.

    Args:
        folder_path (str): The path to the folder containing CSV files.
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            try:
                # Load the CSV file
                df = pd.read_csv(file_path)

                # Ensure 'Address' column exists
                if 'Address' not in df.columns:
                    print(f"Skipping {file_name}: 'Address' column not found.")
                    continue

                # Extract the street name:
                # - Split at the first comma
                # - Remove extra whitespace
                # - Remove leading numbers and any following whitespace
                df['Street'] = (
                    df['Address']
                    .str.split(',').str[0]
                    .str.strip()
                    .str.replace(r'^\d+\s*', '', regex=True)
                )

                # Overwrite the original CSV file with the modified DataFrame
                df.to_csv(file_path, index=False)
                print(f"Processed {file_name} successfully.")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    # Update this path to the directory containing your CSV files
    folder_path = "/Users/eduardodecastilhosgimenis/Desktop/Everything/programming/python_programming/MapsApp/files_to_filter"
    process_folder(folder_path)
