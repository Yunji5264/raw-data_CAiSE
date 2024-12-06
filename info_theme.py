def find_longest_common_prefix(paths):
    """
    Find the longest common prefix among a list of paths.

    Parameters:
        paths (list): List of theme paths as strings.

    Returns:
        list: Longest common prefix as a list of levels.
    """
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


def validate_common_prefix(theme_structure, common_prefix):
    """
    Validate the common prefix against the theme folder structure.

    Parameters:
        theme_structure (dict): Nested dictionary representing the theme hierarchy.
        common_prefix (list): List of levels representing the common prefix.

    Returns:
        bool: True if the prefix is valid within the theme structure, False otherwise.
    """
    current_structure = theme_structure
    for level in common_prefix:
        if level in current_structure:
            current_structure = current_structure[level]
        else:
            return False  # The prefix doesn't exist in the theme structure
    return True


def find_min_common_theme(eis, theme_folder_structure):
    """
    Find the minimum common theme for the indicators (EIs).

    Parameters:
        eis (list): List of Existing Indicator objects.
        theme_folder_structure (dict): Nested dictionary representing the theme hierarchy.

    Returns:
        str: Minimum common theme path or None if no themes found.
    """
    # Extract themes from indicators
    themes = [ei.indicatorTheme for ei in eis if ei.indicatorTheme]  # Ensure indicatorTheme is not None

    if not themes:  # If themes list is empty
        print("No themes found for the provided indicators.")
        return None

    # Normalize theme paths
    themes = [theme.replace("\\", "/") for theme in themes]

    # Find the longest common prefix
    common_prefix = find_longest_common_prefix(themes)

    # Validate the common prefix against the theme folder structure
    if validate_common_prefix(theme_folder_structure, common_prefix):
        # Join the prefix back into a path
        return "/".join(common_prefix)
    else:
        print("Common prefix does not exist in the theme folder structure.")
        return None
