
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

from nagiosnotify_slack import SlackNotify


class TestSlackNotify(unittest.TestCase):
    # __web_hook_url = "http://put.a.real.value.here"
    __web_hook_url = "https://hooks.slack.com/services/PUT URL HERE"
    __primary = "#primary"
    # __primary = "#alerts"
    __secondary = "#secondary"
    # __secondary = "#alerts-updates-dev"
    __override = "#override"
    # __override = "#alerts-criticals"
    __nagios_server = ""

    __list_servicedisplaynames = ["Yum Update", "APT Update"]
    __list_state = ["WARNING"]
    __service_message = "HOST: {0} Some service message"
    __service_message_list = ["NAGIOS_HOSTNAME"]
    __host_message = "HOST: {0} Some host message"
    __host_message_list = ["NAGIOS_HOSTNAME"]
    __slack_botname = "nagios"
    __test = False

    def __get_default_slacknotify(self):
        slack_notify = SlackNotify()
        slack_notify._PRIMARY_CHANNEL = self.__primary
        slack_notify._SECONDARY_CHANNEL = self.__secondary
        slack_notify._NAGIOS_SERVER = self.__nagios_server
        slack_notify._LIST_SERVICEDISPLAYNAMES = self.__list_servicedisplaynames
        slack_notify._LIST_STATE = self.__list_state
        slack_notify._SERVICE_MESSAGE = self.__service_message
        slack_notify._SERVICE_MESSAGE_LIST = self.__service_message_list
        slack_notify._HOST_MESSAGE = self.__host_message
        slack_notify._HOST_MESSAGE_LIST = self.__host_message_list
        slack_notify._WEB_HOOK_URL = self.__web_hook_url
        slack_notify._SLACK_BOTNAME = self.__slack_botname
        slack_notify._TEST = self.__test
        return slack_notify

    def setUp(self):
        self.__mock_slack_notify = self.__get_default_slacknotify()

    def test_get_args(self):
        mock_argv_list = ["nagiosnotify_slack.py"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

    def test_get_args_override(self):
        override_channel = "#override"
        mock_argv_list = ["nagiosnotify_slack.py", "-c", override_channel]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertEqual(override_channel, args.channel)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

    def test_get_args_testmode(self):
        mock_argv_list = ["nagiosnotify_slack.py", "-t"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)
        self.assertTrue(args.test)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)

        self.assertNotEqual(self.__test, self.__mock_slack_notify._TEST)
        self.assertTrue(self.__mock_slack_notify._TEST)

    def test_get_args_clear(self):
        mock_argv_list = ["nagiosnotify_slack.py", "-clr"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)
        self.assertTrue(args.clear)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        self.assertListEqual([], self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual([], self.__mock_slack_notify._LIST_STATE)

    def test_get_args_skiplink(self):
        mock_argv_list = ["nagiosnotify_slack.py", "-sk"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)
        self.assertFalse(args.skiplink)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

    def test_get_args_primary_channel(self):
        primary_channel = "#new_primary"
        mock_argv_list = ["nagiosnotify_slack.py", "-pc", primary_channel]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertEqual(primary_channel, args.primary)

        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        self.assertNotEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(primary_channel, self.__mock_slack_notify._PRIMARY_CHANNEL)

    def test_get_args_secondary_channel(self):
        secondary_channel = "#new_secondary"
        mock_argv_list = ["nagiosnotify_slack.py", "-sc", secondary_channel]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertEqual(secondary_channel, args.secondary)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        self.assertNotEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(secondary_channel, self.__mock_slack_notify._SECONDARY_CHANNEL)

    def test_get_args_nagios_server(self):
        nagios_server = "nagios2.somedomain.com"
        mock_argv_list = ["nagiosnotify_slack.py", "-n", nagios_server]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertEqual(nagios_server, args.nagios)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        self.assertNotEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertEqual(nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)

    def test_get_args_service_list(self):
        svc_list = ["Ping", "Load"]
        mock_argv_list = ["nagiosnotify_slack.py", "-svc", svc_list[0], svc_list[1]]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        for old_val in self.__list_servicedisplaynames:
            self.assertNotIn(old_val, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)

        self.assertListEqual(svc_list, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)

    def test_get_args_state_list(self):
        state_list = ["CRITICAL", "DOWN"]
        mock_argv_list = ["nagiosnotify_slack.py", "-st", state_list[0], state_list[1]]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        for old_val in self.__list_state:
            self.assertNotIn(old_val, self.__mock_slack_notify._LIST_STATE)

        self.assertListEqual(state_list, self.__mock_slack_notify._LIST_STATE)

    def test_get_args_host_message(self):
        host_message = "HOST: {0}  STATUS: {1}"
        mock_argv_list = ["nagiosnotify_slack.py", "-hm", host_message]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        self.assertNotEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertEqual(host_message, self.__mock_slack_notify._HOST_MESSAGE)

    def test_get_args_host_message_list(self):
        host_message_list = ["NAGIOS_HOSTNAME", "NAGIOS_HOSTSTATUS"]
        mock_argv_list = ["nagiosnotify_slack.py", "-hl", host_message_list[0], host_message_list[1]]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        self.assertListEqual(host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)

    def test_get_args_service_message(self):
        service_message = "HOST: {0}  SERVICE: {1}"
        mock_argv_list = ["nagiosnotify_slack.py", "-sm", service_message]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        self.assertNotEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertEqual(service_message, self.__mock_slack_notify._SERVICE_MESSAGE)

    def test_get_args_service_message_list(self):
        service_message_list = ["NAGIOS_HOSTNAME", "NAGIOS_SERVICESTATE"]
        mock_argv_list = ["nagiosnotify_slack.py", "-sl", service_message_list[0], service_message_list[1]]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()
        args = self.__mock_slack_notify._get_args()
        k.stop()
        self.assertIsNone(args.channel)

        self.assertEqual(self.__primary, self.__mock_slack_notify._PRIMARY_CHANNEL)
        self.assertEqual(self.__secondary, self.__mock_slack_notify._SECONDARY_CHANNEL)
        self.assertEqual(self.__nagios_server, self.__mock_slack_notify._NAGIOS_SERVER)
        self.assertListEqual(self.__list_servicedisplaynames, self.__mock_slack_notify._LIST_SERVICEDISPLAYNAMES)
        self.assertListEqual(self.__list_state, self.__mock_slack_notify._LIST_STATE)
        self.assertEqual(self.__host_message, self.__mock_slack_notify._HOST_MESSAGE)
        self.assertListEqual(self.__host_message_list, self.__mock_slack_notify._HOST_MESSAGE_LIST)
        self.assertEqual(self.__service_message, self.__mock_slack_notify._SERVICE_MESSAGE)
        self.assertEqual(self.__web_hook_url, self.__mock_slack_notify._WEB_HOOK_URL)
        self.assertEqual(self.__slack_botname, self.__mock_slack_notify._SLACK_BOTNAME)
        self.assertEqual(self.__test, self.__mock_slack_notify._TEST)

        self.assertListEqual(service_message_list, self.__mock_slack_notify._SERVICE_MESSAGE_LIST)

    def test_get_link(self):
        host_name = "host01"
        link_builder = [" <https://", self.__nagios_server, "/nagiosxi/includes/components/xicore/status.php?host=",
                        host_name, "|See Nagios>"]
        html_link_expected = "".join(link_builder)

        html_link = self.__mock_slack_notify._get_link(host_name)

        self.assertEqual(html_link_expected, html_link)

    def test_get_icon(self):
        service_state_list = ["CRITICAL", "WARNING", "OK"]
        host_state_list = ["DOWN", "UP", "UNKNOWN", "SOMEUNKNOWNSTATE"]

        icon = self.__mock_slack_notify._get_icon(service_state_list[0])
        self.assertEqual(":x:  ", icon)

        icon = self.__mock_slack_notify._get_icon(service_state_list[1])
        self.assertEqual(":warning:  ", icon)

        icon = self.__mock_slack_notify._get_icon(service_state_list[2])
        self.assertEqual(":white_check_mark:  ", icon)

        icon = self.__mock_slack_notify._get_icon(host_state_list[0])
        self.assertEqual(":x:  ", icon)

        icon = self.__mock_slack_notify._get_icon(host_state_list[1])
        self.assertEqual(":white_check_mark:  ", icon)

        icon = self.__mock_slack_notify._get_icon(host_state_list[2])
        self.assertEqual(":question:  ", icon)

        icon = self.__mock_slack_notify._get_icon(host_state_list[3])
        self.assertEqual(":white_medium_square:  ", icon)

    def test_get_request_data(self):
        nagios_hostname = "host1"

        mock_argv_list = ["nagiosnotify_slack.py"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()

        mock_env_list = {"NAGIOS_HOSTNAME":nagios_hostname,
                         "NAGIOS_HOSTSTATE":"DOWN",
                         "NAGIOS_HOSTOUTPUT":"Host message testing"}
        l = mock.patch.dict(os.environ, mock_env_list)
        l.start()

        results = self.__mock_slack_notify._get_request_data()

        l.stop()
        k.stop()

        self.assertEqual(self.__web_hook_url, results['url'])

        text_str_builder = [":x:  HOST: ", nagios_hostname, " Some host message <https://",
                            self.__nagios_server, "/nagiosxi/includes/components/xicore/status.php?host=",
                            nagios_hostname, "|See Nagios>"]

        expected_data = {
            "username" : self.__slack_botname,
            "channel" : self.__primary,
            "text" : ''.join(text_str_builder)
        }

        actual_data = json.loads(results['data']['payload'])

        self.assertDictEqual(expected_data, actual_data)

    def test_get_request_data_override(self):
        nagios_hostname = "host1"
        override_channel = self.__override

        mock_argv_list = ["nagiosnotify_slack.py", "-c", override_channel, "-sk"]
        k = mock.patch('sys.argv', mock_argv_list)
        k.start()

        mock_env_list = {"NAGIOS_HOSTNAME":nagios_hostname,
                         "NAGIOS_HOSTSTATE":"DOWN",
                         "NAGIOS_HOSTOUTPUT":"Host message testing"}
        l = mock.patch.dict(os.environ, mock_env_list)
        l.start()

        results = self.__mock_slack_notify._get_request_data()

        l.stop()
        k.stop()

        text_str_builder = [":x:  HOST: ", nagios_hostname, " Some host message"]

        expected_data = {
            "username" : self.__slack_botname,
            "channel" : override_channel,
            "text" : ''.join(text_str_builder)
        }

        actual_data = json.loads(results['data']['payload'])

        self.assertDictEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
