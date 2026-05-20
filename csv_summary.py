import sys
import pandas as pd
import matplotlib.pyplot as plt



def summarize_csv(file_path):
    try:

        df = pd.read_csv(file_path)
       
        summary_df_data = {}

        for column in df.select_dtypes(exclude="object"):
            
            null_values = df[column].isnull().sum()
            unique_vals = df[column].unique().size
            data_type = df[column].dtype
            col_max = df[column].max()
            col_min = df[column].min()
            col_mean= df[column].mean()
            col_med = df[column].median()
            col_std = df[column].std()

            summary_col_vals = pd.Series(data=[data_type, null_values, unique_vals, col_max, 
                                    col_min, col_mean, col_med, col_std])
            
            summary_df_data[column] = summary_col_vals
    

        for column in df.select_dtypes("object"):
            null_values = df[column].isnull().sum()
            unique_vals = df[column].unique().size
            data_type = df[column].dtype
            col_max = df[column].max()
            col_min = df[column].min()
            col_mean= "NA"
            col_med = "NA"
            col_std = "NA"

            summary_col_vals = pd.Series(data=[data_type, null_values, unique_vals, col_max, 
                                    col_min, col_mean, col_med, col_std])
            
            summary_df_data[column] = summary_col_vals

        
        idxs = ["Data Type", "Null Vals", "Unique Vals", "Max", "Min", "Mean", "Med", "STD"]



        summary_df = pd.DataFrame(data=summary_df_data)
        summary_df.index = idxs

        print(summary_df)

        fig, ax = plt.subplots()
        ax.hist(x=df["tip"], bins=20, linewidth = 0.5, edgecolor = "white")
        plt.show()



        


    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty.")
        return








if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python csv_summary.py <path_to_csv_file>")
    else:
        summarize_csv(sys.argv[1]) 
