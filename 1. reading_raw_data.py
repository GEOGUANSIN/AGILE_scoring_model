import pandas as pd
import re
import _number_of_country
read = 'test.xlsx'
output = 'transformed_data.xlsx'

df = pd.read_excel(read)
print([i for i in df.columns])


# Regular expressions and conditions
condition_1 = df.columns.str.contains('D')  # Columns containing 'D'
condition_2 = df.columns == 'cca3'           # Columns exactly named 'cca'
condition_3 = df.columns.str.contains('ppl|gdp|art|opr|pro', case=False, regex=True)
condition_4 = df.columns.str.match(r'^[a-z]\.\d+')  # Starts with a lowercase letter, followed by a dot and a number
condition_5 = df.columns.str.match(r'^[a-z]$')  # Single lowercase letter

# Combine conditions for column names
combined_conditions = condition_1 | condition_2 | condition_3 | condition_4 | condition_5

# Filter the DataFrame based on combined conditions
filtered_df = df.loc[:, combined_conditions]



def create_mapping():
    # Create lists for each letter with extensions .1 to .20
    letter_lists = {}
    for letter in "abcdefghijklmnopqrstuvwxyz":
        entries = [f"{letter}.{i}" for i in range(1, 51)]  # from a.1 to a.20
        entries.insert(0, letter)  # prepend the letter itself, e.g., 'a'
        letter_lists[letter] = entries
    return letter_lists


def map_dimensions(columns, letter_lists):
    # Initialize the transformation map
    transformation_map = {}
    # Pattern to capture dimension columns
    dim_pattern = re.compile(r'^D\d+')

    # Traverse through columns to map dimensions
    for i, col in enumerate(columns):
        if col in sum(letter_lists.values(), []):  # flatten list of lists and check if col is in any
            # Find the next dimension 'Dx' that follows
            for j in range(i + 1, len(columns)):
                if dim_pattern.match(columns[j]):
                    transformation_map[col] = f"{col.split('.')[0]}_{columns[j]}"
                    break

    return transformation_map


def transform_columns(columns):
    letter_lists = create_mapping()
    transformation_map = map_dimensions(columns, letter_lists)

    # Replace column names according to the transformation map
    new_columns = [transformation_map.get(col, col) for col in columns]
    return new_columns


if __name__ == "__main__":
    columns = filtered_df.columns
    new_columns = transform_columns(columns)
    result = list(zip(columns, new_columns))
    print(result)
    rename_dict = dict(result)
    print(rename_dict)
    filtered_df.rename(columns=rename_dict, inplace=True)
    print([i for i in filtered_df.columns])
    filtered_df.to_excel(output, index=False)
