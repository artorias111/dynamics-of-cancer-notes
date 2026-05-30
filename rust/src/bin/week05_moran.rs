//! Week 5 — Moran Process & Fixation Probability (Ch. 9)
//!
//! Fixation probability of a mutant with relative fitness r:
//!   P_fix = (1 - 1/r) / (1 - 1/r^N)   [r ≠ 1]
//!   P_fix = 1/N                          [neutral]
//!
//! Run: cargo run --release --bin week05_moran
//! Try changing N and R below.

use rand::Rng;

const N: usize = 100;
const R: f64 = 1.5;
const RUNS: usize = 5_000;

fn moran_fixation(rng: &mut impl Rng, n: usize, r: f64) -> bool {
    let mut mutants: usize = 1;
    loop {
        if mutants == 0 { return false; }
        if mutants == n { return true; }
        let normals = n - mutants;
        let total = r * mutants as f64 + normals as f64;
        let parent_is_mutant = rng.gen::<f64>() * total < r * mutants as f64;
        let die_is_mutant = rng.gen::<usize>() % n < mutants;
        match (parent_is_mutant, die_is_mutant) {
            (true, false) => mutants += 1,
            (false, true) => mutants -= 1,
            _ => {}
        }
    }
}

fn p_fix_analytic(n: usize, r: f64) -> f64 {
    if (r - 1.0).abs() < 1e-10 { return 1.0 / n as f64; }
    let inv_r = 1.0 / r;
    (1.0 - inv_r) / (1.0 - inv_r.powi(n as i32))
}

fn main() {
    let mut rng = rand::thread_rng();
    let fixations = (0..RUNS).filter(|_| moran_fixation(&mut rng, N, R)).count();
    let p_sim = fixations as f64 / RUNS as f64;
    let p_theory = p_fix_analytic(N, R);

    println!("=== Moran Process (Ch. 9) ===");
    println!("N={N}, r={R}, runs={RUNS}");
    println!("  Simulation : {p_sim:.4}  ({fixations}/{RUNS} fixed)");
    println!("  Analytic   : {p_theory:.4}");
    println!("  Neutral 1/N: {:.4}", 1.0 / N as f64);
    println!();
    println!("{:>6}  {:>10}  {:>12}", "r", "P_fix", "fold over 1/N");
    for r_val in [0.5f64, 0.8, 0.9, 1.0, 1.1, 1.5, 2.0, 5.0] {
        let p = p_fix_analytic(N, r_val);
        println!("{:>6.2}  {:>10.6}  {:>12.2}", r_val, p, p * N as f64);
    }
    println!();
    println!("QUESTION: for large N, P_fix ≈ 1 - 1/r. What does that mean?");
}
