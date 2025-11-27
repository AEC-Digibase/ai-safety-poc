.PHONY: up down eval gate prep

up:
	docker compose up --build -d
	sleep 2
	echo ">> HEALTH" && curl -s localhost:8000/health || echo "health check failed (API may still be starting)"

down:
	docker compose down

prep:
	mkdir -p .evalcache
	mkdir -p evals/results

# Run evals; capture the path of the results file that run.py prints
eval: prep
	# Use bash -o pipefail so a failure in python propagates
	bash -o pipefail -c 'python evals/run.py' > .evalcache/latest-path.txt
	echo "Latest eval results at: $$(cat .evalcache/latest-path.txt)"

# Read the *real* JSONL file that run.py created and feed it into check.py
gate:
	python evals/check.py < "$$(cat .evalcache/latest-path.txt)" && echo "✅ All safety gates passed."

report:
	python scripts/summarize.py "$$(cat .evalcache/latest-path.txt)"


