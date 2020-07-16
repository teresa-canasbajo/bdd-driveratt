import sys


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print()


def normalize(coord, width, height):
    x = coord[0] / width
    y = coord[1] / height
    return (x, y)


def intersection(L1, L2):
    xdiff = (L1[0][0] - L1[1][0], L2[0][0] - L2[1][0])
    ydiff = (L1[0][1] - L1[1][1], L2[0][1] - L2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div != 0:
        d = (det(*L1), det(*L2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return int(x), int(y)
    else:
        return False


def midpoint(lst):
    side = sum(lst) / len(lst) if not len(lst) % 2 else lst[int(len(lst) / 2)]
    return side
