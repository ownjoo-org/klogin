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
        expected_cache = 'Ticket cache:'
        expected_principle = 'Default principal: WELLKNOWN/ANONYMOUS@WELLKNOWN:ANONYMOUS'
        expected_empty = 'klist: No credentials cache found'

        # execute

        actual = klogin.get_klist(local_dir)

        # assess
        self.assertIsNotNone(actual, 'actual is None')
        if expected_cache in actual:
            self.assertIn(expected_cache, actual, 'actual did not contain Ticket cache')
            self.assertIn(expected_principle, actual, 'actual did not contain WELLKNOWN/ANONYMOUS principle')
        else:
            self.assertIn(expected_empty, actual)

        # teardown

    def test_do_kdestroy_and_get_klist(self):
        # setup
        local_dir = props.local_dir
        expected_empty = 'klist: No credentials cache found'

        # execute
        klogin.do_kdestroy(local_dir)
        actual = klogin.get_klist(local_dir)

        # assess
        self.assertIsNotNone(actual, 'actual is None')
        self.assertIn(expected_empty, actual)

        # teardown

    # # integration test: OTP values are dynamic/unpredictable, TODO: software token?
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
