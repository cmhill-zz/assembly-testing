'''
Created on Nov 11, 2013

@author: kzampog
'''

import math
import matplotlib.pyplot as plt

def write_bvs_to_image(cov_dict, over_dict, under_dict, width, height, filename):
    # m rows, n cols
    n = int(math.ceil(math.sqrt((1.0 * len(cov_dict) * width) / height)))
    n = min(n, len(cov_dict))
    m = int(math.ceil((1.0 * len(cov_dict)) / n))
    global_max = max([max(cov_dict[cid]) for cid in cov_dict])
    global_min = min([min(cov_dict[cid]) for cid in cov_dict])
    plot_max = 1.2 * global_max
    plot_min = 0.9 * global_min
    plot_range = plot_max - plot_min
    plt.figure(figsize=(width, height))
    cnt = 1
    for cid in cov_dict:
        plt.subplot(m, n, cnt)
        x = range(len(cov_dict[cid]))
        y1 = cov_dict[cid]
        y2 = 0.5 * plot_range * over_dict[cid] + plot_min
        y3 = plot_range * (1 - 0.5 * under_dict[cid]) + plot_min
        plt.plot(x, y1, x, y2, x, y3)
        plt.title('Contig ' + cid)
        plt.ylim(plot_min, plot_max)
        cnt += 1
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.10, hspace=None)
    if filename != '':
        plt.savefig(filename)
    else:
        plt.show()
    return

def write_all_images(bp_cov, w_cov, stat, width, height, partial_name):
    write_bvs_to_image(bp_cov.contig_coverage, stat.contig_overcovered_bps, stat.contig_undercovered_bps, width, height, partial_name + '_BP.png')
    write_bvs_to_image(w_cov.contig_coverage, stat.contig_overcovered_windows, stat.contig_undercovered_windows, width, height, partial_name + '_WIN.png')
