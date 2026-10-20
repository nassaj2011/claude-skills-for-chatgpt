"""Offline tool-contract dispatcher, not an MCP server or actual connector."""
from __future__ import annotations

class ToolError(Exception):
    def __init__(self, code:str): super().__init__(code); self.code=code
CATALOG={
 "list_bookings":{"read":True,"fields":{"venue_id"}},
 "set_slot_status":{"read":False,"fields":{"venue_id","slot_id","status","request_key"}},
}

class Dispatcher:
    def __init__(self):
        self.bookings={"v1":[{"slot_id":"s1","state":"reserved"}],
                       "v2":[{"slot_id":"s2","state":"reserved"}]}
        self.history={}
        self.events=[]
    def invoke(self,tool:str,args:dict,*,actor:str,venues:set[str],approved:bool=False):
        if tool not in CATALOG:raise ToolError("UNKNOWN_TOOL")
        if not isinstance(args,dict) or set(args)!=CATALOG[tool]["fields"]:raise ToolError("BAD_ARGUMENTS")
        if any(not isinstance(v,str) or not v or len(v)>80 for v in args.values()):raise ToolError("BAD_ARGUMENTS")
        if not actor or args["venue_id"] not in venues:raise ToolError("FORBIDDEN")
        venue=args["venue_id"]
        if tool=="list_bookings":
            return {"bookings":[dict(row) for row in self.bookings.get(venue,[])],"source":"MOCK"}
        if not approved:raise ToolError("APPROVAL_REQUIRED")
        if args["status"] not in {"closed","open"}:raise ToolError("BAD_ARGUMENTS")
        key=(actor,args["request_key"])
        signature=(venue,args["slot_id"],args["status"])
        if key in self.history:
            if self.history[key]!=signature:raise ToolError("IDEMPOTENCY_CONFLICT")
            return {"updated":False,"replayed":True}
        row=next((x for x in self.bookings.get(venue,[]) if x["slot_id"]==args["slot_id"]),None)
        if row is None:raise ToolError("SLOT_NOT_FOUND")
        self.history[key]=signature
        row["state"]=args["status"]
        self.events.append({"tool":tool,"actor":actor,"venue":venue,"slot":args["slot_id"]})
        return {"updated":True,"replayed":False}
