# YANG-PATCH examples

YANG patch is defined in RFC 8072 (https://datatracker.ietf.org/doc/html/rfc8072), although it's a powerful feature, finding any documentation or examples of this on modern systems proved very difficult. This repo will provide a handful of useful examples for iOS XE and NX-OS.

This was written during my studies for the Cisco DevNet Expert certification. While it's not on the blueprint, the topics here will help with understanding vanilla RESTCONF (RFC 8040), which is on the blueprint.


## Using the example_cli.py CLI in this repo

I've added a simple CLI application `example_cli.py` that will let you run the iOS-XE or NX-OS examples on your own devices. 

### Prerequisites
- Python 3.6 or higher
- Pip (Python package installer)
- Virtual environment (recommended)

### Setting Up the Environment
1. Clone the repository:
   ```
   git clone https://github.com/jamesduv9/yang-patch_examples.git
   ```
2. Navigate to the project directory:
   ```
   cd yang-patch_examples
   ```
3. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Interacting with the CLI

The CLI provides built-in help, to assist with running the examples.

```
add snippet of CLI
```

## Benefits of YANG Patch over normal RESTCONF operations

Quoted from the RFC:

```
YANG Patch has some features that are not possible with the
   "plain-patch" mechanism defined in RESTCONF [RFC8040]:

   o  YANG Patch allows multiple sub-resources to be edited within the
      same PATCH method.

   o  YANG Patch allows a more precise edit operation than the
      "plain patch" mechanism found in [RFC8040].  There are seven
      operations supported ("create", "delete", "insert", "merge",
      "move", "replace", and "remove").

   o  YANG Patch uses an "edit" list with an explicit processing order.
      The edits are processed in client-specified order, and error
      processing can be precise even when multiple errors occur in the
      same YANG Patch request.
```

Essentially this makes RESTCONF operations act more like NETCONF operations. They become atomic (all or nothing), and have multiple different types of operations that aren't driven by the HTTP method used. For example, I can "create" an ACL, "merge" a prefix list, and "delete" an IP route all from the same YANG Patch operation. If any of those operations fail, the configuration will roll back to its previous state.

From personal experience with both RESTCONF and YANG Patch, the error messages provided by YANG Patch are also much more informative than vanilla RESTCONF.

## Drawbacks of YANG Patch

While YANG-Patch provides more functionality, it has a drawback that should be noted.

Quoted from the RFC:
```
Each edit within a YANG Patch MUST identify exactly one data resource
   instance.  If an edit represents more than one resource instance,
   then the request MUST NOT be processed and a "400 Bad Request" error
   response MUST be sent by the server.
```

Said a bit differently, the target of your edits must be an element in a list, it cannot be the entire list, or a container.

For example, if you want to target the datastore of `/Cisco-IOS-XE-acl:standard` you must specify exactly one element within that yang list to modify by using its key. You cannot add multiple in a single edit.

```
Invalid edit:
        <edit>
          <edit-id>Add the second ACL</edit-id>
          <operation>create</operation>
          <target>/Cisco-IOS-XE-acl:standard</target>
          <value>
            <standard xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
                <name>EX_5_2</name>
            </standard>
            <standard xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
                <name>EX_5_3</name>
            </standard>
          </value>
        </edit>

Valid edit:
        <edit>
          <edit-id>Add the second ACL</edit-id>
          <operation>create</operation>
          <target>/Cisco-IOS-XE-acl:standard</target>
          <value>
            <standard xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
                <name>EX_5_2</name>
            </standard>
          </value>
        </edit>
```



## Headers

YANG-Patch supports two different values for headers, `application/yang-patch+json` or `application/yang-patch+xml`. One of these values must be used for both the `Content-type` and `Accept` headers. The Content-type header specifies the value of the data you are sending to the RESTCONF server, while the Accept header specifies the data your client expects to receive back from the RESTCONF server. The CLI script only uses JSON for the accept header to make the responses predictable.

**Caveat** - The Ansible module - `ansible.netcommon.restconf_config` does not support the yang-patch headers or provide a way to change them when writing your tasks. If you plan to use yang-patch alongside Ansible, I would recommend using the `ansible.builtin.uri` module instead.


## Operations

The main operations displayed in these examples are create, merge, replace, delete

A couple of notes on each of these,
1. **create** - Creates a new data resource, if the resource already exists it will throw an error - ex.`"error-message": "object already exists: /ios:native/ios:router/ios-bgp:bgp[ios-bgp:id='65000']"`
2. **merge** - Can create new data resources, or add data into an existing one. Probably the one you will use the most.
3. **replace** - Completely replaces a data resource with your provided value, this is dangerous, can see this used in IaC deployment where you have your desired state completely defined.
4. **delete** - Does what it says, deletes an object, of the 4 mentioned here, this is the only one that doesn't require a value.

YANG Patch also includes the move and insert operations, however, I was unable to get either working on iOS-XE. I believe this is because iOS relies on values within the data resource to specify its order, and doesn't rely on the lists to be ordered. For example, prefix-list has a required key of "no" to specify which order the prefix-list is interpreted. Using move or insert to place a new prefix list line before or after a specific place in a prefix-list doesn't make sense.

## Ghost configs

Sometimes when using a create operation, the router will return with a `"error-message": "object already exists` when it does not actually exist on the router. I've had this happen a few times without much indication as to why. Merge seems to be the answer. 

