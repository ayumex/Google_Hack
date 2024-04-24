import random

class Simulator:
    def __init__(self, noc_frequency):
        self.noc_frequency = noc_frequency
        self.cpu_buffer_size = 100
        self.io_buffer_size = 100
        self.system_memory_latency = 10
        self.cpu_arbitration_rate = 0.5
        self.io_arbitration_rate = 0.5
        self.throttling_probability = 0.05

    def get_powerlimit_threshold(self):
        if random.random() < self.throttling_probability:
            return 1
        else:
            return 0

    def generate_monitor_output(self, num_transactions):
        output = "Timestamp TxnType Data (32B)\n"
        timestamp = 0
        for _ in range(num_transactions):
            txn_type = random.choice(['Rd', 'Wr'])
            if txn_type == 'Rd':
                data = '-'
                latency = self.system_memory_latency
            else:
                data = ''.join(random.choices('0123456789abcdef', k=8))
                latency = random.randint(1, 10)
            output += f"{timestamp} {txn_type} {data}\n"
            timestamp += latency * self.noc_frequency
        return output

    def get_buffer_occupancy(self, buffer_id):
        if buffer_id == 'CPU':
            return random.randint(0, self.cpu_buffer_size)
        elif buffer_id == 'IO':
            return random.randint(0, self.io_buffer_size)
        else:
            return 0

    def get_arbrates(self, agent_type):
        if agent_type == 'CPU':
            return self.cpu_arbitration_rate
        elif agent_type == 'IO':
            return self.io_arbitration_rate
        else:
            return 0


# Example usage
simulator = Simulator(noc_frequency=1)

monitor_output = simulator.generate_monitor_output(10)
print("Generated Monitor Output:")
print(monitor_output)

cpu_buffer_occupancy = simulator.get_buffer_occupancy('CPU')
io_arbitration_rate = simulator.get_arbrates('IO')

print("\nCPU Buffer Occupancy:", cpu_buffer_occupancy)
print("IO Arbitration Rate:", io_arbitration_rate)


###########################################################################################################################3
class Transaction:
    def __init__(self, timestamp, txn_type, data=None):
        self.timestamp = timestamp
        self.txn_type = txn_type
        self.data = data


def parse_monitor_output(output):
    transactions = []
    lines = output.split('\n')
    for line in lines[1:]:
        if line.strip():
            parts = line.split(' ')
            if len(parts) >= 3:
                timestamp = int(parts[0])
                txn_type = parts[1]
                data = ' '.join(parts[2:]) if len(parts) > 2 else None
                transactions.append(Transaction(timestamp, txn_type, data))
            else:
                print("Invalid line format:", line)
    return transactions



def calculate_latency(transactions):
    read_timestamps = []
    total_latency = 0
    total_reads = 0
    for txn in transactions:
        if txn.txn_type == 'Rd':
            read_timestamps.append(txn.timestamp)
        elif txn.txn_type == 'Wr':
            if read_timestamps:
                read_timestamp = read_timestamps.pop(0)
                latency = txn.timestamp - read_timestamp
                total_latency += latency
                total_reads += 1
    average_latency = total_latency / total_reads if total_reads > 0 else 0
    return average_latency


def calculate_bandwidth(transactions):
    if not transactions:
        return 0

    total_data_transferred = 0
    start_time = transactions[0].timestamp
    end_time = transactions[-1].timestamp
    total_time = end_time - start_time

    for txn in transactions:
        if txn.txn_type == 'Wr':
            total_data_transferred += len(txn.data) if txn.data else 0
    bandwidth = total_data_transferred / total_time if total_time > 0 else 0
    return bandwidth


#Example
simulator = Simulator(noc_frequency=1)
monitor_output = simulator.generate_monitor_output(10)
print("Generated Monitor Output:")
print(monitor_output)

transactions = parse_monitor_output(monitor_output)

average_latency = calculate_latency(transactions)
print("\nAverage Latency:", average_latency)

bandwidth = calculate_bandwidth(transactions)
print("Bandwidth:", bandwidth)
