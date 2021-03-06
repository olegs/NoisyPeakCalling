import numpy as np
from matplotlib import pyplot as plt
from project_structure import fdr_05_path, fdr_e6_path
from jbr_gb_data import AlgorithmsStats
from peaks_dynamics import full_peak_dynamics, peak_dynamics


alg_s = AlgorithmsStats()
histones = ["h3k4me1", "h3k4me3", "h3k27ac", "h3k27me3", "h3k36me3"]
fdrs = ["FDR 1E-6", "FDR 0.05"]
algorithms = ["macs2", "sicer", "span"]
alg_colors = ["b", "r", "g"]


def plot_peaks_dynamics(path_dict, ind, fdr):
    # draw plot of changing number of peaks and average peak length
    ns = np.zeros((len(histones) * len(algorithms) * len(ind),))
    means = np.zeros((len(histones) * len(algorithms) * len(ind),))
    idx = 0
    for h in histones:
        for [folder, file_end] in path_dict[h]:
            n, m = peak_dynamics(folder, file_end, ind)
            ns[idx:idx + len(ind)] = n
            means[idx:idx + len(ind)] = m
            idx += len(ind)

    def dynamic_plot(values, title, title_to_save, ylim):
        x = np.asarray([i * 0.25 for i in range(len(ind))])
        plt.figure(figsize=(10, 5))
        plt.ylim([0, ylim])
        for i in range(
                0, len(histones) * len(algorithms) * len(ind), len(algorithms) * len(ind)
        ):
            for j in range(len(algorithms)):
                plt.bar(
                    x,
                    values[i + j * len(ind): i + (j + 1) * len(ind)],
                    width=0.25,
                    color=alg_colors[j],
                )
                x += 0.25 * len(ind)
            x += 0.5

        plt.legend(algorithms)
        plt.xticks(
            [2.5, 8.25, 14, 19.75, 25.5],
            ["h3k4me1", "h3k4me3", "h3k27ac", "h3k27me3", "h3k36me3"],
            fontsize=15,
        )
        plt.title(f"{title}; {fdr}")
        plt.savefig(f"../result/{title_to_save}_fdr_{fdr}.png")
        plt.show()

    dynamic_plot(ns, 'Number of peaks', 'n_peaks', 130000)
    dynamic_plot(means, 'Average peak length', 'len_peaks', 14000)


def plot_true_peaks_comparison():
    # draw plot of changing percentage of true peaks in algorithms output
    plt.figure(figsize=(17, 12))
    i = 1
    subplot_grid = 230
    for h in histones:
        plt.subplot(subplot_grid + i)
        i += 1
        if i == 3:
            i += 1

        for alg, c in zip(algorithms, alg_colors):
            for fdr, linestyle in zip(fdrs, ["--", "-"]):
                plt.plot(
                    [i * 10 for i in range(10)],
                    alg_s.pc_stability_data[fdr][alg][h],
                    linestyle=linestyle,
                    c=c,
                )
            if alg == algorithms[0]:
                plt.legend(fdrs)

        plt.title(f"{h}", fontsize=20)
        plt.ylabel("percentage of true peaks", fontsize=15)
        plt.xlabel("percentage of noise", fontsize=15)
    plt.savefig("../result/true_peaks_dynamics.png")


def plot_peak_set_comparison(fdr):
    # compare the set of peaks from different algorithms
    plt.figure(figsize=(20, 12))
    n = 2
    subplot_grid = 230
    for h in histones:
        plt.subplot(subplot_grid + n)
        n += 1
        x = 0
        leg = []
        i = 0

        for pc in algorithms:
            others = algorithms.copy()
            others.remove(pc)
            for other in others:
                sim = AlgorithmsStats().get_pc_histone_similarity([pc, other], fdr, h)
                plt.bar([x], sim[0], width=0.2, color="g")
                plt.bar([x + 0.2], sim[1], width=0.2, color="r")
                x += 0.5
                leg.append(other)
            i += 1
            x += 0.5

        plt.xticks([0, 0.625, 1.5, 2.125, 3, 3.625], leg, size=15)
        plt.title(f"{h}", size=20)
        plt.ylabel("percentage of peaks", size=15)
    plt.savefig(f"../result/plot_peak_set_comparison_fdr_{fdr}.png")


if __name__ == "__main__":
    plot_true_peaks_comparison()
    ind = [i for i in range(7)]
    for fdr, path_dict in zip(fdrs, [fdr_e6_path, fdr_05_path]):
        plot_peaks_dynamics(path_dict, ind, fdr)
        plot_peak_set_comparison(fdr)
