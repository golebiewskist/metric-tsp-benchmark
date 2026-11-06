class CalibratedTheory:

    def __init__(self, hk_ref, ch_ref):

        hk_n, hk_time, hk_mem = hk_ref

        self.hk_c_time = hk_time / (hk_n**2 * (2**hk_n))
        self.hk_c_mem = hk_mem / (hk_n * (2**hk_n))

        ch_n, ch_time, ch_mem = ch_ref

        self.ch_c_time = ch_time / (ch_n**3)
        self.ch_c_mem = ch_mem / (ch_n**2)

    def hk_time(self, n):
        return self.hk_c_time * (n**2) * (2**n)

    def hk_mem(self, n):
        return self.hk_c_mem * n * (2**n)

    def ch_time(self, n):
        return self.ch_c_time * (n**3)

    def ch_mem(self, n):
        return self.ch_c_mem * (n**2)

    def enrich(self, results):

        out = []

        for r in results:
            n = r["n"]

            hk_t = self.hk_time(n)
            hk_m = self.hk_mem(n)

            ch_t = self.ch_time(n)
            ch_m = self.ch_mem(n)

            out.append({
                **r,

                "hk_theory_time": hk_t,
                "hk_theory_mem": hk_m,
                "hk_time_ratio": r["hk_time"] / hk_t,
                "hk_mem_ratio": r["hk_mem"] / hk_m,

                "ch_theory_time": ch_t,
                "ch_theory_mem": ch_m,
                "ch_time_ratio": r["chr_time"] / ch_t,
                "ch_mem_ratio": r["chr_mem"] / ch_m,
            })

        return out