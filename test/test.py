import sys
sys.path.append('../')
import unittest
from cloudlib import data as clib
import pprint

class UtilitiesTestCase(unittest.TestCase):
   def setUp(self):
      print("setup")
      self.pp = pprint.PrettyPrinter(indent=3)

   def tearDown(self):
      print("tear down")

   def test_runProcess(self):
      cmd = ["echo", "test"]
      rtn = clib.runProcess(cmd)
      expected = {'returncode': 0, 'stdout': "test\n", 'stderr': "", 'cmd': cmd}
      assert cmp(rtn, expected) == 0, "unexpected result"

   def test_runProcessFromTemplate(self):
      rtn = clib.runProcessFromTemplate('./runProcessFromTemplateTest', {'instring': 'test'})
      del rtn['cmd']
      expected = {'returncode': 0, 'stdout': "test\n", 'stderr': "", 'command_text': "#!/bin/bash\necho test"}
      assert cmp(rtn, expected) == 0, "unexpected result"
      

if __name__ == '__main__':
   unittest.main()

