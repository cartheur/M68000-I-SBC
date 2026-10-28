# Upstream provenance

This is a source snapshot of [vaelen/vasm](https://github.com/vaelen/vasm),
vendored so this project's Motorola-syntax M68k assembler can be built locally.

- Upstream commit: `8ecb8e6c7a31350ef32c7f1fee289e3677a9a8f0`
- Snapshot date: 2026-07-30

Build the required assembler from this directory:

```sh
make CPU=m68k SYNTAX=mot
```

That produces `vasmm68k_mot`. The upstream Git metadata was omitted to avoid a
nested worktree; the source itself is otherwise unmodified.
