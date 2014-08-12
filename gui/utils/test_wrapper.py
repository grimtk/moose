import sys
import unittest
import doctest

import wrapper

options = {}

"""
#######################################################################
Test the function that determines the units the memory is given in
and then determines a multiplier to convert the units to MB.
#######################################################################

>>> import wrapper
>>> wrapper.get_mem_units("1000kb")
('kb', 1024.0)

>>> wrapper.get_mem_units("1000mb")
('mb', 1048576.0)

>>> wrapper.get_mem_units("1000MB")
('MB', 1048576.0)

>>> wrapper.get_mem_units("2GB")
('GB', 1073741824.0)

>>> wrapper.get_mem_units("1000")
('None', -1)

>>> wrapper.get_mem_units("1kb")
('kb', 1024.0)

>> from socket import gethostname
>> clustername = wrapper.getClusterName()
>> print clustername
rocky

#######################################################################
Test the function that checks if the number of cpus or cores
requested is sensible.
#######################################################################

>>> clustername = 'fission'
>>> options= {'executable': 'Unknown', 'placement': 'exclusive', \
...       'ncpus': 8, 'project': 'neams', 'debug': False, \
...       'memory': '2048MB', 'chunks': 1, 'mpiprocs': 8, \
...       'walltime': '10:00:00'}
>>> resourceRequestDict = {}
>>> resourceRequestDict['ncpus'] = 0
>>> wrapper.check_procs(options, clustername, resourceRequestDict)
"""

class TestOptions(unittest.TestCase):

   def setUp(self):
      #opt,arg = wrapper.getOptions()
      #self.options = opt
      #del arg
      #del sys.argv
      self.clustername = 'fission'
      self.resourceRequestDict = {}
      

   def test_correct_number_cores_for_machine(self):
      returncode = wrapper.check_procs(options, self.clustername, \
                           self.resourceRequestDict)
      self.assertEqual(returncode, 0)

   def test_check_for_correct_memory_units(self):
      mem_units,multiplier = wrapper.get_mem_units("1000kb")
      self.assertEqual(mem_units, "kb")
      self.assertEqual(multiplier, 1024.0)

      mem_units,multiplier = wrapper.get_mem_units("1000mb")
      self.assertEqual(mem_units, "mb")
      self.assertEqual(multiplier, 1048576.0)

      mem_units,multiplier = wrapper.get_mem_units("1000MB")
      self.assertEqual(mem_units, "MB")
      self.assertEqual(multiplier, 1048576.0)

#----------------------------------------------------------------------

def test_main():
   opt,arg = wrapper.getOptions()
   options = opt
   #del arg
   del sys.argv[1:]
   clustername = 'fission'
   resourceRequestDict = {}
   if options.debug == True:
      printOptions(options)
#   suite = unittest.TestLoader().loadTestsFromTestCase(TestOptions)
   #suite1 = unittest.TestLoader().loadTestsFromTestCase(TestNCPUOptions)
   #suite2 = unittest.TestLoader().loadTestsFromTestCase(TestMemoryOptions)
   #suite  = unittest.TestSuite([suite1, suite2])
#   unittest.TextTestRunner(verbosity=2).run(suite)
   unittest.main()


#######################################################################
#######################################################################

#suite = unittest.TestLoader().loadTestsFromTestCase(TestOptions)
#suite1 = unittest.TestLoader().loadTestsFromTestCase(TestNCPUOptions)
#suite2 = unittest.TestLoader().loadTestsFromTestCase(TestMemoryOptions)
#suite  = unittest.TestSuite([suite1, suite2])
#unittest.TextTestRunner(verbosity=2).run(suite)

#def suite():
#    suite = unittest.TestSuite()
#    suite.addTest(WidgetTestCase('test_default_size'))
#    suite.addTest(WidgetTestCase('test_resize'))
#    return suite



if __name__ == "__main__":
   #self.args = arg
   #del opt
   #print >> sys.stderr, 'options=',self.options, type(self.options)
   #print >> sys.stderr, 'args=',self.args, type(self.args)
   test_main()
#   doctest.testmod()

