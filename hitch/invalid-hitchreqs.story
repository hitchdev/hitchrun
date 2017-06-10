Invalid hitchreqs:
  description: |
    Catch the invalid version of requests in
    hitchreqs.txt.
  preconditions:
    files:
      key.py: |
        from hitchrun import cwd, Path

        def command():
            print("This should never run")
      hitchreqs.in: |
        hitchrun
        requests
      hitchreqs.txt: |
        argcomplete==1.7.0
        click==6.7
        colorama==0.3.7
        commandlib==0.2.5
        first==2.0.1
        hitchrun==0.1
        humanize==0.5.1
        Jinja2==2.9.5
        MarkupSafe==0.23
        path.py==10.1
        pip-tools==1.8.0
        six==1.10.0
        requests==99999 # invalid version
  scenario:
    - Run:
       cmd: ~/hvenv/bin/hitchrun command
       expect: Error compiling hitchreqs.txt
       exit_code: 1
