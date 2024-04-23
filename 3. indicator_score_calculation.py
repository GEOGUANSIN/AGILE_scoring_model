import pandas as pd
import numpy as np
import _quantile_adaptation as qa
import _number_of_country

number_country = _number_of_country.number_country
read = 'transformed_data2.xlsx'
output = 'indicator_score.xlsx'
indicator_scheme = {'D1.1': ['a_D1.1', 'b_D1.1', 'c_D1.1', 'a_D1.1/ppl', 'b_D1.1/ppl', 'c_D1.1/ppl'],
                       'D1.2': ['a_D1.2', 'b_D1.2', 'a_D1.2/ppl', 'b_D1.2/ppl'],
                       'D1.3': ['a_D1.3', 'b_D1.3', 'c_D1.3', 'a_D1.3/gdp', 'b_D1.3/gdp', 'c_D1.3/gdp'],
                       'D1.4': ['a_D1.4', 'b_D1.4', 'a_D1.4/ppl', 'b_D1.4/ppl'], 'D2.1': ['a_D2.1', 'a_D2.1/ppl'],
                       'D2.2': ['a_D2.2', 'b_D2.2', 'c_D2.2', 'a_D2.2/ppl', 'b_D2.2/ppl', 'c_D2.2/ppl'],
                       'D3.1': ['a_D3.1', 'a_D3.1/gdp'], 'D3.2': ['a_D3.2', 'a_D3.2/gdp'],
                       'D3.3': ['a_D3.3', 'a_D3.3/gdp'],
                       'D4.1': ['a_D4.1', 'b_D4.1', 'c_D4.1', 'd_D4.1', 'e_D4.1', 'a_D4.1/gdp', 'b_D4.1/gdp',
                                'c_D4.1/gdp', 'd_D4.1/gdp', 'e_D4.1/gdp'],
                       'D6.4': ['a_D6.4', 'a_D6.4/gdp'],
                       'D9.2': ['a_D9.2'],
                       'D13.1': ['a_D13.1', 'b_D13.1', 'c_D13.1'], 'D13.2': ['a_D13.2', 'b_D13.2', 'c_D13.2'],
                       'D14.1': ['a_D14.1', 'b_D14.1', 'c_D14.1', 'd_D14.1'], 'D14.2': ['a_D14.2', 'b_D14.2'],
                       'D15.1': ['a_D15.1', 'b_D15.1'], 'D15.2': ['a_D15.2', 'b_D15.2'],
                       'D15.3': ['a_D15.3', 'b_D15.3'], 'D16.1': ['a_D16.1', 'b_D16.1', 'a_D16.1/pro', 'b_D16.1/pro'],
                       'D16.2': ['a_D16.2', 'b_D16.2', 'c_D16.2', 'a_D16.2/pro', 'b_D16.2/pro', 'c_D16.2/pro'],
                       'D17.1': ['a_D17.1', 'b_D17.1', 'a_D17.1/art', 'b_D17.1/art'],
                       'D18.1': ['a_D18.1', 'a_D18.1/art'], 'D18.2': ['a_D18.2', 'a_D18.2/gdp']}
df_data = pd.read_excel(read).drop([number_country, number_country+1])


def qa_scoring(x_adapt: list[list[float]], y_score: list[list[float]]):
    result = pd.DataFrame({})
    for i in range(len(x_adapt)):
        qax = qa.QuantileAdaptation(x_adapt[i])
        # print(qax.distribution)
        qax.adapt_distribution()
        # print(qax.distribution)
        qax.infer_score_by_distribution(y_score[i])
        qax.create_final_score()
        result[f'row{i}'] = qax.final_score['qn_score']
    result['total'] = result.mean(axis=1)
    return result


def cleaning_data(dt):
    data = [x if isinstance(x, (int, float)) else np.nan for x in dt]
    data_array = np.array(data)

    # Calculate the mean excluding np.nan
    mean_value = np.nanmean(data_array)

    # Replace np.nan values with the mean value
    data_array = np.where(np.isnan(data_array), mean_value, data_array)

    # Convert array back to list if needed
    cleaned_data = data_array.tolist()
    return cleaned_data


if __name__ == '__main__':
    score = pd.DataFrame({})
    for key in indicator_scheme:
        print(f'key:{key}')
        globals()[key + '_adapt'] = []
        globals()[key + '_infer'] = []
        for item in indicator_scheme[key]:
            cleaned_dt = cleaning_data(df_data[item].tolist()[0:14])
            globals()[key + '_adapt'].append(cleaned_dt)
            cleaned_dt = cleaning_data(df_data[item].tolist())
            globals()[key + '_infer'].append(cleaned_dt)
        print(f"adapt:{globals()[key + '_adapt']}")
        print(qa_scoring(globals()[key + '_adapt'], globals()[key + '_infer']))
        score[key] = qa_scoring(globals()[key + '_adapt'], globals()[key + '_infer'])['total']
    score.to_excel(output, index=False)