"""
Author: James Duvall
Purpose: Just a brief helper module
"""


def get_examples(device_ip: str) -> tuple[dict]:
    """
    Returns example data
    """
    ios_xe_examples = {
        "1": {"file_": "./ios-xe-examples/ios-xe-example1.json",
              "data_type": "json",
              "restconf_path": f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native",
              "example_description": "A simple example with a single edit using a JSON payload, 'merge' a new subinterface G1.101 and assigns it an address using a merge operation."
              },
        "2": {"file_": "./ios-xe-examples/ios-xe-example2.xml",
              "data_type": "xml",
              "restconf_path": f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native",
              "example_description": "A simple example with a single edit using an XML payload, 'merge' a new subinterface G1.101 and assigns it an address using a merge operation."
              },
        "3": {"file_": "./ios-xe-examples/ios-xe-example3.json",
              "data_type": "json",
              "restconf_path": f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native",
              "example_description": "A slightly more complex operation using a JSON payload, 'merge' a subinterface, ospf pid, and enables ospf with a network statement"
              },
        "4": {"file_": "./ios-xe-examples/ios-xe-example4.xml",
              "data_type": "xml",
              "restconf_path": f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native",
              "example_description": "A slightly more complex operation using an XML payload, 'merge' a subinterface, ospf pid, and enables ospf with a network statement"
              },
        "5": {"file_": "./ios-xe-examples/ios-xe-example5.json",
              "data_type": "json",
              "restconf_path": f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native/ip/access-list",
              "example_description": "Example 5, Displaying the order of operations in yang-patch using a JSON payload, executes from top to bottom, while also being atomic. 'create' two standard ACLs, then 'delete' the first."
              },
        "6": {"file_": "./ios-xe-examples/ios-xe-example6.xml",
              "data_type": "xml",
              "restconf_path": f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native/ip/access-list",
              "example_description": "Example 6, Displaying the order of operations in yang-patch using a XML payload, executes from top to bottom, while also being atomic. 'create' two standard ACLs, then 'delete' the first."
              },
        "7": {"file_": "./ios-xe-examples/ios-xe-example7.json",
              "data_type": "json",
              "restconf_path": f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native",
              "example_description": "Complex operation with JSON payload, 'create' bgp asn 65000, 'merge' a new neighbor, 'create' a prefix list, 'merge' the PL on the neighbor, 'replace' the PL with new values"
              },
    }
    nxos_examples = {
    }

    return ios_xe_examples, nxos_examples
