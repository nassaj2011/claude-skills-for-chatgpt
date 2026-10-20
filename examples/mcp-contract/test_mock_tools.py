import importlib.util,sys,unittest
from pathlib import Path
p=Path(__file__).resolve().parent/"mock_tools.py"
s=importlib.util.spec_from_file_location("mcp_fixture",p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
class ToolContractTests(unittest.TestCase):
    def setUp(self):self.d=m.Dispatcher()
    def test_scoped_read(self):
        self.assertEqual(len(self.d.invoke("list_bookings",{"venue_id":"v1"},actor="a",venues={"v1"})["bookings"]),1)
    def test_cross_tenant_read_block(self):
        with self.assertRaises(m.ToolError):self.d.invoke("list_bookings",{"venue_id":"v2"},actor="a",venues={"v1"})
    def test_unknown_tool_block(self):
        with self.assertRaises(m.ToolError):self.d.invoke("delete_all",{},actor="a",venues={"v1"})
    def test_unknown_field_block(self):
        with self.assertRaises(m.ToolError):self.d.invoke("list_bookings",{"venue_id":"v1","debug":"true"},actor="a",venues={"v1"})
    def test_write_needs_approval(self):
        with self.assertRaises(m.ToolError):self.d.invoke("set_slot_status",{"venue_id":"v1","slot_id":"s1","status":"closed","request_key":"k"},actor="a",venues={"v1"})
    def test_write_replay_returns_not_updated(self):
        x={"venue_id":"v1","slot_id":"s1","status":"closed","request_key":"k"}
        self.assertTrue(self.d.invoke("set_slot_status",x,actor="a",venues={"v1"},approved=True)["updated"])
        self.assertFalse(self.d.invoke("set_slot_status",x,actor="a",venues={"v1"},approved=True)["updated"])
        self.assertEqual(len(self.d.events),1)
    def test_payload_change_with_replayed_key_fails(self):
        x={"venue_id":"v1","slot_id":"s1","status":"closed","request_key":"k"}
        self.d.invoke("set_slot_status",x,actor="a",venues={"v1"},approved=True)
        with self.assertRaises(m.ToolError):self.d.invoke("set_slot_status",dict(x,status="open"),actor="a",venues={"v1"},approved=True)
    def test_client_mutation_does_not_change_dispatcher_data(self):
        result=self.d.invoke("list_bookings",{"venue_id":"v1"},actor="a",venues={"v1"})
        result["bookings"][0]["state"]="fake"
        self.assertEqual(self.d.bookings["v1"][0]["state"],"reserved")
if __name__=="__main__":unittest.main()
