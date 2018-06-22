import StringIO
import sys
import unittest
import diskspace
import os
import subprocess
from diskspace import bytes_to_readable, print_tree, show_space_list,subprocess_check_output

class TestDiskSpaceMethods(unittest.TestCase):

    def test_zero_bytes_to_readable(self):
        blocks = 0
        self.assertEqual(diskspace.bytes_to_readable(blocks), '0.00B')

    def test_kbytes_to_readable(self):
        blocks = 2
        self.assertEqual(diskspace.bytes_to_readable(blocks), '1.00Kb') 

    def test_mbytes_to_readable(self):
        blocks = 2*1024
        self.assertEqual(diskspace.bytes_to_readable(blocks), '1.00Mb')

    def test_gbytes_to_readable(self):
        blocks = 2*1024*1024
        self.assertEqual(diskspace.bytes_to_readable(blocks), '1.00Gb')

    def test_tbytes_to_readable(self):
        blocks = 2*1024*1024*1024
        self.assertEqual(diskspace.bytes_to_readable(blocks), '1.00Tb')

    def test_display_correct_output_for_command(self):
        command = 'echo test'
        output = diskspace.subprocess_check_output(command)
        self.assertEqual('test\n', output)

    def test_raises_error_for_invalid_command(self):
        command = '1'
        with self.assertRaises(OSError):
                output = diskspace.subprocess_check_output(command)

    def test_subprocess_check_output(self):
        depth = -1
        abs_directory = os.path.abspath('.')
        string = 'du '

        if depth != -1:
            string += '-d {} '.format(depth)
        
        string += abs_directory
        result = subprocess.check_output(string.strip().split(' '))
        self.assertEqual(subprocess_check_output(string),result)
    
    def test_show_space_list(self):
        self.assertIsNone(show_space_list(directory = '.', depth = 0, order=True))

    def show_space_list_test(self):
        file_tree = {'/home/mock': {'print_size': '2.00Kb','children': [], 'size': 4}}
        file_tree_node = {'print_size': '2.00Kb', 'children': [], 'size': 4}
        largest_size = 6
        total_size = 4

        caps = StringIO.StringIO()
        sys.stdout = caps
        print_space_list(largest_size, file_tree, path, total_size)
        result = "  Size   (%)  File\n2.00Kb  100%  {}\n".format(path)
        sys.stdout = sys.__stdout__
        self.assertEqual(result, caps.getvalue())

    def test_print_tree(self):
        largest_size = 8
        total_size = 4
        cmd = 'du '
        path = os.path.abspath('.')
        cmd += path
        file_tree = {path: {'print_size': '50.00Kb', 'children': [], 'size': 3}}

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        print_tree(file_tree, file_tree[path], path, largest_size, total_size)
        
        sys.stdout = sys.__stdout__
        self.assertEqual('50.00Kb   75%  '+ path, capturedOutput.getvalue().strip())

if __name__ == '__main__':
    unittest.main()