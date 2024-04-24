#q1 - Write pseudocode to measure average latency and bandwidth using the simulator provided
# monitor output (as shown in Table 1.0). The pseudocode needs to be efficient and robust.


'''
Simulator
Class:
Properties:
- noc_frequency
- cpu_buffer_size
- io_buffer_size
- system_memory_latency
- cpu_arbitration_rate
- io_arbitration_rate
- throttling_probability


- get_powerlimit_threshold():
If random value < throttling_probability:
Return 1 // Throttle
Else:
Return 0 // No throttle

- generate_monitor_output(num_transactions):
    Initialize output string with header
    Initialize timestamp to 0
    Loop num_transactions times:
        Randomly choose transaction type(Read or Write)
        If transaction type is Read:
            Set data as '-'
            Set latency as system_memory_latency
        Else(transaction type is Write):
            Generate random data
            Generate random latency
        Append transaction details to output string
        Update timestamp based on latency and NOC frequency
    Return generated output

- get_buffer_occupancy(buffer_id):
            If buffer_id is CPU:
                Return random integer between 0 and cpu_buffer_size
            Else if buffer_id is IO:
                Return random integer between 0 and io_buffer_size
            Else:
                Return 0  // Placeholder

        - get_arbrates(agent_type):
            If agent_type is CPU:
                Return cpu_arbitration_rate
            Else if agent_type is IO:
                Return io_arbitration_rate
            Else:
                Return 0  // Placeholder
Transaction Class:
    Properties:
        - timestamp
        - txn_type
        - data

parse_monitor_output(output):
    Initialize empty list transactions
    Split output string into lines
    Iterate over lines, skipping header line:
        If line is not empty:
            Split line into parts
            If parts count >= 3:
                Extract timestamp, txn_type, and data
                Append Transaction object to transactions list
            Else:
                Print "Invalid line format"
    Return transactions list

calculate_latency(transactions):
    Initialize empty list read_timestamps
    Initialize total_latency to 0
    Initialize total_reads to 0
    Iterate over transactions:
        If txn_type is Read:
            Append timestamp to read_timestamps
        Else if txn_type is Write:
            If read_timestamps is not empty:
                Pop earliest read timestamp
                Calculate latency and add to total_latency
                Increment total_reads
    Calculate average_latency (total_latency / total_reads) if total_reads > 0, else 0
    Return average_latency

calculate_bandwidth(transactions):
    If transactions list is empty:
        Return 0
    Initialize total_data_transferred to 0
    Extract start_time from first transaction and end_time from last transaction
    Calculate total_time as end_time - start_time
    Iterate over transactions:
        If txn_type is Write:
            Add length of data to total_data_transferred
    Calculate bandwidth as total_data_transferred / total_time if total_time > 0, else 0
    Return bandwidth

'''