from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

def executed(event):
    from flaskr import get_scheduler
    _scheduler = get_scheduler()

    if event.job_id == 'create_file_test':
        _scheduler.remove_job(event.job_id)
    
def stock_scraping(event):
    from flaskr import get_scheduler
    _scheduler = get_scheduler()

    print('scheduler listener')
    print(dir(event))
    print('event print')
    print(event)
    print('scheduler job id')
    print(event.job_id)
    print('scheduler code')
    print(event.code)
    
    print('scheduler alias')
    print(event.alias)
    print('scheduler jobstore')
    print(event.jobstore)

    
    # print('scheduler run time')
    # print(event.scheduled_run_times)
    # scheduler listener
    # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'alias', 'code', 'job_id', 'jobstore', 'scheduled_run_times']
    # event print
    # <JobSubmissionEvent (code=32768)>
    # scheduler job id
    # create_file_test
    # scheduler code
    # 32768
    # scheduler alias
    # None
    # scheduler jobstore
    # default
    # scheduler run time
    # [datetime.datetime(2020, 1, 5, 18, 28, 10, tzinfo=<DstTzInfo 'Asia/Seoul' KST+9:00:00 STD>)]


    # if event.exception:
    #     print('The job crashed :(')
    # else:
    #     print('The job worked :)')
    # pass

# Description

# Event class
# EVENT_SCHEDULER_STARTED                   The scheduler was started
# SchedulerEvent
# EVENT_SCHEDULER_SHUTDOWN                  The scheduler was shut down
# SchedulerEvent
# EVENT_SCHEDULER_PAUSED                    Job processing in the scheduler was paused
# SchedulerEvent
# EVENT_SCHEDULER_RESUMED                   Job processing in the scheduler was resumed
# SchedulerEvent
# EVENT_EXECUTOR_ADDED                  An executor was added to the scheduler
# SchedulerEvent
# EVENT_EXECUTOR_REMOVED                    An executor was removed to the scheduler
# SchedulerEvent
# EVENT_JOBSTORE_ADDED                  A job store was added to the scheduler
# SchedulerEvent
# EVENT_JOBSTORE_REMOVED                    A job store was removed from the scheduler
# SchedulerEvent
# EVENT_ALL_JOBS_REMOVED                    All jobs were removed from either all job stores or one particular job store
# SchedulerEvent
# EVENT_JOB_ADDED                   A job was added to a job store
# JobEvent
# EVENT_JOB_REMOVED                 A job was removed from a job store
# JobEvent
# EVENT_JOB_MODIFIED                    A job was modified from outside the scheduler
# JobEvent
# EVENT_JOB_SUBMITTED                   A job was submitted to its executor to be run
# JobSubmissionEvent
# EVENT_JOB_MAX_INSTANCES                   A job being submitted to its executor was not accepted by the executor because the job has already reached its maximum concurrently executing instances
# JobSubmissionEvent
# EVENT_JOB_EXECUTED                    A job was executed successfully
# JobExecutionEvent
# EVENT_JOB_ERROR                   A job raised an exception during execution
# JobExecutionEvent
# EVENT_JOB_MISSED                  A job’s execution was missed
# JobExecutionEvent
# EVENT_ALL                     A catch-all mask that includes every event type