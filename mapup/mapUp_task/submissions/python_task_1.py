import pandas as pd
import os

# read all dataset csv
script_directory = os.path.dirname(os.path.realpath(__file__))

dataset_path = os.path.join(script_directory, '../datasets/dataset-1.csv')
df = pd.read_csv(dataset_path)

dataset_path2 = os.path.join(script_directory, '../datasets/dataset-2.csv')
df2 = pd.read_csv(dataset_path2)


def generate_car_matrix(df):
    # pivot the DataFrame to create the desired matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # set diagonal values to 0
    for idx in car_matrix.index:
        car_matrix.at[idx, idx] = 0

    return car_matrix


def get_type_count(dataframe):
    # add a new categorical column 'car_type' based on values of the 'car' column
    dataframe['car_type'] = pd.cut(dataframe['car'],
                                   bins=[float('-inf'), 15, 25, float('inf')],
                                   labels=['low', 'medium', 'high'],
                                   right=False)

    # calculate the count of occurrences for each 'car_type' category
    type_counts = dataframe['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts



def get_bus_indexes(data_frame):
    if 'bus' not in data_frame.columns:
        raise ValueError("The 'bus' column is not present in the DataFrame.")

    bus_mean = data_frame['bus'].mean()

    # Filter indices where bus values are greater than twice the mean
    selected_indices = data_frame[data_frame['bus'] > 2 * bus_mean].index

    return sorted(selected_indices)



def filter_routes(df):

    average_truck = df["truck"].mean()
    print(f"the mean of truck column is {average_truck}")

    # filter rows where the average truck value is greater than 7
    filtered_routes = df.loc[df["truck"] > average_truck, "route"]
    print(f"\ntotal rows of route column where the value of truck column are greater then the mean of truck column are: {len(filtered_routes)}")
    
    print(f"\nsorted list of unique values of route columns for which above condition lies")
    sorted_routes = sorted(filtered_routes.unique().tolist())

    return sorted_routes


def multiply_matrix(input_df):
    modified_df = input_df.copy()

    for row_index, row in modified_df.iterrows():
        for col_index, value in row.items():
            if value > 20:
                modified_df.at[row_index, col_index] = round(value * 0.75, 1)
            else:
                modified_df.at[row_index, col_index] = round(value * 1.25, 1)

    return modified_df



def parse_time(row):
    # Convert startDay and endDay to integers representing days of the week
    days_of_week = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    
    start_day = days_of_week[row['startDay']]
    end_day = days_of_week[row['endDay']]
    
    start_time = pd.to_datetime(row['startTime']).time()
    end_time = pd.to_datetime(row['endTime']).time()
    
    return start_day, start_time, end_day, end_time


def check_time_completeness(df):
    # Apply the parse_time function to convert timestamps
    df[['startDay', 'startTime', 'endDay', 'endTime']] = df.apply(parse_time, axis=1, result_type='expand')
    
    df.set_index(['id', 'id_2'], inplace=True)
    
    # Initialize a boolean series indicating correct timestamps
    correct_timestamps = pd.Series(True, index=df.index)
    print(correct_timestamps)
    
    # Check for incorrect timestamps
    for day in range(7):
        for time in pd.date_range('00:00:00', '23:59:59', freq='1s').time:
            mask = (df['startDay'] <= day) & (df['endDay'] >= day) & (df['startTime'] <= time) & (df['endTime'] >= time)
            correct_timestamps &= mask
    
    # Reset the index to get the desired MultiIndex
    correct_timestamps.reset_index(inplace=True)
    
    return correct_timestamps



Question1 = generate_car_matrix(df)
print(Question1)


Question2= get_type_count(df)
print(Question2)


Question3 = get_bus_indexes(df)
print(Question3)


Question4 = filter_routes(df)
print(Question4)


Question5 = multiply_matrix(Question1)
print(Question5)

Question6 = check_time_completeness(df2.head(30))
print(Question6)
