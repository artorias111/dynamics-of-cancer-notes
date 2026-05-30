//! Week 8 — Colon Crypt Hierarchical Model (Ch. 11, 12)
//!
//! ~5 stem cells at crypt base feed transit-amplifying (TA) cells.
//! Mutations in TA cells flush out in days. Only stem mutations persist.
//! Once a mutant fixes in stems, the whole crypt converts.
//!
//! Run: cargo run --release --bin week08_crypt
//! Try: N_STEMS = 1  (P_fix becomes 1.0)

use rand::Rng;

const N_STEMS: usize = 5;
const N_TA_DIVS: usize = 4;
const R_MUT: f64 = 1.2;
const RUNS: usize = 10_000;

fn stem_moran(rng: &mut impl Rng, n: usize, r: f64) -> bool {
    let mut m = 1usize;
    loop {
        if m == 0 { return false; }
        if m == n { return true; }
        let total = r * m as f64 + (n - m) as f64;
        let pm = rng.gen::<f64>() * total < r * m as f64;
        let dm = rng.gen::<usize>() % n < m;
        match (pm, dm) { (true,false) => m+=1, (false,true) => m-=1, _ => {} }
    }
}

fn main() {
    let mut rng = rand::thread_rng();
    println!("=== Colonic Crypt (Ch. 11/12) ===");
    println!("N_stems={N_STEMS}, TA_divs={N_TA_DIVS}, r={R_MUT}, runs={RUNS}");
    let analytic = { let ir=1.0/R_MUT; (1.0-ir)/(1.0-ir.powi(N_STEMS as i32)) };
    let mut stem_fix = 0usize;
    for i in 0..RUNS {
        if i % 1000 == 0 { eprint!("\r  {i}/{RUNS}  "); }
        if stem_moran(&mut rng, N_STEMS, R_MUT) { stem_fix += 1; }
    }
    eprintln!("\r              \r");
    let p = stem_fix as f64 / RUNS as f64;
    let ta = 1usize << N_TA_DIVS;
    println!("Crypt: {N_STEMS} stems + {} TA = {} total", N_STEMS*ta, N_STEMS+N_STEMS*ta);
    println!("P(fix in stems): {p:.4}  analytic: {analytic:.4}");
    println!("fold over neutral (1/{N_STEMS}={:.4}): {:.2}x", 1.0/N_STEMS as f64, p*N_STEMS as f64);
    println!();
    println!("{:>8}  {:>10}  {:>14}", "N_stems", "P_fix", "fold/neutral");
    for ns in [1usize, 2, 5, 10, 20, 50] {
        let ir = 1.0/R_MUT;
        let pn = (1.0-ir)/(1.0-ir.powi(ns as i32));
        println!("{:>8}  {:>10.6}  {:>14.2}", ns, pn, pn*ns as f64);
    }
    println!("\nKEY: more stems = lower P_fix per mutant, but total conversion once one fixes.");
}
