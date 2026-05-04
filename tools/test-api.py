#!/usr/bin/env python3
import argparse
import os
import sys

os.environ["RUNNING_OPENAPI_CURL_TEST"] = "1"

ZULIP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ZULIP_PATH)
os.chdir(ZULIP_PATH)

# check for the venv
from tools.lib import sanity_check

sanity_check.check_venv(__file__)

from zulip import Client

from tools.lib.test_script import add_provision_check_override_param, assert_provisioning_status_ok
from tools.lib.test_server import test_server_running

usage = """test-api [options]"""
parser = argparse.ArgumentParser(usage)
add_provision_check_override_param(parser)
options = parser.parse_args()

assert_provisioning_status_ok(options.skip_provision_check)

with test_server_running(
    skip_provision_check=options.skip_provision_check, external_host="zulipdev.com:9981"
):
    # zerver imports should happen after `django.setup()` is run
    # by the test_server_running decorator.
    from zerver.actions.create_user import do_create_user, do_reactivate_user
    from zerver.actions.realm_settings import (
        do_change_realm_permission_group_setting,
        do_deactivate_realm,
        do_reactivate_realm,
    )
    from zerver.actions.user_settings import do_change_user_setting
    from zerver.actions.users import change_user_is_active
    from zerver.lib.test_helpers import reset_email_visibility_to_everyone_in_zulip_realm
    from zerver.models.groups import NamedUserGroup, SystemGroups
    from zerver.models.realms import get_realm
    from zerver.models.users import get_user
    from zerver.openapi.javascript_examples import test_js_bindings
    from zerver.openapi.python_examples import (
        reset_realm_uploaded_emoji,
        test_invalid_api_key,
        test_realm_deactivated,
        test_the_api,
        test_user_account_deactivated,
    )
    from zerver.openapi.test_curl_examples import test_generated_curl_examples_for_success

    print("Running API tests...")



print("API tests passed!")
