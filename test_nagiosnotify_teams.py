
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

import urllib
import json

import os

from nagiosnotify_teams import TeamsNotify


class TestSlackNotify(unittest.TestCase):
    __primary = "https://outlook.office.com/webhook/primary"
    __secondary = "https://outlook.office.com/webhook/secondary"
    __override = "https://outlook.office.com/webhook/override"

    __nagios_server = "nagios.somedomain.com"
    __list_servicedisplaynames = ["Yum Update", "APT Update"]
    __list_state = ["WARNING"]
    __service_message = "HOST: {0} Some service message"
    __service_message_list = ["NAGIOS_HOSTNAME"]
    __host_message = "HOST: {0} Some host message"
    __host_message_list = ["NAGIOS_HOSTNAME"]
    __test = False

    def __get_default_teamsnotify(self):
        teams_notify = TeamsNotify()
        teams_notify._PRIMARY_CHANNEL = self.__primary
        teams_notify._SECONDARY_CHANNEL = self.__secondary
        teams_notify._NAGIOS_SERVER = self.__nagios_server
        teams_notify._LIST_SERVICEDISPLAYNAMES = self.__list_servicedisplaynames
        teams_notify._LIST_STATE = self.__list_state
        teams_notify._SERVICE_MESSAGE = self.__service_message
        teams_notify._SERVICE_MESSAGE_LIST = self.__service_message_list
        teams_notify._HOST_MESSAGE = self.__host_message
        teams_notify._HOST_MESSAGE_LIST = self.__host_message_list
        teams_notify._TEST = self.__test
        return teams_notify

    def setUp(self):
        self.__mock_teams_notify = self.__get_default_teamsnotify()

    def test_get_args(self):
        mock_argv_list = ["nagiosnotify_teams.py"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

    def test_get_args_override(self):
        override_channel = "#override"
        mock_argv_list = ["nagiosnotify_teams.py", "-c", override_channel]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertEqual(override_channel, args.channel)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

    def test_get_args_testmode(self):
        mock_argv_list = ["nagiosnotify_teams.py", "-t"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)
        self.assertTrue(args.test)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)

        self.assertNotEqual(self.__test, self.__mock_teams_notify._TEST)
        self.assertTrue(self.__mock_teams_notify._TEST)

    def test_get_args_clear(self):
        mock_argv_list = ["nagiosnotify_teams.py", "-clr"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)
        self.assertTrue(args.clear)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        self.assertListEqual([], self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual([], self.__mock_teams_notify._LIST_STATE)

    def test_get_args_skiplink(self):
        mock_argv_list = ["nagiosnotify_teams.py", "-sk"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)
        self.assertFalse(args.skiplink)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

    def test_get_args_primary_channel(self):
        primary_channel = "#new_primary"
        mock_argv_list = ["nagiosnotify_teams.py", "-pc", primary_channel]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertEqual(primary_channel, args.primary)

        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        self.assertNotEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(primary_channel, self.__mock_teams_notify._PRIMARY_CHANNEL)

    def test_get_args_secondary_channel(self):
        secondary_channel = "#new_secondary"
        mock_argv_list = ["nagiosnotify_teams.py", "-sc", secondary_channel]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertEqual(secondary_channel, args.secondary)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        self.assertNotEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(secondary_channel, self.__mock_teams_notify._SECONDARY_CHANNEL)

    def test_get_args_nagios_server(self):
        nagios_server = "nagios2.somedomain.com"
        mock_argv_list = ["nagiosnotify_teams.py", "-n", nagios_server]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertEqual(nagios_server, args.nagios)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        self.assertNotEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertEqual(nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)

    def test_get_args_service_list(self):
        svc_list = ["Ping", "Load"]
        mock_argv_list = ["nagiosnotify_teams.py", "-svc", svc_list[0], svc_list[1]]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        for old_val in self.__list_servicedisplaynames:
            self.assertNotIn(old_val, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)

        self.assertListEqual(svc_list, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)

    def test_get_args_state_list(self):
        state_list = ["CRITICAL", "DOWN"]
        mock_argv_list = ["nagiosnotify_teams.py", "-st", state_list[0], state_list[1]]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        for old_val in self.__list_state:
            self.assertNotIn(old_val, self.__mock_teams_notify._LIST_STATE)

        self.assertListEqual(state_list, self.__mock_teams_notify._LIST_STATE)

    def test_get_args_host_message(self):
        host_message = "HOST: {0}  STATUS: {1}"
        mock_argv_list = ["nagiosnotify_teams.py", "-hm", host_message]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        self.assertNotEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertEqual(host_message, self.__mock_teams_notify._HOST_MESSAGE)

    def test_get_args_host_message_list(self):
        host_message_list = ["NAGIOS_HOSTNAME", "NAGIOS_HOSTSTATUS"]
        mock_argv_list = ["nagiosnotify_teams.py", "-hl", host_message_list[0], host_message_list[1]]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        self.assertListEqual(host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)

    def test_get_args_service_message(self):
        service_message = "HOST: {0}  SERVICE: {1}"
        mock_argv_list = ["nagiosnotify_teams.py", "-sm", service_message]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        self.assertNotEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertEqual(service_message, self.__mock_teams_notify._SERVICE_MESSAGE)

    def test_get_args_service_message_list(self):
        service_message_list = ["NAGIOS_HOSTNAME", "NAGIOS_SERVICESTATE"]
        mock_argv_list = ["nagiosnotify_teams.py", "-sl", service_message_list[0], service_message_list[1]]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_teams_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_teams_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_teams_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_teams_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_teams_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_teams_notify._LIST_STATE)
        self.assertEqual(self.__host_message, self.__mock_teams_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_teams_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__service_message, self.__mock_teams_notify._SERVICE_MESSAGE)
        self.assertEqual(self.__test, self.__mock_teams_notify._TEST)

        self.assertListEqual(service_message_list, self.__mock_teams_notify._SERVICE_MESSAGE_LIST)

    def test_get_link(self):
        host_name = "host01"
        link_builder = [" [See Nagios](https://", self.__nagios_server, "/nagiosxi/includes/components/xicore/status.php?host=",
                        host_name, ") "]
        html_link_expected = "".join(link_builder)

        html_link = self.__mock_teams_notify._get_link(host_name)

        self.assertEqual(html_link_expected, html_link)

    def test_get_color(self):
        service_state_list = ["CRITICAL", "WARNING", "OK"]
        host_state_list = ["DOWN", "UP", "UNKNOWN", "SOMEUNKNOWNSTATE"]

        color = self.__mock_teams_notify._get_color(service_state_list[0])
        self.assertEqual("ff0000", color)

        color = self.__mock_teams_notify._get_color(service_state_list[1])
        self.assertEqual("ffaa1d", color)

        color = self.__mock_teams_notify._get_color(service_state_list[2])
        self.assertEqual("00ff00", color)

        color = self.__mock_teams_notify._get_color(host_state_list[0])
        self.assertEqual("ff0000", color)

        color = self.__mock_teams_notify._get_color(host_state_list[1])
        self.assertEqual("00ff00", color)

        color = self.__mock_teams_notify._get_color(host_state_list[2])
        self.assertEqual("888888", color)

        color = self.__mock_teams_notify._get_color(host_state_list[3])
        self.assertEqual("000000", color)

    def test_get_request_data(self):
        nagios_hostname = "host1"

        mock_argv_list = ["nagiosnotify_teams.py"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()

        mock_env_list = {"NAGIOS_HOSTNAME":nagios_hostname,
                         "NAGIOS_HOSTSTATE":"DOWN",
                         "NAGIOS_HOSTOUTPUT":"Host message testing"}
        l = mock.patch.dict(os.environ, mock_env_list)
        l.start()

        results = self.__mock_teams_notify._get_request_data()

        l.stop()
        k.stop()

        self.assertEqual(self.__primary, results['url'])

        text_str_builder = ["HOST: ", nagios_hostname, " Some host message [See Nagios](https://",
                            self.__nagios_server, "/nagiosxi/includes/components/xicore/status.php?host=",
                            nagios_hostname, ") "]

        expected_data = {
            "@type": "MessageCard",
            "themeColor" : "ff0000",
            "text" : ''.join(text_str_builder)
        }

        actual_data = json.loads(results['data'])

        self.assertDictEqual(expected_data, actual_data)

    def test_get_request_data_override(self):
        nagios_hostname = "host1"
        override_channel = self.__override

        mock_argv_list = ["nagiosnotify_teams.py", "-c", override_channel, "-sk"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()

        mock_env_list = {"NAGIOS_HOSTNAME":nagios_hostname,
                         "NAGIOS_HOSTSTATE":"DOWN",
                         "NAGIOS_HOSTOUTPUT":"Host message testing"}
        l = mock.patch.dict(os.environ, mock_env_list)
        l.start()

        results = self.__mock_teams_notify._get_request_data()

        l.stop()
        k.stop()

        text_str_builder = ["HOST: ", nagios_hostname, " Some host message"]

        expected_data = {
            "@type": "MessageCard",
            "themeColor" : "ff0000",
            "text" : ''.join(text_str_builder)
        }

        actual_data = json.loads(results['data'])

        self.assertDictEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()











