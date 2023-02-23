import multiprocessing
import sys

import openbb_terminal.core.session.user as _
from openbb_terminal.base_helpers import load_dotenv_and_reload_configs
from openbb_terminal.terminal_helper import is_auth_enabled

# pylint: disable=import-outside-toplevel


def main():
    multiprocessing.freeze_support()
    sent_args = sys.argv[1:]

    # After implementing the UserModel we will not need to load the dotenv here
    load_dotenv_and_reload_configs()

    if "-t" in sent_args or "--test" in sent_args:
        from openbb_terminal.core.integration_tests import integration_controller

        integration_controller.main()
    else:
        from openbb_terminal.core.session import session_controller

        if is_auth_enabled():
            session_controller.main()
        else:
            session_controller.launch_terminal()


if __name__ == "__main__":
    main()
