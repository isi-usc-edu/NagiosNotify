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

from __future__ import print_function  # (at top of module)

import argparse
import os
import sys


class NagiosNotify:
    # Run in test mode, bypassing invalid ENV check
    _TEST = False

    def __init__(self):
        pass

    def _get_parser(self):
        parser = argparse.ArgumentParser(description="Nagios slack integration")
        # The Override channel will force the message to only go to that channel
        parser.add_argument('-c', '--channel', required=False, action='store', help='Override Channel')
        parser.add_argument('-pc', '--primary', required=False, action='store', help='Primary Channel')
        parser.add_argument('-sc', '--secondary', required=False, action='store', help='Secondary Channel')
        parser.add_argument('-n', '--nagios', required=False, action='store', help='Nagios Hostname')
        parser.add_argument('-svc', '--services', required=False, nargs='*', help='List of services')
        parser.add_argument('-st', '--states', required=False, nargs='*', help='List of states')
        parser.add_argument('-clr', '--clear', required=False, action='store_true',
                            help='Clear list of services and list of states')
        parser.add_argument('-t', '--test', required=False, action='store_true',
                            help='Set Nagios values to dummy values for running locally')

        parser.add_argument('-hm', '--hostmessage', required=False, action='store', help='Host message')
        parser.add_argument('-hl', '--hostmessagelist', required=False, nargs='*', help='Nagios ENV for host message')
        parser.add_argument('-sm', '--servicemessage', required=False, action='store', help='Service message')
        parser.add_argument('-sl', '--servicemessagelist', required=False, nargs='*',
                            help='Nagios ENV for service message')
        parser.add_argument('-sk', '--skiplink', required=False, action='store_false',
                            help='Skip ending the message with a Nagios link')

        return parser

    def _get_link(self, host):
        pass

    # Get Nagios environment variables - or, set to "test-VARIABLENAME" to run locally
    def _get_env(self, env_var):
        if env_var in os.environ:
            return os.environ[env_var]
        else:
            if self._TEST:
                if env_var == 'NAGIOS_SERVICESTATE':
                    return 'WARNING'
                elif env_var == 'NAGIOS_HOSTSTATE':
                    return 'DOWN'
                elif env_var == 'NAGIOS_SERVICEDISPLAYNAME':
                    return 'Yum Updates'
                # elif env_var == 'NAGIOS_SERVICEDISPLAYNAME':
                #     return ''
                else:
                    test_value = "test-{0}"
                    return test_value.format(env_var)
            return None

    # Get Nagios environment variables from list - MUST BE VALID Nagios ENVIRONMENT VARIABLES
    def _get_env_list(self, message_list):
        msg_list = []
        for env in message_list:
            if env not in os.environ:
                if not self._TEST:
                    print("INVALUD ENVIRONMENT VARIABLE: ", env)
                    sys.exit(1)
            msg_list.append(self._get_env(env))
        return msg_list

    # Decision code to determine which channel the message will go into.
    def _calculate_channel(self, primary, secondary, list_state, list_servicename, nagios_state, nagios_service):
        if not secondary:
            # no secondary value
            return primary
        elif not list_state and not list_servicename:
            # there is a secondary value, but no state or servicename lists
            return primary
        elif not list_state and nagios_service in list_servicename:
            # no state list, but the service is in the servicename list
            return secondary
        elif not list_servicename and nagios_state in list_state:
            # no servicename list, but the state is in the state list
            return secondary
        elif nagios_state in list_state and nagios_service in list_servicename:
            # there is a secondary value and respective values in the state and service list
            return secondary
        else:
            return primary

    def _get_channel(self, override, primary, secondary, list_state, list_servicename, nagios_state, nagios_service):
        if override and not override == '$':
            # override channel was passed in as an arg
            return override
        else:
            return self._calculate_channel(primary, secondary, list_state, list_servicename, nagios_state,
                                           nagios_service)

    def _customization_call(self, state):
        pass

    def _get_message(self, nagios_servicestate, nagios_hoststate, service_message, service_message_list, host_message,
                     host_message_list):
        if nagios_servicestate:
            # Service format message
            text_message = service_message
            self._customization_call(nagios_servicestate)
            msg_list = self._get_env_list(service_message_list)
        else:
            # Host format message
            text_message = host_message
            self._customization_call(nagios_hoststate)
            msg_list = self._get_env_list(host_message_list)

        return text_message.format(*msg_list)

