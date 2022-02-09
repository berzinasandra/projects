import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pdb

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
        base_df = self._create_base_count_of_connections_df(connections_df)
        
        whole_time_period_df = self._create_whole_time_period_df(connections_df)
        
        connection_count_df = pd.concat([base_df, whole_time_period_df]).drop_duplicates("Connected On") 
        connection_count_df.sort_values('Connected On', ascending=True, inplace=True)
        connection_count_df.reset_index(inplace=True)
        connection_count_df.drop(["index"], 1)
        connection_count_df['Count of connections'].fillna(0, inplace=True)
        
        return connection_count_df

    def _create_base_count_of_connections_df(self, connections_df):
        # the same --> connections_df.groupby(['Connected On']).size() == connections_df['Connected On'].value_counts()
        
        
        count_of_connections = connections_df.groupby(['Connected On']).size()
        count_of_connections_df = pd.DataFrame(count_of_connections, columns=['Count of connections'])
        count_of_connections_df.reset_index(inplace=True)

        return count_of_connections_df
    
    def _create_whole_time_period_df(self,connections_df):
        start = connections_df['Connected On'].apply(lambda x: x.date()).min()
        end = connections_df['Connected On'].apply(lambda x: x.date()).max()
        whole_time_period = pd.date_range(start, end)
        whole_time_period_df = pd.DataFrame(whole_time_period,columns=['Connected On'])

        return whole_time_period_df


    def _create_visualisation(self,count_of_connections_df):
        # connections per year
        connections_per_year_df = pd.DataFrame(count_of_connections_df.groupby(count_of_connections_df["Connected On"].dt.year)["Count of connections"].agg(['sum']))
        # pdb.set_trace()
        # create plot
        plt.plot(connections_per_year_df.index, connections_per_year_df["sum"]) # line 
        # count_of_connections_df["Count of connections"].plot(kind='bar')
        plt.ylabel('Count of connections', fontsize=9)
        y_ticks = np.arange(0, 30, 5)
        plt.yticks(y_ticks)
        plt.gcf().autofmt_xdate()
        # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
        plt.xlabel('Connected On', fontsize=9, )
        
        plt.title(f'Amount of connected people in time perdiod of {count_of_connections_df["Connected On"].min()} - {count_of_connections_df["Connected On"].max()}', fontsize=11)
        
        plt.show()

      
       

# count_of_connections_df["Count of connections"].plot(kind='bar') --> bar chart
# count_of_connections_df.plot.scatter(x='Connected On', y='Count of connections')


if __name__ == "__main__":
    LinkedinConnections().display_visualisation()

