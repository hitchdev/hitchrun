Catch exceptions:
  preconditions:
    files:
      hitchreqs.in: |
        hitchrun
      key.py: |
        from hitchrun import expected

        class ExpectedException(Exception):
            pass

        class UnexpectedException(Exception):
            pass

        def uncaught():
            """
            Command A help.
            """
            raise UnexpectedException("message")

        @expected(ExpectedException)
        def expected_exception():
            """
            Command B help.
            """
            raise ExpectedException("message")
  scenario:
    - hitchrun:
       args: expected_exception
       expect: ExpectedException
       exit_code: 1
    - hitchrun:
       args: uncaught
       expect: UnexpectedException
       exit_code: 1
