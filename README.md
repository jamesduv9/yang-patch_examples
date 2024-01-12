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