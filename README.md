# YANG-PATCH examples

YANG patch is described in RFC 8072 (https://datatracker.ietf.org/doc/html/rfc8072), although it's a powerful feature, finding any documentation or examples of this on modern systems proved very difficult. This repo will provide a handful of examples for ios xe and nxos.

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

Essentially this makes RESTCONF operations act more like NETCONF operations. They become atomic (all or nothing), and have multiple different types of operations that aren't driven by the HTTP method used. For example, I can "create" an ACL, "merge" a prefix list, and "delete" an ip route all from the same YANG Patch operation. If any of those operations fail, the configuration will roll back to it's previous state. 

From personal experience with both RESTCONF and YANG Patch, the error messages provided by YANG Patch are also much more informative than vanilla RESTCONF. 

## Drawbacks of YANG Patch

While YANG-Patch provides more functionality, it has a drawback that should be noted

Quoted from the RFC
```
 Each edit within a YANG Patch MUST identify exactly one data resource
   instance.  If an edit represents more than one resource instance,
   then the request MUST NOT be processed and a "400 Bad Request" error
   response MUST be sent by the server.
```

Said a bit differently, the target of your edits must be an element in a list, it cannot be the entire list, or a container.

For example, if configuring an access-list, the following target would be considered invalid - `<target>/Cisco-IOS-XE-acl:standard</target>` as it specifies an entire list, not specifying an element. To correct this, you would pass it the key of the element you want to edit, such as - `<target>/Cisco-IOS-XE-acl:standard=EX_5_2</target>`, where EX_5_2 is the key value of name, as specified by the yang model.

## Headers

YANG-Patch supports two different values for headers, `application/yang-patch+json` or `application/yang-patch+xml`. One of these values must be used for both the `Content-type` and `Accept` headers. The Content-type header specifies the value of the data you are sending to the RESTCONF server, while the Accept header specifies the data your client expects to receieve back from the RESTCONF server. The CLI script only uses json for the accept header to make the responses predictable.

**Caveat** - The ansible module - `anisble.netcommon.restconf_config` does not support the yang-patch headers or provide a way to change them when writing your tasks. If you plan to use yang-patch alongside ansible, I would recommend using the `ansible.builtin.uri` module instead.

## Using the examples.py cli in this repo

I've added a simple CLI application `examples.py` that will let you run the ios-xe or nxos examples on your own devices. 

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

The cli provides built-in help, to assist with running the examples.

```
add snippet of cli
```