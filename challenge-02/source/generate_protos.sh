#!/bin/bash

# Generate Python code from protobuf definitions

# Output dir
mkdir -p generated

# Generate Python code
python3 -m grpc_tools.protoc \
  -I./protos \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./protos/bank.proto

# Create __init__.py to make it a package
touch generated/__init__.py

echo "Protobuf code generated in ./generated/"
