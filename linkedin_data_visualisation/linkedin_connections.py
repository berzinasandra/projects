import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

class LinkedinConnections:    
    def display_visualisation(self):
        connections_df = self._create_df()
        count_of_connections_df = self._create_connection_count_df(connections_df)
        self._create_visualisation(count_of_connections_df)


    def _create_df(self):
        connections_df = pd.read_csv('linkedin_data_visualisation\linkedin_data\Connections.csv',  sep=',')
        # connections_df.sort_values(by=['Email Address'])
        connections_df['Connected On'] = pd.to_datetime(connections_df['Connected On'])
        connections_df = connections_df.sort_values('Connected On', ascending=True)
        return connections_df

    def _create_connection_count_df(self, connections_df):
        # the same --> connections_df.groupby(['Connected On']).size() == connections_df['Connected On'].value_counts()
        count_of_connections = connections_df.groupby(['Connected On']).size()
        count_of_connections_df = pd.DataFrame(count_of_connections, columns=['Count of connections'])
        count_of_connections_df.reset_index(inplace=True)

        # create wider time period 
        start = connections_df['Connected On'].apply(lambda x: x.date()).min()
        end = connections_df['Connected On'].apply(lambda x: x.date()).max()
        whole_time_period = pd.date_range(start, end)
        wider_index_range = range(len(whole_time_period))
        df2 = pd.DataFrame(whole_time_period,columns=['Connected On'])
        df3 = pd.concat([count_of_connections_df, df2]).drop_duplicates("Connected On") 
        df3.sort_values('Connected On', ascending=True, inplace=True)
        # import pdb;pdb.set_trace()     
        df3.reset_index(inplace=True)
        df3.drop(["index"], 1)
        df3['Count of connections'].fillna(0, inplace=True)
        
        return df3

    def _create_visualisation(self,count_of_connections_df):
        # create plot
        # plt.plot(count_of_connections_df["Connected On"], count_of_connections_df["Count of connections"]) # line 
        count_of_connections_df["Count of connections"].plot(kind='bar')
        plt.ylabel('Count of connections', fontsize=9)
        y_ticks = np.arange(0, 4, 1)
        plt.yticks(y_ticks)
        plt.gcf().autofmt_xdate()
        plt.xlabel('Connected On', fontsize=9)
        plt.title(f'Amount of connected people in time perdiod of {count_of_connections_df["Connected On"].min()} - {count_of_connections_df["Connected On"].max()}', fontsize=11)
        plt.show()


# count_of_connections_df["Count of connections"].plot(kind='bar') --> bar chart
# count_of_connections_df.plot.scatter(x='Connected On', y='Count of connections')


if __name__ == "__main__":
    LinkedinConnections().display_visualisation()

