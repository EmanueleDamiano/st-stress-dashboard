import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

# serotype_df = pd.DataFrame({'13v': {(2002, 1): 5,
#   (2002, 2): 9,
#   (2002, 3): 23,
#   (2002, 4): 11,
#   (2003, 1): 1,
#   (2003, 2): 12,
#   (2003, 3): 22,
#   (2003, 4): 15,
#   (2004, 1): 10,
#   (2004, 2): 11,
#   (2004, 3): 30,
#   (2004, 4): 11,
#   (2005, 1): 9,
#   (2005, 2): 20,
#   (2005, 3): 20,
#   (2005, 4): 7},
#  '23v': {(2002, 1): 1,
#   (2002, 2): 8,
#   (2002, 3): 18,
#   (2002, 4): 5,
#   (2003, 1): 5,
#   (2003, 2): 16,
#   (2003, 3): 13,
#   (2003, 4): 7,
#   (2004, 1): 4,
#   (2004, 2): 4,
#   (2004, 3): 20,
#   (2004, 4): 5,
#   (2005, 1): 4,
#   (2005, 2): 5,
#   (2005, 3): 10,
#   (2005, 4): 5},
#  '7v': {(2002, 1): 30,
#   (2002, 2): 75,
#   (2002, 3): 148,
#   (2002, 4): 68,
#   (2003, 1): 26,
#   (2003, 2): 75,
#   (2003, 3): 147,
#   (2003, 4): 67,
#   (2004, 1): 32,
#   (2004, 2): 84,
#   (2004, 3): 151,
#   (2004, 4): 62,
#   (2005, 1): 21,
#   (2005, 2): 49,
#   (2005, 3): 81,
#   (2005, 4): 26},
#  'Non-typed': {(2002, 1): 1,
#   (2002, 2): 2,
#   (2002, 3): 4,
#   (2002, 4): 4,
#   (2003, 1): 3,
#   (2003, 2): 5,
#   (2003, 3): 9,
#   (2003, 4): 8,
#   (2004, 1): 1,
#   (2004, 2): 4,
#   (2004, 3): 6,
#   (2004, 4): 4,
#   (2005, 1): 4,
#   (2005, 2): 10,
#   (2005, 3): 7,
#   (2005, 4): 11},
#  'Non-vaccine': {(2002, 1): 2,
#   (2002, 2): 7,
#   (2002, 3): 10,
#   (2002, 4): 6,
#   (2003, 1): 4,
#   (2003, 2): 5,
#   (2003, 3): 13,
#   (2003, 4): 8,
#   (2004, 1): 2,
#   (2004, 2): 4,
#   (2004, 3): 19,
#   (2004, 4): 8,
#   (2005, 1): 4,
#   (2005, 2): 3,
#   (2005, 3): 15,
#   (2005, 4): 5}})
# print(serotype_df)
# print(serotype_df.index)


# def plot_linechart(employee):
# df = df.loc[df["Employee"] == "Employee_4",:]
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