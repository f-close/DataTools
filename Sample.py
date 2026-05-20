import scipy.stats as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from sklearn.preprocessing import StandardScaler



class Sample():

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.min = np.min(data)
        self.max = np.max(data)
        self.mean = np.mean(data)
        self.median = np.median(data)
        self.std = np.std(data)
        self.dist_name = ""
        self.dist_params = ()

    def summary(self):
        print(f"-------- Summary for {self.name} --------")
        print(f"Min: {self.min:.5f}")
        print(f"Max: {self.max:.5f}")
        print(f"Mean: {self.mean:.5f}")
        print(f"Median: {self.median:.5f}")
        print(f"Std: {self.std:.5f}")
        print(f"Fit Distribution: {self.dist_name}")
        print(f"Distribution params: {self.dist_params}")
        print("--------------------------------------------")

    def fit_to_dist(self, dist):

        dist_to_fit = getattr(st, dist)
        params = dist_to_fit.fit(self.data)
        self.dist_name = dist
        self.dist_params = params

        d, p = st.kstest(self.data, dist_to_fit.name, args=params)
        print(f"Sample '{self.name}' was fit to distribution: '{dist_to_fit.name}' with p-val: {p}")

    def auto_fit(self):
        dist_names = ["norm", "lognorm", "uniform", "expon", "gamma", "laplace", "chi2"]
        dist_results = []
        params_dict = {}

        for dist_name in dist_names:
            dist = getattr(st, dist_name)
            params = dist.fit(self.data)
            params_dict[dist_name] = params

            d, p = st.kstest(self.data, dist.name, args = params)
            dist_results.append((dist_name, p))

        best_dist = max(dist_results, key=lambda item : item[1])

        self.dist_name = best_dist[0]
        self.dist_params = params_dict[best_dist[0]]

        print(f"Sample '{self.name}' was fit to '{self.dist_name}' with p-val: {best_dist[1]}")
        print(f"params: {self.dist_params}")

    def scale(self):
        #DO the Scaling
        scaler = StandardScaler()

        self.data = scaler.fit_transform(np.array(self.data).reshape(-1,1)).flatten()

        #Recalculate stats
        self.min = np.min(self.data)
        self.max = np.max(self.data)
        self.mean = np.mean(self.data)
        self.median = np.median(self.data)
        self.std = np.std(self.data)
        print(f"Sample '{self.name}' was scaled!")

    def view(self):
        sns.displot(data=self.data, kde=True)
        plt.show()

    def qq(self):

        # TODO: Use correct range for quantile calculations.
        # Split the observed data into equal inervals 
        quants = np.arange(self.min, self.max, (self.max-self.min)/20)
        dist = getattr(st, self.dist_name) # Access the fit distribution

        # if there are 3 dist params then the dist uses a shape parameter
        if len(self.dist_params) == 3:
            shape = self.dist_params[0]
            loc = self.dist_params[1]
            scale = self.dist_params[2]
        else:
            # Otherwise only use location and scalen parameters
            loc = self.dist_params[0]
            scale = self.dist_params[1]

        # CDF generated from the distribution fit to the sample
        cdf = dist.cdf(quants, shape, loc, scale)


        #Calculate the empircal CDF to compare with the fit CDF

        #make ndarray of the same length as quants
        emp_cdf = np.empty(len(quants))


        index = 0 #index to be used when indexing the emp_cdf array
        for quant in quants:
            sum_leq = 0 #set a counter to 0

            for val in self.data: #now count all occurences that are less than or equal to our current quantile
                if val <= quant: 
                    sum_leq += 1 #sum values that are less than or equal to our current quantile
                else:
                    continue
            
            emp_cdf[index] = sum_leq/len(self.data) # at position index, divide our # of observations less than quanitle by length of the data
            index += 1 #move to next index

        df = pd.DataFrame(data={"x": quants, "CDF": cdf, "EMP CDF": emp_cdf})

        print(df)

        # This is analagous to a QQ plot but not quite right because of the qunatiles chosen earlier
        sns.scatterplot(x=df["CDF"], y=df["EMP CDF"])
        plt.show()











if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python Sample.py <path_to_csv_file>")
    else:
            
        df = pd.read_csv(sys.argv[1])

        x = df["total_bill"]
        y = df["tip"]

        s1 = Sample("total_bill", x)
        s2 = Sample("tip", y)
        

        
        s1.summary()
        s1.auto_fit()
        s1.summary()


        #s1.view()

        s1.qq()


        '''
        x2 = np.log(df["total_bill"])
        s3 = Sample("log_total_bill", x2)

        s3.summary()
        s3.auto_fit()
        s3.view()
        
        
        '''


    



        



