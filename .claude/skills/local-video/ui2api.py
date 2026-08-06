#!/usr/bin/env python3
"""Convert a ComfyUI UI-format workflow JSON into the API ("Export (API)") format.

The skill asks for the API JSON to be produced by clicking Export (API) in the ComfyUI
web UI. That needs a browser session; this does the same conversion headlessly by asking
a running ComfyUI for /object_info, which is what maps a node's positional
widgets_values onto named inputs.

usage:
  ui2api.py <ui_workflow.json> <out_api.json> [--server 127.0.0.1:8188]
"""
from __future__ import annotations

import json
import sys
import urllib.request


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    args = sys.argv[1:]
    server = "127.0.0.1:8188"
    if "--server" in args:
        i = args.index("--server")
        server = args[i + 1]
        del args[i : i + 2]
    if len(args) != 2:
        fail("usage: ui2api.py <ui_workflow.json> <out_api.json> [--server host:port]")
    ui_path, out_path = args

    with open(ui_path, encoding="utf-8") as fh:
        ui = json.load(fh)

    with urllib.request.urlopen(f"http://{server}/object_info", timeout=120) as r:
        object_info = json.load(r)

    nodes = ui.get("nodes") or []
    links = ui.get("links") or []

    # link id -> (origin_node_id, origin_slot)
    link_src: dict[int, tuple[str, int]] = {}
    for link in links:
        # UI link format: [link_id, origin_id, origin_slot, target_id, target_slot, type]
        if isinstance(link, list) and len(link) >= 5:
            link_src[link[0]] = (str(link[1]), link[2])
        elif isinstance(link, dict):
            link_src[link["id"]] = (str(link["origin_id"]), link["origin_slot"])

    # Nodes that exist only in the UI and must be skipped / bypassed
    UI_ONLY = {"Note", "MarkdownNote", "Reroute", "PrimitiveNode"}

    api: dict[str, dict] = {}
    skipped: list[str] = []

    for node in nodes:
        node_id = str(node.get("id"))
        class_type = node.get("type")
        if class_type in UI_ONLY:
            skipped.append(f"{node_id}:{class_type}")
            continue
        # mode 4 = bypass, mode 2 = muted
        if node.get("mode") in (2, 4):
            skipped.append(f"{node_id}:{class_type}(muted/bypassed)")
            continue
        info = object_info.get(class_type)
        if info is None:
            fail(
                f"node type '{class_type}' (id {node_id}) is unknown to this ComfyUI — "
                "the H3 nodes may need a newer ComfyUI or a missing custom node pack"
            )

        inputs: dict = {}

        # 1) linked inputs, by the node's declared input slots
        for slot in node.get("inputs") or []:
            name = slot.get("name")
            link_id = slot.get("link")
            if link_id is None:
                continue
            src = link_src.get(link_id)
            if src is None:
                continue
            inputs[name] = [src[0], src[1]]

        # 2) widget inputs, matching widgets_values positionally against the
        #    required+optional input order that object_info reports
        required = info.get("input", {}).get("required", {}) or {}
        optional = info.get("input", {}).get("optional", {}) or {}
        widget_names: list[str] = []
        for name, spec in list(required.items()) + list(optional.items()):
            if name in inputs:  # already satisfied by a link
                continue
            type_or_list = spec[0] if isinstance(spec, list) and spec else spec
            # A list of choices (combo) is a widget; so are the scalar widget types.
            if isinstance(type_or_list, list):
                widget_names.append(name)
            elif type_or_list in ("INT", "FLOAT", "STRING", "BOOLEAN", "COMBO"):
                widget_names.append(name)

        values = node.get("widgets_values")
        if isinstance(values, dict):
            for name, value in values.items():
                inputs[name] = value
        elif isinstance(values, list):
            vi = 0
            for name in widget_names:
                if vi >= len(values):
                    break
                inputs[name] = values[vi]
                vi += 1
                # seed/noise_seed widgets are followed by a control_after_generate widget
                spec = required.get(name) or optional.get(name) or []
                extra = spec[1] if isinstance(spec, list) and len(spec) > 1 and isinstance(spec[1], dict) else {}
                if name in ("seed", "noise_seed") or extra.get("control_after_generate"):
                    vi += 1

        entry = {"class_type": class_type, "inputs": inputs}
        title = (node.get("title") or "").strip()
        if title:
            entry["_meta"] = {"title": title}
        api[node_id] = entry

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(api, fh, ensure_ascii=False, indent=2)

    print(f"converted {len(api)} nodes -> {out_path}")
    if skipped:
        print("skipped UI-only/muted nodes: " + ", ".join(skipped))
    print("node types: " + ", ".join(sorted({v['class_type'] for v in api.values()})))


if __name__ == "__main__":
    main()
