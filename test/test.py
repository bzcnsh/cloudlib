import sys
import os
test_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(test_dir)
sys.path.append(root_dir)
import unittest
from cloudlib import data as clib
import pprint

class UtilitiesTestCase(unittest.TestCase):
   def setUp(self):
      print("setup")
      self.pp = pprint.PrettyPrinter(indent=3)
      self.testdict = {'key1': 'val1', 'key2': 'val2', 'key3': ['text', 'text2'] }

   def tearDown(self):
      print("tear down")

   def test_runProcess(self):
      cmd = ["echo", "test"]
      rtn = clib.runProcess(cmd)
      expected = {'returncode': 0, 'stdout': "test\n", 'stderr': "", 'cmd': cmd}
      assert cmp(rtn, expected) == 0, "unexpected result"

   def test_runProcessFromTemplate(self):
      rtn = clib.runProcessFromTemplate(test_dir + '/runProcessFromTemplateTest', {'instring': 'test'})
      del rtn['cmd']
      expected = {'returncode': 0, 'stdout': "test\n", 'stderr': "", 'command_text': "#!/bin/bash\necho test"}
      assert cmp(rtn, expected) == 0, "unexpected result"

   def write_read_test(self, filename):
      clib.writeDataFile(filename, self.testdict)
      data = clib.readDataFile(filename)
      assert cmp(data, self.testdict) == 0, "data corrupted during read/write for " + filename

   #write python dict to file
   #read data back
   def test_writeDataFile_yaml(self):
      self.write_read_test('/tmp/test.yml')
      self.write_read_test('/tmp/test.json')
      self.write_read_test('/tmp/test.toml')

if __name__ == '__main__':
   unittest.main()

