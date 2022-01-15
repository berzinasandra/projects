import plotly.graph_objects as go
import pandas as pd
import matplotlib
import random




def create_vis(data:list):
    df = pd.DataFrame.from_dict(data)
    df.set_index("City", inplace=True)

    if 'Whole_country' in df.index:
        df.drop('Whole_country', inplace=True)
    
    
    fig = go.Figure()
    buttons = []
    i = 0

    colors = _get_colors(len(df))
    # TODO: 
    # remove 'trace 0' when hover over bars
    count = 0
    for column in df:
        fig.add_trace(
            go.Bar(
                x =  df[column].index,
                y =  [float(value) for value in df[column].values],
                marker_color = colors,
                visible = (count==0),
            )
        )

        count +=1


        args = [False] *  len(df.columns)
        args[i] = True

        button = {
            "label": column,
            "method": "update",
            "args":[{
                "visible":args
                }]
        }

        buttons.append(button)

        i+=1

    fig.update_layout(
        updatemenus=[
            dict(
            type="dropdown",
            direction="down",
            x = 1,
            y = 1,
            buttons = buttons, 
    )
        ])

    return fig.show()

def _get_colors(len_of_df):
    names_of_colors = [name for name in matplotlib.colors.cnames.keys()]
    colors = [random.choice(names_of_colors) for color in range(len_of_df)]
    return colors

if __name__ == "__main__":
    data =  [{'City': 'Espoo', 'Number of establishments': '13', 'Number of bedrooms': '1367', 'Occupancy rate of bedrooms, %': '43.6', 'Change compared to previous year, %-units': '1.9', 'Room price, euros (incl. VAT 10 %)': '63.56', 'RevPAR, euros (incl. VAT 10 %)': '27.70'}, {'City': 'Helsinki', 'Number of establishments': '59', 'Number of bedrooms': '10582', 'Occupancy rate of bedrooms, %': '25.9', 'Change compared to previous year, %-units': '2.5', 'Room price, euros (incl. VAT 10 %)': '95.20', 'RevPAR, euros (incl. VAT 10 %)': '24.65'}]
    create_vis(data)
    