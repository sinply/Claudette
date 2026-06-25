"""Build Claudette.sublime-package from the current source tree.

Strips BOM from .py/.pyi files (Sublime's Python 3.8 zip importer cannot
handle BOM), then zips everything except .git, __pycache__, the output
package itself, and test scripts.

Run: python build_package.py
"""
import os
import sys
import zipfile

REPO = os.path.dirname(os.path.abspath(__file__))
BOM = b"\xef\xbb\xbf"

EXCLUDE_DIRS = {".git", "__pycache__", ".ruff_cache", ".venv"}
EXCLUDE_FILES = {
    "Claudette.sublime-package",
    "build_package.py",
    "test_standalone.py",
    "repomix-output.xml",
}
EXCLUDE_EXTS = {".pyc", ".pyo"}


def strip_bom():
    """Strip BOM from all .py/.pyi files in the tree."""
    stripped = 0
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            if not fname.endswith((".py", ".pyi")):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, "rb") as fh:
                data = fh.read()
            if data[:3] == BOM:
                with open(fpath, "wb") as fh:
                    fh.write(data[3:])
                stripped += 1
                print("Stripped BOM: {0}".format(fpath))
    return stripped


def build():
    output = os.path.join(REPO, "Claudette.sublime-package")
    count = 0
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(REPO):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for fname in files:
                if fname in EXCLUDE_FILES:
                    continue
                if os.path.splitext(fname)[1] in EXCLUDE_EXTS:
                    continue
                fpath = os.path.join(root, fname)
                arcname = os.path.relpath(fpath, REPO).replace(os.sep, "/")
                with open(fpath, "rb") as fh:
                    data = fh.read()
                if fname.endswith((".py", ".pyi")) and data[:3] == BOM:
                    data = data[3:]
                zf.writestr(arcname, data)
                count += 1
    size = os.path.getsize(output)
    print(
        "Created {0} ({1} files, {2} bytes)".format(
            os.path.basename(output), count, size
        )
    )
    return output


if __name__ == "__main__":
    strip_bOM = strip_bom()
    build()
