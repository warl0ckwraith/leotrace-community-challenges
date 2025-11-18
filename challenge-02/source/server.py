#!/usr/bin/env python3
"""
Vulnerable gRPC Banking Server
WARNING: This server has intentional security vulnerabilities for educational purposes.
DO NOT use in production!
"""

import grpc
from concurrent import futures
import sys
import os

# Add the generated protobuf code to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

import bank_pb2
import bank_pb2_grpc
from grpc_reflection.v1alpha import reflection


class BankingServiceServicer(bank_pb2_grpc.BankingServiceServicer):

    def __init__(self):
        self.accounts = {
            "ACC001": 1500.00,
            "ACC002": 2300.50,
            "ACC003": 500.00
        }

    def GetBalance(self, request, context):
        account_id = request.account_id
        if account_id in self.accounts:
            return bank_pb2.BalanceResponse(
                account_id=account_id,
                balance=self.accounts[account_id]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Account {account_id} not found")
            return bank_pb2.BalanceResponse()

    def Transfer(self, request, context):
        from_account = request.from_account
        to_account = request.to_account
        amount = request.amount

        if from_account not in self.accounts:
            return bank_pb2.TransferResponse(
                success=False,
                message=f"Source account {from_account} not found"
            )

        if to_account not in self.accounts:
            return bank_pb2.TransferResponse(
                success=False,
                message=f"Destination account {to_account} not found"
            )

        if self.accounts[from_account] < amount:
            return bank_pb2.TransferResponse(
                success=False,
                message="Insufficient funds"
            )

        self.accounts[from_account] -= amount
        self.accounts[to_account] += amount

        return bank_pb2.TransferResponse(
            success=True,
            message=f"Transferred ${amount} from {from_account} to {to_account}"
        )


class AdminServiceServicer(bank_pb2_grpc.AdminServiceServicer):

    def __init__(self):
        self.users = {
            "admin": {
                "api_key": "sk_live_51HxK2jL9m3n4o5p6",
                "notes": "System administrator account"
            },
            "alice": {
                "api_key": "sk_test_4eC39HqLyjWDarjtT1zdp7dc",
                "notes": "Finance team lead"
            }
        }

    def ListAllAccounts(self, request, context):
        return bank_pb2.AccountList(
            accounts=["ACC001", "ACC002", "ACC003", "ACC999_ADMIN"]
        )

    def GetUserSecrets(self, request, context):
        username = request.username

        if username == "admin":
            return bank_pb2.SecretData(
                username=username,
                api_key=self.users.get(username, {}).get("api_key", ""),
                internal_notes=self.users.get(username, {}).get("notes", ""),
                flag="FLAG{grpc_reflection_exposes_hidden_services_4f8a2c}"
            )

        if username in self.users:
            return bank_pb2.SecretData(
                username=username,
                api_key=self.users[username]["api_key"],
                internal_notes=self.users[username]["notes"],
                flag="Try 'admin' user to get the flag!"
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User {username} not found")
            return bank_pb2.SecretData()

    def ExecuteCommand(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Command execution disabled for safety")
        return bank_pb2.CommandResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    bank_pb2_grpc.add_BankingServiceServicer_to_server(
        BankingServiceServicer(), server
    )
    bank_pb2_grpc.add_AdminServiceServicer_to_server(
        AdminServiceServicer(), server
    )

    SERVICE_NAMES = (
        bank_pb2.DESCRIPTOR.services_by_name['BankingService'].full_name,
        bank_pb2.DESCRIPTOR.services_by_name['AdminService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()

    print("=" * 60)
    print("SecureBank gRPC Server Started")
    print("=" * 60)
    print("Listening on: localhost:50051")
    print("Status: Running")
    print("")
    print("WARNING: This server contains intentional vulnerabilities")
    print("    for educational purposes. DO NOT expose to internet!")
    print("=" * 60)

    server.wait_for_termination()


if __name__ == '__main__':
    serve()
