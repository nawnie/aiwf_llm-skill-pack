# ComfyUI Workflow Conversion Policy

## Evidence Model

- Local workflow JSON proves graph shape, node ids, constants, and links.
- `/object_info` proves the node catalog for the running ComfyUI instance: inputs, outputs, display names, categories, modules, and output-node flags.
- ComfyUI source files prove execution behavior only for the exact local checkout or commit inspected.
- Official ComfyUI docs prove format and API expectations, but custom-node packages can still diverge.

## Format Notes

ComfyUI has two common workflow JSON forms:

- API prompt format: execution-facing dict keyed by node id. Each value has `class_type` and `inputs`; links appear as `[source_node_id, output_index]`.
- UI save format: frontend graph format with node arrays, positions, groups, links, and `widgets_values`. This is useful for visual editing, but it needs conversion before direct API execution.

Prefer API prompt format whenever the goal is Python execution. Use UI save format for topology recovery and implementation planning, not as proof that every widget value was mapped.

## Conversion Decision

Use an API wrapper when:

- most nodes are custom nodes,
- the workflow depends on ComfyUI-only execution control,
- no native AIWF engine exists for the model family,
- the user wants to preserve exact ComfyUI behavior.

Use a native AIWF plan when:

- the graph is mostly core loader, prompt, sampler, VAE, LoRA, ControlNet, or image I/O nodes,
- AIWF already has route-specific engine support,
- model files and runtime settings can be mapped cleanly.

Use a mixed adapter plan when:

- only one or two custom branches block native conversion,
- the custom branch can be isolated behind a sidecar call,
- the AIWF route can own validation, settings, and output handling.

## Output Requirements

Every conversion pass should produce:

- workflow format and source path,
- node count, edge count, output nodes, and execution order,
- node type inventory with repeated node counts,
- mutable user inputs such as text prompts, seeds, dimensions, filenames, and model names,
- missing or unknown node classes,
- recommended implementation mode: native, ComfyUI API wrapper, or mixed adapter,
- exact next files or code areas to inspect before implementation.

## Safety Rules

- Do not import arbitrary custom-node packages just to inspect metadata unless Shawn asks and the package source has been reviewed.
- Do not start ComfyUI, queue prompts, or run generation unless Shawn explicitly asks.
- Keep generated pipeline skeletons free of credentials and absolute user secrets.
- Keep original workflow JSON untouched; write generated files to a separate output directory.
