
# Copyright 2019 University of Southern California Information Sciences Institute All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import mock

import os

from nagiosnotify import NagiosNotify


class TestNagiosNotify(unittest.TestCase):

    def test_get_parser(self):
        nagios_notify = NagiosNotify()
        parser = nagios_notify._get_parser()
        self.assertEqual("Nagios slack integration", parser.description)
        self.assertEqual("channel", parser._actions[1].dest)
        self.assertFalse(parser._actions[1].required)
        self.assertEqual("-c", parser._actions[1].option_strings[0])
        self.assertEqual("--channel", parser._actions[1].option_strings[1])
        self.assertEqual("primary", parser._actions[2].dest)
        self.assertFalse(parser._actions[2].required)
        self.assertEqual("-pc", parser._actions[2].option_strings[0])
        self.assertEqual("--primary", parser._actions[2].option_strings[1])
        self.assertEqual("secondary", parser._actions[3].dest)
        self.assertFalse(parser._actions[3].required)
        self.assertEqual("-sc", parser._actions[3].option_strings[0])
        self.assertEqual("--secondary", parser._actions[3].option_strings[1])
        self.assertEqual("nagios", parser._actions[4].dest)
        self.assertFalse(parser._actions[4].required)
        self.assertEqual("-n", parser._actions[4].option_strings[0])
        self.assertEqual("--nagios", parser._actions[4].option_strings[1])
        self.assertEqual("services", parser._actions[5].dest)
        self.assertFalse(parser._actions[5].required)
        self.assertEqual("-svc", parser._actions[5].option_strings[0])
        self.assertEqual("--services", parser._actions[5].option_strings[1])
        self.assertEqual("states", parser._actions[6].dest)
        self.assertFalse(parser._actions[6].required)
        self.assertEqual("-st", parser._actions[6].option_strings[0])
        self.assertEqual("--states", parser._actions[6].option_strings[1])
        self.assertEqual("clear", parser._actions[7].dest)
        self.assertFalse(parser._actions[7].required)
        self.assertEqual("-clr", parser._actions[7].option_strings[0])
        self.assertEqual("--clear", parser._actions[7].option_strings[1])
        self.assertEqual("test", parser._actions[8].dest)
        self.assertFalse(parser._actions[8].required)
        self.assertEqual("-t", parser._actions[8].option_strings[0])
        self.assertEqual("--test", parser._actions[8].option_strings[1])
        self.assertEqual("hostmessage", parser._actions[9].dest)
        self.assertFalse(parser._actions[9].required)
        self.assertEqual("-hm", parser._actions[9].option_strings[0])
        self.assertEqual("--hostmessage", parser._actions[9].option_strings[1])
        self.assertEqual("hostmessagelist", parser._actions[10].dest)
        self.assertFalse(parser._actions[10].required)
        self.assertEqual("-hl", parser._actions[10].option_strings[0])
        self.assertEqual("--hostmessagelist", parser._actions[10].option_strings[1])
        self.assertEqual("servicemessage", parser._actions[11].dest)
        self.assertFalse(parser._actions[11].required)
        self.assertEqual("-sm", parser._actions[11].option_strings[0])
        self.assertEqual("--servicemessage", parser._actions[11].option_strings[1])
        self.assertEqual("servicemessagelist", parser._actions[12].dest)
        self.assertFalse(parser._actions[12].required)
        self.assertEqual("-sl", parser._actions[12].option_strings[0])
        self.assertEqual("--servicemessagelist", parser._actions[12].option_strings[1])
        self.assertEqual("skiplink", parser._actions[13].dest)
        self.assertFalse(parser._actions[13].required)
        self.assertEqual("-sk", parser._actions[13].option_strings[0])
        self.assertEqual("--skiplink", parser._actions[13].option_strings[1])

    def test_get_env_is_none(self):
        domain = "www.somedomain.com"
        k = mock.patch.dict(os.environ, {'NAGIOS_HOSTNAME': domain})
        k.start()
        nagios_notify = NagiosNotify()
        env_value = nagios_notify._get_env("NAGIOS_HOSTSTATE")
        k.stop()
        self.assertIsNone(env_value)

    def test_get_env(self):
        domain = "www.somedomain.com"
        k = mock.patch.dict(os.environ, {'NAGIOS_HOSTNAME': domain})
        k.start()
        nagios_notify = NagiosNotify()
        env_value = nagios_notify._get_env("NAGIOS_HOSTNAME")
        k.stop()
        self.assertEqual(domain, env_value)

    def test_get_env_test_data(self):
        domain = "www.somedomain.com"
        k = mock.patch.dict(os.environ, {'NAGIOS_HOSTNAME': domain})
        k.start()
        nagios_notify = NagiosNotify()
        nagios_notify._TEST = True
        env_value = nagios_notify._get_env("NAGIOS_HOSTSTATE")
        k.stop()
        self.assertEqual("DOWN", env_value)

    def test_get_env_list_invalid_env(self):
        domain = "www.somedomain.com"
        k = mock.patch.dict(os.environ, {'NAGIOS_HOSTNAME': domain})
        k.start()
        nagios_notify = NagiosNotify()
        invalid_list = ["NAG_HOSTNAME"]
        with self.assertRaises(SystemExit) as cm:
            nagios_notify._get_env_list(invalid_list)
        k.stop()
        self.assertEqual(1, cm.exception.code)

    def test_get_env_list(self):
        domain = "www.somedomain.com"
        k = mock.patch.dict(os.environ, {'NAGIOS_HOSTNAME': domain, "NAGIOS_HOSTSTATE": "DOWN"})
        k.start()
        nagios_notify = NagiosNotify()
        valid_list = ["NAGIOS_HOSTNAME", "NAGIOS_HOSTSTATE"]
        valid_return = nagios_notify._get_env_list(valid_list)
        k.stop()
        self.assertEqual(2, len(valid_return))
        self.assertEqual(domain, valid_return[0])
        self.assertEqual("DOWN", valid_return[1])

    def test_get_channel_override(self):
        override = "#criticals"
        primary = "#alerts"
        secondary = None
        list_state = ["WARNING"]
        list_servicename = ["Yum Update"]
        nagios_state = "WARNING"
        nagios_service = "Yum Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(override, channel)

    def test_get_channel_invalid_override(self):
        override = "$"
        primary = "#alerts"
        secondary = None
        list_state = ["WARNING"]
        list_servicename = ["Yum Update"]
        nagios_state = "WARNING"
        nagios_service = "Yum Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_secondary_none(self):
        override = None
        primary = "#alerts"
        secondary = None
        list_state = ["WARNING"]
        list_servicename = ["Yum Update"]
        nagios_state = "WARNING"
        nagios_service = "Yum Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_empty_lists(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = []
        list_servicename = []
        nagios_state = "WARNING"
        nagios_service = "Yum Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_none_lists(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = None
        list_servicename = None
        nagios_state = "WARNING"
        nagios_service = "Yum Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_none_selectors(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = ["WARNING"]
        list_servicename = ["Yum Update"]
        nagios_state = None
        nagios_service = None
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_empty_selectors(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = ["WARNING"]
        list_servicename = ["Yum Update"]
        nagios_state = ""
        nagios_service = ""
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_not_right_state(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = ["WARNING"]
        list_servicename = []
        nagios_state = "CRITICAL"
        nagios_service = ""
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_right_state(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = ["WARNING"]
        list_servicename = []
        nagios_state = "WARNING"
        nagios_service = ""
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(secondary, channel)

    def test_get_channel_not_right_service(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = []
        list_servicename = ["Yum Update"]
        nagios_state = ""
        nagios_service = "APT Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_right_service(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = []
        list_servicename = ["Yum Update"]
        nagios_state = ""
        nagios_service = "Yum Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(secondary, channel)

    def test_get_channel_not_right_service_and_state(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = ["WARNING"]
        list_servicename = ["Yum Update"]
        nagios_state = "WARNING"
        nagios_service = "APT Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_not_right_state_and_service(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = ["WARNING"]
        list_servicename = ["Yum Update"]
        nagios_state = "CRITICAL"
        nagios_service = "Yum Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(primary, channel)

    def test_get_channel_right_state_and_service(self):
        override = None
        primary = "#alerts"
        secondary = "#alerts-updates"
        list_state = ["WARNING"]
        list_servicename = ["Yum Update"]
        nagios_state = "WARNING"
        nagios_service = "Yum Update"
        nagios_notify = NagiosNotify()
        channel = nagios_notify._get_channel(override, primary, secondary, list_state, list_servicename, nagios_state,
                                             nagios_service)
        self.assertEqual(secondary, channel)

    def test_get_message_invalid_service_message_list(self):
        domain = "www.somedomain.com"
        k = mock.patch.dict(os.environ, {'NAGIOS_HOSTNAME': domain})
        k.start()
        nagios_notify = NagiosNotify()

        nagios_servicestate = "WARNING"
        nagios_hoststate = "DOWN"
        service_message = "HOST: {0} Yum Update needs updating"
        invalid_service_message_list = ["NAG_HOSTNAME"]
        host_message = "HOST: {0} Host is down"
        host_message_list = ["NAGIOS_HOSTNAME"]

        with self.assertRaises(SystemExit) as cm:
            nagios_notify._get_message(nagios_servicestate, nagios_hoststate, service_message,
                                       invalid_service_message_list, host_message, host_message_list)
        k.stop()
        self.assertEqual(1, cm.exception.code)

    def test_get_message_service_message(self):
        domain = "www.somedomain.com"
        k = mock.patch.dict(os.environ, {'NAGIOS_HOSTNAME': domain})
        k.start()
        nagios_notify = NagiosNotify()

        nagios_servicestate = "WARNING"
        nagios_hoststate = "DOWN"
        service_message = "HOST: {0} Yum Update needs updating"
        service_message_list = ["NAGIOS_HOSTNAME"]
        host_message = "HOST: {0} Host is down"
        host_message_list = ["NAGIOS_HOSTNAME"]

        message = nagios_notify._get_message(nagios_servicestate, nagios_hoststate, service_message,
                                             service_message_list, host_message, host_message_list)
        k.stop()
        self.assertEqual("HOST: www.somedomain.com Yum Update needs updating", message)

    def test_get_message_invalid_host_message_list(self):
        domain = "www.somedomain.com"
        k = mock.patch.dict(os.environ, {'NAGIOS_HOSTNAME': domain})
        k.start()
        nagios_notify = NagiosNotify()

        nagios_servicestate = None
        nagios_hoststate = "DOWN"
        service_message = "HOST: {0} Yum Update needs updating"
        service_message_list = ["NAGIOS_HOSTNAME"]
        host_message = "HOST: {0} Host is down"
        invalid_host_message_list = ["NAG_HOSTNAME"]

        with self.assertRaises(SystemExit) as cm:
            nagios_notify._get_message(nagios_servicestate, nagios_hoststate, service_message,
                                       service_message_list, host_message, invalid_host_message_list)
        k.stop()
        self.assertEqual(1, cm.exception.code)

    def test_get_message_host_message(self):
        domain = "www.somedomain.com"
        k = mock.patch.dict(os.environ, {'NAGIOS_HOSTNAME': domain})
        k.start()
        nagios_notify = NagiosNotify()

        nagios_servicestate = None
        nagios_hoststate = "DOWN"
        service_message = "HOST: {0} Yum Update needs updating"
        service_message_list = ["NAGIOS_HOSTNAME"]
        host_message = "HOST: {0} Host is down"
        host_message_list = ["NAGIOS_HOSTNAME"]

        message = nagios_notify._get_message(nagios_servicestate, nagios_hoststate, service_message,
                                             service_message_list, host_message, host_message_list)
        k.stop()
        self.assertEqual("HOST: www.somedomain.com Host is down", message)


if __name__ == '__main__':
    unittest.main()

