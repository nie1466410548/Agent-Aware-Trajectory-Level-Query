from pathlib import Path
from datetime import datetime
import importlib.util
import logging

def validate(query_dir: Path, llm_answer: str, reason: str=None):
    gt_path = query_dir / "ground_truth.csv"
    if not gt_path.exists():
        logging.getLogger(__name__).warning(f"⚠️ {gt_path} not found")
        gt_lines = ["<ground truth file missing>"]
    else:
        with open(gt_path, encoding="utf-8") as f:
            gt_lines = [line.strip() for line in f if line.strip()]
    gt_str = "\n".join(gt_lines)


    if llm_answer == "":
        return {
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "query_name": query_dir.name,
            "is_valid": False,
            "reason": reason,
            "ground_truth": gt_str,
            "llm_answer": "",
        }
    
    validate_py = query_dir / "validate.py"
    if not validate_py.exists():
        raise FileNotFoundError(f"validate.py not found at: {validate_py}")

    spec = importlib.util.spec_from_file_location("validate", str(validate_py))
    validate_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validate_mod)

    is_valid, reason = validate_mod.validate(llm_answer)

    return {
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "query_name": query_dir.name,
        "is_valid": is_valid,
        "reason": reason,
        "ground_truth": gt_str,
        "llm_answer": llm_answer.strip(),
    }