"""Script For Generate Protocol Buffers. Run this script before running server.py and in app directory."""


import argparse
from pathlib import Path
from sys import platform
import subprocess

class ProtoFiles:
    PROTO_V1="protos/v1/groom.proto"

def main():
    """Protocol Buffer Generator CLI Script."""
    
    # Check OS Type for python execution.
    if platform == "linux" or platform == "linux2":
        PYTHON_STR = "python3"
    elif platform == "darwin":
        PYTHON_STR = "python3"
    elif platform == "win32":
        PYTHON_STR = "python"

    PARRENT_DIR = Path(__file__).parent

    parser = argparse.ArgumentParser(description="Google Protocol Buffer Generator Script for gRPC")
    parser.add_argument("--proto-path", "-pp", help="Path of Proto file", type=str, required=False, default=ProtoFiles.PROTO_V1)

    args = parser.parse_args()

    proto_path_abs = PARRENT_DIR / args.proto_path
    proto_path = args.proto_path
    proto_path_abs_parrent_dir = Path(proto_path_abs).parent
    init_file_path = proto_path_abs_parrent_dir / "__init__.py"

    print("=" * 50)
    print("Proto file Absolute path: ", proto_path_abs)
    print("Proto file Relative path: ", proto_path)
    print("=" * 50)

    if not Path(proto_path_abs).is_file():
        raise Exception("Proto File: {proto_path} not exist!".format(proto_path=proto_path))

    print("Protocol buffer codes will be generated on {}".format(proto_path_abs_parrent_dir))

    # Create __init__.py if not exist
    if not Path(init_file_path).is_file():
        init_file_path.parent.mkdir(exist_ok=True, parents=True)
        with open(str(init_file_path), "w") as f:
            f.close()

    CMD = """     
    {} -m grpc_tools.protoc \
    -I=./ \
    --pyi_out=./ \
    --python_out=./ \
    --grpc_python_out=./ \
    {}
    """.format(
        PYTHON_STR,
        proto_path,
    )
        
    p = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0: 
        print("Protocol Buffer Creation Failed!")
        print("Return Code:", p.returncode)
        print("Output: ", output.decode())
        print("Error: ", error.decode())
        print("STATUS: Failed!")
        raise Exception("Error!")
        
    print("STATUS: O.K.")
    print("Protocol Buffer files are generated on path: ", proto_path_abs_parrent_dir)
            
if __name__ == "__main__":
    main()