from __future__ import annotations

import argparse
import copy
import json
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


KNOWN_STAGE_HINTS = {
    "CheckpointLoaderSimple": "model_loader",
    "CheckpointLoader": "model_loader",
    "DiffusersLoader": "model_loader",
    "UNETLoader": "model_loader",
    "CLIPLoader": "text_encoder_loader",
    "DualCLIPLoader": "text_encoder_loader",
    "VAELoader": "vae_loader",
    "LoraLoader": "lora",
    "LoraLoaderModelOnly": "lora",
    "CLIPTextEncode": "conditioning",
    "EmptyLatentImage": "latent_source",
    "LoadImage": "image_input",
    "LoadImageMask": "mask_input",
    "KSampler": "sampler",
    "KSamplerAdvanced": "sampler",
    "VAEDecode": "decode",
    "VAEDecodeTiled": "decode",
    "VAEEncode": "encode",
    "VAEEncodeTiled": "encode",
    "ControlNetLoader": "controlnet_loader",
    "ControlNetApply": "controlnet",
    "ControlNetApplyAdvanced": "controlnet",
    "SaveImage": "output",
    "PreviewImage": "output",
    "SaveImageWebsocket": "output",
}


COMMON_MUTABLE_INPUTS = {
    "text",
    "seed",
    "steps",
    "cfg",
    "denoise",
    "width",
    "height",
    "batch_size",
    "sampler_name",
    "scheduler",
    "ckpt_name",
    "lora_name",
    "vae_name",
    "unet_name",
    "clip_name",
    "filename_prefix",
    "image",
    "mask",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug[:64] or "comfy-workflow"


def detect_format(data: Any) -> str:
    if isinstance(data, dict) and isinstance(data.get("prompt"), dict):
        prompt = data["prompt"]
        if is_api_prompt(prompt):
            return "wrapped_api_prompt"
    if is_api_prompt(data):
        return "api_prompt"
    if isinstance(data, dict) and isinstance(data.get("nodes"), list):
        return "ui_save_workflow"
    return "unknown"


def is_api_prompt(data: Any) -> bool:
    if not isinstance(data, dict) or not data:
        return False
    node_values = [v for v in data.values() if isinstance(v, dict)]
    return bool(node_values) and all("class_type" in v and "inputs" in v for v in node_values)


def normalize_node_id(value: Any) -> str:
    return str(value)


def normalize_link(raw: Any) -> dict[str, Any] | None:
    if isinstance(raw, dict):
        required = {"id", "origin_id", "origin_slot", "target_id", "target_slot"}
        if required.issubset(raw):
            return {
                "id": raw["id"],
                "origin_id": normalize_node_id(raw["origin_id"]),
                "origin_slot": raw["origin_slot"],
                "target_id": normalize_node_id(raw["target_id"]),
                "target_slot": raw["target_slot"],
                "type": raw.get("type"),
            }
    if isinstance(raw, list) and len(raw) >= 5:
        return {
            "id": raw[0],
            "origin_id": normalize_node_id(raw[1]),
            "origin_slot": raw[2],
            "target_id": normalize_node_id(raw[3]),
            "target_slot": raw[4],
            "type": raw[5] if len(raw) > 5 else None,
        }
    return None


def input_order_for(node_type: str, object_info: dict[str, Any] | None) -> list[str]:
    if not object_info or node_type not in object_info:
        return []
    node_info = object_info[node_type]
    order = node_info.get("input_order")
    if isinstance(order, dict):
        names: list[str] = []
        for group in ("required", "optional", "hidden"):
            values = order.get(group)
            if isinstance(values, list):
                names.extend(str(v) for v in values)
        return names
    inputs = node_info.get("input")
    if isinstance(inputs, dict):
        names = []
        for group in ("required", "optional", "hidden"):
            group_inputs = inputs.get(group)
            if isinstance(group_inputs, dict):
                names.extend(str(v) for v in group_inputs)
        return names
    return []


def convert_ui_to_api(data: dict[str, Any], object_info: dict[str, Any] | None) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    link_by_id = {}
    for raw_link in data.get("links", []):
        link = normalize_link(raw_link)
        if link is not None:
            link_by_id[link["id"]] = link

    api_prompt: dict[str, Any] = {}
    for node in data.get("nodes", []):
        node_id = normalize_node_id(node.get("id"))
        node_type = str(node.get("type", "Unknown"))
        inputs: dict[str, Any] = {}

        for input_slot in node.get("inputs", []) or []:
            if not isinstance(input_slot, dict):
                continue
            link_id = input_slot.get("link")
            input_name = input_slot.get("name")
            if input_name is None or link_id is None:
                continue
            link = link_by_id.get(link_id)
            if link:
                inputs[str(input_name)] = [link["origin_id"], link["origin_slot"]]

        widget_values = node.get("widgets_values")
        unmapped_widgets: list[Any] = []
        if isinstance(widget_values, list):
            candidate_names = [name for name in input_order_for(node_type, object_info) if name not in inputs]
            if candidate_names:
                for name, value in zip(candidate_names, widget_values):
                    inputs[name] = value
                if len(widget_values) > len(candidate_names):
                    unmapped_widgets = widget_values[len(candidate_names):]
            else:
                unmapped_widgets = list(widget_values)
        elif isinstance(widget_values, dict):
            for key, value in widget_values.items():
                inputs.setdefault(str(key), value)

        title = node.get("title")
        properties = node.get("properties")
        if not title and isinstance(properties, dict):
            title = properties.get("Node name for S&R")

        api_node: dict[str, Any] = {
            "class_type": node_type,
            "inputs": inputs,
            "_meta": {"title": title or node_type},
        }
        if unmapped_widgets:
            api_node["_conversion"] = {"unmapped_widgets": unmapped_widgets}
            warnings.append(f"Node {node_id} ({node_type}) has {len(unmapped_widgets)} unmapped widget value(s).")
        api_prompt[node_id] = api_node

    if not object_info:
        warnings.append("UI save workflow was converted without object_info; widget-to-input mapping is partial.")
    return api_prompt, warnings


def extract_prompt(data: Any, workflow_format: str, object_info: dict[str, Any] | None) -> tuple[dict[str, Any], list[str]]:
    if workflow_format == "api_prompt":
        return copy.deepcopy(data), []
    if workflow_format == "wrapped_api_prompt":
        return copy.deepcopy(data["prompt"]), []
    if workflow_format == "ui_save_workflow":
        return convert_ui_to_api(data, object_info)
    raise ValueError(f"Unsupported workflow format: {workflow_format}")


def link_inputs(prompt: dict[str, Any]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for node_id, node in prompt.items():
        for input_name, value in node.get("inputs", {}).items():
            if isinstance(value, list) and len(value) == 2:
                edges.append(
                    {
                        "source": normalize_node_id(value[0]),
                        "source_output": value[1],
                        "target": normalize_node_id(node_id),
                        "target_input": input_name,
                    }
                )
    return edges


def topological_order(prompt: dict[str, Any], edges: list[dict[str, Any]]) -> list[str]:
    node_ids = {normalize_node_id(k) for k in prompt}
    indegree = {node_id: 0 for node_id in node_ids}
    outgoing: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        if source in node_ids and target in node_ids:
            outgoing[source].append(target)
            indegree[target] += 1
    ready = deque(sorted(node_id for node_id, degree in indegree.items() if degree == 0))
    order: list[str] = []
    while ready:
        node_id = ready.popleft()
        order.append(node_id)
        for target in sorted(outgoing[node_id]):
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    if len(order) != len(node_ids):
        remaining = sorted(node_ids - set(order))
        order.extend(remaining)
    return order


def is_output_node(node_type: str, object_info: dict[str, Any] | None) -> bool:
    if object_info and node_type in object_info:
        return bool(object_info[node_type].get("output_node"))
    return node_type.startswith("Save") or node_type.startswith("Preview") or node_type.endswith("Websocket")


def analyze_prompt(
    prompt: dict[str, Any],
    workflow_format: str,
    workflow_path: Path,
    object_info: dict[str, Any] | None,
    conversion_warnings: list[str],
) -> dict[str, Any]:
    edges = link_inputs(prompt)
    order = topological_order(prompt, edges)
    node_types = Counter(str(node.get("class_type", "Unknown")) for node in prompt.values())
    mutable_inputs: list[dict[str, Any]] = []
    unresolved_nodes: list[dict[str, Any]] = []
    output_nodes: list[dict[str, Any]] = []

    for node_id, node in prompt.items():
        node_type = str(node.get("class_type", "Unknown"))
        title = node.get("_meta", {}).get("title") if isinstance(node.get("_meta"), dict) else None
        if object_info is not None and node_type not in object_info:
            unresolved_nodes.append({"node_id": node_id, "class_type": node_type, "title": title or node_type})
        if is_output_node(node_type, object_info):
            output_nodes.append({"node_id": node_id, "class_type": node_type, "title": title or node_type})
        for input_name, value in node.get("inputs", {}).items():
            if input_name in COMMON_MUTABLE_INPUTS and not (isinstance(value, list) and len(value) == 2):
                mutable_inputs.append(
                    {
                        "node_id": node_id,
                        "class_type": node_type,
                        "input": input_name,
                        "value": value,
                    }
                )

    stage_counts = Counter(KNOWN_STAGE_HINTS.get(node_type, "unknown_or_custom") for node_type in node_types)
    if workflow_format == "ui_save_workflow" and object_info is None:
        recommended_mode = "comfy_api_wrapper_or_mixed_adapter"
    elif unresolved_nodes:
        recommended_mode = "comfy_api_wrapper_or_mixed_adapter"
    elif stage_counts.get("unknown_or_custom", 0) > max(2, len(prompt) // 3):
        recommended_mode = "comfy_api_wrapper"
    else:
        recommended_mode = "native_aiwf_plan_candidate"

    return {
        "schema": "aiwf.comfy.workflow_analysis.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workflow_path": str(workflow_path),
        "workflow_format": workflow_format,
        "node_count": len(prompt),
        "edge_count": len(edges),
        "node_type_counts": dict(sorted(node_types.items())),
        "stage_counts": dict(sorted(stage_counts.items())),
        "execution_order": order,
        "edges": edges,
        "output_nodes": output_nodes,
        "mutable_inputs": mutable_inputs,
        "unresolved_nodes": unresolved_nodes,
        "conversion_warnings": conversion_warnings,
        "recommended_mode": recommended_mode,
    }


def build_pipeline_skeleton(prompt: dict[str, Any], analysis: dict[str, Any], module_name: str) -> str:
    workflow_json = json.dumps(prompt, indent=2, sort_keys=True)
    node_sequence_json = json.dumps(analysis["execution_order"], indent=2)
    unresolved_json = json.dumps(analysis["unresolved_nodes"], indent=2, sort_keys=True)
    mutable_json = json.dumps(analysis["mutable_inputs"], indent=2, sort_keys=True)
    return f'''"""Generated ComfyUI workflow pipeline skeleton.

This file preserves the original ComfyUI API graph and exposes safe Python
hooks for parameter injection. Native AIWF replacements should be added only
after each node class has a verified adapter.
"""

from __future__ import annotations

import copy
import json
from urllib import request


WORKFLOW_API = {workflow_json}

NODE_SEQUENCE = {node_sequence_json}

MUTABLE_INPUTS = {mutable_json}

UNRESOLVED_NODES = {unresolved_json}


def workflow_copy() -> dict:
    return copy.deepcopy(WORKFLOW_API)


def set_input(workflow: dict, node_id: str, input_name: str, value) -> dict:
    workflow[str(node_id)]["inputs"][input_name] = value
    return workflow


def apply_common_inputs(
    workflow: dict,
    positive_prompt: str | None = None,
    negative_prompt: str | None = None,
    seed: int | None = None,
    width: int | None = None,
    height: int | None = None,
) -> dict:
    text_nodes = [
        node_id for node_id, node in workflow.items()
        if node.get("class_type") == "CLIPTextEncode" and "text" in node.get("inputs", {{}})
    ]
    if positive_prompt is not None and text_nodes:
        workflow[text_nodes[0]]["inputs"]["text"] = positive_prompt
    if negative_prompt is not None and len(text_nodes) > 1:
        workflow[text_nodes[1]]["inputs"]["text"] = negative_prompt
    for node in workflow.values():
        inputs = node.get("inputs", {{}})
        if seed is not None and "seed" in inputs:
            inputs["seed"] = seed
        if width is not None and "width" in inputs:
            inputs["width"] = width
        if height is not None and "height" in inputs:
            inputs["height"] = height
    return workflow


def queue_comfy_prompt(workflow: dict, base_url: str = "http://127.0.0.1:8188", timeout: int = 300) -> dict:
    payload = json.dumps({{"prompt": workflow}}).encode("utf-8")
    req = request.Request(f"{{base_url.rstrip('/')}}/prompt", data=payload, headers={{"Content-Type": "application/json"}})
    with request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def build_pipeline_request(**kwargs) -> dict:
    workflow = workflow_copy()
    return apply_common_inputs(workflow, **kwargs)


if __name__ == "__main__":
    graph = build_pipeline_request()
    print(json.dumps({{"nodes": len(graph), "sequence": NODE_SEQUENCE, "unresolved": UNRESOLVED_NODES}}, indent=2))
'''


def build_report(analysis: dict[str, Any], skeleton_path: Path) -> str:
    lines = [
        "# ComfyUI Workflow Conversion Report",
        "",
        f"- Workflow: `{analysis['workflow_path']}`",
        f"- Format: `{analysis['workflow_format']}`",
        f"- Nodes: `{analysis['node_count']}`",
        f"- Edges: `{analysis['edge_count']}`",
        f"- Recommended mode: `{analysis['recommended_mode']}`",
        f"- Skeleton: `{skeleton_path.name}`",
        "",
        "## Node Type Inventory",
        "",
    ]
    for node_type, count in analysis["node_type_counts"].items():
        stage = KNOWN_STAGE_HINTS.get(node_type, "unknown_or_custom")
        lines.append(f"- `{node_type}`: {count} ({stage})")
    lines.extend(["", "## Mutable Inputs", ""])
    if analysis["mutable_inputs"]:
        for item in analysis["mutable_inputs"]:
            lines.append(f"- Node `{item['node_id']}` `{item['class_type']}` input `{item['input']}` = `{item['value']}`")
    else:
        lines.append("- None detected.")
    lines.extend(["", "## Output Nodes", ""])
    if analysis["output_nodes"]:
        for item in analysis["output_nodes"]:
            lines.append(f"- Node `{item['node_id']}` `{item['class_type']}` ({item['title']})")
    else:
        lines.append("- None detected. ComfyUI validation may reject this prompt until an output node is present.")
    lines.extend(["", "## Unresolved Nodes", ""])
    if analysis["unresolved_nodes"]:
        for item in analysis["unresolved_nodes"]:
            lines.append(f"- Node `{item['node_id']}` `{item['class_type']}` ({item['title']})")
    else:
        lines.append("- None when checked against the provided metadata.")
    lines.extend(["", "## Conversion Warnings", ""])
    if analysis["conversion_warnings"]:
        lines.extend(f"- {warning}" for warning in analysis["conversion_warnings"])
    else:
        lines.append("- None.")
    lines.extend(["", "## Next Implementation Step", ""])
    if analysis["recommended_mode"] == "native_aiwf_plan_candidate":
        lines.append("Inspect AIWF route support for the model family, then replace known ComfyUI stages with native AIWF service calls one node group at a time.")
    elif analysis["recommended_mode"] == "comfy_api_wrapper":
        lines.append("Keep exact behavior through the ComfyUI API first; native conversion is blocked by custom or unknown node density.")
    else:
        lines.append("Use a mixed adapter: wrap unresolved nodes through ComfyUI or inspect custom-node source before writing native AIWF adapters.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a ComfyUI workflow and emit a Python pipeline skeleton.")
    parser.add_argument("workflow_json", type=Path)
    parser.add_argument("--object-info", type=Path, help="Optional JSON captured from ComfyUI /object_info.")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--name", help="Base name for generated files.")
    args = parser.parse_args()

    workflow_path = args.workflow_json.resolve()
    data = load_json(workflow_path)
    object_info = load_json(args.object_info.resolve()) if args.object_info else None
    workflow_format = detect_format(data)
    prompt, warnings = extract_prompt(data, workflow_format, object_info)

    out_dir = (args.output_dir or workflow_path.with_suffix("")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    base_name = slugify(args.name or workflow_path.stem)

    analysis = analyze_prompt(prompt, workflow_format, workflow_path, object_info, warnings)
    analysis_path = out_dir / f"{base_name}_analysis.json"
    skeleton_path = out_dir / f"{base_name}_pipeline_skeleton.py"
    report_path = out_dir / f"{base_name}_conversion_report.md"

    write_json(analysis_path, analysis)
    skeleton_path.write_text(build_pipeline_skeleton(prompt, analysis, base_name), encoding="utf-8")
    report_path.write_text(build_report(analysis, skeleton_path), encoding="utf-8")

    print(json.dumps({
        "analysis": str(analysis_path),
        "report": str(report_path),
        "skeleton": str(skeleton_path),
        "recommended_mode": analysis["recommended_mode"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
