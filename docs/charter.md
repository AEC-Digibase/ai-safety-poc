MD
# Risk & Test Charter (Draft)
- Context: Text-generation API for internal PoC
- Key risks: jailbreaks, prompt-injection, PII echo, toxic output, hallucinations
- Controls to test: PII scrubber, refusal policy, toxicity/PII detectors, truthfulness checks
- Release gate: build fails if safety thresholds are not met
MD
