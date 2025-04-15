from prometheus_client import Counter, Gauge, Histogram

# ---------------- vLLM Specific Metrics ----------------

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
