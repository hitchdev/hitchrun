Compile hitchreqs.in:
  description: |
    When hitchreqs.in is changed, hitchreqs.txt should reflect
    the change and the extra package or packages should be installed.
  preconditions:
    files:
      hitchreqs.in: |
        hitchrun
        humanize
      hitchreqs.txt: |
        argcomplete==1.7.0
        click==6.7
        commandlib==0.2.5
        first==2.0.1
        hitchrun==0.1
        path.py==10.0
        pip-tools==1.8.0
        six==1.10.0
      key.py: |
        import datetime

        def humantime():
            """Use a library."""
            import humanize
            print(humanize.naturaltime(datetime.datetime.now()))
  scenario:
    - Run:
       cmd: ~/hvenv/bin/hitchrun humantime
       expect: now
