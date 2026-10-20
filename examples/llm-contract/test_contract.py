import importlib.util,sys,unittest
from pathlib import Path
f=Path(__file__).resolve().parent/"contract.py"
s=importlib.util.spec_from_file_location("llm_contract",f)
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
class LLMContractTests(unittest.TestCase):
    def test_valid_no_tool(self):
        self.assertEqual(m.execute(['{"decision":"answer","reason":"OK","tool":"none"}'])["attempts"],1)
    def test_unknown_json_keys(self):
        with self.assertRaises(m.ContractError):m.validate('{"decision":"answer","reason":"yes","tool":"none","override":true}')
    def test_untrusted_output_does_not_execute_tool(self):
        with self.assertRaises(m.ContractError):m.validate('{"decision":"lookup","reason":"go","tool":"shell"}')
    def test_auth_denied(self):
        with self.assertRaises(PermissionError):m.execute(['{"decision":"lookup","reason":"look","tool":"lookup_venue"}'])
    def test_auth_granted(self):
        self.assertEqual(m.execute(['{"decision":"lookup","reason":"look","tool":"lookup_venue"}'],actor_can_read=True)["result"]["tool"],"lookup_venue")
    def test_bounded_transient_retry(self):
        self.assertEqual(m.execute([m.ProviderUnavailable("offline"),'{"decision":"answer","reason":"ok","tool":"none"}'])["attempts"],2)
    def test_retries_exhausted(self):
        with self.assertRaises(m.ProviderUnavailable):m.execute([m.ProviderUnavailable("offline")]*4)
    def test_quota_exhausted(self):
        with self.assertRaises(m.BudgetExceeded):m.execute(['{"decision":"answer","reason":"ok","tool":"none"}'],cost_limit=0)
    def test_oversized_or_malformed(self):
        for value in ["x"*5000,"{broken","[]"]:
            with self.subTest(value=value[:10]):
                with self.assertRaises(m.ContractError):m.validate(value)
if __name__=="__main__":unittest.main()
