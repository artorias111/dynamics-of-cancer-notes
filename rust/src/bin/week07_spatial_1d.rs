//! Week 7 — 1D Spatial Moran Process (Ch. 13)
//!
//! Cells on a LINE: division replaces only left/right neighbours.
//! Surprise: P_fix is the same as well-mixed, but fixation TIME scales as N^2 vs N log N.
//!
//! Run: cargo run --release --bin week07_spatial_1d
//! Try: R = 1.0 (neutral) — ratio of 1D to WM time should be very large.

use rand::Rng;

const N: usize = 200;
const R: f64 = 1.3;
const RUNS: usize = 2_000;
const MAX_STEPS: u64 = 20_000_000;

fn spatial_1d(rng: &mut impl Rng, n: usize, r: f64) -> Option<u64> {
    let mut cells = vec![false; n];
    cells[0] = true;
    let mut mutants = 1usize;
    for step in 0..MAX_STEPS {
        if mutants == 0 { return None; }
        if mutants == n { return Some(step); }
        let total = r * mutants as f64 + (n - mutants) as f64;
        let pick = rng.gen::<f64>() * total;
        let parent = if pick < r * mutants as f64 {
            let k = (rng.gen::<f64>() * mutants as f64) as usize;
            cells.iter().enumerate().filter(|(_, &m)| m).nth(k).unwrap().0
        } else {
            let k = (rng.gen::<f64>() * (n - mutants) as f64) as usize;
            cells.iter().enumerate().filter(|(_, &m)| !m).nth(k).unwrap().0
        };
        let nbrs: Vec<usize> = [parent.checked_sub(1),
                                 if parent+1 < n { Some(parent+1) } else { None }]
            .iter().flatten().copied().collect();
        if nbrs.is_empty() { continue; }
        let die = nbrs[rng.gen::<usize>() % nbrs.len()];
        let was_mut = cells[die];
        cells[die] = cells[parent];
        if cells[parent] && !was_mut { mutants += 1; }
        if !cells[parent] && was_mut  { mutants -= 1; }
    }
    None
}

fn wellmixed(rng: &mut impl Rng, n: usize, r: f64) -> Option<u64> {
    let mut m = 1usize;
    for step in 0..MAX_STEPS {
        if m == 0 { return None; }
        if m == n { return Some(step); }
        let total = r * m as f64 + (n - m) as f64;
        let pm = rng.gen::<f64>() * total < r * m as f64;
        let dm = rng.gen::<usize>() % n < m;
        match (pm, dm) { (true,false) => m+=1, (false,true) => m-=1, _ => {} }
    }
    None
}

fn main() {
    let mut rng = rand::thread_rng();
    println!("=== 1D Spatial vs Well-Mixed Moran (Ch. 13) ===");
    println!("N={N}, r={R}, runs={RUNS}");
    let (mut f1d, mut fwm) = (0usize, 0usize);
    let (mut t1d, mut twm): (Vec<u64>, Vec<u64>) = (vec![], vec![]);
    for i in 0..RUNS {
        if i % 200 == 0 { eprint!("\r  run {i}/{RUNS}  "); }
        if let Some(t) = spatial_1d(&mut rng, N, R) { f1d += 1; t1d.push(t); }
        if let Some(t) = wellmixed(&mut rng, N, R)   { fwm += 1; twm.push(t); }
    }
    eprintln!("\r                    \r");
    let analytic = { let ir = 1.0/R; (1.0-ir)/(1.0-ir.powi(N as i32)) };
    println!("Fixation probability:");
    println!("  1D  : {:.4} ({f1d} fixed)", f1d as f64/RUNS as f64);
    println!("  WM  : {:.4} ({fwm} fixed)", fwm as f64/RUNS as f64);
    println!("  Analytic: {analytic:.4}  (same for both)");
    if !t1d.is_empty() && !twm.is_empty() {
        t1d.sort_unstable(); twm.sort_unstable();
        let m1 = t1d[t1d.len()/2];
        let mw = twm[twm.len()/2];
        println!("Fixation time (median): 1D={m1}  WM={mw}  ratio={:.1}x", m1 as f64/mw as f64);
    }
    println!("\nKEY: same P_fix, but 1D is much slower because the clone must spread contiguously.");
}
