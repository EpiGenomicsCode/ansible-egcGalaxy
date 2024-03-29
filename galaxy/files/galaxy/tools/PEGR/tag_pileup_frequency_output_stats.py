#!/usr/bin/env python
import argparse
import stats_util

parser = argparse.ArgumentParser()
parser.add_argument('--config_file', dest='config_file', help='stats_config.ini')
parser.add_argument('--history_id', dest='history_id', help='History id')
parser.add_argument('--history_name', dest='history_name', help='History name')
parser.add_argument('--input_sense', dest='input_sense', help='Input sense dataset')
parser.add_argument('--input_sense_id', dest='input_sense_id', help='Input sense dataset id')
parser.add_argument('--input_sense_datatype', dest='input_sense_datatype', help='Input sense dataset datatype (i.e., tabular)')
parser.add_argument('--input_anti', dest='input_anti', help='Input anti dataset')
parser.add_argument('--input_anti_id', dest='input_anti_id', help='Input anti dataset id')
parser.add_argument('--input_anti_datatype', dest='input_anti_datatype', help='Input anti dataset datatype (i.e., tabular)')
parser.add_argument('--input_tabular', dest='input_tabular', help='Input tabular dataset')
parser.add_argument('--input_tabular_id', dest='input_tabular_id', help='Input tabular dataset id')
parser.add_argument('--input_tabular_datatype', dest='input_tabular_datatype', help='Input tabular dataset datatype (i.e., tabular)')
parser.add_argument('--dbkey', dest='dbkey', help='Input dataset dbkey')
parser.add_argument('--stats_tool_id', dest='stats_tool_id', help='The caller of this script')
parser.add_argument('--stderr', dest='stderr', help='Job stderr')
parser.add_argument('--tool_id', dest='tool_id', help='Tool that was executed to produce the input dataset')
parser.add_argument('--tool_category', dest='tool_category', help='Tool category key for PEGR to parse')
parser.add_argument('--tool_parameters', dest='tool_parameters', help='Tool parameters that were set when producing the input dataset')
parser.add_argument('--output', dest='output', help='Output statistics dataset for tabular input')
parser.add_argument('--workflow_step_id', dest='workflow_step_id', default=None, help='Workflow step id')
parser.add_argument('--user_email', dest='user_email', help='Current user email')
args = parser.parse_args()

# Initialize the payload.
payload = stats_util.get_base_json_dict(args.config_file, args.dbkey, args.history_id, args.history_name, args.stats_tool_id, args.stderr, args.tool_id, args.tool_category, args.tool_parameters, args.user_email, args.workflow_step_id)
statistics = []
datasets = []

# Generate statistics for sense dataset.
statistics.append({})
datasets.append(stats_util.get_datasets(args.config_file, args.input_sense_id, args.input_sense_datatype))
# Generate statistics for anti dataset.
statistics.append({})
datasets.append(stats_util.get_datasets(args.config_file, args.input_anti_id, args.input_anti_datatype))
# Generate statistics for tabular dataset.
statistics.append({})
datasets.append(stats_util.get_datasets(args.config_file, args.input_tabular_id, args.input_tabular_datatype))
payload['statistics'] = statistics
payload['datasets'] = datasets
payload['history_url'] = stats_util.get_history_url(args.config_file, args.history_id)
# Send the payload to PEGR.
pegr_url = stats_util.get_pegr_url(args.config_file)
response = stats_util.submit(args.config_file, payload)
# Make sure all is well.
stats_util.check_response(pegr_url, payload, response)
# If all is well, store the results in the output.
stats_util.store_results(args.output, pegr_url, payload, response)
