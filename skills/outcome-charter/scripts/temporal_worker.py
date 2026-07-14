#!/usr/bin/env python3
"""Start the outcome-charter Temporal worker with a runner-owned adapter."""

from __future__ import annotations

import argparse
import asyncio
import importlib
import os


def load_adapter():
    module_name = os.environ.get("OUTCOME_CHARTER_ADAPTER_MODULE")
    if not module_name:
        raise RuntimeError("OUTCOME_CHARTER_ADAPTER_MODULE must name a runner-owned adapter module")
    module = importlib.import_module(module_name)
    required = ("preflight", "authorize", "execute_step", "emit_receipt")
    missing = [name for name in required if not callable(getattr(module, name, None))]
    if missing:
        raise RuntimeError(f"adapter module missing callables: {', '.join(missing)}")
    return module


def load_data_converter():
    module_name = os.environ.get("OUTCOME_CHARTER_CODEC_MODULE", "temporal_codec")
    module = importlib.import_module(module_name)
    factory = getattr(module, "data_converter", None)
    if not callable(factory):
        raise RuntimeError("Temporal codec module must expose data_converter()")
    return factory()


async def run_worker(address: str, namespace: str, task_queue: str) -> None:
    try:
        from temporalio.client import Client
        from temporalio.worker import Worker
        from temporal_runtime import ACTIVITIES, OutcomeCharterWorkflow, configure_adapter
    except ImportError as exc:
        raise RuntimeError("install scripts/requirements.txt before starting the Temporal worker") from exc
    configure_adapter(load_adapter())
    client = await Client.connect(address, namespace=namespace, data_converter=load_data_converter())
    async with Worker(
        client,
        task_queue=task_queue,
        workflows=[OutcomeCharterWorkflow],
        activities=ACTIVITIES,
    ):
        await asyncio.Event().wait()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--address", default="localhost:7233")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--task-queue", default="outcome-charters")
    args = parser.parse_args()
    try:
        asyncio.run(run_worker(args.address, args.namespace, args.task_queue))
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"outcome-charter worker error: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
