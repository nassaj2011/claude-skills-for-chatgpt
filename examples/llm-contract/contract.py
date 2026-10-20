"""Offline fake LLM provider contract: no network, tokens, accounts, or real inference."""
from __future__ import annotations
import json

class ContractError(ValueError): pass
class BudgetExceeded(RuntimeError): pass
class ProviderUnavailable(RuntimeError): pass

REQUIRED={"decision", "reason", "tool"}
TOOLS={"none", "lookup_venue"}

def validate(text: str) -> dict:
    if not isinstance(text,str) or len(text)>4096: raise ContractError("Invalid output size")
    try: value=json.loads(text)
    except (ValueError,TypeError) as ex: raise ContractError("Invalid JSON") from ex
    if not isinstance(value,dict) or set(value)!=REQUIRED: raise ContractError("Invalid response keys")
    if value["decision"] not in {"answer","refuse","lookup"}: raise ContractError("Unknown decision")
    if not isinstance(value["reason"],str) or len(value["reason"])>200: raise ContractError("Invalid reason")
    if value["tool"] not in TOOLS: raise ContractError("Unknown/unauthorized tool")
    if value["decision"]=="lookup" and value["tool"]!="lookup_venue": raise ContractError("Unbound lookup")
    if value["decision"]!="lookup" and value["tool"]!="none": raise ContractError("Unexpected tool")
    return value

def execute(fake_responses: list[str|Exception], *, max_calls:int=2, cost_limit:int=2, actor_can_read:bool=False) -> dict:
    """Deterministic fake call stream; an action is returned only after authorization."""
    if not (1<=max_calls<=3 and 0<=cost_limit<=3): raise ValueError("Limits out of range")
    attempts=0
    for response in fake_responses[:max_calls]:
        if attempts>=cost_limit: raise BudgetExceeded("Budget exhausted")
        attempts+=1
        if isinstance(response,ProviderUnavailable):
            continue  # Simulates bounded retry on transient *read-only* request
        if isinstance(response,Exception): raise response
        parsed=validate(response)
        if parsed["decision"]=="lookup" and not actor_can_read:
            raise PermissionError("Unapproved tool operation")
        return {"result":parsed,"attempts":attempts,"provider":"OFFLINE_FIXTURE_ONLY"}
    raise ProviderUnavailable("No safe provider result")
