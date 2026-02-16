#!/usr/bin/env python3
"""Count path-local refs in the patched bundled spec."""

import yaml

spec = yaml.safe_load(open("generated/bundled_spec.yaml"))

count = 0
examples = []


def walk(node, path=""):
    global count
    if not isinstance(node, (dict, list)):
        return
    if isinstance(node, list):
        for i, item in enumerate(node):
            walk(item, path + "[" + str(i) + "]")
        return
    ref = node.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/paths/"):
        count += 1
        if count <= 10:
            examples.append(path + " -> " + ref)
    for k, v in node.items():
        walk(v, path + "/" + k)


walk(spec)
print("Total path-local refs:", count)
for e in examples:
    print(" ", e)
