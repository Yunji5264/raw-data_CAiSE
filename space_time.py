from class_predefine import *

spatial_granularity_mapping = {}
for hierarchy in hS_F:
    spatial_granularity_mapping.update({level: value for value, level in hierarchy})

temporal_granularity_mapping = {}
for hierarchy in hT_F:
    temporal_granularity_mapping.update({level: value for value, level in hierarchy})

# For spatial parameters
def get_space(spatial_parameter_list, df):
    with_granularity = []
    for param in spatial_parameter_list:
        granularity_value = spatial_granularity_mapping[param.spatialLevel]
        with_granularity.append((granularity_value, param))

    if not with_granularity:
        print("No valid spatial parameters found.")
        return None, None

    # Sort by granularity value
    sorted_para = sorted(with_granularity, key=lambda x: x[0])

    # Return the smallest and largest granularity items
    spatial_min = sorted_para[0][1]  # Item with smallest granularity value
    spatial_max = sorted_para[-1][1]  # Item with largest granularity value
    # Define the spatial granularity, which is the maximum granularity level in all spatial parameters
    spatial_granularity = spatial_max.spatialLevel
    # Define the spatial scope level, which is the minimum granularity level in all spatial parameters
    spatial_scope_level = spatial_min.spatialLevel

    # Get the saptial scope list
    # Extract column name from the spatial_min parameter
    column_name = spatial_min.dataName
    # Get unique values from the corresponding column in the DataFrame
    spatial_scope = df[column_name].dropna().unique()

    return spatial_granularity, spatial_scope_level, spatial_scope



# For temporal parameters
def get_time(temporal_parameter_list, df):
    with_granularity = []
    for param in temporal_parameter_list:
        granularity_value = temporal_granularity_mapping[param.temporalLevel]
        with_granularity.append((granularity_value, param))

    if not with_granularity:
        print("No valid spatial parameters found.")
        return None, None

    # Sort by granularity value
    sorted_para = sorted(with_granularity, key=lambda x: x[0])

    # Return the smallest and largest granularity items
    temporal_min = sorted_para[0][1]  # Item with smallest granularity value
    temporal_max = sorted_para[-1][1]  # Item with largest granularity value
    # Define the temporal granularity, which is the maximum granularity level in all temporal parameters
    temporal_granularity = temporal_max.temporalLevel
    # Define the temporal scope level, which is the minimum granularity level in all temporal parameters
    temporal_scope_level = temporal_min.temporalLevel

    # Get the saptial scope
    # Extract column name from the temporal_min parameter
    column_name = temporal_min.dataName
    temporalScopeStart = df[column_name].dropna().unique().min()
    temporalScopeEnd = df[column_name].dropna().unique().max()

    return temporal_granularity, temporal_scope_level, temporalScopeStart, temporalScopeEnd

