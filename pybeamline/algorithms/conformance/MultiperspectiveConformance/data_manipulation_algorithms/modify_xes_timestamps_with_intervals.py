
import gzip
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import random

def modify_xes_timestamps(input_file, output_file, max_random_days=10):
    # Open and parse the XES file
    with gzip.open(input_file, 'rt', encoding='utf-8') as file:
        xml_content = file.read()

    root = ET.fromstring(xml_content)

    # Determine the first timestamp in the file
    first_timestamp = None
    for event in root.findall(".//{http://www.xes-standard.org/}event"):
        timestamp_element = event.find("{http://www.xes-standard.org/}string[@key='time:timestamp']")
        if timestamp_element is not None:
            timestamp_str = timestamp_element.get("value")
            event_time = datetime.fromisoformat(timestamp_str)
            if first_timestamp is None or event_time < first_timestamp:
                first_timestamp = event_time

    if first_timestamp is None:
        raise ValueError("No timestamps found in the file.")

    # Adjust timestamps for each trace
    for trace in root.findall(".//{http://www.xes-standard.org/}trace"):
        # Generate a random base datetime within the specified max range of days
        random_offset = timedelta(days=random.uniform(0, max_random_days))
        base_datetime = first_timestamp + random_offset

        trace_start_time = None

        for event in trace.findall(".//{http://www.xes-standard.org/}event"):
            timestamp_element = event.find("{http://www.xes-standard.org/}string[@key='time:timestamp']")
            if timestamp_element is not None:
                timestamp_str = timestamp_element.get("value")
                event_time = datetime.fromisoformat(timestamp_str)

                # Set the base time if not already set
                if trace_start_time is None:
                    trace_start_time = event_time

                # Calculate the new timestamp based on the difference
                time_difference = event_time - trace_start_time
                new_timestamp = base_datetime + time_difference
                timestamp_element.set("value", new_timestamp.isoformat())

    # Write the modified XES back to a gzip file
    tree = ET.ElementTree(root)
    with gzip.open(output_file, 'wb') as file:
        tree.write(file, encoding='utf-8', xml_declaration=True)

# Usage example
input_file = "extension-log-noisy-4.xes.gz"
output_file = "modified-extension-log-noisy-4.xes.gz"
max_random_days = 10  # Adjust this value to change the random interval range

modify_xes_timestamps(input_file, output_file, max_random_days)
