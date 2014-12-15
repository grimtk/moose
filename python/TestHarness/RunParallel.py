from subprocess import *
from time import sleep
from timeit import default_timer as clock

from tempfile import TemporaryFile
#from Queue import Queue
from collections import deque
from Tester import Tester
from signal import SIGTERM

import os, sys, re, pickle

## This class provides an interface to run commands in parallel
#
# To use this class, call the .run() method with the command and the test
# options. When the test is finished running it will call harness.testOutputAndFinish
# to complete the test. Be sure to call join() to make sure all the tests are finished.
#
class RunParallel:

  ## Return this return code if the process must be killed because of timeout
  TIMEOUT = -999999

  def __init__(self, harness, max_processes=1, average_load=64.0):
    ## The test harness to run callbacks on
    self.harness = harness

    # Retrieve and store the TestHarness options for use in this object
    self.options = harness.getOptions()

    ## List of currently running jobs as (Popen instance, command, test, time when expires) tuples
    # None means no job is running in this slot
    self.jobs = [None] * max_processes

    # Requested average load level to stay below
    self.average_load = average_load

    # queue for jobs needing a prereq
    self.queue = deque()

    # Jobs that have been finished
    self.finished_jobs = set()

    # List of skipped jobs to resolve prereq issues for tests that never run
    self.skipped_jobs = set()

    # Jobs we are reporting as taking longer then 10% of MAX_TIME
    self.reported_jobs = set()

    # Reporting timer which resets when ever data is printed to the screen.
    self.reported_timer = clock()

  ## run the command asynchronously and call testharness.testOutputAndFinish when complete
  def run(self, tester, command, recurse=True):
    # First see if any of the queued jobs can be run but only if recursion is allowed on this run
    if recurse:
      self.startReadyJobs()

    # Now make sure that this job doesn't have an unsatisfied prereq
    if tester.specs['prereq'] != None and len(set(tester.specs['prereq']) - self.finished_jobs) and self.options.pbs is None:
      self.queue.append([tester, command, os.getcwd()])
      return

    # Make sure we are complying with the requested load average
    self.satisfyLoad()

    # Wait for a job to finish if the jobs queue is full
    while self.jobs.count(None) == 0:
      self.spinwait()

    # Pre-run preperation
    tester.prepare()

    job_index = self.jobs.index(None) # find an empty slot
    log( 'Command %d started: %s' % (job_index, command) )

    # It seems that using PIPE doesn't work very well when launching multiple jobs.
    # It deadlocks rather easy.  Instead we will use temporary files
    # to hold the output as it is produced
    try:
      if self.options.dry_run:
        tmp_command = command
        command = "echo"

      f = TemporaryFile()
      p = Popen([command],stdout=f,stderr=f,close_fds=True, shell=True)
      if self.options.dry_run:
        command = tmp_command
    except:
      print "Error in launching a new task"
      raise

    self.jobs[job_index] = (p, command, tester, clock(), f)

  def startReadyJobs(self):
    queue_items = len(self.queue)
    for i in range(0, queue_items):
      (tester, command, dirpath) = self.queue.popleft()
      saved_dir = os.getcwd()
      sys.path.append(os.path.abspath(dirpath))
      os.chdir(dirpath)
      # We want to avoid "dual" recursion so pass a False flag here
      self.run(tester, command, False)
      os.chdir(saved_dir)
      sys.path.pop()

  ## Return control to the test harness by finalizing the test output and calling the callback
  def returnToTestHarness(self, job_index):
    (p, command, tester, time, f) = self.jobs[job_index]

    log( 'Command %d done:    %s' % (job_index, command) )
    did_pass = True

    if p.poll() == None: # process has not completed, it timed out
    #if os.kill(p.pid,0) != None: # process has completed
      output = self.readOutput(f)
      output += '\n' + "#"*80 + '\nProcess terminated by test harness. Max time exceeded (' + str(tester.specs['max_time']) + ' seconds)\n' + "#"*80 + '\n'
      f.close()
      #os.kill(p.pid, SIGTERM)        # Python 2.4 compatibility
      p.terminate()                 # Python 2.6+

      if not self.harness.testOutputAndFinish(tester, RunParallel.TIMEOUT, output, time, clock()):
        did_pass = False
    else:
      output = 'Working Directory: ' + tester.specs['test_dir'] + '\nRunning command: ' + command + '\n'
      output += self.readOutput(f)
      f.close()

      if tester in self.reported_jobs:
        tester.specs.addParam('caveats', ['FINISHED'], "")

      if not self.harness.testOutputAndFinish(tester, p.returncode, output, time, clock()):
        did_pass = False

    if did_pass:
      self.finished_jobs.add(tester.specs['test_name'])
    else:
      self.skipped_jobs.add(tester.specs['test_name'])

    self.jobs[job_index] = None

  ## Don't return until one of the running processes exits.
  #
  # When a process exits (or times out) call returnToTestHarness and return from
  # this function.
  def spinwait(self, time_to_wait=0.05):
    now = clock()
    job_index = 0
    slot_freed = False
    for tuple in self.jobs:
      if tuple != None:
        (p, command, tester, start_time, f) = tuple
        ## None value of p.poll() indicates process hasn't terminated yet.
        if p.poll() != None or now > (start_time + float(tester.specs['max_time'])):
        #(pid, command, tester, start_time, f) = tuple
        # None value of os.kill(pid,0) indicates process hasn't terminated yet, still running.
        #print >> sys.stderr, "RunParallel.spinwait: p.pid=",p.pid
        #if os.kill(p.pid,0) != None or now > (start_time + float(tester.specs['max_time'])):
          # finish up as many jobs as possible, don't sleep until
          # we've cleared all of the finished jobs
          self.returnToTestHarness(job_index)
          # We just output to the screen so reset the test harness "activity" timer
          self.reported_timer = now

          slot_freed = True
          # We just reset the timer so no need to check if we've been waiting for awhile in
          # this iteration

        # Has the TestHarness done nothing for awhile
        elif now > (self.reported_timer + 10.0):
          # Has the current test been previously reported?
          if tester not in self.reported_jobs:
            if tester.specs.isValid('min_reported_time'):
              start_min_threshold = start_time + float(tester.specs['min_reported_time'])
            else:
              start_min_threshold = start_time + (0.1 * float(tester.specs['max_time']))

            threshold = max(start_min_threshold, (0.1 * float(tester.specs['max_time'])))

            if now >= threshold:
              self.harness.handleTestResult(tester.specs, '', 'RUNNING...', start_time, now, False)

              self.reported_jobs.add(tester)
              self.reported_timer = now

      job_index += 1

    if not slot_freed:
      sleep(time_to_wait)

  def satisfyLoad(self):
    # We'll always run at least one job regardless of load or we'll starve!
    while self.jobs.count(None) < len(self.jobs) and os.getloadavg()[0] >= self.average_load:
