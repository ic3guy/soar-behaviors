from soarsdk.objects import Container
from soarsdk.client import PhantomClient
from behave.runner import Context
from behave.model import Scenario, Step
import soarbehaviors.features.steps.utility_functions as utils
import re

# Optional configuration step
# def after_scenario(context, scenario):
#     if scenario.status == "failed" and context.container.id:
#         context.execute_steps("""then open the browser""")


def before_all(context: Context):
    context.replacement_vars: dict = {}


def before_scenario(context: Context, scenario: Scenario) -> None:
    """Initializes replacement variables and establishes a connection"""
    
    import requests
    from urllib3.exceptions import InsecureRequestWarning
    from urllib3 import disable_warnings

    disable_warnings(InsecureRequestWarning)
    
    import os
    user = os.environ.get("SOAR_USER", "soar_local_admin")
    password = os.environ.get("SOAR_PASSWORD", "password")
    
    s=requests.Session()
    s.auth=(user, password)

    soar_url = os.environ.get("SOAR_URL")
    context.phantom = PhantomClient(soar_url, session=s, verify=False)

    if not context.phantom:
        raise NotImplementedError(
            f"Authentication and connection details not implemented in the environment.py file"
        )


def before_step(context: Context, step: Step) -> None:
    if hasattr(context, "container"):
        utils.context_variable_replacement(context.container, context.replacement_vars)


def after_step(context: Context, step: Step) -> None:
    if hasattr(context, "container"):
        utils.context_variable_replacement(context.container, context.replacement_vars)