.PHONY: up down eval gate prep

up:
	# Bring up the API container and wait a bit for it to be ready
	docker compose up --build -d
	sleep 2
	echo ">> HEALTH" && curl -s localhost:8000/health || echo "health check failed (API may still be starting)"

down:
	docker compose down

# Pre-flight: create local cache/results dirs so evals never explode on missing paths
prep:
	mkdir -p .evalcache
	mkdir -p evals/results

# Run evals and write latest.jsonl in a guaranteed-existing directory
eval: prep
	# Use bash -o pipefail so a failure in python propagates
	bash -o pipefail -c 'python evals/run.py | tee .evalcache/latest.jsonl'


# Safety gate: fail the build if thresholds are violated
gate:
	python evals/check.py < .evalcache/latest.jsonl
