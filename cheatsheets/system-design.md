# 🏗️ System Design Calculations & Heuristics

### Latency Numbers Every Programmer Should Know
- L1 cache reference: ~0.5 ns
- L2 cache reference: ~7 ns
- RAM reference: ~100 ns
- Read 1 MB sequentially from memory: ~3,000 ns (3 µs)
- Read 1 MB sequentially from SSD: ~1,000,000 ns (1 ms)
- Send 1 MB over 1 Gbps network: ~10,000,000 ns (10 ms)
- Disk seek: ~10,000,000 ns (10 ms)
- Packet round trip (California to Netherlands): ~150 ms

### Back-of-the-Envelope Conversions
- $10^6$ requests/day $pprox 12$ requests/second
- $10^7$ requests/day $pprox 120$ requests/second
- $10^8$ requests/day $pprox 1,200$ requests/second
- 1 byte $	imes 10^9 pprox 1$ GB
- 1 KB $	imes 10^6 pprox 1$ GB
- 1 MB $	imes 10^6 pprox 1$ TB
