import re
import pandas as pd
import _number_of_country

number_country = _number_of_country.number_country
read = 'transformed_data.xlsx'
output = 'transformed_data2.xlsx'

df = pd.read_excel(read)
new_df = df.iloc[[0, number_country+1]].copy()
print(new_df)
df = df.drop([0, number_country+1])

# Augmentation scheme as defined
augmentation_scheme = {
    'ppl': ['D1.1', 'D1.2', 'D1.4', 'D2.1', 'D2.2'],
    'gdp': ['D1.3', 'D2.3', 'D3.1', 'D3.2', 'D3.3', 'D4.1', 'D6.4', 'D18.2'],
    'pro': ['D16.1', 'D16.2'],
    'art': ['D17.1', 'D18.1']
}

# Function to determine the appropriate division column
def find_divisor(dimension):
    for key, values in augmentation_scheme.items():
        if any(dimension == v.replace(',', '.') for v in values):  # Ensure format consistency
            return key
    return None

if __name__ == '__main__':
    # Process the DataFrame to add new columns
    for col in df.columns:
        if '_' in col:
            # print(col.split('_'))
            if col.split('_')[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
                base = col.split('_')[0]
                dimension = col.split('_')[1]
                dimension = dimension.replace(',', '.')  # Adjusting the dimension format to match the scheme
                divisor = find_divisor(dimension)
                if divisor and divisor in df.columns:
                    new_col_name = f"{base}_{dimension}/{divisor}"
                    df[new_col_name] = df[col] / df[divisor]

    # Show the modified DataFrame

    df = pd.concat([df,new_df])
    # df.reset_index()
    df.drop(columns='a_D17.1/art')
    df.to_excel(output, index=False)
    print(df)

    # Regular expression to match the pattern 'letter_Dnumber.number'
    pattern = re.compile(r'^[a-z]_D\d+\.\d+')

    # Dictionary to hold dimension mappings
    dimension_dict = {}

    # Iterate over column names
    for col in df.columns:
        match = pattern.match(col)
        if match:
            # Extract dimension
            dimension = re.search(r'D\d+\.\d+', col).group()
            # Append the column name to the corresponding dimension list in the dictionary
            if dimension in dimension_dict:
                dimension_dict[dimension].append(col)
            else:
                dimension_dict[dimension] = [col]



    # Print the resulting dictionary
    print(dimension_dict)