#      print "DEBUG: Sleeping... ", len(self.jobs) - self.jobs.count(None), " jobs running (load average: ", os.getloadavg()[0], ")\n"
      self.spinwait(0.5) # If the load average is high we'll sleep longer here to let things clear out
#      print "DEBUG: Ready to run (load average: ", os.getloadavg()[0], ")\n"

  ## Wait until all processes are done, then return
  def join(self):
    while self.jobs.count(None) != len(self.jobs):
      self.spinwait()
      self.startReadyJobs()

    print >> sys.stderr, "RunParallel.join: len(self.queue) = ",len(self.queue)
    if len(self.queue) != 0:
      # See if there are any tests left in the queue simply because their dependencies where skipped
      keep_going = True
      while keep_going:
        keep_going = False
        queue_items = len(self.queue)
        for i in range(0, queue_items):
          (tester, command, dirpath) = self.queue.popleft()
          if len(set(tester.specs['prereq']) & self.skipped_jobs):
            self.harness.handleTestResult(tester.specs, '', 'skipped (skipped dependency)')
            self.skipped_jobs.add(tester.specs['test_name'])
            keep_going = True
          else:
            self.queue.append([tester, command, dirpath])
      # Anything left is a cyclic dependency
      if len(self.queue) != 0:
        print "Cyclic or Invalid Dependency Detected!"
        for (tester, command, dirpath) in self.queue:
          print tester.specs['test_name']
        sys.exit(1)

    # Exit TestHarness as soon as queue is empty when running in pbs emulation mode
    elif self.options.pbs_emulator:
      sys.exit(0)

    # Return to TestHarness as soon as queue is empty
    else:
      return

  # This function reads output from the file (i.e. the test output)
  # but trims it down to the specified size.  It'll save the first two thirds
  # of the requested size and the last third trimming from the middle
  def readOutput(self, f, max_size=100000):
    first_part = int(max_size*(2.0/3.0))
    second_part = int(max_size*(1.0/3.0))
    output = ''

    f.seek(0)
    if self.harness.options.sep_files != True:
      output = f.read(first_part)     # Limit the output to 1MB
      if len(output) == first_part:   # This means we didn't read the whole file yet
        output += "\n" + "#"*80 + "\n\nOutput trimmed\n\n" + "#"*80 + "\n"
        f.seek(-second_part, 2)       # Skip the middle part of the file

        if (f.tell() <= first_part):  # Don't re-read some of what you've already read
          f.seek(first_part+1, 0)

    output += f.read()              # Now read the rest
    return output


  # Add a skipped job to the list
  def jobSkipped(self, name):
    self.skipped_jobs.add(name)

  def writeState(self):
    new_list = []
    #print >> sys.stderr, 'RunParallel.writeState: self.jobs=', self.jobs
    if self.jobs[0] is not None:
      for tuple in self.jobs:
        #print >> sys.stderr, 'RunParallel.writeState: tuple=', tuple
        (p, command, tester, start_time, f) = tuple
        new_list.append([p.pid, command, tester, start_time])

      #print p.pid

      f1 = open(os.path.join(os.getcwd(), "current_jobs"), "w")
      pickle.dump(new_list, f1)
      f1.close()


