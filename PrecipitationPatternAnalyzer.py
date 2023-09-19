# ================================================
# 0. LIBRARIES AND COLAB SETUP
# ================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

try:
    from google.colab import drive
    drive.mount('/content/drive', force_remount=True)
    COLAB = True
    print("Note: using Google CoLab")
    %tensorflow_version 2.x
except:
    print("Note: not using Google CoLab")
    COLAB = False


# ================================================
# 1. DATA LOADING
# ================================================
file = '/content/2022_with_fire_mrms_v7 (1) (1).csv'
df_file = pd.read_csv(file)
print(df_file.columns.values)


# ================================================
# 2. DUPLICATES HANDLING
# ================================================

# 2.1: Identifying Duplicates based on 'idx' and 'f_name'

# Finding Rows with the Same 'idx' and 'f_name'
duplicates = df_file[df_file.duplicated(subset=['idx', 'f_name'], keep=False)]
print(len(duplicates))

# 2.2: Counting Duplicates

# Counting the number of Data Points with the same 'idx' and 'f_name'
num_duplicates = duplicates.groupby('idx')['f_name'].count()
print(len(num_duplicates))
print(num_duplicates)

# 2.3: Filtering Out Records with More Than 2 Duplicates

# Finding records where the count of duplicates is greater than 2
idx_more_than_2 = num_duplicates[num_duplicates > 2]
print(idx_more_than_2)

# 2.4: Removing All Duplicates and Creating the Cleaned DataFrame

# Dropping all duplicates from the original DataFrame
df_fires = df_file.drop_duplicates()
print(len(df_fires))
df_fires.head()

# ================================================
# 3. UNIT CONVERSION (inches to mm)
# ================================================
# Copy of dataframe to convert precipitation values
df_fires_mm = df_fires.copy()
columns_to_convert = [
    'precip24h_ltg', 'precip24h+1h_ltg', 'precip24h+2h_ltg', 'precip24h_day_ltg',
    'precip24h-1d_ltg', 'precip24h_day_fire', 'precip24h_fire',
    'precip24h+1h_fire', 'precip24h+2h_fire', 'precip24h-1d_fire'
]

for col in columns_to_convert:
    df_fires_mm[col] = df_fires_mm[col] * 25.4


# ================================================
# 4. DATA VISUALIZATION: PRECIPITATION DISTRIBUTIONS
# ================================================
# Filtering out NaN values and melting dataframe for plotting
df_clean = df_fires_mm[['precip24h-1d_ltg','precip24h_ltg', 'precip24h+1h_ltg', 'precip24h+2h_ltg', 'precip24h_day_ltg']].dropna()
df_melt = df_clean.melt(var_name="Columns", value_name="Precipitation (mm)")
fire_classes = ['Class 1 (0-5 ac)', 'Class 2 (6-50 ac)', 'Class 3 (51-500 ac)', 'Class 4 (> 500 ac)']

# === 4.1: Basic Box Plot ===
# Box plot of precipitation distributions for all fire classes
fig = px.box(df_melt, x="Columns", y="Precipitation (mm)", title="Precipitation Distributions for All Fire Classes",
             labels={"Columns": ""})
fig.update_layout(showlegend=False)
fig.update_traces(marker_color='blue')
fig.show()

# === 4.2: Box Plot Across Fire Classes ===
# Box plot of precipitation distributions across different fire classes
fig = px.box(df_melted, x='Measurement', y='Precipitation (mm)', color='size_class',
             title="Precipitation Distributions Across Fire Classes",
             labels={"Measurement": ""},
             category_orders={"Measurement": columns_to_plot, "size_class": fire_classes})
fig.update_layout(showlegend=True, colorway=list(color_map.values()))
fig.update_traces(marker=dict(line=dict(width=2)))
fig.show()

# === 4.3: Distribution of Lightning Strikes per Fire ===
# Histogram of number of lightning strikes per fire
fig = px.histogram(df_dist_lighting_fire, nbins=int(df_dist_lighting_fire.max()),
                   title='Distribution of Number of Lightning Strikes per Fire',
                   labels={'value': 'Number of Lightning Strikes',
                           'count': 'Number of Fires'})
fig.update_layout(bargap=0.1)
fig.update_traces(opacity=0.7)
fig.show()

# Histograms of number of lightning strikes per fire for each class
fig = go.Figure()
for fire_class in fire_classes:
    fig.add_trace(go.Histogram(x=dfs[fire_class], name=fire_class))
fig.update_layout(barmode='group', xaxis_title='Number of Lightning Strikes',
                  yaxis_title='Number of Fires',
                  title='Distribution of Number of Lightning Strikes per Fire by Class',
                  bargap=0.1)
