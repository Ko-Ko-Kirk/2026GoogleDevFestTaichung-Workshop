"""Server-owned identities and data; the model cannot provide a role or tenant."""

from devfest_security.common import Blocked

PRINCIPALS = {
    "alice": {"role": "employee", "tenant": "panda", "user": "alice"},
    "bob": {"role": "manager", "tenant": "panda", "user": "bob"},
}
EXPENSES = {
    "EXP-ALICE": {"owner": "alice", "tenant": "panda", "amount": 120, "status": "pending"},
    "EXP-BOB": {"owner": "bob", "tenant": "panda", "amount": 240, "status": "pending"},
    "EXP-OTHER": {"owner": "eve", "tenant": "other", "amount": 360, "status": "pending"},
}
ALLOWED_TOOLS = {"get_expense", "approve_expense"}


def authorize(principal: str, tool: str, arguments: dict) -> None:
    if principal not in PRINCIPALS or tool not in ALLOWED_TOOLS:
        raise Blocked("Unknown identity or tool")
    if set(arguments) != {"expense_id"} or not isinstance(arguments["expense_id"], str):
        raise Blocked("Exactly one string expense_id is required")
    person = PRINCIPALS[principal]
    expense = EXPENSES.get(arguments["expense_id"])
    if expense is None or expense["tenant"] != person["tenant"]:
        raise Blocked("Object is outside principal's tenant")
    if tool == "approve_expense" and person["role"] != "manager":
        raise Blocked("Only managers can approve expenses")
    if tool == "get_expense" and person["role"] != "manager" and expense["owner"] != person["user"]:
        raise Blocked("Employees can only read their own expenses")
