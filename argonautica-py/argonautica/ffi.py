from distutils.sysconfig import get_python_lib
from glob import glob
import os
import re
from typing import Any, Tuple

from cffi import FFI

RE = re.compile(r'^\s*#.*?$(?m)')


def init_ffi() -> Tuple[FFI, Any]:
    ffi = FFI()

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "argonautica.h"), 'r') as f:
        header = f.read()
    header = RE.sub('', header)

    ffi.cdef(header)

    try:
        site_dir = get_python_lib()
        rust_glob = os.path.join(site_dir, "argonautica", "rust.*")
        rust_path = glob(rust_glob)[0]
    except:
        try:
            here = os.path.abspath(os.path.dirname(__file__))
            rust_glob = os.path.join(here, "rust.*")
            rust_path = glob(rust_glob)[0]
        except:
            raise Exception("Error")

    rust = ffi.dlopen(rust_path)

    return (ffi, rust)


(ffi, rust) = init_ffi()
