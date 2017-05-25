Only hitchreqs.in is available:
  description: |
    Install from hitchreqs.in when hitchreqs.txt
    is not available.
  preconditions:
    files:
      key.py: |
        import humanize
        import datetime

        def now():
            print("Output of library is {0}".format(humanize.naturaltime(datetime.datetime.now())))
      hitchreqs.in: |
        humanize
        hitchrun
  scenario:
    - Run:
       cmd: ~/hvenv/bin/hitchrun now
       expect: Output of library is now
       exit_code: 0
