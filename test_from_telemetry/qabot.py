"""analyses telemetry metadata and generates pytests"""
import json


class QaBot:
    """contains methods to clean telemetry log file, generate tests"""

    def __init__(self, trace_log_file) -> None:
        self.trace_file = trace_log_file

    def get_telemetry_info(self):
        """reads telemetry logs and returns trace:response and \
           rest of the logs in array of json blocks"""
        all_trace = {}
        with open(self.trace_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        filtered_lines = ""
        for line in lines:
            if not line.startswith("INFO"):
                filtered_lines += line
            if line.startswith("INFO:root"):
                stripped_line = line.replace("INFO:root:", "").strip() + "\n"
                response_line = json.loads(stripped_line)
                traceid = response_line["trace_context"]["trace_id"]
                all_trace[traceid] = response_line["body"]
        combinedjson = self._get_combined_json_block(filtered_lines)
        return combinedjson, all_trace

    def _get_combined_json_block(self, filtered_lines):
        """converts telemetry logs into array of different json blocks"""
        combined_json = []
        json_block = ""
        brace_count = 0
        for line in filtered_lines.splitlines():
            line = line.strip()
            brace_count += line.count("{") - line.count("}")

            if brace_count > 0:
                json_block += line
            elif brace_count == 0 and json_block:
                json_block += line
                try:
                    log_entry = json.loads(json_block)
                    combined_json.append(log_entry)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                json_block = ""

        return combined_json

    def get_attributes_for_trace_id_and_kind(self, telemetry_data, traceid, kind):
        """given a traceid and telemetry.kind its return the telemetry.attributes"""
        for entry in telemetry_data:
            if (
                entry.get("context", {}).get("trace_id") == traceid
                and entry.get("kind") == kind
            ):
                return entry.get("attributes")
        return None

    def _get_trace_id_for_trace_name(self, telemetry_data, tracename):
        for entry in telemetry_data:
            if entry.get("name") == tracename:
                return entry.get("context", {}).get("trace_id")
        return None

    def get_test_metadata(self, telemetry_data, trace_names, traces_responses):
        """returns a dictionary of telemetrydata and responses for all trace names"""
        testcase_metadata = {}
        for trace_name in trace_names:
            testcase_metadata[trace_name] = {}
            trace_id = self._get_trace_id_for_trace_name(telemetry_data, trace_name)

            # we get telemetry attributes for traceid
            testcase_metadata[trace_name][
                "attributes"
            ] = self.get_attributes_for_trace_id_and_kind(
                telemetry_data, trace_id, "SpanKind.SERVER"
            )
            # we get the response for traceid
            testcase_metadata[trace_name]["response"] = traces_responses[trace_id]
        return testcase_metadata

    def generate_pytest(self, metadata):
        """generates pytest using metadata extracted from telemetry logs"""
        testcases = ""
        for test_name, data in metadata.items():
            # Replace hyphens with underscores to create valid Python function names
            test_name = test_name.replace("-", "_")
            method = data["attributes"]["http.method"]
            url = data["attributes"]["http.url"]
            expected_status = data["attributes"]["http.status_code"]
            expected_response = data["response"]

            testcases += f"""\n
def test_{test_name}():
    response = requests.{method.lower()}('{url}')
    assert response.status_code == {expected_status}
    assert response.json() == json.loads('{expected_response}')
    """
        return testcases

    def write_testcases(self, testfilename, testcases_content):
        """Writes automatically generated tests into a pytest file"""
        test_file_content = """\n
import requests\n
import json\n
        """

        with open(testfilename, "w", encoding="utf-8") as file:
            file.write(test_file_content)
            file.write(testcases_content)

        print(f"Test cases generated in {testfilename}")
