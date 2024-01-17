def find_content_in_dict(d):
    # Check if the argument is a dictionary
    if isinstance(d, dict):
        # Iterate through each key-value pair
        for key, value in d.items():
            # If the key is 'content', return the value
            if key == 'content':
                return value
            # If the value is a dictionary, recursively search it
            elif isinstance(value, dict):
                found = find_content_in_dict(value)
                # If the key was found in the nested dictionary, return the value
                if found is not None:
                    return found
            # If the value is a list, iterate through it and search any dictionaries within it
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        found = find_content_in_dict(item)
                        # If the key was found in any dictionary within the list, return the value
                        if found is not None:
                            return found
    # Return None if 'content' key is not found in the dictionary or its sub-dictionaries
    return None