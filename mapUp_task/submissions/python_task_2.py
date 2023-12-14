import pandas as pd
import os

# read csv from dataset
script_directory = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join(script_directory, '../datasets/dataset-3.csv')
df = pd.read_csv(csv_file_path)


def calculate_distance_matrix(df):
    data = df.to_dict(orient='list')

    matrix_size = len(data['id_start'])
    matrix = pd.DataFrame(0.0, index=data['id_start'], columns=data['id_start'], dtype=float)

    # Fill the matrix with distances
    for i in range(matrix_size - 1):
        start_id = data['id_start'][i]
        end_id = data['id_end'][i]
        distance = data['distance'][i]

        matrix.at[start_id, end_id] = distance
        matrix.at[end_id, start_id] = distance

    # Calculate cumulative distances
    for i in range(matrix_size):
        for j in range(i + 1, matrix_size):
            matrix.iloc[i, j] = matrix.iloc[i, j - 1] + matrix.iloc[j - 1, j]

            # Populate the lower triangle of the matrix
            matrix.iloc[j, i] = matrix.iloc[i, j]

    matrix = matrix.fillna(0.0)

    pd.set_option('display.float_format', '{:.2f}'.format)

    return matrix


def unroll_distance_matrix(df):
    id_start_list = []
    id_end_list = []
    distance_list = []

    for id_start, row in df.iterrows():
        for id_end, distance in row.iteritems():
            # Skip the diagonal entries (same id_start and id_end)
            if id_start != id_end:
                id_start_list.append(id_start)
                id_end_list.append(id_end)
                distance_list.append(distance)

    result_df = pd.DataFrame({'id_start': id_start_list, 'id_end': id_end_list, 'distance': distance_list})

    return result_df


def find_ids_within_ten_percentage_threshold(dataframe, reference_value):
    # Filter rows with the given reference_value in id_start column
    reference_rows = dataframe[dataframe['id_start'] == reference_value]

    avg_distance = reference_rows['distance'].mean()

    threshold = 0.1 * avg_distance

    # Filter rows within the threshold range
    within_threshold_rows = dataframe[
        (dataframe['distance'] >= avg_distance - threshold) &
        (dataframe['distance'] <= avg_distance + threshold)
    ]

    result = sorted(within_threshold_rows['id_start'].unique())

    return result


def calculate_toll_rate(input_df):
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    
    for vehicle_type in rate_coefficients.keys():
        input_df[vehicle_type] = 0.0
    
    # Calculate toll rates for each row based on the distance and rate coefficients
    for index, row in input_df.iterrows():
        for vehicle_type, rate_coefficient in rate_coefficients.items():
            input_df[vehicle_type] = rate_coefficient * input_df['distance']

    return input_df


def calculate_time_based_toll_rates(df):
    df['start_day'] = ''
    df['end_day'] = ''
    df['start_time'] = ''
    df['end_time'] = ''
    time_intervals = [(('00:00:00', '10:00:00'), 0.8),
                      (('10:00:00', '18:00:00'), 1.2),
                      (('18:00:00', '23:59:59'), 0.8),
                      (('00:00:00', '23:59:59'), 0.7)
                    ]
    new_rows = []
    for index, row in df.iterrows():
        for i in range(4):
            if i==0:
                start_time = str(time_intervals[0][0][0])
                end_time = str(time_intervals[0][0][1])
                discount_factor = time_intervals[0][1]
                modified_row = row.copy()
                modified_row['start_day'] = 'Monday'
                modified_row['end_day'] = 'Friday'
                modified_row['start_time'] = start_time
                modified_row['end_time'] = end_time
                
                modified_row['moto'] = round(modified_row['moto'] * discount_factor, 2)
                modified_row['car'] = round(modified_row['car'] * discount_factor, 2)
                modified_row['rv'] = round(modified_row['rv'] * discount_factor, 2)
                modified_row['bus'] = round(modified_row['bus'] * discount_factor, 2)
                modified_row['truck'] = round(modified_row['truck'] * discount_factor, 2)
                new_rows.append(modified_row)
                
            if i==1:
                start_time = str(time_intervals[1][0][0])
                end_time = str(time_intervals[1][0][1])
                discount_factor = time_intervals[1][1]
                modified_row = row.copy()
                modified_row['start_day'] = 'Thuesday'
                modified_row['end_day'] = 'Saturday'
                modified_row['start_time'] = start_time
                modified_row['end_time'] = end_time
                
                modified_row['moto'] = round(modified_row['moto'] * discount_factor, 2)
                modified_row['car'] = round(modified_row['car'] * discount_factor, 2)
                modified_row['rv'] = round(modified_row['rv'] * discount_factor, 2)
                modified_row['bus'] = round(modified_row['bus'] * discount_factor, 2)
                modified_row['truck'] = round(modified_row['truck'] * discount_factor, 2)
                new_rows.append(modified_row)
            if i==2:
                start_time = str(time_intervals[2][0][0])
                end_time = str(time_intervals[2][0][1])
                discount_factor = time_intervals[2][1]
                modified_row = row.copy()
                modified_row['start_day'] = 'Wednesday'
                modified_row['end_day'] = 'Sunday'
                modified_row['start_time'] = start_time
                modified_row['end_time'] = end_time
                
                modified_row['moto'] = round(modified_row['moto'] * discount_factor, 2)
                modified_row['car'] = round(modified_row['car'] * discount_factor, 2)
                modified_row['rv'] = round(modified_row['rv'] * discount_factor, 2)
                modified_row['bus'] = round(modified_row['bus'] * discount_factor, 2)
                modified_row['truck'] = round(modified_row['truck'] * discount_factor, 2)
                new_rows.append(modified_row)
            if i==3:
                start_time = str(time_intervals[3][0][0])
                end_time = str(time_intervals[3][0][1])
                discount_factor = time_intervals[3][1]
                modified_row = row.copy()
                modified_row['start_day'] = 'Saturday'
                modified_row['end_day'] = 'Sunday'
                modified_row['start_time'] = start_time
                modified_row['end_time'] = end_time
                
                modified_row['moto'] = round(modified_row['moto'] * discount_factor, 2)
                modified_row['car'] = round(modified_row['car'] * discount_factor, 2)
                modified_row['rv'] = round(modified_row['rv'] * discount_factor, 2)
                modified_row['bus'] = round(modified_row['bus'] * discount_factor, 2)
                modified_row['truck'] = round(modified_row['truck'] * discount_factor, 2)
                new_rows.append(modified_row)

    new_df = pd.DataFrame(new_rows)
    new_df['start_time'] = pd.to_datetime(new_df['start_time'], format='%H:%M:%S').dt.time
    new_df['end_time'] = pd.to_datetime(new_df['end_time'], format='%H:%M:%S').dt.time
    
    return new_df


# calling all fuction
Question1 = calculate_distance_matrix(df)
print(Question1)


Question2 = unroll_distance_matrix(Question1)
print(Question2)


reference_value = 1001400
Question3 = find_ids_within_ten_percentage_threshold(Question2, reference_value)
print(Question3)


Question4 = calculate_toll_rate(Question2)
print(Question4)


Question5 = calculate_time_based_toll_rates(Question4)
print(Question5)
