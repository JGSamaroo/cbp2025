#!/usr/bin/env bash
: '
CBP="./cbp.exe"
TRACE="./cbp_traces/int.tar-004/int/int_0_trace/int_15_trace"
OUTPUT_FILE1="./bitest_single_trace_output.txt"

echo "running single trace..." > "$OUTPUT_FILE1"
echo "=============" >> "$OUTPUT_FILE1"
echo "running trace: int_0_trace" >> "$OUTPUT_FILE1"
echo "=============" >> "$OUTPUT_FILE1"

#run CBP on single trace 
$CBP "$TRACE" >> "$OUTPUT_FILE1" 2>&1
...'


CBP="./cbp.exe"
INT_DIR="./cbp_traces/int.tar-004/int"
OUTPUT_FILE="./all_int_results_bimodal.txt"


echo "running all int traces Bimodal..." > "$OUTPUT_FILE"

for dir in "$INT_DIR"/*; do
	if [[ -d "$dir" ]]; then
		trace_name=$(basename "$dir")
		trace_file="$dir/$trace_name"

		if [[ -f "$trace_file" ]]; then
			echo "===================" >> "$OUTPUT_FILE"
			echo "running trace: $trace_name" | tee -a "$OUTPUT_FILE"
			echo "===================" >> "$OUTPUT_FILE"

			./cbp.exe "$trace_file" >> "$OUTPUT_FILE" 2>&1 || {
				echo "ERROR running $trace_name" | tee -a "$OUTPUT_FILE"
			}
			echo " " >> "$OUTPUT_FILE"
		else 
			echo "warning: no trace file inside $trace_name"
		fi
	fi
done

echo "DONE and saved to output file: $OUTPUT_FILE"



