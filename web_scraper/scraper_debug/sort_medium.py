import pandas as pd

def main():
    input_file = 'for_medium.csv'
    output_file = 'for_medium_sorted.csv'

    print(f"Reading {input_file}...")
    try:
        df = pd.read_csv(input_file)
        
        print("Sorting by 'Column Name'...")
        # Sort values by Column Name, filling NaNs with empty string for consistent sorting if any
        df = df.sort_values(by='Column Name', na_position='last')
        
        print(f"Saving sorted data to {output_file}...")
        df.to_csv(output_file, index=False)
        print("Done!")
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")

if __name__ == "__main__":
    main()
