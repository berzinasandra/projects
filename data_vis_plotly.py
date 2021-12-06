import plotly.graph_objects as go
import plotly.express as px
import pandas as pd




def create_vis(data:list):
    df = pd.DataFrame.from_dict(data)
    df.set_index("City", inplace=True)

    fig = go.Figure()
    buttons = []
    i = 0

    colors = ["firebrick", "steelblue"]
    # TODO: remove 'trace 0' when hover over bars
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


if __name__ == "__main__":
    data =  [{'City': 'Espoo', 'Number of establishments': '13', 'Number of bedrooms': '1367', 'Occupancy rate of bedrooms, %': '43.6', 'Change compared to previous year, %-units': '1.9', 'Room price, euros (incl. VAT 10 %)': '63.56', 'RevPAR, euros (incl. VAT 10 %)': '27.70'}, {'City': 'Helsinki', 'Number of establishments': '59', 'Number of bedrooms': '10582', 'Occupancy rate of bedrooms, %': '25.9', 'Change compared to previous year, %-units': '2.5', 'Room price, euros (incl. VAT 10 %)': '95.20', 'RevPAR, euros (incl. VAT 10 %)': '24.65'}]
    create_vis(data)
    