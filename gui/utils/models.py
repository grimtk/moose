from django.db import models

class User(models.Model):
   g_user = models.CharField('Username', max_length=1024)
   g_desc = models.CharField('Description', max_length=1024)
   g_special = models.CharField('Special', max_length=5)
   g_deleted = models.CharField('Deleted?', max_length=5)
   g_creation_time = models.IntegerField('Creation Time', default=0)
   g_modification_time = models.IntegerField('Modification Time', default=0)
   g_request_id = models.IntegerField('Request ID', default=0)
   g_transaction_id = models.IntegerField('Transaction ID', default=0)
   g_active = models.CharField('Active', max_length=5)
   g_common_name = models.CharField('Name', max_length=1024)
   g_phone_number = models.CharField('Phone', max_length=1024)
   g_email_address = models.CharField('Email', max_length=1024)
   g_default_project = models.CharField('Default Project', max_length=1024)
   g_organization = models.CharField('Org', max_length=1024)

   def __unicode__(self):
      return (self.g_user)

   class Meta:
      db_table = 'g_user'


class Job(models.Model):
   g_creation_time = models.IntegerField('Creation Time',default=0)
   g_modification_time = models.IntegerField('Modification Time',default=0)
   g_deleted = models.CharField('Deleted?', max_length=5)
   g_request_id = models.IntegerField('Request_ID', default=0)
   g_transaction_id = models.IntegerField('Trans_ID',default=0)
   g_id = models.IntegerField('Id', default=0)
   g_job_id = models.CharField('Job_ID',max_length=1024)
   g_user = models.ForeignKey(User)
   #g_user = models.CharField('User',max_length=1024)
   g_project = models.CharField('Project',max_length=1024)
   g_machine = models.CharField('Machine',max_length=1024)
   g_charge = models.FloatField('Charge')
   g_queue = models.CharField('Queue', max_length=1024)
   g_type = models.CharField('Type', max_length=1024)
   g_stage = models.CharField('Stage', max_length=1024)
   g_quality_of_service = models.CharField('Quality of Service', max_length=1024)
   g_nodes = models.IntegerField('Nodes', default=0)
   g_processors = models.IntegerField('Procs', default=0)
   g_executable = models.CharField('Executable', max_length=1024)
   g_application = models.CharField('Application', max_length=1024)
   g_start_time = models.IntegerField('Start Time', default=0)
   g_end_time = models.IntegerField('End Time', default=0)
   g_wall_duration = models.IntegerField('Wall Duration', default=0)
   g_quote_id = models.CharField('Quote Id', max_length=1024)
   g_call_type = models.CharField('Call Type', max_length=1024)
   g_description = models.CharField('Description', max_length=1024)

   def __unicode__(self):
      return (self.g_job_id)

   class Meta:
      db_table = 'g_job'

class Project(models.Model):
   g_creation_time = models.IntegerField('Creation Time',default=0)
   g_modification_time = models.IntegerField('Modification Time',default=0)
   g_deleted = models.CharField('Deleted?', max_length=5, default='False')
   g_request_id = models.IntegerField('Request_ID', default=0)
   g_transaction_id = models.IntegerField('Trans_ID', default=0)
   g_name = models.CharField('Name', max_length=1024)
   g_active = models.CharField('Active', max_length=5, default='True')
   g_organization = models.CharField('Org', max_length=1024)
   g_special = models.CharField('Special', max_length=5, default='False')
   g_description = models.CharField('Description', max_length=1024)

   def __unicode__(self):
      return (self.g_name)

   class Meta:
      db_table = 'g_project'

class Project_User(models.Model):
   g_creation_time = models.IntegerField('Creation Time',default=0)
   g_modification_time = models.IntegerField('Modification Time',default=0)
   g_deleted = models.CharField('Deleted?', max_length=5, default='False')
   g_request_id = models.IntegerField('Request_ID', default=0)
   g_transaction_id = models.IntegerField('Trans_ID',default=0)
   g_project = models.CharField('Name', max_length=1024)
   g_name = models.CharField('Name', max_length=1024)
   g_active = models.CharField('Active', max_length=5, default='True')
   g_admin = models.CharField('Special', max_length=5, default='False')

   def __unicode__(self):
      return (self.g_name)

   class Meta:
      db_table = 'g_project_user'

