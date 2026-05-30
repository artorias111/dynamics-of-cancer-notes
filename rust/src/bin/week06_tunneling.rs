//! Week 6 — Two-Hit Mutations & Stochastic Tunneling (Ch. 10)
//!
//! wt → one-hit (1h) → two-hit (2h, fitness advantage FITNESS_2H)
//! Tunneling: 2h arises and fixes before 1h ever dominates the population.
//! Most common when N*u ≈ 1.
//!
//! Run: cargo run --release --bin week06_tunneling
//! Try: FITNESS_1H = 0.8 (costly intermediate) — does tunneling increase?

use rand::Rng;

const N: usize = 1_000;
const U: f64 = 1e-4;
const FITNESS_1H: f64 = 1.0;
const FITNESS_2H: f64 = 1.5;
const RUNS: usize = 2_000;

fn simulate(rng: &mut impl Rng) -> (u64, bool) {
    let (mut wt, mut h1, mut h2) = (N - 1, 1usize, 0usize);
    let mut max_h1_frac: f64 = 0.0;
    let mut t: u64 = 0;
    loop {
        let total = wt as f64 + h1 as f64 * FITNESS_1H + h2 as f64 * FITNESS_2H;
        let pick = rng.gen::<f64>() * total;
        let (mut nwt, mut nh1, mut nh2) = (wt, h1, h2);
        if pick < wt as f64 {
            if rng.gen::<f64>() < U { nh1 += 1; } else { nwt += 1; }
        } else if pick < wt as f64 + h1 as f64 * FITNESS_1H {
            if rng.gen::<f64>() < U { nh2 += 1; } else { nh1 += 1; }
        } else {
            nh2 += 1;
        }
        let new_pop = nwt + nh1 + nh2;
        let die = rng.gen::<usize>() % new_pop;
        if die < nwt { nwt -= 1; } else if die < nwt + nh1 { nh1 -= 1; } else { nh2 -= 1; }
        (wt, h1, h2) = (nwt, nh1, nh2);
        t += 1;
        let frac = h1 as f64 / N as f64;
        if frac > max_h1_frac { max_h1_frac = frac; }
        if h2 == N { return (t, max_h1_frac < 0.1); }
        if t > 50_000_000 { return (t, false); }
    }
}

fn main() {
    let mut rng = rand::thread_rng();
    println!("=== Stochastic Tunneling (Ch. 10) ===");
    println!("N={N}, u={U}, 1h fitness={FITNESS_1H}, 2h fitness={FITNESS_2H}");
    let mut tunnel_count = 0usize;
    let mut times: Vec<u64> = Vec::with_capacity(RUNS);
    for i in 0..RUNS {
        if i % 200 == 0 { eprint!("\r  run {i}/{RUNS}  "); }
        let (t, tunneled) = simulate(&mut rng);
        times.push(t);
        if tunneled { tunnel_count += 1; }
    }
    eprintln!("\r                    \r");
    times.sort_unstable();
    println!("Tunneling: {tunnel_count}/{RUNS} ({:.1}%)",
             tunnel_count as f64 / RUNS as f64 * 100.0);
    println!("Time to 2h fixation:");
    println!("  mean={}, median={}, p10={}, p90={}",
             times.iter().sum::<u64>() / RUNS as u64,
             times[RUNS/2], times[RUNS/10], times[RUNS*9/10]);
    println!();
    println!("INSIGHT: tunneling is most common when N*u ≈ 1 = {}", N as f64 * U);
}
