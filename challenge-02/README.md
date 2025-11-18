# Name - Hidden Service

You're a security researcher testing **SecureBank**, a new fintech startup's gRPC API. 

**Goal:** Discover and exploit the hidden admin service to retrieve the flag

## Start the challenge

### Option 1: Docker (recommended)

```bash
docker-compose up --build
```

### Option 2: Python + pipenv

```bash
pipenv shell
pipenv install
./generate_protos.sh  # Generate Python code from .proto files
python3 server.py
```

## What you know

- Server runs on `localhost:50051`
- You have `grpcurl` installed (or can use it via Docker)
- The public API accepts these requests:

```bash
# Example: Check balance
grpcurl -plaintext -d '{"account_id": "ACC001"}' \
  localhost:50051 bank.BankingService/GetBalance
```

## Hints

<details>
<summary>Hint 1: What is gRPC reflection?</summary>

gRPC servers can optionally enable a "reflection" service that allows clients to discover what services and methods are available without having the `.proto` files.

Check if reflection is enabled on this server...
</details>

<details>
<summary>Hint 2: How to list services?</summary>

Try this command:
```bash
grpcurl -plaintext localhost:50051 list
```

If reflection is enabled, you'll see all available services!
</details>

<details>
<summary>Hint 3: I found a service, now what?</summary>

Once you discover a service, you can:
1. List its methods: `grpcurl -plaintext localhost:50051 list ServiceName`
2. Describe a method: `grpcurl -plaintext localhost:50051 describe ServiceName.MethodName`
3. Call it: `grpcurl -plaintext -d '{"field": "value"}' localhost:50051 ServiceName/MethodName`
</details>

## References

- [gRPC Server Reflection](https://github.com/grpc/grpc/blob/master/doc/server-reflection.md)
- [grpcurl Documentation](https://github.com/fullstorydev/grpcurl)
- [OWASP gRPC Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/gRPC_Security_Cheat_Sheet.html)
- [Trend Micro: How Unsecure gRPC Implementations Can Compromise APIs](https://www.trendmicro.com/en_us/research/20/h/how-unsecure-grpc-implementations-can-compromise-apis.html)
