def inlezen_file(input, output):
    line_number = 0
    read_lenghts = []
    read_cg = 0
    cg_pos = dict()
    uitvoer =  open(output, "w")
    with open(input, "r") as fh:
        for line in fh:
            if line_number % 4 == 1:
                line = line.strip("\n")
                read_lenghts.append(len(line.strip("\n")))
                read_cg += (line.count("C") + line.count("G")) / len(line) * 100
                teller = 1
                for base in line:
                    if teller in cg_pos:
                        if base == "C" or base == "G":
                            cg_pos[teller][0]  += 1
                    else:
                        cg_pos[teller] = [0, 0]
                    cg_pos[teller][1] += 1
                    teller += 1
            line_number += 1
    read_lenghts.sort()
    uitvoer.write(f"Aantal reads: {len(read_lenghts)}\n" +
                  f"Gemiddelde lengte read: {sum(read_lenghts) / len(read_lenghts)}\n" +
                  f"Minimumlengte read: {read_lenghts[0]}\n" +
                  f"Maximumlengte read: {read_lenghts[-1]}\n" +
                  f"Gemiddelde GC% reads: {round(read_cg / len(read_lenghts), 2)}%\n" +
                  f"%-12s %-12s\n"% ("Positie", "GC-Percentage"))
    for k, v in cg_pos.items():
        gc = v[0] / v[1] * 100
        uitvoer.write(f"{k:<13}{round(gc, 2):>4.2f}%\n")

inlezen_file(snakemake.input.a, snakemake.output.b)