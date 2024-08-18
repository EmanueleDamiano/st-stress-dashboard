import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import seaborn as sn 
from test_grouped_graph import LineChart
plt.rcParams.update({'font.size': 25})
st. set_page_config(layout="wide")


df = pd.read_csv("./simulated_data.csv")
df['Composite'] = df['Employee'] + '\n' + df['Product Line'] + '\n' + df['Activity'] + '\n' + df['Workstation']
st.header('Population Stress Monitoring')
st.subheader("stress levels:")
st.divider()
st.text(f"Population Minimum Stress: {round(df['Stress'].min(),2)}")
st.text(f"Population Average Stress: {round(df['Stress'].mean(),2)}")
st.text(f"Population Max Stress: {round(df['Stress'].max(),2)}")
# st.divider()
# st.subheader("stress conditioned by company role")
# st.text(f"{df.groupby(by = 'Role')['Stress'].mean()}")
# st.divider()
# st.text(f"{df.groupby(by = 'Gender')['Stress'].mean()}")
# st.divider()
# st.text(f"{df.groupby(by = 'Activity')['Stress'].mean()}")

# # First set of filters; these apply to both  the barplot and the linechart
employee_options = df['Employee'].unique()

selected_employee   = st.sidebar.multiselect('Select Employee:', employee_options, default=employee_options)
selected_role       = st.sidebar.multiselect('Employee Role', df["Role"].unique(), default = df["Role"].unique())
selected_gender     = st.sidebar.multiselect('Select Category:', df["Gender"].unique(), default = df["Gender"].unique())
# selected_age          = st.sidebar.select_slider("Select by Age", df["Age"],value = [i for i in df["Age"]])# value = df["Age"].max()) ## all the ages selected by the default
selected_pl         = st.sidebar.multiselect('Select Product Line', df["Product Line"].unique(), default = df["Product Line"].unique())
selected_activity   = st.sidebar.multiselect('Select by Activity:', df["Activity"].unique(), default = df["Activity"].unique())
selected_ws   = st.sidebar.multiselect('Select Workstation:', df["Workstation"].unique(), default = df["Workstation"].unique())


filtered_stress = df[
    (df['Employee'].isin(selected_employee)) &
    (df['Role'].isin(selected_role)) & 
    (df['Gender'].isin(selected_gender)) &
    # (df['Age'] == selected_age) &
    df["Product Line"].isin(selected_pl)&
    df["Activity"].isin(selected_activity)&
    df["Workstation"].isin(selected_ws)
]



# # Second set of filters
## employee options for the second filter. This takes count of the selection of the first filter
second_filter_options = filtered_stress["Employee"].unique()
st.sidebar.markdown("---")
employee_linechart   = st.sidebar.multiselect('Select Employee for the linechaert:', second_filter_options, default=second_filter_options)
## filtro su giorni selezionati 
min_day_to_display = st.sidebar.select_slider("Dispaly data from this day",  options = df["Day"],value = df["Day"].min())
max_day_to_display = st.sidebar.select_slider("Display data until this day", options = df["Day"],value = df["Day"].max())

## si selezionano le osservazioni restituite dal secondo filtro 
## oppure quelle ritornate dal primo, che sono state già applicate sul barplot 
## il primo filtro seleziona le osservazioni da ritornare sia sul barplot che sul linechart 

line_chart_filter = filtered_stress[
    (filtered_stress['Employee'].isin(employee_linechart) ) &
    (filtered_stress['Day'] >= min_day_to_display) &
    (filtered_stress['Day'] <= max_day_to_display)
]

## raggruppamento per lineplot
indexes = pd.MultiIndex.from_arrays([line_chart_filter["Month"],line_chart_filter["Day"]],names = ("month", "day")) 
df_lineplot = pd.DataFrame(line_chart_filter["Stress"].values, index = indexes)
# df_lineplot = pd.DataFrame({"Month" : line_chart_filter["Month"], "Day": line_chart_filter["Day"], "Stress": line_chart_filter["Month"]})

if not filtered_stress.empty:
    fig = plt.figure(figsize = (24,12))
    g = sn.FacetGrid(filtered_stress,col="Employee")
    g.map_dataframe(sn.barplot,x = "Activity", y = "Stress", hue = "Workstation",errorbar = None,palette = "pastel")
    g.set_titles(col_template="{col_name}")

    g.add_legend()
    st.pyplot(g)
else:
    st.write('data not available for any employee')




if not line_chart_filter.empty:
    # fig, ax = plt.subplots(2, 1, figsize = (20,16))
    # sn.barplot(data=filtered_stress, x='Composite', y='Stress', hue='Employee', errorbar=None, dodge=True, ax=ax[0])
    
    # sn.lineplot(data=line_chart_filter, x='Day', y='Stress', hue='Employee', ax=ax[1])
    # print(line_chart_filter)
    lc = LineChart(line_chart_filter)
    fig,axes = lc.make_lineplot()
    fig.subplots_adjust(wspace=0)

    # fig.tight_layout(pad=3.0)

    st.pyplot(fig)
else:
    st.write('No data to display for the selected filters.')

