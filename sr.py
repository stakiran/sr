# -*- coding: utf-8 -*-

import os
import subprocess

class execlib:
    @staticmethod
    def get_stdout(cmdline):
        """ @return A byte string, so maybe need to decode with .decode('cp932')"""
        return subprocess.check_output(cmdline, shell=True)

    @staticmethod
    def execute(cmdline):
        """ @return A return code. """
        childobj = subprocess.Popen(cmdline, shell=True)
        childobj.communicate()
        return childobj.returncode

    @staticmethod
    def nonblocking_exec(cmdline):
        """ windows only.
        `(binpath) (params)` 形式の場合は両方とも "" で囲むこと. """
        commandline = 'start "" %s' % cmdline
        return execlib.execute(commandline)


def abort(msg):
    raise RuntimeError(msg)
    exit(1)

def nowstr():
    import datetime
    return datetime.datetime.now().strftime("%y%m%d_%H%M%S")

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('comment', default='', nargs='*',
        help='Comment for appending to a filename.')

    parser.add_argument('-s', '--second', default=0, type=int)
    parser.add_argument('-m', '--minutes',  default=0, type=int)
    parser.add_argument('--hour',  default=0, type=int)
    parser.add_argument('-t', '--time',  default=None,
        help='The format must be `HHHH:MM:SS`.')

    parser.add_argument('--wav', default=False, action='store_true',
        help='Use not default WMA but WAV format.')

    #parser.add_argument('-p', '--progress', default=False, action='store_true',
    #    help='Show waiting progress.')
    parser.add_argument('--ps', default=False, action='store_true',
        help='Show soundrecorder.exe processes information.')

    parser.add_argument('-d', '--dialog', default=False, action='store_true',
        help='Open the mic dialog. (Single Use)')
    parser.add_argument('--here', default=False, action='store_true',
        help='Open the current directory with explorer.exe (Single Use)')

    parser.add_argument('--test', default=False, action='store_true',
        help='No execution. (Only show the commandline.)')

    parsed_args = parser.parse_args()
    return parsed_args

args = parse_arguments()

curdir = os.getcwd()
comment = ''
for elm in args.comment:
    comment += elm

# single commands when given.
# ---------------------------

if args.dialog:
    err = execlib.nonblocking_exec('"C:\\Windows\\system32\\rundll32.exe" Shell32.dll,Control_RunDLL mmsys.cpl,,recording')
    exit(err)

if args.here:
    err = execlib.nonblocking_exec(curdir)
    exit(err)

if args.ps:
    commandline = "WMIC PROCESS WHERE \"Name LIKE '%soundrecorder%'\" GET CREATIONDATE,CAPTION /FORMAT:LIST"
    stdout_raw = execlib.get_stdout(commandline)
    # cmd 前提なので文字コードも固定
    stdout_str = stdout_raw.decode('cp932')
    stdout_lines = stdout_str.split('\r\n')
    stdout_lines = [line for line in stdout_lines if len(line.strip())!=0]
    if stdout_lines:
        # Before: ['Caption=SoundRecorder.exe\r\r', 'CreationDate=20170221144301.365129+540\r\r', ...]
        # After : from yyyymmdd_hhmmss
        for i in range(len(stdout_lines)):
            line = stdout_lines[i]
            if i%2!=0:
                print('from {}_{}'.format(line.split('=')[1][:8], line.split('=')[1][8:8+6]))
    exit(0)

# fix filename
# ------------

timestr = args.time
if args.second:
    timestr = '0000:00:%02d' % args.second
elif args.minutes:
    timestr = '0000:%02d:00' % args.minutes
elif args.hour:
    timestr = '%04d:00:00' % args.hour

def abort_if_time_format_is_invalid(timestr):
    if not(timestr):
        abort('No recording time.')

    if len(timestr)!=len('HHHH:MM:SS'):
        abort('Invalid time format. (invalid length)')

    try:
        h, m, s = [int(elm) for elm in timestr.split(':')]
    except (ValueError, IndexError):
        abort('Invalid time format. (not `HHHH:MM:SS`)')

    if h<0 or h>9999:
        abort('Invalid time format. (invalid hour "%d")' % h)
    if m<0 or m>59:
        abort('Invalid time format. (invalid minute "%d")' % m)
    if s<0 or s>59:
        abort('Invalid time format. (invalid second "%d")' % s)
abort_if_time_format_is_invalid(timestr)

recordee_name = nowstr()
def timestr_to_filename(timestr):
    h, m, s = [int(elm) for elm in timestr.split(':')]

    ret = '_'
    if h!=0:
        ret += '%dh' % h
    if m!=0:
        ret += '%dm' % m
    if s!=0:
        ret += '%ds' % s

    return ret
recordee_name += timestr_to_filename(timestr)

if comment:
    recordee_name += '_%s' % comment

ext = '.wma'
if args.wav:
    ext = '.wav'
recordee_name += ext

# execute
# -------

# @todo progress mode.
#   0000:00:00 0000:00:30 30
#   0000:00:01 0000:00:30 29
#   ....
#   いや違う, 現プロセス起動時間から「あと何分で使えるか」を表示しよう.
#   ...いやダメだ. wmic からは起動時のパラメータまでわからん...
#
# @todo print curdir information?

commandline = 'soundrecorder /FILE %s /DURATION %s' % (recordee_name, timestr)
if not(args.test):
    err = execlib.nonblocking_exec(commandline)
    exit(err)
else:
    print(commandline)
    exit(0)
