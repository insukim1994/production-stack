from prometheus_client import Counter, Gauge, Histogram

# ---------------- System and Python Runtime Metrics ----------------

python_gc_objects_collected_total = Counter(
    "python_gc_objects_collected_total", "Objects collected during gc", ["server"]
)
python_gc_objects_uncollectable_total = Counter(
    "python_gc_objects_uncollectable_total",
    "Uncollectable objects found during GC",
    ["server"],
)
python_gc_collections_total = Counter(
    "python_gc_collections_total",
    "Number of times this generation was collected",
    ["server"],
)
python_info = Gauge("python_info", "Python platform information", ["server"])
process_virtual_memory_bytes = Gauge(
    "process_virtual_memory_bytes", "Virtual memory size in bytes.", ["server"]
)
process_resident_memory_bytes = Gauge(
    "process_resident_memory_bytes", "Resident memory size in bytes.", ["server"]
)
process_start_time_seconds = Gauge(
    "process_start_time_seconds",
    "Start time of the process since unix epoch in seconds.",
    ["server"],
)
process_cpu_seconds_total = Counter(
    "process_cpu_seconds_total",
    "Total user and system CPU time spent in seconds.",
    ["server"],
)
process_open_fds = Gauge(
    "process_open_fds", "Number of open file descriptors.", ["server"]
)
process_max_fds = Gauge(
    "process_max_fds", "Maximum number of open file descriptors.", ["server"]
)

# ---------------- vLLM Specific Metrics ----------------

cache_config_info = Gauge(
    "vllm:cache_config_info", "information of cache_config", ["server"]
)
num_requests_running = Gauge(
    "vllm:num_requests_running",
    "Number of requests currently running on GPU.",
    ["server"],
)
num_requests_waiting = Gauge(
    "vllm:num_requests_waiting",
    "Number of requests waiting to be processed.",
    ["server"],
)
num_requests_swapped = Gauge(
    "vllm:num_requests_swapped", "Number of requests swapped to CPU.", ["server"]
)
gpu_cache_usage_perc = Gauge(
    "vllm:gpu_cache_usage_perc",
    "GPU KV-cache usage. 1 means 100 percent usage.",
    ["server"],
)
cpu_cache_usage_perc = Gauge(
    "vllm:cpu_cache_usage_perc",
    "CPU KV-cache usage. 1 means 100 percent usage.",
    ["server"],
)
num_preemptions_total = Counter(
    "vllm:num_preemptions_total",
    "Cumulative number of preemption from the engine.",
    ["server"],
)
prompt_tokens_total = Counter(
    "vllm:prompt_tokens_total", "Number of prefill tokens processed.", ["server"]
)
generation_tokens_total = Counter(
    "vllm:generation_tokens_total", "Number of generation tokens processed.", ["server"]
)
request_success_total = Counter(
    "vllm:request_success_total",
    "Count of successfully processed requests.",
    ["server"],
)
avg_prompt_throughput_toks_per_s = Gauge(
    "vllm:avg_prompt_throughput_toks_per_s",
    "Average prefill throughput in tokens/s.",
    ["server"],
)
avg_generation_throughput_toks_per_s = Gauge(
    "vllm:avg_generation_throughput_toks_per_s",
    "Average generation throughput in tokens/s.",
    ["server"],
)

# ---------------- Histogram Metrics ----------------

time_to_first_token_seconds = Histogram(
    "vllm:time_to_first_token_seconds",
    "Histogram of time to first token in seconds.",
    ["server"],
)
time_per_output_token_seconds = Histogram(
    "vllm:time_per_output_token_seconds",
    "Histogram of time per output token in seconds.",
    ["server"],
)
e2e_request_latency_seconds = Histogram(
    "vllm:e2e_request_latency_seconds",
    "Histogram of end to end request latency in seconds.",
    ["server"],
)
request_prompt_tokens = Histogram(
    "vllm:request_prompt_tokens", "Number of prefill tokens processed.", ["server"]
)
request_generation_tokens = Histogram(
    "vllm:request_generation_tokens",
    "Number of generation tokens processed.",
    ["server"],
)
request_params_best_of = Histogram(
    "vllm:request_params_best_of",
    "Histogram of the best_of request parameter.",
    ["server"],
)
request_params_n = Histogram(
    "vllm:request_params_n", "Histogram of the n request parameter.", ["server"]
)
