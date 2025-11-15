# How to Fix It

## The Problem

The code enables reflection and registers admin services on the public port:

```python
# Both services on same port
bank_pb2_grpc.add_AdminServiceServicer_to_server(AdminServiceServicer(), server)

# Reflection exposes everything
reflection.enable_server_reflection(SERVICE_NAMES, server)
```

## Solution: Disable Reflection + Separate Services

```python
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Only register public service
    bank_pb2_grpc.add_BankingServiceServicer_to_server(
        BankingServiceServicer(), server
    )

    # Do NOT register AdminService on public port
    # Do NOT enable reflection

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

**Why this works:**
- Attackers cannot enumerate services
- AdminService not registered = not accessible
- Attack surface minimized

### Minimum Fix: Environment-Based Reflection

If you need reflection for development:

```python
import os

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    bank_pb2_grpc.add_BankingServiceServicer_to_server(
        BankingServiceServicer(), server
    )

    # Only enable reflection in development
    if os.getenv('ENVIRONMENT') == 'development':
        from grpc_reflection.v1alpha import reflection
        SERVICE_NAMES = (
            bank_pb2.DESCRIPTOR.services_by_name['BankingService'].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

**Why this is minimal:**
- Still risks accidental production enabling
- Doesn't fix admin service exposure
- But at least prevents reflection leak
