import pandas as pd
import numpy as np
import _number_of_country
import _quantile_adaptation as qa

read_for_country_name = 'test.xlsx'
read = 'indicator_score_final.xlsx'
output = 'final_score.xlsx'
number_country = _number_of_country.number_country


# Read the Excel file header
# Note: Update 'your_file.xlsx' to the path of your Excel file.
dfcca = pd.read_excel(read_for_country_name)
selected_columns = pd.read_excel(read)

added_columns = dfcca.filter(regex='cca3$').drop(0).drop(number_country+1).reset_index(drop=True)
selected_columns['cca3'] = added_columns['cca3']
pillar_breakdown = {'P1': ["D1", "D2", "D3"], 'P2': ["D4", "D5"], 'P3': ["D6", "D7", "D8", "D9", "D10", "D11", "D12"],
                    'P4': ["D13", "D14", "D15", "D16", "D17", "D18"]}
dimension_breakdown = {'D1': ['D1.1', 'D1.2', 'D1.3', 'D1.4'], 'D2': ['D2.1', 'D2.2'], 'D3': ['D3.1', 'D3.2', 'D3.3'], 'D4': ['D4.1'], 'D5': ['D5.1', 'D5.2'], 'D6': ['D6.1', 'D6.2', 'D6.3', 'D6.4'], 'D7': ['D7.1'], 'D8': ['D8.1'], 'D9': ['D9.1', 'D9.2'], 'D10': ['D10.1'], 'D11': ['D11.1', 'D11.2', 'D11.3', 'D11.4'], 'D12': ['D12.1', 'D12.2'], 'D13': ['D13.1', 'D13.2'], 'D14': ['D14.1', 'D14.2'], 'D15': ['D15.1', 'D15.2', 'D15.3'], 'D16': ['D16.1', 'D16.2'], 'D17': ['D17.1'], 'D18': ['D18.1', 'D18.2']}
total_score_breakdown = {'Sum': ['P1', 'P2', 'P3', 'P4']}


def average_by_scheme(data, scheme):
    df = pd.DataFrame({})
    df['cca3'] = data['cca3']
    for key in scheme:
        df[key] = data[scheme[key]].mean(axis=1)
    for index, row in df.iterrows():
        for key in scheme:
            df.loc[index, key] = round(df.loc[index, key], 1)
    print(df)
    return df


def standardize_and_clip(data):
    """
    Standardize the input data array using the provided mean and standard deviation,
    and then clip values to be within the range [0, 100].

    Parameters:
    data (np.array): The input data array.
    mean (float): The mean value used for standardization.
    std (float): The standard deviation used for standardization.

    Returns:
    np.array: The standardized and clipped data array.
    """
    mean = np.mean(data[0:14])

    # Calculate the standard deviation of the data
    std = np.std(data[0:14], ddof=1)
    # Standardize data
    standardized_data = list(map(lambda x: (25 * (x - mean) / std) + 50, data))
    # Clip data to be within the range of 0 to 100
    clipped_data = np.clip(standardized_data, 0, 100)
    return clipped_data


if __name__ == '__main__':
    dimension_score = average_by_scheme(selected_columns, dimension_breakdown)
    for column in dimension_score.columns:
        if column != 'cca3' and column not in pillar_breakdown['P3'] and column not in ['D5']:
            data = [round(x, 1) for x in standardize_and_clip(dimension_score[column].tolist()).tolist()]
            print(f'column:{column}: data:{data}')
            dimension_score[column] = data
    dimension_score_negative_D4 = dimension_score.copy()
    dimension_score_negative_D4['D4'] = 100 - dimension_score_negative_D4['D4']
    pillar_score = average_by_scheme(dimension_score_negative_D4, pillar_breakdown)
    total_score = average_by_scheme(pillar_score, total_score_breakdown)

    merged_df = pd.merge(dimension_score, pillar_score, on='cca3', how='inner')
    # Merge the result with df3
    final_merged_df = pd.merge(merged_df, total_score, on='cca3', how='inner')
    final_merged_df.to_excel(output)