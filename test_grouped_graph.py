import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

class LineChart:
    def __init__(self, df):
        self.df = df
    def grouping(self, df):
        df = df.groupby(["Employee", "Month","Day"])["Stress"].mean().reset_index()
        # print(df)
        indexes = pd.MultiIndex.from_arrays([df["Month"],df["Day"],df["Employee"]]) ## si dovrebbe aggiungere anche employee
        grouped_df = pd.DataFrame({"EMployees": df["Employee"].values, "Stress":df["Stress"].values}, index = indexes)
        return grouped_df

    def plot_function(self,x, ax,df):
        ax = self.graph[x]
        ax.set_xlabel(x, weight='bold')
        ax.tick_params(axis='both', which='both',labelsize = 9)
        ## set only the bottom axis as visible for better visualization
        ax.spines[["left","right","top"]].set_visible(False)

        for employee in self.grouped_df.index.levels[2]:
            data = self.grouped_df.xs((x, employee), level=('Month', 'Employee'))
            data.plot(kind='line', y='Stress', ax=ax, legend=False, label=employee,xlabel=str(x))
        
        # ax.legend(title='Employee')

        # return grouped_df.xs(x).plot(kind='line', stacked='True', ax=ax, legend=False,xlabel=str(x))
    
    def make_lineplot(self):
            
        
        self.grouped_df = self.grouping(self.df)
        print("grouped data into this: ", self.grouped_df)
        n_subplots = len(self.grouped_df.index.levels[0])
        fig, axes = plt.subplots(nrows=1, ncols=n_subplots, sharey=True, figsize=(15, 6))  # width, height
        self.graph = dict(zip(self.grouped_df.index.levels[0], axes))
        plots= list(map(lambda x: self.plot_function(x, self.graph[x],self.grouped_df), self.graph))


        # fig.subplots_adjust(wspace=0)
        fig.suptitle("daily streess for employees")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left',fontsize=10)
        # fig.subplots_adjust(wspace=0)
        # plt.show()
        return fig,axes
        # plots = list(map(lambda x: serotype_df.xs(x).plot(kind='bar', stacked='True', ax=graph[x], legend=False), graph
        # df[""]



if __name__=="__main__":
    df = pd.read_csv("./simulated_data.csv")
    lc = LineChart(df)
    lc.make_lineplot()
