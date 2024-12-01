from pm4py.algo.discovery.dfg import algorithm as dfg_factory
from pm4py.objects.log.importer.xes import importer as xes_importer

import pickle
import os
import sys

# Function to load the event logs from a file and cache the parsed event logs
def load_event_log(file_path, *cache):
    ''' Load the event log from the file path 
    :param file_path: The path to the event log xes file
    :param cache: A boolean indicating whether to cache the parsed event log. cached event logs will be loaded from catched files upon subsequent calls
    :return: The parsed event log
    '''

    if cache == True:
        file_name = file_path.split("\\")[-1].split(".")[0]
        pm4py_cache_file = file_name + '_pm4py_event_log_cache' + '.pkl'

        if os.path.exists(pm4py_cache_file):
            # Load the parsed event log from the cache file
            with open(pm4py_cache_file, 'rb') as f:
                pm4py_event_log = pickle.load(f)

            print("Event log loaded from cache file")
        else:
            # Parse the event log
            pm4py_event_log = xes_importer.apply(file_path)

            # Save the parsed event log to a cache file
            with open(pm4py_cache_file, 'wb') as f:
                pickle.dump(pm4py_event_log, f)
            print("Event log loaded and cached")
    else:
        # Parse the event log
        pm4py_event_log = xes_importer.apply(file_path)
        print("Event log loaded")

    return pm4py_event_log

# Function to count the number of simultaneously active traces
def simultaneously_active_traces(event_log):
    ''' Count the number of simultaneously active traces 
    :param event_log: pm4py event log
    :return: The max number of simultaneously active traces
    '''
    # Initialize a list to store the start and end times of each trace
    trace_intervals = []

    # Iterate over all traces in the event log
    for trace in event_log:
        start_time = trace[0]["time:timestamp"]
        end_time = trace[-1]["time:timestamp"]
        trace_intervals.append((start_time, end_time))

    # Sort the intervals by start time
    trace_intervals.sort(key=lambda x: x[0])

    # Initialize variables to count the number of active traces
    max_active_traces = 0
    current_active_traces = 0
    intervals = []

    # Create a list of all start and end events
    for interval in trace_intervals:
        intervals.append((interval[0], 'start'))
        intervals.append((interval[1], 'end'))

    # Sort the events by time
    intervals.sort(key=lambda x: x[0])

    # Iterate over the events and count the number of active traces
    for event in intervals:
        if event[1] == 'start':
            current_active_traces += 1
            max_active_traces = max(max_active_traces, current_active_traces)
        else:
            current_active_traces -= 1

    return max_active_traces

# Function to calculate the average trace length
def trace_length(event_log):
    ''' Calculate the average and max trace length
    :param event_log: pm4py event log
    :return: average trace length and max trace length
    '''
    min_length = len(event_log[0]._list)
    total_length = 0
    max_length = 0
    for trace in event_log:
        total_length += len(trace._list)
        max_length = max(max_length, len(trace._list))
        min_length = min(min_length, len(trace._list))
    return (total_length / len(event_log)), min_length, max_length

# Function to calculate the average time between events in the DFG
def average_time_between_events(event_log):
    ''' Calculate the average time between two events
    :param event_log: pm4py event log
    :return: The average time between events
    '''
    dfg = dfg_factory.apply(event_log)

    time_differences = {key: [] for key in dfg.keys()}

    for trace in event_log:
        for i in range(len(trace) - 1):
            event1 = trace[i]
            event2 = trace[i + 1]
            key = (event1["concept:name"], event2["concept:name"])
            if key in time_differences:
                time_diff = (event2["time:timestamp"] - event1["time:timestamp"]).total_seconds()
                time_differences[key].append(time_diff)

    average_times = {}
    for key, times in time_differences.items():
        if times:
            average_time = sum(times) / len(times)
            average_times[key[0]] = (key[1], average_time)

    return average_times

if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 1:
        print("Usage: python Analysis.py <path_to_xes_file: string> <optional use cache?: boolean>")
        sys.exit(1)

    xes_file_path = sys.argv[1]

    print("Event log loading...")

    if len(sys.argv) == 2:
        event_log = load_event_log(xes_file_path, sys.argv[1])
    else:
        event_log = load_event_log(xes_file_path)

    print("----------------------------------------------")
    print("Calculating metrics...")

    print("----------------------------------------------")
    print("Total amount of traces: ")
    print (len(event_log))

    print("----------------------------------------------")
    print("Simultaneously active traces: ")
    print (simultaneously_active_traces(event_log))

    print("----------------------------------------------")
    print("Trace length: ")
    average, min, max = trace_length(event_log)
    print ("Average: " + str(average)
           + "\nMin: " + str(min)
           + "\nMax: " + str(max))

    print("----------------------------------------------")
    print("Average time between events: ")
    for event, time in average_time_between_events(event_log).items():
        print(event + " -> " + time[0] + " : " + str(time[1]))