import json

from qabot import QaBot

traces = ["trace_get_item"]
qabot = QaBot("server_logs.txt")
teletry_json_data, trace_response = qabot.get_telemetry_info()
test_metadata = qabot.get_test_metadata(teletry_json_data, traces, trace_response)
print(json.dumps(test_metadata))
test_cases = qabot.generate_pytest(test_metadata)
print(test_cases)
qabot.write_testcases("auto_created_test.py", test_cases)
