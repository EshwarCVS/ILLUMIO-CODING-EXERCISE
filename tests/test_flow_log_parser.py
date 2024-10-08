import unittest
import tempfile
import os
from src.flow_log_parser import parse_flow_logs, parse_lookup_table, write_results

class TestFlowLogParser(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.flow_log_file = os.path.join(self.temp_dir, 'flow_log.txt')
        self.lookup_file = os.path.join(self.temp_dir, 'lookup.csv')
        self.output_file = os.path.join(self.temp_dir, 'output.csv')

        with open(self.flow_log_file, 'w') as f:
            f.write("2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 49153 443 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
            f.write("2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 49154 23 6 15 12000 1620140761 1620140821 REJECT OK\n")

        with open(self.lookup_file, 'w') as f:
            f.write("dstport,protocol,tag\n")
            f.write("443,tcp,sv_P2\n")
            f.write("23,tcp,sv_P1\n")

    def tearDown(self):
        for file in [self.flow_log_file, self.lookup_file, self.output_file]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.temp_dir)

    def test_parse_flow_log(self):
        # Test flow log parsing and result writing
        lookup_dict = parse_lookup_table(self.lookup_file)
        tag_counts, port_protocol_counts = parse_flow_logs(self.flow_log_file, lookup_dict)
        write_results(tag_counts, port_protocol_counts, self.output_file)

        with open(self.output_file, 'r') as f:
            output = f.read()

        # Check if tag counts are correct
        self.assertIn("sv_p2,1", output) # Expects lowercase elements
        self.assertIn("sv_p1,1", output)

        # Check if port/protocol counts are correct
        self.assertIn("443,tcp,1", output)
        self.assertIn("23,tcp,1", output)

    def test_load_lookup_table(self):
        # Test lookup table loading
        lookup = parse_lookup_table(self.lookup_file)

        # Validate that the lookup table is parsed correctly
        self.assertEqual(lookup[('443', 'tcp')], 'sv_p2') # Expects lowercase elements
        self.assertEqual(lookup[('23', 'tcp')], 'sv_p1')

if __name__ == '__main__':
    unittest.main()