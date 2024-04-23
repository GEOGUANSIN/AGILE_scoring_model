import numpy as np
import pandas as pd


class QuantileAdaptation:
    def __init__(self, data):
        self.data = data
        self.distribution = pd.DataFrame({})
        self.inferred_score = pd.DataFrame({})
        self.final_score = pd.DataFrame({})

    import numpy as np

    def compute_mean_std(self, data):
        """
        Compute the mean and standard deviation of a given numpy array.

        Parameters:
        data (np.array): The input data array.

        Returns:
        tuple: A tuple containing the mean and standard deviation of the data.
        """
        # Calculate the mean of the data
        mean_of_data = np.mean(data)

        # Calculate the standard deviation of the data
        std_of_data = np.std(data, ddof=1)

        return mean_of_data, std_of_data


    def standardize_and_clip(self, data, mean, std):
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
        # Standardize data
        standardized_data = list(map(lambda x: (25 * (x - mean) / std) + 50, data))
        # Clip data to be within the range of 0 to 100
        clipped_data = np.clip(standardized_data, 0, 100)

        return clipped_data


    def filter_greater_than(self, data, scores, bound):
        """
        Return the elements of the input data array that are greater than a specified bound.

        Parameters:
        data (np.array): The input data array.
        bound (float): The lower bound for filtering the data.

        Returns:
        np.array: An array containing elements that are greater than the specified bound.
        :param self:
        """
        # Filter data to find elements greater than the bound
        # print(f"max(scores):{max(scores)}")
        filtered_data = [item for item, score in zip(data, scores) if score <= bound * 100]

        assert isinstance(filtered_data, object)
        return filtered_data


    def adapt_distribution(self, data = None):
        if self.data is None:
            raw_data = data
        else:
            raw_data = self.data
        try:
            mean, std = self.compute_mean_std(raw_data)
            std_mean_sheet = pd.DataFrame({'name': 'raw', 'data': [raw_data], 'mean': [mean], 'std': [std]})  # Example large dataset
            scores = self.standardize_and_clip(raw_data, mean, std)
            quantiles = [1, 0.75, 0.5, 0.25]
            filtered_data = raw_data
            for quantile in quantiles:
                filtered_data = self.filter_greater_than(filtered_data, scores, quantile)
                filtered_mean, filtered_std = self.compute_mean_std(filtered_data)
                scores = self.standardize_and_clip(filtered_data, filtered_mean, filtered_std) * quantile
                df = pd.DataFrame({'name': f'within_{quantile}_data', 'data': [filtered_data], 'mean': [filtered_mean], 'std': [filtered_std]})
                std_mean_sheet = pd.concat([std_mean_sheet, df])
                std_mean_sheet = std_mean_sheet.reset_index(drop=True)
                # print(std_mean_sheet)
                self.distribution = std_mean_sheet
        except Exception as e:
            print(f"Can not proceed to adapt be cause of:{e}")


    def infer_score_by_distribution(self, infr_data):
        if self.distribution.empty:
            print("Please run the adapt_distribution method first.")
            return
        else:
            if infr_data is None:
                raw_data = infr_data
            else:
                raw_data = infr_data
            try:
                process_sheet = pd.DataFrame({'raw_data': raw_data})
                # print(self.distribution.loc[0, 'mean'])
                mean, std = self.distribution.loc[0, 'mean'], self.distribution.loc[0, 'std']
                scores = self.standardize_and_clip(raw_data, mean, std).tolist()
                # process_sheet['raw_data'] = list(zip(raw_data, scores))
                quantiles = [1, 0.75, 0.5, 0.25]
                filtered_data = raw_data
                j = 0
                for quantile in quantiles:
                    j += 1
                    filtered_data = self.filter_greater_than(filtered_data, scores, quantile)
                    # print(f"self.distribution:{self.distribution}")
                    filtered_mean, filtered_std = self.distribution.loc[j, 'mean'], self.distribution.loc[j, 'std']
                    scores = (self.standardize_and_clip(filtered_data, filtered_mean, filtered_std) * quantile).tolist()
                    process_sheet[f'{quantile}_quantile'] = [np.nan] * len(raw_data)
                    for i in range(len(filtered_data)):
                        process_sheet.loc[process_sheet['raw_data'] == filtered_data[i],f'{quantile}_quantile'] = scores[i]
                    # print(process_sheet)
                    self.inferred_score = process_sheet
            except Exception as e:
                print(f"Can not proceed to adapt be cause of:{e}")

    def create_final_score(self):
        if self.inferred_score.empty:
            print("Please run the infer_score_by_distribution method first.")
            return
        else:
            self.final_score['raw_data'] = self.inferred_score['raw_data']
            self.final_score['qn_score'] = self.inferred_score.apply(
                lambda row: row.dropna().iloc[-1].round(0).astype(int), axis=1)
            self.final_score.loc[self.final_score['raw_data'] == 0, 'qn_score'] = 0
            # print(self.final_score)


if __name__ == '__main__':
    data = [255, 44, 54, 17, 16, 2, 48, 4, 1, 3, 0, 0, 6, 0]
    qa = QuantileAdaptation(data)
    qa.adapt_distribution()
    qa.infer_score_by_distribution(data + [245, 0, 5])
    qa.inferred_score.to_excel('inferred_score.xlsx', index=True)
    qa.create_final_score()