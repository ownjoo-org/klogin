#!/usr/bin/python

import unittest
import klogin
import props
import creds


class TestKLogin(unittest.TestCase):
    def test_get_armor_cache(self):
        # setup
        local_dir = props.local_dir
        realm = props.realm
        expected = props.expected_cache

        # execute
        actual = klogin.get_armor_cache(realm, search_dir=local_dir)

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_get_klist(self):
        # setup
        local_dir = props.local_dir

        # execute
        actual = klogin.get_klist(local_dir)

        # assess
        self.assertIsNotNone(actual)

        # teardown

    # integration test: OTP values are dynamic/unpredictable
    # def test_kinit(self):
    #     # setup
    #     local_dir = props.local_dir
    #     expected = props.expected_cache
    #
    #     # execute
    #     actual = klogin.do_kinit(principle=creds.principle, password=creds.password, otp=None, search_dir=local_dir)
    #
    #     # assess
    #     self.assertEqual(expected, actual)
    #
    #     # teardown


if __name__ == '__main__':
    unittest.main()
