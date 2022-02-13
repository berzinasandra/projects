import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pdb

class LinkedinConnections:    
    def display_visualisation(self):
        connections_df = self._create_df()
        count_of_connections_df = self._create_connection_count_df(connections_df)
        
        self._create_visualisation_for_whole_period(count_of_connections_df)
        self._create_visualisation_per_year(count_of_connections_df)


    def _create_df(self):
        connections_df = pd.read_csv('linkedin_data_visualisation\linkedin_data\Connections.csv',  sep=',')
        connections_df['Connected On'] = pd.to_datetime(connections_df['Connected On'])
        connections_df = connections_df.sort_values('Connected On', ascending=True)
        return connections_df

    def _create_connection_count_df(self, connections_df):
        base_df = self._create_base_count_of_connections_df(connections_df)
        whole_time_period_df = self._create_whole_time_period_df(connections_df)
        
        connection_count_df = pd.concat([base_df, whole_time_period_df]).drop_duplicates("Connected On") 
        
        connection_count_df.set_index(connection_count_df["Connected On"], inplace=True)
        connection_count_df.drop("Connected On", axis=1, inplace=True)
        connection_count_df.sort_index(ascending=True, inplace=True)       
        connection_count_df['Count of connections'].fillna(0, inplace=True)
        connection_count_df['Count of connections'] = connection_count_df['Count of connections'].astype(int)

        return connection_count_df

    def _create_base_count_of_connections_df(self, connections_df):
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


    def _create_visualisation_for_whole_period(self,count_of_connections_df):
        connections_per_year=count_of_connections_df.groupby([(count_of_connections_df.index.year)]).sum()

        plt.plot(connections_per_year.index, connections_per_year["Count of connections"]) # line 
        plt.ylabel('Count of connections', fontsize=9)
        y_ticks = np.arange(0, 30, 5)
        plt.yticks(y_ticks)
        plt.gcf().autofmt_xdate()
        plt.xlabel('Connected On', fontsize=9, )
        
        start = str(count_of_connections_df.index.min()).replace(' 00:00:00', '')
        end = str(count_of_connections_df.index.max()).replace(' 00:00:00', '')
        plt.title(f'Amount of connected people in time perdiod of {start} - {end}', fontsize=11)
        
        plt.show()

    def _create_visualisation_per_year(self, count_of_connections_df):
        year_2016 = count_of_connections_df[:'2017-01-01']
        # parse for each year

       


if __name__ == "__main__":
    LinkedinConnections().display_visualisation()

