# Setup status

- RocketRide: SDK 1.3.0 installed; authenticated against https://staging.rocketride.ai.
- Cognee: supplied project key verified with authenticated dataset-list request against the existing cloud tenant. No datasets changed.
- Hotdata: supplied token verified; workspace selected in .env.
- Rote: existing installation is healthy and signed in; hello play already installed. Research replay still needs implementation.
- Snyk: CLI installed locally in .setup/snyk; interactive authentication launched, awaiting completion.
- HydraDB: account and credentials still required; public Ship plan is free.

Credentials are stored in .env with owner-only permissions and excluded from Git.
Run `.venv/bin/python check_connections.py` to repeat the read-only service checks.

The research pipeline has not yet been implemented or executed. No research results were generated. Next: complete HydraDB and Snyk authentication, then implement RocketRide's pipeline and sponsor adapters. Verify the funded model configuration before inference.
