"""Analyze client behavior at floor (permits_max=1) from matrix test results."""

clients_b = [
    # (client, started, completed, errors, elapsed, permits_max)
    (1, 21, 32, 606, 21.2, 1),
    (2, 22, 22, 381, 21.2, 1),
    (3, 20, 29, 627, 20.7, 1),
    (4, 21, 29, 488, 21.7, 2),
    (5, 22, 19, 396, 307.7, None),
    (6, 20, 20, 480, 21.3, 1),
    (7, 22, 40, 555, 21.1, 1),
    (8, 23, 21, 473, 21.2, 1),
    (9, 20, 20, 318, 21.3, 1),
    (10, 20, 32, 349, 21.7, 1),
    (11, 22, 32, 713, 21.8, 2),
    (12, 22, 22, 440, 21.2, 1),
    (13, 20, 32, 466, 21.7, 1),
    (14, 21, 26, 448, 20.6, 1),
    (15, 21, 24, 781, 21.2, 1),
    (16, 23, 22, 671, 21.2, 1),
    (17, 22, 10, 497, 307.7, None),
    (18, 21, 8, 674, 307.7, None),
    (19, 21, 29, 511, 21.7, 1),
    (20, 20, 49, 575, 21.8, 2),
    (21, 22, 30, 852, 21.8, 3),
    (22, 22, 32, 555, 21.5, 1),
    (23, 23, 32, 660, 21.7, 1),
    (24, 20, 23, 687, 21.2, 2),
    (25, 21, 23, 638, 21.1, 1),
]

stuck = [(c, s, comp, e, el, p) for c, s, comp, e, el, p in clients_b if p is not None]
recovered = [(c, s, comp, e, el, p) for c, s, comp, e, el, p in clients_b if p is None]

print("=== BALANCED: Stuck clients (permits_max <= 3) ===")
total_attempts = 0
total_elapsed = 0
for c, s, comp, e, el, p in stuck:
    attempts = s + e
    rate = attempts / el
    total_attempts += attempts
    total_elapsed += el
    print(f"  client-{c}: {attempts} attempts in {el:.1f}s = {rate:.1f} req/s (permits_max={p})")

avg_rate = total_attempts / len(stuck) / (total_elapsed / len(stuck))
print(f"\n  Average rate: {avg_rate:.1f} req/s per client")
print(f"  Aggregate rate: {avg_rate * len(stuck):.0f} req/s (from {len(stuck)} stuck clients)")

print("\n=== BALANCED: Recovered clients ===")
for c, s, comp, e, el, p in recovered:
    attempts = s + e
    rate = attempts / el
    print(f"  client-{c}: {attempts} attempts in {el:.1f}s = {rate:.1f} req/s (completed={comp})")

print("\n=== Success rate at floor ===")
for c, s, comp, e, el, p in stuck[:8]:
    success_rate = s / (s + e) * 100
    err_rate = e / el
    print(f"  client-{c}: success={s}/{s+e} = {success_rate:.1f}%, error rate={err_rate:.1f}/s")

print("\n=== Recovery dynamics ===")
# At permits_max=1: one request at a time, sequential
# Average response time = elapsed / (started + errors)
for c, s, comp, e, el, p in stuck[:5]:
    attempts = s + e
    avg_response_ms = (el * 1000) / attempts
    print(f"  client-{c}: avg response time = {avg_response_ms:.0f}ms ({attempts} attempts)")

print("\n=== The core problem ===")
# 22 stuck clients, each at ~25 req/s = 550 aggregate req/s
# Even at permits_max=1, this is too much for the server
print(f"  Stuck clients: {len(stuck)}")
print(f"  Each at ~{avg_rate:.0f} sequential req/s")
print(f"  Aggregate: ~{avg_rate * len(stuck):.0f} req/s")
print(f"  Server success rate: ~{sum(s for _, s, _, _, _, _ in stuck) / sum(s + e for _, s, _, e, _, _ in stuck) * 100:.1f}%")

# What if we added 500ms backoff at floor?
hypothetical_rate = 1.0 / 0.5  # 2 req/s max per client with 500ms delay
print(f"\n  With 500ms backoff at floor:")
print(f"    Per client: ~{hypothetical_rate:.0f} req/s")
print(f"    Aggregate: ~{hypothetical_rate * len(stuck):.0f} req/s")
print(f"    Reduction: {(1 - hypothetical_rate * len(stuck) / (avg_rate * len(stuck))) * 100:.0f}%")
