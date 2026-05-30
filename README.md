# Dynamics of Cancer — Summer Reading Notes

Interactive exercises for *Dynamics of Cancer* (Wodarz & Komarova).
Python weeks use [marimo](https://marimo.io) notebooks with sliders and live plots.
Stochastic weeks use Rust for speed — each binary runs in seconds, not minutes.

## Setup

```bash
# Python notebooks
pip install marimo scipy numpy matplotlib

# Rust simulations (run once to compile dependencies)
cd rust && cargo build
```

---

## Phase 1 — Deterministic Systems (Weeks 1–4)

### Week 1 — Single-Species Growth (Ch. 4)
**Read**: Chapter 4. Focus on the S-shaped saturation curves, not the derivations.

**Key concepts**: logistic vs Gompertz growth, carrying capacity $K$, why Gompertz fits tumour
data better (it decelerates earlier).

**Run**: `marimo edit python/week01_growth_laws.py`
- Drag the sliders for $a$, $K$, and $W_0$ and watch the curves update live.
- Notice where the two models diverge — before or after $K/2$?

---

### Week 2 — Two-Species Competition (Ch. 5)
**Read**: Chapter 5. Skim the derivations; spend time on Figure 5.1.

**Key concepts**: competitive exclusion, nullclines, bistability vs stable coexistence.
The phase portrait shows *all* possible futures at once.

**Run**: `marimo edit python/week02_competition.py`
- The left panel shows time trajectories; the right panel is the phase portrait with nullclines.
- Try: $r_2 > r_1$ with weak $a_{21}$ → clone 2 dominates regardless of starting point.
- Try: both cross-suppression terms large → bistability, outcome depends on initial conditions.

---

### Week 3 — The Mutator Phenotype (Ch. 6.1)
**Read**: Chapter 6, Section 6.1.

**Key concepts**: mutator cells skip DNA repair for a replication speed-up $s$, but pay in
deleterious hits per division $u$. There is a critical threshold $u_c$: below it, mutators
win; above it, stable cells win.

**Run**: `marimo edit python/week03_mutator_phenotype.py`
- Watch $u_c$ shift as you change $s$ and $n$.
- Question: what happens to $u_c$ as $n \to \infty$?

---

### Week 4 — Quasispecies & Mutation Cascades (Ch. 6.2)
**Read**: Chapter 6, Section 6.2.

**Key concepts**: a chain of increasingly fit mutant clones, each produced by the previous.
Dominance *waves* through the population. Very high mutation rate → error catastrophe.

**Run**: `marimo edit python/week04_quasispecies.py`
- With $r > 1$ and low $u$, watch the successive wave peaks.
- Crank $u$ to ~0.4: the waves blur and the fittest clone never takes over.

---

## Phase 2 — Stochastic Evolution (Weeks 5–8)

These are Rust binaries. Edit the constants at the top of each file and re-run.
Use `--release` for faster runs when doing many simulations.

```bash
cd rust
cargo run --release --bin week05_moran
```

---

### Week 5 — Moran Process & Oncogenes (Ch. 9)
**Read**: Chapter 9.

**Key concepts**: the Moran process models fixed-size cell populations. A mutant with
relative fitness $r$ fixes with probability:
$$P_{fix} = \frac{1 - 1/r}{1 - 1/r^N}$$
For large $N$ and $r > 1$, this approaches $1 - 1/r$ — independent of $N$.

**Run**: `cargo run --release --bin week05_moran`
- The output compares simulation to the analytic formula.
- Try: `R = 0.8` (deleterious mutant). How low does $P_{fix}$ get?
- Try: `N = 10` vs `N = 1000`. How does population size affect selective advantage?

---

### Week 6 — Two-Hit Mutations & Tunneling (Ch. 10)
**Read**: Chapter 10.

**Key concepts**: tumour suppressors need two hits (e.g. both APC alleles). Classical
thinking: first hit fixes, then second hit. Reality: *stochastic tunneling* — the
two-hit mutant can arise and fix before the one-hit intermediate ever dominates.
This makes cancer progression much faster than the sequential model predicts.

**Run**: `cargo run --release --bin week06_tunneling`
- Output reports what fraction of runs tunneled (1h never exceeded 10%).
- Try: `FITNESS_1H = 0.8` (costly intermediate). Does tunneling increase or decrease? Why?
- The insight: tunneling is most efficient when $N \cdot u \approx 1$.

---

### Week 7 — 1D Spatial Moran (Ch. 13)
**Read**: Chapter 13.

**Key concepts**: in a tissue with spatial structure (e.g. a crypt column), cells can
only divide into neighbouring positions. Surprising result: fixation *probability* is
the same as well-mixed, but fixation *time* scales as $N^2$ in 1D vs $N \log N$ well-mixed.

**Run**: `cargo run --release --bin week07_spatial_1d`
- Output shows both probabilities (should match the analytic formula) and median times.
- Try: `R = 1.0` (neutral). The ratio of 1D to well-mixed time should be large.

---

### Week 8 — Colon Crypt Architecture (Ch. 11, 12)
**Read**: Chapters 11 and 12.

**Key concepts**: a colonic crypt has ~5 stem cells at the base. Mutations in
transit-amplifying (TA) cells flush out in days and cannot accumulate. Only stem
cell mutations persist. The small stem pool creates a tight bottleneck — each
individual mutant has low $P_{fix} \approx 1/N_s$, but once it fixes, the whole crypt converts.

**Run**: `cargo run --release --bin week08_crypt`
- The table shows how $P_{fix}$ changes with stem cell number.
- Try: `N_STEMS = 1`. Every mutation that doesn't kill the cell immediately becomes permanent.

---

## Phase 3 — Spatial Dynamics & Treatment (Weeks 9–12)

### Week 9 — 2D Contact Process (Ch. 14)
**Read**: Chapter 14.

**Key concepts**: unlike the Moran process, the contact process allows empty sites —
cells grow into vacant space. This creates spatial *cluster islands* of mutant cells,
which has clinical consequences: a single biopsy may miss entire clone populations.

**Run**: `marimo edit python/week09_spatial_2d.py`
- Hit "Run simulation" and watch the mutant (red) island grow.
- Increase the death rate: empty patches appear and growth fragments.
- This is why intratumour heterogeneity makes biopsy-based diagnostics unreliable.

---

### Week 10 — Drug Resistance (Ch. 15)
**Read**: Chapter 15.

**Key concepts**: resistant mutants arise stochastically during tumour growth, *before*
treatment starts. The Luria-Delbrück result: once $N > 1/u$, resistance is nearly certain.
Treatment timing relative to this threshold determines outcome.

**Run**: `marimo edit python/week10_drug_resistance.py`
- The right panel shows the theory curve: P(resistance) as a function of tumour size.
- The left panel shows the jackpot distribution — most runs have few resistant cells,
  but occasionally one has many (because the mutation arose early in the lineage).

---

### Week 11 — CML and Combination Therapy (Ch. 16)
**Read**: Chapter 16.

**Key concepts**: imatinib (Gleevec) blocks BCR-ABL in CML but single-point mutations
(e.g. T315I) confer resistance. A single drug requires only *one* hit to escape;
combination therapy requires *two simultaneous* hits, scaling probability as $(uN)^2$.

**Run**: `marimo edit python/week11_leukemia_cml.py`
- Compare the bar heights and the log-log curves.
- The crossover point: below $N \sim 1/u$, both strategies work. Above it, only combination.

---

### Week 12 — Angiogenesis (Ch. 8)
**Read**: Chapter 8.

**Key concepts**: tumours beyond ~1–2 mm must recruit blood vessels. The Hahnfeldt
model tracks tumour volume $V$ and vascular carrying capacity $K$ separately. $K$ evolves
dynamically — a tumour can only grow as fast as it can recruit vessels. The *angiogenic
switch* is when pro-angiogenic stimulation overtakes inhibition.

**Run**: `marimo edit python/week12_angiogenesis.py`
- Start with $K_0 \gg V_0$ vs $K_0 \ll V_0$ and compare trajectories.
- Dormant micrometastases correspond to a stable equilibrium where $V \approx K$ at low values.
- Anti-angiogenic drugs shift $c$ up or $b$ down — watch the equilibrium move.

---

### Week 13 — Buffer & Synthesis
**Read**: Ch. 7 (optimal chromosome loss rate) and Ch. 23 (cooperation in tumours).

Use this week to:
- Re-run any notebook or simulation that didn't click the first time.
- Tick off the checklist below.
- Flip back to any figure in the book and see if you can reproduce it.

---

## Progress checklist

- [ ] Week 1  — Growth laws
- [ ] Week 2  — Competition
- [ ] Week 3  — Mutator phenotype
- [ ] Week 4  — Quasispecies
- [ ] Week 5  — Moran process
- [ ] Week 6  — Stochastic tunneling
- [ ] Week 7  — 1D spatial
- [ ] Week 8  — Crypt model
- [ ] Week 9  — 2D contact process
- [ ] Week 10 — Drug resistance
- [ ] Week 11 — CML / combination therapy
- [ ] Week 12 — Angiogenesis
- [ ] Week 13 — Buffer / synthesis
