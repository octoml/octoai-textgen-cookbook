import time
import uuid
import pandas as pd


class Benchmark:
    def __init__(self):
        self.error_per_run: dict = {}
        self.token_usage_per_run: dict = {}
        self.retries_per_run: dict = {}
        self.total_time_per_run: dict = {}

    def new_run(self):
        run_id = f"run-{uuid.uuid4()}"
        self.error_per_run[run_id] = False
        self.retries_per_run[run_id] = 0
        self.token_usage_per_run[run_id] = [0, 0]
        self.total_time_per_run[run_id] = time.perf_counter()
        return run_id
    
    def add_input_tokens(self, run_id, usage):
        self.token_usage_per_run[run_id][0] += usage.prompt_tokens
        self.token_usage_per_run[run_id][1] += usage.completion_tokens

    def increment_retries(self, run_id):
        self.retries_per_run[run_id] += 1

    def end_with_error(self, run_id):
        self.error_per_run[run_id] = True
        self.total_time_per_run[run_id] = time.perf_counter() - self.total_time_per_run[run_id]

    def end(self, run_id):
        self.total_time_per_run[run_id] = time.perf_counter() - self.total_time_per_run[run_id]

    def print_summary(self, save_to_file=None):
        run_ids = list(self.token_usage_per_run.keys())
        summary_df = pd.DataFrame({
            "run_ids": run_ids,
            "error_per_run": [self.error_per_run[rid] for rid in run_ids],
            "retries_per_run": [self.retries_per_run[rid] for rid in run_ids],
            "input_token_usage_per_run": [self.token_usage_per_run[rid][0] for rid in run_ids],
            "output_token_usage_per_run": [self.token_usage_per_run[rid][1] for rid in run_ids],
            "total_time_per_run": [self.total_time_per_run[rid] for rid in run_ids],
        })

        print(summary_df)

        if save_to_file is not None:
            if isinstance(save_to_file, str):
                summary_df.to_csv(save_to_file)
            else:
                summary_df.to_csv("benchmark_measurements.csv")