fig.update_traces(opacity=0.7)
fig.show()

# === 4.4: Number of Lightning Strikes by Hour of the Day ===
# Histograms showing the number of lightning strikes by hour
fig = px.histogram(df_fires_mm, x='hour', nbins=24, title='Number of Lightning Strikes by Hour of the Day',
                   labels={'hour': 'Hour of the Day'})
fig.update_layout(barmode='group',
                  yaxis_title='Number of Lighting Strikes',
                  bargap=0.1)
fig.update_xaxes(tickvals=list(range(0, 24, 2)))
fig.update_traces(opacity=0.7)
fig.show()

# Histogram showing number of lightning strikes by hour and grouped by fire size
fig = px.histogram(df_fires_mm, x='hour', color='size_class', nbins=24,
                   title='Number of Lightning Strikes by Hour of the Day (Grouped by Fire Size)',
                   labels={'hour': 'Hour of the Day'},
                   barmode='group',
                   category_orders={"size_class": fire_classes})
fig.update_layout(yaxis_title='Number of Lighting Strikes',
                  bargap=0.1)
fig.update_xaxes(tickvals=list(range(0, 24, 2)))
fig.update_traces(opacity=0.6)
fig.show()

# === 4.5: Median Precipitation by Hour of the Day ===
# Bar plots showing the median precipitation by the hour of the day lightning struck
# Plot for the day of the lightning
fig = px.bar(medians_by_hour, x='hour', y='precip24h_day_ltg',
             title='Median Precipitation on the Day of Lightning by Hour of the Day',
             labels={'precip24h_day_ltg': 'Median Precipitation (mm)', 'hour': 'Hour of the Day That Lighting Striked'})
fig.update_layout(bargap=0.1)
fig.update_xaxes(tickvals=list(range(0, 24)))
fig.update_traces(opacity=0.7)
fig.show()

# Plot for 1 hour after the lightning
fig = px.bar(medians_by_hour, x='hour', y='precip24h+1h_ltg',
             title='Median Precipitation 1 Hour After Lightning by Hour of the Day',
             labels={'precip24h+1h_ltg': 'Median Precipitation (mm)', 'hour': 'Hour of the Day That Lighting Striked'})
fig.update_layout(bargap=0.1)
fig.update_xaxes(tickvals=list(range(0, 24)))
fig.update_traces(opacity=0.7)
fig.show()

# Bar plots showing median precipitation by the hour of the day and grouped by fire size
# Plot for the day of the lightning
fig = px.bar(medians_by_hour_class, x='hour', y='precip24h_day_ltg', color='size_class',
             title='Median Precipitation on the Day of Lightning by Hour of the Day (Grouped by Fire Size)',
             labels={'precip24h_day_ltg': 'Median Precipitation (mm)', 'hour': 'Hour of the Day That Lighting Striked'},
             category_orders={"size_class": fire_classes})
fig.update_layout(bargap=0.1, yaxis_title='Median Precipitation (mm)')
fig.update_xaxes(tickvals=list(range(0, 24)))
fig.update_traces(opacity=0.7)
fig.show()

# Plot for 1 hour after the lightning
fig = px.bar(medians_by_hour_class, x='hour', y='precip24h+1h_ltg', color='size_class',
             title='Median Precipitation 1 Hour After Lightning by Hour of the Day (Grouped by Fire Size)',
             labels={'precip24h+1h_ltg': 'Median Precipitation (mm)', 'hour': 'Hour of the Day That Lighting Striked'},
             category_orders={"size_class": fire_classes})
fig.update_layout(bargap=0.1, yaxis_title='Median Precipitation (mm)')
fig.update_xaxes(tickvals=list(range(0, 24)))
fig.update_traces(opacity=0.7)
fig.show()

# ================================================
# 5. Heatmaps for Lightning Strikes and Precipitation Levels
# ================================================
# === 5.1: Bar Plots for Median Precipitation by Hour of the Day and Grouped by Fire Size

# - This first bar plot visualizes the median precipitation on the day of the lightning strike.
# It is categorized by the fire size and the hour of the day when the lightning struck.
medians_by_hour = df_fires_mm.groupby('hour')['precip24h_day_ltg'].mean().reset_index()
fig = px.bar(medians_by_hour_class, x='hour', y='precip24h_day_ltg', color='size_class',
             title='Median Precipitation on the Day of Lightning by Hour of the Day (Grouped by Fire Size)',
             labels={'precip24h_day_ltg': 'Median Precipitation (mm)', 'hour': 'Hour of the Day That Lighting Striked'},
             category_orders={"size_class": fire_classes})
