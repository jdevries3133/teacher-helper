#!/Users/JohnDeVries/repos/teacher_helper/venv/bin/python3.7
import code
import os
import sys
from pprint import pprint
from helper import Helper


class ShellUtils:

    def improper_usage(self):
        self.print_help()
        print('IMPROPER USAGE, SEE HELP ABOVE')
        sys.exit()

    @staticmethod
    def check_cache():
        if Helper.cache_exists():
            return Helper.read_cache()
        else:
            print(
                'Error: Database does not exist.\nHelper object must be cached '
                'to use the shell'
            )
            sys.exit()

    @staticmethod
    def print_help(self):
        print("""
        Supported commands:

        student [name] (-v)
            Pretty prints the dictionary of the matching student. If verbose, also
            print the dict of the students' guardians.

        clock
            Automatically clocks in or out of Paychex, depending on time of day
            and previous clock state.

        [no arguments]
            Run this script with no arguments, and it will enter the shell mode.
            Here, the helper object is instantiated in the local namespace with
            the variable name "helper". All attributes and methods are accessible.
        """)

if '-h' in sys.argv or 'help' in sys.argv:
    ShellUtils.print_help()

if '-v' in sys.argv:
    verbose = True
else:
    verbose = False

try:
    # student search
    if sys.argv[1] == 'student':
        helper = ShellUtils.check_cache()
        try:
            query_parts = [i for i in sys.argv[2:] if i != '-v']
        except IndexError:
            ShellUtils.improper_usage()
        query_name = ' '.join(query_parts)
        try:
            st = helper.find_nearest_match([query_name])[0]
            print(st.__str__(verbose))
            sys.exit()
        except IndexError:
            print(f'Student {sys.argv[2]} was not found.')
            sys.exit()

    # auto clock in / out
    if sys.argv[1] == 'clock':
        from helper.paychex import Paychex
        u = os.getenv('PAYCHEX_USR'),  # username
        p = os.getenv('PAYCHEX_PASS')  # password
        with Paychex(u, p) as pcx:
            pcx.clock()
        sys.exit()

    # silly timer
    if sys.argv[1] == 'timer':
        try:
            mins = int(sys.argv[2])
            msg = ' '.join(sys.argv[3:])
            if not msg:
                msg = input(
                    'Enter a message to be spoken after the timer is finished\n'
                )
            helper = Helper().timer(mins, msg)
        except IndexError:
            ShellUtils.improper_usage()

except IndexError:
    pass


helper = ShellUtils.check_cache()
code.interact(local=locals())
