import json
import sys
from pathlib import Path


def max_score_for_state(state: str) -> int:
	state = (state or "").strip().lower()
	if state == "diagnosis":
		return 10
	if state == "support":
		return 5
	if state == "synthesis":
		return 10
	return -1



if len(sys.argv) < 2:
	print(
		"Usage: python adder.py <judge_grades.json>",
		file=sys.stderr,
	)
	sys.exit(1)

repo_root = Path(__file__).resolve().parents[1]
grades_dir = repo_root / "dataset" / "grades"

grade_name = sys.argv[1]
grade_path = Path(grade_name)
if not grade_path.is_absolute():
	if grade_path.exists():
		pass
	elif (repo_root / grade_path).exists() or len(grade_path.parts) > 1:
		grade_path = repo_root / grade_path
	else:
		grade_path = grades_dir / grade_path.name
data = json.loads(grade_path.read_text(encoding="utf-8"))

for convo in data:

	total_score = 0
	max_score = 0
	total_turns=0
	d=0
	sup=0
	syn=0

	for turn in convo.get("turn_by_turn_scores", []):
		total_score += int(turn.get("total_score", 0))
		# print(turn.get("state"), turn.get("total_score"))
		max_score += max_score_for_state(str(turn.get("state")))
		total_turns+=1
		if turn.get("state") == "Diagnosis":
			d+=1
		elif turn.get("state") == "Support":
			sup+=1
		elif turn.get("state") == "Synthesis":
			syn+=1

	print(f"Total score: {total_score}")
	print(f"Maximum possible score: {max_score}")
	print(f"Percentage: {total_score / max_score * 100:.2f}%")
	print(f"Diagnosis turns: {d}")
	print(f"Support turns: {sup}")
	print(f"Synthesis turns: {syn}")
	print(f"Total turns: {total_turns}\n")


