# Code review sample — Daniel

This is an original fictional demonstration of a small specification review, not previous client work. It contains a deliberately flawed Python function, a revision, and 26 explicit fixtures.

## Read and run

- [Review and observed results](runtime-validation-sample.txt)
- [Python source and all fixtures](runtime-review-demo.py)

Run `python runtime-review-demo.py` using Python 3. No third-party packages, client files, credentials or network access are needed.

## Observed result

The original example matches 17 of 26 fixtures. The revision matches all 26. The runner prints the differences and fails if the revision misses a fixture.

The input contract requires a JSON object with exactly `op`, `a` and `b`, the `add` operation, signed 64-bit integer tokens, and a result in the same range. It rejects booleans, duplicate keys, extra fields and non-standard JSON constants. The findings show why ordinary integer checks and default JSON decoding can be insufficient for that particular contract.

## Limits

The contract is invented for this demonstration. These fixtures are focused regression checks, not an exhaustive proof or a security audit. Only Python was executed; no Rust or client implementation was reviewed. Exception handling normalizes ValueError, KeyError and TypeError into rejection and does not assert a production error-code contract.

## Project inquiries

For a small Python or frontend fix, share a redacted reproduction, the expected behavior and your deadline. Scope, price, acceptance checks and delivery date are agreed before work begins. Contact Daniel at danitythemanity@gmail.com.
