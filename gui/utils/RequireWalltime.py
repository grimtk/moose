import pbs

try:
   je = pbs.event()
   j = je.job
   pbs.logmsg(pbs.LOG_DEBUG, "$<<<<<------ Ready to run hook:%s" % (repr(j.Resource_List["mem"])) )
   if repr(j.Resource_List["mem"]) == None :
      je.reject("Job has no memory requested")

except pbs.UnsetResourceNameError:
   je.reject("Job has no walltime requested")

