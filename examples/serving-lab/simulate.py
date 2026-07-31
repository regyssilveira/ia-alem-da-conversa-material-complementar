from __future__ import annotations

import argparse
import heapq
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SimulationConfig:
    requests: int = 100
    workers: int = 4
    arrival_ms: float = 50
    service_ms: float = 120
    batch_size: int = 1
    batch_window_ms: float = 8
    max_queue_ms: float = 500
    cost_per_request: float = 0.02
    success_rate: float = 0.9


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = math.ceil(fraction * len(ordered)) - 1
    return ordered[max(0, min(position, len(ordered) - 1))]


def simulate(config: SimulationConfig) -> dict:
    if config.requests < 1 or config.workers < 1 or config.batch_size < 1:
        raise ValueError("requests, workers e batch_size devem ser positivos.")
    if not 0 < config.success_rate <= 1:
        raise ValueError("success_rate deve estar entre 0 e 1.")

    available = [0.0 for _ in range(config.workers)]
    heapq.heapify(available)
    latencies: list[float] = []
    queue_times: list[float] = []
    rejected = 0

    batch_efficiency = 1 + 0.55 * (min(config.batch_size, 8) - 1)
    effective_service = config.service_ms * config.batch_size / batch_efficiency
    service_per_request = effective_service / config.batch_size

    for index in range(0, config.requests, config.batch_size):
        batch_count = min(config.batch_size, config.requests - index)
        arrival = index * config.arrival_ms
        worker_available = heapq.heappop(available)
        start = max(arrival + config.batch_window_ms, worker_available)
        queue_ms = start - arrival

        if queue_ms > config.max_queue_ms:
            rejected += batch_count
            heapq.heappush(available, worker_available)
            continue

        end = start + effective_service * (batch_count / config.batch_size)
        heapq.heappush(available, end)
        for _ in range(batch_count):
            queue_times.append(queue_ms)
            latencies.append(queue_ms + service_per_request)

    accepted = len(latencies)
    successes = accepted * config.success_rate
    elapsed_ms = max(available) if accepted else config.requests * config.arrival_ms
    total_cost = accepted * config.cost_per_request
    busy_ms = accepted * service_per_request
    return {
        "config": asdict(config),
        "accepted": accepted,
        "rejected": rejected,
        "successes_estimated": successes,
        "throughput_requests_s": accepted / (elapsed_ms / 1000) if elapsed_ms else 0,
        "latency_p50_ms": percentile(latencies, 0.50) if latencies else None,
        "latency_p95_ms": percentile(latencies, 0.95) if latencies else None,
        "queue_p95_ms": percentile(queue_times, 0.95) if queue_times else None,
        "worker_utilization_estimated": min(1.0, busy_ms / (elapsed_ms * config.workers))
        if elapsed_ms
        else 0,
        "total_cost": total_cost,
        "cost_per_success": total_cost / successes if successes else None,
        "limitations": [
            "Tempos são sintéticos e determinísticos.",
            "Batching é uma aproximação, não um modelo de scheduler específico.",
            "Teste de carga real deve incluir hardware, modelo, contexto e dependências.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--arrival-ms", type=float, default=50)
    parser.add_argument("--service-ms", type=float, default=120)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--batch-window-ms", type=float, default=8)
    parser.add_argument("--max-queue-ms", type=float, default=500)
    parser.add_argument("--cost-per-request", type=float, default=0.02)
    parser.add_argument("--success-rate", type=float, default=0.9)
    args = parser.parse_args()
    report = simulate(
        SimulationConfig(
            requests=args.requests,
            workers=args.workers,
            arrival_ms=args.arrival_ms,
            service_ms=args.service_ms,
            batch_size=args.batch_size,
            batch_window_ms=args.batch_window_ms,
            max_queue_ms=args.max_queue_ms,
            cost_per_request=args.cost_per_request,
            success_rate=args.success_rate,
        )
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
