from experiment import run


def print_time_table(results):

    print("\n" + "="*120)
    print("TIME COMPARISON")
    print("="*120)

    print(
        f"{'n':>3} | "
        f"{'HK':>8} | {'HK_th':>8} | {'ratio':>4} | "
        f"{'CHR':>8} | {'CHR_th':>8} | {'ratio':>4}"
    )

    for r in results:
        print(
            f"{r['n']:>3} | "
            f"{r['hk_time']:.6f} | {r['hk_theory_time']:.6f} | {r['hk_time_ratio']:.2f} | "
            f"{r['chr_time']:.6f} | {r['ch_theory_time']:.6f} | {r['ch_time_ratio']:.2f}"
        )


def print_memory_table(results):

    print("\n" + "="*120)
    print("MEMORY COMPARISON")
    print("="*120)

    print(
        f"{'n':>3} | "
        f"{'HK':>8} | {'HK_th':>8} | {'ratio':>6} | "
        f"{'CHR':>8} | {'CHR_th':>8} | {'ratio':>6}"
    )

    for r in results:
        print(
            f"{r['n']:>3} | "
            f"{r['hk_mem']/1024:.6f} | {r['hk_theory_mem']/1024:.6f} | {r['hk_mem_ratio']:.6f} | "
            f"{r['chr_mem']/1024:.6f} | {r['ch_theory_mem']/1024:.6f} | {r['ch_mem_ratio']:.6f}"
        )


def print_quality_table(results):

    print("\n" + "="*120)
    print("QUALITY (Christofides)")
    print("="*120)

    print(f"{'n':>3} | {'OPT':>8} | {'CHR':>8} | {'gap %':>8}")

    for r in results:
        print(
            f"{r['n']:>3} | "
            f"{r['opt_cost']:.2f} | "
            f"{r['chr_cost']:.2f} | "
            f"{r['gap_%']:.2f}"
        )


if __name__ == "__main__":

    sizes = list(range(10, 15))

    results = run(sizes)

    print_time_table(results)
    print_memory_table(results)
    print_quality_table(results)