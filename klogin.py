#!/usr/bin/python

import argparse
from subprocess import run, CalledProcessError, CompletedProcess
import re
import props
from getpass import getpass, getuser, GetPassWarning
import os


def do_kdestroy(search_dir: str = '') -> None:
    try:
        argv: list = [f'{search_dir}kdestroy']
        process: CompletedProcess = run(argv, timeout=5, text=True, capture_output=True)
    except CalledProcessError as c:
        print(c)


def get_klist(search_dir: str = '') -> str:
    result: str | None = None
    try:
        # klist to show the name of the cache
        argv = [f'{search_dir}klist']
        process: CompletedProcess = run(argv, capture_output=True, timeout=5, text=True)
        result = process.stdout + process.stderr
    except CalledProcessError as c:
        raise c
    finally:
        return result


def get_armor_cache(realm: str, search_dir: str = '') -> str:
    result: str | None = None
    do_kdestroy(search_dir=search_dir)
    try:
        # anonymous kinit to create armor cache
        argv = [f'{search_dir}kinit', '-n', f'@{realm}']
        process: CompletedProcess = run(argv, capture_output=True, timeout=5, text=True)
        output = str(get_klist(search_dir))
        result = re.findall(props.cache_regex, output)[0]
    except CalledProcessError as c:
        raise c
    except IndexError:
        msg: str = f'''
            ERROR: No WELLKNOWN/ANONYMOUS ticket cache found in klist output.
            Perhaps specify --search_dir to make sure you're calling the right copy of klist:
        '''
        print(msg)

    return result


def do_kinit(
        principle: str | None = None,
        password: str | None = None,
        otp: str | None = None,
        search_dir: str = '',
        cache: str | None = None,
) -> str:
    realm: str = ''
    argv: list = [f'{search_dir}kinit']
    try:
        if not principle:
            principle = getuser()
        if '@' in principle:
            realm = principle.split('@')[1]
        argv.append(principle)
        if not password:
            password = getpass()
    except GetPassWarning as g:
        raise g
    if not otp:
        otp = input('enter OTP: ')
    if not otp:
        if not cache:
            cache = get_armor_cache(realm=realm, search_dir=search_dir)
        if cache:
            argv.append('-T')
            argv.append(cache)

    try:
        # real kinit using armor cache to support OTP if needed
        secrets = f'{password}{otp}'
        process: CompletedProcess = run(argv, capture_output=True, text=True, input=secrets)
        # process.stdin.write(secrets)
    except CalledProcessError as c:
        raise c
    except TypeError as t:
        print(t)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--principle', help='user[@REALM]')
    parser.add_argument('--password', help='password (without OTP)')
    parser.add_argument('--otp', help='OTP value (will be appended to password)')
    parser.add_argument('--cache', help='credential cache specifier')
    parser.add_argument(
        '--search_dir',
        default='',
        help='specify a path name for the kdestroy, kinit, klist executables',
    )

    args = parser.parse_args()

    # do_kdestroy(args.search_dir)
    do_kinit(principle=args.principle, password=args.password, otp=args.otp, search_dir=args.search_dir)
    klist: str = get_klist(search_dir=args.search_dir)
    if args.principle in klist:
        print(f'login succeeded: {os.linesep}klist')
    else:
        print('login failed')