fig.update_layout(bargap=0.1, yaxis_title='Median Precipitation (mm)')
fig.update_xaxes(tickvals=list(range(0, 24)))
fig.update_traces(opacity=0.7)
fig.show()

# - This next bar plot visualizes the median precipitation 1 hour after the lightning strike.
# Again, it's grouped by fire size and hour of the day.
fig = px.bar(medians_by_hour_class, x='hour', y='precip24h+1h_ltg', color='size_class',
             title='Median Precipitation 1 Hour After Lightning by Hour of the Day (Grouped by Fire Size)',
             labels={'precip24h+1h_ltg': 'Median Precipitation (mm)', 'hour': 'Hour of the Day That Lighting Striked'},
             category_orders={"size_class": fire_classes})
fig.update_layout(bargap=0.1, yaxis_title='Median Precipitation (mm)')
fig.update_xaxes(tickvals=list(range(0, 24)))
fig.update_traces(opacity=0.7)
fig.show()

# === 5.2: Data Preparation for Heatmap

# - Extract the hour from the timestamp data to understand the hour when the lightning struck.
df_fires_mm['hour'] = pd.to_datetime(df_fires_mm['dttime_utc']).dt.hour

# - Define the bins for precipitation levels, calculate their sizes, and label each bin.
min_precip = df_fires_mm['precip24h+1h_ltg'].min()
max_precip = df_fires_mm['precip24h+1h_ltg'].max()
bin_size = (max_precip - min_precip) / 5
bin_edges = [min_precip + i*bin_size for i in range(6)]
labels = [f"{round(bin_edges[i], )}-{round(bin_edges[i+1], 0)}" for i in range(5)]

# - Categorize or bin the precipitation data based on the defined bins.
df_fires_mm['precip_bins'] = pd.cut(df_fires_mm['precip24h+1h_ltg'], bins=bin_edges, labels=labels, right=False)

# - Create a pivot table to represent lightning strikes by hour and the binned precipitation levels.
pivot_table = df_fires_mm.groupby(['hour', 'precip_bins']).size().unstack(fill_value=0)
all_hours = list(range(24))
pivot_table = pivot_table.reindex(all_hours).fillna(0).astype(int).transpose()

# === 5.3: Data Transformation for Heatmap Visualization

# - Convert the data in the pivot table to a logarithmic scale. This transformation makes the heatmap more visually informative.
log_pivot_table = np.log(pivot_table + 1)
rounded_max_value = int(np.ceil(pivot_table.values.max() / 100.0) * 100)
tick_values = list(range(0, rounded_max_value + 1, 200))
log_tick_values = [np.log(val + 1) for val in tick_values]

# === 5.4: Create Heatmap

# - Generate the heatmap visualizing the number of lightning strikes by the hour of the day and the binned precipitation levels.
fig = go.Figure(go.Heatmap(
    z=log_pivot_table.values,
    x=log_pivot_table.columns,
    y=log_pivot_table.index,
    customdata=pivot_table.values,
    colorscale="Viridis",
    zmin=0,
    zmax=np.log(pivot_table.values.max() + 1),
    hovertemplate='%{customdata} strikes<br>Hour: %{x}<br>Precipitation: %{y}<extra></extra>',
    colorbar=dict(
        title='Number of Strikes',
        tickvals=log_tick_values,
        ticktext=tick_values,
        tickmode='array'
    )
))
fig.update_xaxes(tickvals=list(range(24)), ticktext=[str(i) for i in range(24)])
fig.update_traces(xgap=1, ygap=1)
fig.update_layout(yaxis_autorange="reversed", title="Number of Lightning Strikes by Hour of the Day and Precipitation Range for precip24+1h_ltg")
fig.show()

# ================================================
# 6. ANALYSIS
# ================================================

# === 6.1: Median Precipitation Analysis by Fire Class

# Calculating median precipitation values for each Fire Class
medians = df_fires_mm.groupby('size_class')[columns_to_plot].median()
print(medians)

# === 6.2: Fire Count Analysis for df_fires_mm

# Counting the number of unique fires in df_fires_mm for each Fire Class
count_classes_mm = df_fires_mm.drop_duplicates(subset='f_name').groupby('size_class').size()
print(count_classes_mm)
print(sum(count_classes_mm))

# === 6.3: Fire Count Analysis for df_fires

# Counting the number of unique fires in df_fires for each Fire Class
count_classes = df_fires.drop_duplicates(subset='f_name').groupby('size_class').size()
print(count_classes)
print(sum(count_classes))

# === 6.4: Lightning Strikes Analysis

# Counting the number of lightning strikes associated with each fire
df_dist_lighting_fire = df_fires_mm.groupby('f_name')['idx'].count()
print(len(df_dist_lighting_fire))
df_dist_lighting_fire.head()


