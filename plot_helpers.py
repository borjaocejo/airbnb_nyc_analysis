import pandas as pd
import folium

def plotting_quantiles(df,col):
    ''' Finds the quantiles that are input in the color_on_col function
        Input: Dataframe and column to attain quantiles for.
        Output: Values of first and third quantile
    '''
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    
    return q1,q3

def color_on_col(x,q1,q3):
    
    ''' Produces color dependent on where the value falls on its column (quantile 1 and 3 or greater)
        Input: value x, quantile 1 and quantile 3
        Output: Color for map
    '''
    if x <= q1:
        color = 'green'
    elif x <= q3:
        color = 'orange'
    else:
        color = 'red'
        
    return color

def run_mapping_color(df,col):
    ''' Uses helper functions to finally output the color based on the input dataframe and column.
        Input: Dataframe and color
        Output: Color based on the dataframe and column for mapping
    '''
    q1,q3 = plotting_quantiles(df,col)
    
    return df[col].apply(color_on_col, args = (q1,q3))

def plot_points(row,map_):
    ''' Adds points to a map
        Input: row: row in dataframe (to use it with .apply)
               map_: folium map object
    '''
    folium.Circle(location = [row.latitude,row.longitude], radius = 25, color = row['color']).add_to(map_)

def make_map(df,col):
    '''Makes a map/plots points based on input column
        Inputs: df: DataFrame
                col: string, column in DataFrame to select colors based on quantiles.
        Output: new_map: map object with points plotted
    '''
    new_map = folium.Map(location = [40.73,-73.935], tiles = 'cartodb positron', zoom_start = 10)
    df['color'] = run_mapping_color(df,col)
    
    df.apply(plot_points, args = (new_map,), axis=1)
    df.drop(columns='color',inplace = True )
    
    return new_map