# PBS Defs
  def processPBSResults(self):
    # If batch file exists, check the contents for pending tests.
    #f = None
    print >> sys.stderr, "RunParallel.processPBSResults: self.options.pbs=",self.options.pbs
    print >> sys.stderr, "RunParallel.processPBSResults: self.options.pbs_emulator=",self.options.pbs_emulator
    #print >> sys.stderr, "RunParallel.processPBSResults: 1: f=",f
    #try:
    if self.options.pbs: 
      if os.path.exists(self.options.pbs):
        print >> sys.stderr, "RunParallel.processPBSResults: self.options.pbs 2nd if"
        f = open(self.options.pbs, "r")
    #except TypeError:
    #  f = None
    #try:
    if self.options.pbs_emulator: 
      if os.path.exists(self.options.pbs_emulator):
        print >> sys.stderr, "RunParallel.processPBSResults: self.options.pbs_emulator 2nd if"
        f = open(self.options.pbs_emulator, "r")
    #except TypeError:
    #  f = None

    print >> sys.stderr, "RunParallel.processPBSResults: 2: f=",f
    if f != None:
      batch_file = pickle.load(f)
      print >> sys.stderr, "RunParallel.processPBSResults: 2a: batch_file=",batch_file
      for tuple in batch_file:
        (pid, command, tester, start_time) = tuple

      #sys.exit(0)

      # Build a list of launched jobs
      #if self.options.pbs:
      #  batch_file = open(self.options.pbs)
      #elif self.options.pbs_emulator:
      #  batch_file = open(self.options.pbs_emulator)
      batch_list = [y.split(':') for y in [x for x in batch_file.read().split('\n')]]
      batch_file.close()
      print >> sys.stderr, "RunParallel.processPBSResults: 3: batch_list=",batch_list
      del batch_list[-1:]

      # Loop through launched jobs and match the TEST_NAME to determine correct stdout (Output_Path)
      for job in batch_list:
        print >> sys.stderr, "RunParallel.processPBSResults: 4: job=",job
        file = '/'.join(job[2].split('/')[:-2]) + '/' + job[3]

        # Build a Warehouse to hold the MooseObjects
        warehouse = Warehouse()

        # Build a Parser to parse the objects
        parser = Parser(self.factory, warehouse)

        # Parse it
        parser.parse(file)

        # Retrieve the tests from the warehouse
        testers = warehouse.getAllObjects()
        for tester in testers:
          self.augmentParameters(file, tester)

        for tester in testers:
          # Build the requested Tester object
          if job[1] == tester.parameters()['test_name']:
            # Create Test Type
            # test = self.factory.create(tester.parameters()['type'], tester)

            # Get PBS job status via qstat
            if self.options.pbs:
               qstat = ['qstat', '-f', '-x', str(job[0])]
               qstat_command = subprocess.Popen(qstat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
               qstat_stdout = qstat_command.communicate()[0]
               if qstat_stdout != None:
                 output_value = re.search(r'job_state = (\w+)', qstat_stdout).group(1)
               else:
                 return ('QSTAT NOT FOUND', '')

            # Get PBS emulator job status by checking if the job is still running
            elif self.options.pbs_emulator:
               try:
                 if os.kill(p.pid, 0) is None:
                   output_value = 'R'
                 else:
                   output_value = 'U'
               except:
                  output_value = 'F'

            # Report the current status of JOB_ID
            if self.options.pbs and output_value == 'F':
              # F = Finished. Get the exit code reported by qstat
              exit_code = int(re.search(r'Exit_status = (-?\d+)', qstat_stdout).group(1))

              # Read the stdout file
              if os.path.exists(job[2]):
                output_file = open(job[2], 'r')
                # Not sure I am doing this right: I have to change the TEST_DIR to match the temporary cluster_launcher TEST_DIR location, thus violating the tester.specs...
                tester.parameters()['test_dir'] = '/'.join(job[2].split('/')[:-1])
                outfile = output_file.read()
                output_file.close()
              else:
                # I ran into this scenario when the cluster went down, but launched/completed my job :)
                self.handleTestResult(tester.specs, '', 'FAILED (NO STDOUT FILE)', 0, 0, True)

              self.testOutputAndFinish(tester, exit_code, outfile)

            elif output_value == 'R':
              # Job is currently running
              self.handleTestResult(tester.specs, '', 'RUNNING', 0, 0, True)
            elif output_value == 'E':
              # Job is exiting
              self.handleTestResult(tester.specs, '', 'EXITING', 0, 0, True)
            elif output_value == 'Q':
              # Job is currently queued
              self.handleTestResult(tester.specs, '', 'QUEUED', 0, 0, True)
    else:
      return ('BATCH FILE NOT FOUND', '')

  def buildPBSBatch(self, output, tester):
    print >> sys.stderr, 'buildPBSBatch: output=', output
    # Create/Update the batch file
    if 'command not found' in output:
      return ('QSUB NOT FOUND', '')
    else:
      # Get the PBS Job ID using qstat
      results = re.findall(r'JOB_NAME: (\w+\d+) JOB_ID: (\d+) TEST_NAME: (\S+)', output, re.DOTALL)
      print >> sys.stderr, "buildPBSBatch:, results=", results, len(results)
      if len(results) != 0:
        if self.options.pbs:
           file_name = self.options.pbs
        elif self.options.pbs_emulator:
           file_name = self.options.pbs_emulator
        print >> sys.stderr, 'buildPBSBatch: file_name=', file_name
        job_list = open(os.path.abspath(os.path.join(tester.specs['executable'], os.pardir)) + '/' + file_name, 'a')
        for result in results:
          (test_dir, job_id, test_name) = result
          qstat_command = subprocess.Popen(['qstat', '-f', '-x', str(job_id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          qstat_stdout = qstat_command.communicate()[0]
          # Get the Output_Path from qstat stdout
          if qstat_stdout != None:
            output_value = re.search(r'Output_Path(.*?)(^ +)', qstat_stdout, re.S | re.M).group(1)
            output_value = output_value.split(':')[1].replace('\n', '').replace('\t', '')
          else:
            job_list.close()
            return ('QSTAT NOT FOUND', '')
          # Write job_id, test['test_name'], and Ouput_Path to the batch file
          job_list.write(str(job_id) + ':' + test_name + ':' + output_value + ':' + self.options.input_file_name  + '\n')
        # Return to TestHarness and inform we have launched the job
        job_list.close()
        return ('', 'LAUNCHED')
      else:
        return ('QSTAT INVALID RESULTS', '')

  def cleanPBSBatch(self):
    # Open the PBS batch file and assign it to a list
    if os.path.exists(self.options.pbs_cleanup):
      batch_file = open(self.options.pbs_cleanup, 'r')
      batch_list = [y.split(':') for y in [x for x in batch_file.read().split('\n')]]
      batch_file.close()
      del batch_list[-1:]
    else:
      print 'PBS batch file not found:', self.options.pbs_cleanup
      sys.exit(1)

    # Loop through launched jobs and delete whats found.
    for job in batch_list:
      if os.path.exists(job[2]):
        batch_dir = os.path.abspath(os.path.join(job[2], os.pardir)).split('/')
        if os.path.exists('/'.join(batch_dir)):
          shutil.rmtree('/'.join(batch_dir))
        if os.path.exists('/'.join(batch_dir[:-1]) + '/' + job[3] + '.cluster'):
          os.remove('/'.join(batch_dir[:-1]) + '/' + job[3] + '.cluster')
    os.remove(self.options.pbs_cleanup)

# END PBS Defs



## Static logging string for debugging
LOG = []
LOG_ON = False
def log(msg):
  if LOG_ON:
    LOG.append(msg)
    print msg
