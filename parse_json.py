import json
import re
import os

def parse_json(data):

    if isinstance(data, (list, dict)):
        return data
    
    try:
        # Load the JSON data
        parsed = json.loads(data)

        parsed = get_data_obj(parsed)


        if parsed['data']:
            parsed = parsed['data']

        # If it's a dictionary, check for a 'data' key or return the dictionary as-is
        if isinstance(parsed, dict):
            return parsed.get('data', parsed)

        # If it's a list, return it directly
        elif isinstance(parsed, list):
            # Check if the list contains dictionaries
            if all(isinstance(item, dict) for item in parsed):
                # Convert list of dictionaries to a list of structured data
                structured_data = []
                for item in parsed:
                    structured_item = {key: item.get(key) for key in item}
                    structured_data.append(structured_item)
                return structured_data
            return parsed

        # For other data types (like int or str), wrap in a list
        else:
            return [parsed]

    except json.JSONDecodeError as original_error:
        try:
            # Correct common JSON formatting issues
            # Replace single quotes with double quotes
            corrected_data = data.replace("'", '"')
            corrected_data = re.sub(r"\'", "\"", data)

            # Add quotes around unquoted keys (e.g., {key: "value"} -> {"key": "value"})
            corrected_data = re.sub(r'(?<!")(\b\w+\b)(?!"):', r'"\1":', corrected_data)

            # Remove trailing commas in lists and objects
            corrected_data = re.sub(r',\s*([\]}])', r'\1', corrected_data)

            corrected_data = get_data_obj(corrected_data)

            # Parse the corrected data
            return json.loads(corrected_data)
        
        except json.JSONDecodeError:
            # If still failing, return None or consider logging the error details
            return None
        
def get_data_obj(parsed):
    # log parsed to this directory in a log file if parsed has string 'data' in it
    if parsed and isinstance(parsed, str) and 'data' in parsed: 
        # store in this files directory
        directory = os.path.dirname(os.path.realpath(__file__))
        # create a log file
        with open(f'{directory}/parsed.json', 'w') as f:
            json.dump(parsed, f, indent=4)


    # Find the start index of the "data" array
    start_index = parsed.find("'data': [") + len("'data': ")

    # Find the end index of the "data" array
    end_index = parsed.find(']}', start_index) + 1

    # Extract the "data" array substring if start and end indices are valid
    if start_index > 0 and end_index > 0:
        parsed = parsed[start_index:end_index]
    
    return parsed