from pathlib import Path


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"]).resolve()
    marker = out_dir / "POSTPROCESSING_WAS_HERE"
    marker.write_text("post-processing complete\n", encoding="utf-8")







