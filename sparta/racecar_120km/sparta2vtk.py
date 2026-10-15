# Convert SPARTA text dumps (grid + surf) into legacy VTK files for ParaView.
# Usage: python3 sparta2vtk.py grid.2000.dat surf.2000.dat
import sys

GRID_NAMES = ["nrho", "u", "v", "w", "temp", "press"]   # order of c_1[*] c_2[*]
SURF_NAMES = ["press", "etot"]                           # order of c_3[*]


def read_dump(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    box = []
    for i, line in enumerate(lines):
        if line.startswith("ITEM: BOX BOUNDS"):
            box = [[float(x) for x in lines[i + k].split()] for k in (1, 2, 3)]
        if line.startswith("ITEM: CELLS") or line.startswith("ITEM: SURFS"):
            columns = line.split()[2:]
            rows = [[float(x) for x in l.split()] for l in lines[i + 1:] if l.strip()]
            return box, columns, rows


def grid_to_vtk(filename):
    box, columns, rows = read_dump(filename)
    first = columns.index("xc")
    data = [row[first + 3:] for row in rows]
    # cell index from cell centre (sub-cells of split cells share one centre -> averaged)
    centres = [sorted(set(row[first + k] for row in rows)) for k in range(3)]
    nx, ny, nz = len(centres[0]), len(centres[1]), len(centres[2])
    lookup = [{c: i for i, c in enumerate(cs)} for cs in centres]
    ncells = nx * ny * nz
    sums = [[0.0] * len(GRID_NAMES) for _ in range(ncells)]
    counts = [0] * ncells
    for row, values in zip(rows, data):
        i = lookup[0][row[first]]
        j = lookup[1][row[first + 1]]
        k = lookup[2][row[first + 2]]
        n = i + nx * (j + ny * k)
        counts[n] += 1
        for m, value in enumerate(values):
            sums[n][m] += value
    means = [[s / c if c else 0.0 for s in cell] for cell, c in zip(sums, counts)]

    out = filename.replace(".dat", ".vtk")
    with open(out, "w") as f:
        f.write("# vtk DataFile Version 3.0\nSPARTA grid\nASCII\nDATASET RECTILINEAR_GRID\n")
        f.write("DIMENSIONS %d %d %d\n" % (nx + 1, ny + 1, nz + 1))
        for name, (lo, hi), n in zip("XYZ", box, (nx, ny, nz)):
            edges = [lo + (hi - lo) * i / n for i in range(n + 1)]
            f.write("%s_COORDINATES %d float\n" % (name, n + 1))
            f.write(" ".join("%g" % e for e in edges) + "\n")
        f.write("CELL_DATA %d\n" % ncells)
        for m, name in enumerate(GRID_NAMES):
            f.write("SCALARS %s float 1\nLOOKUP_TABLE default\n" % name)
            f.write("\n".join("%g" % cell[m] for cell in means) + "\n")
        f.write("VECTORS U float\n")
        f.write("\n".join("%g %g %g" % (c[1], c[2], c[3]) for c in means) + "\n")
    print("wrote", out, "with", ncells, "cells")


def surf_to_vtk(filename):
    box, columns, rows = read_dump(filename)
    first = columns.index("v1x")
    ntri = len(rows)
    out = filename.replace(".dat", ".vtk")
    with open(out, "w") as f:
        f.write("# vtk DataFile Version 3.0\nSPARTA surf\nASCII\nDATASET POLYDATA\n")
        f.write("POINTS %d float\n" % (3 * ntri))
        for row in rows:
            v = row[first:first + 9]
            f.write("%g %g %g\n%g %g %g\n%g %g %g\n" % tuple(v))
        f.write("POLYGONS %d %d\n" % (ntri, 4 * ntri))
        for t in range(ntri):
            f.write("3 %d %d %d\n" % (3 * t, 3 * t + 1, 3 * t + 2))
        f.write("CELL_DATA %d\n" % ntri)
        for m, name in enumerate(SURF_NAMES):
            f.write("SCALARS %s float 1\nLOOKUP_TABLE default\n" % name)
            f.write("\n".join("%g" % row[first + 9 + m] for row in rows) + "\n")
    print("wrote", out, "with", ntri, "triangles")


grid_to_vtk(sys.argv[1])
surf_to_vtk(sys.argv[2])
