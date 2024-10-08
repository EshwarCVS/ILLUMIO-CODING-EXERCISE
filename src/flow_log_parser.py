import csv
from collections import defaultdict
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Map protocol numbers to names based on IANA protocol numbers
PROTOCOL_MAP = {
    '6': 'tcp',    # TCP
    '17': 'udp',   # UDP
    '1': 'icmp',   # ICMP
    '2': 'igmp',   # IGMP
    '50': 'esp',   # ESP (Encapsulating Security Payload)
    '51': 'ah',    # AH (Authentication Header)
    # Add more protocols as needed based on IANA numbers from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
}

# Step 1: Parse the lookup table (csv)
def parse_lookup_table(lookup_file):
    lookup_dict = {}
    try:
        with open(lookup_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                dstport, protocol, tag = row
                lookup_dict[(dstport, protocol.lower())] = tag.lower()
    except IOError as e:
        logging.error(f"Error reading lookup file: {e}")
        raise
    return lookup_dict

# Step 2: Parse flow logs
def parse_flow_logs(flow_file, lookup_dict):
    tag_counts = {}
    port_protocol_counts = {}
    
    try:
        with open(flow_file, mode='r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) < 13:
                    logging.warning(f"Skipping invalid line: {line.strip()}")
                    continue  # Handle invalid format
                
                dstport = parts[6]
                protocol_num = parts[7]
                protocol = PROTOCOL_MAP.get(protocol_num, 'unknown')  # Get protocol name from the map
            
                # Lookup tag from the lookup table
                tag = lookup_dict.get((dstport, protocol), 'untagged')
                
                # Update tag counts
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
                
                # Update port/protocol counts
                key = (dstport, protocol)
                port_protocol_counts[key] = port_protocol_counts.get(key, 0) + 1
    except IOError as e:
        logging.error(f"Error reading flow log file: {e}")
        raise

    return tag_counts, port_protocol_counts

# Step 3: Write results to a file
def write_results(tag_counts: dict, port_protocol_counts: dict, output_file: str) -> None:
    """Write the output to a CSV file."""
    try:
        with open(output_file, mode='w') as file:
            # Write Tag Counts
            file.write("Tag Counts:\n")
            file.write("Tag,Count\n")
            for tag, count in tag_counts.items():
                file.write(f"{tag},{count}\n")
            
            # Write Port/Protocol Combination Counts
            file.write("\nPort/Protocol Combination Counts:\n")
            file.write("Port,Protocol,Count\n")
            for (port, protocol), count in port_protocol_counts.items():
                file.write(f"{port},{protocol},{count}\n")
    except IOError as e:
        logging.error(f"Error writing output file: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Parse flow log data and map to tags.")
    parser.add_argument("flow_log_file", help="Path to the flow log file")
    parser.add_argument("lookup_file", help="Path to the lookup table CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    args = parser.parse_args()

    lookup_dict = parse_lookup_table(args.lookup_file)
    tag_counts, port_protocol_counts = parse_flow_logs(args.flow_log_file, lookup_dict)
    write_results(tag_counts, port_protocol_counts, args.output_file)

if __name__ == "__main__":
    main()