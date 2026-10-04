# Implementation decisions recorded before the first run

No models are called. The two producers are scripted adapters over different private containers; the substantive comparison is boundary representation and information retention, not intelligent cognition. Explanation text is ignored by all decoders.

The four dropped compact fields decode to `alternatives=[]`, `attempt=null`, `status=proposed`, `receipt=null`. These are explicit compression defaults, not assertions justified by evidence. Thus unknown intent and previous execution may be flattened into a new proposal. The full-message policy distinguishes unknown alternatives from an empty list. The simulator honors a command idempotency key but cannot recover an omitted earlier attempt identity. This is the intended abstraction ablation, not a neutral encoding comparison.

Each of 20 fixtures is crossed with four formats, two producers, two consumer versions, and two field-order/rationale styles: 640 rows. Each row gets an independent world and a replay through a fresh consumer using the same wire/world. Rejected messages count as unavailable fields in semantic-loss totals; compatibility rejection and lossy successful decoding must therefore be separated in interpretation. Unsupported version rejection is expected safe behavior, not a serialization error.

Full-message evidence verification compares public artifact facts with a trusted registry. Receipt verification supports confirming a past effect without requiring a fresh grant for observation; new effects still cross complete mediation. Forged permissions in free text do not modify the registry. Registry trust and reliable in-memory replay are assumptions, not experimentally established operational guarantees.

Falsification and protocol remain unchanged. Fixture-oracle outcomes are hand-written and inaccessible to production decision/decoder functions. No run output will be overwritten: reproduction must use a different output path. Checksums identify the exact implemented input, protocol, and fixture set.
