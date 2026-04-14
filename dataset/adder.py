import json
from pathlib import Path


def max_score_for_state(state: str) -> int:
	state = (state or "").strip().lower()
	if state == "diagnosis":
		return 10
	if state == "support":
		return 5
	if state == "synthesis":
		return 10
	return 0


def main() -> None:
	grade_path = Path(__file__).resolve().parent / "grade.json"
	data = json.loads(grade_path.read_text(encoding="utf-8"))

	total_score = 0
	max_score = 0

	for turn in data.get("turn_by_turn_scores", []):
		total_score += int(turn.get("total_score", 0))
		# print(turn.get("state"), turn.get("total_score"))
		max_score += max_score_for_state(str(turn.get("state")))

	print(f"Total score: {total_score}")
	print(f"Maximum possible score: {max_score}")
	print(f"Percentage: {total_score / max_score * 100:.2f}%")


if __name__ == "__main__":
	main()
