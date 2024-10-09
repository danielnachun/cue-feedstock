#!/bin/sh
"""exec" "python3" "$0" "$@" #"""  # fmt: off # fmt: on
#
# This file has been generated by conda-smithy in order to build the recipe
# locally.
#
# The line above this comment is a bash / sh / zsh guard
# to stop people from running it with the wrong interpreter
import glob
import os
import platform
import subprocess
from argparse import ArgumentParser


def setup_environment(ns):
    os.environ["CONFIG"] = ns.config
    os.environ["UPLOAD_PACKAGES"] = "False"
    os.environ["IS_PR_BUILD"] = "True"
    if ns.debug:
        os.environ["BUILD_WITH_CONDA_DEBUG"] = "1"
        if ns.output_id:
            os.environ["BUILD_OUTPUT_ID"] = ns.output_id
    if "MINIFORGE_HOME" not in os.environ:
        os.environ["MINIFORGE_HOME"] = os.path.join(
            os.path.dirname(__file__), "miniforge3"
        )


def run_docker_build(ns):
    script = ".scripts/run_docker_build.sh"
    subprocess.check_call([script])


def run_osx_build(ns):
    script = ".scripts/run_osx_build.sh"
    subprocess.check_call([script])


def verify_config(ns):
    valid_configs = {
        os.path.basename(f)[:-5] for f in glob.glob(".ci_support/*.yaml")
    }
    print(f"valid configs are {valid_configs}")
    if ns.config in valid_configs:
        print("Using " + ns.config + " configuration")
        return
    elif len(valid_configs) == 1:
        ns.config = valid_configs.pop()
        print("Found " + ns.config + " configuration")
    elif ns.config is None:
        print("config not selected, please choose from the following:\n")
        selections = list(enumerate(sorted(valid_configs), 1))
        for i, c in selections:
            print(f"{i}. {c}")
        s = input("\n> ")
        idx = int(s) - 1
        ns.config = selections[idx][1]
        print(f"selected {ns.config}")
    else:
        raise ValueError("config " + ns.config + " is not valid")
    # Remove the following, as implemented
    if ns.config.startswith("win"):
        raise ValueError(
            f"only Linux/macOS configs currently supported, got {ns.config}"
        )
    elif ns.config.startswith("osx"):
        if "OSX_SDK_DIR" not in os.environ:
            raise RuntimeError(
                "Need OSX_SDK_DIR env variable set. Run 'export OSX_SDK_DIR=$PWD/SDKs' "
                "to download the SDK automatically to '$PWD/SDKs/MacOSX<ver>.sdk'. "
                "Note: OSX_SDK_DIR must be set to an absolute path. "
                "Setting this variable implies agreement to the licensing terms of the SDK by Apple."
            )


def main(args=None):
    p = ArgumentParser("build-locally")
    p.add_argument("config", default=None, nargs="?")
    p.add_argument(
        "--debug",
        action="store_true",
        help="Setup debug environment using `conda debug`",
    )
    p.add_argument(
        "--output-id", help="If running debug, specify the output to setup."
    )

    ns = p.parse_args(args=args)
    verify_config(ns)
    setup_environment(ns)

    try:
        if ns.config.startswith("linux") or (
            ns.config.startswith("osx") and platform.system() == "Linux"
        ):
            run_docker_build(ns)
        elif ns.config.startswith("osx"):
            run_osx_build(ns)
    finally:
        recipe_license_file = os.path.join(
            "recipe", "recipe-scripts-license.txt"
        )
        if os.path.exists(recipe_license_file):
            os.remove(recipe_license_file)


if __name__ == "__main__":
    main()