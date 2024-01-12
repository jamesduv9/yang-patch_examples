"""
Author: James Duvall
Purpose: Provides a quick CLI to interact with the yang-patch examples
"""

import json
import requests
import click
from urllib3.exceptions import InsecureRequestWarning
from config import get_examples

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def send_patch(username: str, password: str, device_restconf_path: str, patch_path: str, data_type: str):
    """
    Sends the patch based on input
    params:
        username - u/n of device
        password - pw of device
        device_restconf_path - path that is the target of the patch operation
        patch_path - path to xml or json file
        data_type - json or xml, used for Content-type header
    """

    headers = {"Accept": f"application/yang-patch+json",
               "Content-type": f"application/yang-patch+{data_type}"}
    print(f"Sending our patch with headers : {headers}")
    print(f"To the following uri {device_restconf_path}")
    data = open(patch_path).read()
    response = requests.patch(device_restconf_path, headers=headers, auth=(
        username, password), verify=False, data=data).text

    print("Here's the yang-patch response:")
    print(response)
    response = json.loads(response)
    if response.get("ietf-yang-patch:yang-patch-status", {}).get("ok"):
        print("Patch-id should tell which patch we are running")
        print("Since the 'ok' key exists, the operation was successful")

    elif response.get("errors", {}):
        print("Since there are errors in the response.. well.. it failed..")
        print("The edit-id field will tell you exactly which edit-id failed, if no edit-id is provided, it's probably a greater syntax error")
        print("If you are lucky, the error-message/error-tag is descriptive enough to help you troubleshoot")

    return response


@click.group()
def main_menu():
    ...


@main_menu.command(name="ios-xe")
@click.option("--username", help="Username of the device", required=True)
@click.option("--password", help="Password of the device", prompt=True, required=True)
@click.option("--device-ip", help="IP of the device you want to connect to", required=True)
@click.option("--example-number", help="Which example in ios-xe-examples/ directory do you want to run", required=True)
def ios_xe(username: str, password: str, device_ip: str, example_number: str):
    """
    Sends commands to the iosxe device specified
    """
    ios_xe_examples, _ = get_examples(device_ip)
    if not ios_xe_examples.get(example_number):
        print("Example number provided not found\n exiting")
        exit()
    example = ios_xe_examples.get(example_number)
    print("-" * 50, "\n", f"Example : {example_number}\n",
          example.get("example_description"), "\n", "-" * 50)

    send_patch(device_restconf_path=example.get("restconf_path"), username=username,
               password=password, patch_path=example.get("file_"), data_type=example.get("data_type"))


@main_menu.command(name="show-examples")
@click.option("--os", type=click.Choice(["ios-xe", "nxos", "both"]), show_default=True, default="both", help="Filter which platform you want to see examples for")
def show_examples(os: str):
    """
    Lists all the possible examples you can run with a brief description
    """
    if os == "both" or os == "ios-xe":
        ios_xe_examples, _ = get_examples("0.0.0.0")
        print("IOS XE Examples available:")
        for example_id, example_values in ios_xe_examples.items():
            print(f"Example: {example_id}")
            print(
                f"Example Description: {example_values.get('example_description')}", "\n", "-" * 50)
    elif os == "both" or os == "nxos":
        ...


if __name__ == "__main__":
    main_menu()
