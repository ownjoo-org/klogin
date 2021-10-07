#!/usr/bin/python

import argparse
import subprocess
import os
import re
import props


def do_kdestroy(search_dir=''):
    try:
        argv = [str(search_dir) + 'kdestroy']
        process = subprocess.run(argv, timeout=5, text=True, capture_output=True)
    except subprocess.CalledProcessError as c:
        raise c


def get_klist(search_dir=''):
    result = None
    try:
        # klist to show the name of the cache
        argv = [search_dir + 'klist']
        process = subprocess.run(argv, capture_output=True, timeout=5, text=True)
        result = process.stdout
    except subprocess.CalledProcessError as c:
        raise c
    finally:
        return result


def get_armor_cache(realm, search_dir=''):
    result = None

    try:
        # anonymous kinit to create armor cache
        argv = [search_dir + 'kinit', '-n', '@{0}'.format(realm)]
        subprocess.run(argv, capture_output=True, timeout=5, text=True)
        result = re.findall(props.cache_regex, str(get_klist(search_dir)))[0]
    except subprocess.CalledProcessError as c:
        raise c
    except IndexError as i:
        pass

    return result


def do_kinit(principle=None, password=None, otp=None, search_dir=''):
    process = None
    realm = ''
    argv = [search_dir + 'kinit']
    if principle is None:
        principle = input('enter principle: ')
    if '@' in principle:
        realm = principle.split('@')[1]
    argv.append(principle)
    if password is None:
        password = input('enter password: ')
    if otp is None:
        otp = input('enter OTP: ')
    if otp is None or otp is '':
        pass
    else:
        argv.append('-T')
        argv.append(get_armor_cache(realm=realm, search_dir=search_dir))

    try:
        # real kinit using armor cache to support OTP if needed
        secrets = '{0}{1}'.format(password, otp)
        print(argv, secrets)
        process = subprocess.run(argv, capture_output=True, text=True, input=secrets)
        # process.stdin.write(secrets)
    except subprocess.CalledProcessError as c:
        raise c


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--principle", help='user[@REALM]')
    parser.add_argument("--password", help='password (without OTP)')
    parser.add_argument("--otp", help='OTP value (will be appended to password)')
    parser.add_argument("--cache", help='credential cache specifier')
    parser.add_argument("--search_dir", default='', help='specify a path name for the kdestroy, kinit, klist executables')

    args = parser.parse_args()

    # do_kdestroy(args.search_dir)
    do_kinit(principle=args.principle, password=args.password, otp=args.otp, search_dir=args.search_dir)
    print(get_klist(search_dir=args.search_dir))
