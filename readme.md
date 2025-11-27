## AI Safety QA PoC – Architecture Overview

This repo is a small but end-to-end AI safety QA harness around a toy text-generation API. The goal is not model quality, but **safety plumbing**: repeatable evals, explicit gates, and signals you can plug into CI/CD.

### System Under Test (SUT)

- **API:** FastAPI service at `/generate`
- **Safety hooks in the request path:**
  - Simple PII scrubber (email + SSN patterns)
  - Policy check that refuses obviously dangerous prompts (bombs, hacking, credit cards, etc.)
- **Model backend:** a stubbed “model” that:
  - Echos safe answers
  - Hard-codes correct answers for a tiny truthfulness suite (for green CI during the PoC)
  - Returns a consistent refusal string when the policy is violated

The important part is that the SUT looks like a real model API from the outside, even though it’s just a stub.

### Evaluation Harness

All evals are defined as YAML suites in `evals/suites/*.yaml`. Each suite is a small dataset of prompts plus an implied checker function. The runner:

```bash
make eval   # run all suites, write JSONL results
make gate   # enforce thresholds and fail if any gate is violated
