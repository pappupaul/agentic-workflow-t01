#!/usr/bin/env python3
# flake8: noqa
"""
Demo pipeline: convert an issue text into a code patch and (optionally) apply it.
This script is intentionally simple: it shows the planning, preview, and apply steps.
"""
import argparse
import os
import shutil
import sys

issue_text = "Add a /ping endpoint that returns JSON {\"pong\": true}"  # noqa: E501


def make_patch_content():
    return (
        "\n\n# Agentic demo: /ping endpoint\n"
        "from flask import jsonify\n\n"
        "@app.route(\"/ping\")\n"
        "def ping():\n"
        "    return jsonify(pong=True)\n"
    )


def apply_patch(app_path: str):
    backup = app_path + ".bak"
    shutil.copy2(app_path, backup)
    with open(app_path, "a") as f:
        f.write(make_patch_content())
    print('Patched', app_path, '-> backup at', backup)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true", help="Apply the generated patch to app.py")
    args = p.parse_args()

    print('Issue:')
    print(' ', issue_text)
    print('\nPlanned change:')
    print('  Add a /ping Flask endpoint that returns JSON {"pong": true}')  # noqa: E501

    if args.apply:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        app_path = os.path.join(repo_root, "app.py")
        if not os.path.exists(app_path):
            print('Error: app.py not found at', app_path)
            sys.exit(1)
        apply_patch(app_path)
    else:
        print('\nPreview only. Run with --apply to modify app.py (a .bak backup will be created).')


if __name__ == '__main__':
    main()
