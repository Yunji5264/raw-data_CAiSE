from class_predefine import *

# Helper function to find the longest common prefix for a list of paths
def find_longest_common_prefix(paths):
    if not paths:
        return []

    # Split each path into a list of levels
    split_paths = [path.split("/") for path in paths]

    # Find the shortest path for boundary comparison
    min_length = min(len(path) for path in split_paths)

    common_prefix = []
    for i in range(min_length):
        # Check if all paths share the same level at index i
        level_set = {path[i] for path in split_paths}
        if len(level_set) == 1:
            common_prefix.append(level_set.pop())
        else:
            break

    return common_prefix
#
# # Recursive function to validate the common prefix against theme_folder_structure
# def validate_common_prefix(theme_structure, common_prefix):
#     current_structure = theme_structure
#     for level in common_prefix:
#         if level in current_structure:
#             current_structure = current_structure[level]
#         else:
#             return False  # The prefix doesn't exist in the theme structure
#     return True

# Function to find the minimum common theme for all indicators
def find_min_common_theme(indicators, theme_structure):
    # Extract themes from all indicators
    themes = [indicator.indicatorTheme for indicator in indicators]

    # Find the longest common prefix
    common_prefix = find_longest_common_prefix(themes)

    # Validate the common prefix against the theme structure
    # if validate_common_prefix(theme_structure, common_prefix):
    return "/".join(common_prefix)  # Return the common prefix as a path
    # else:
    #     return "No common theme found"

