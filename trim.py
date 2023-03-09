def sliding_window(phred, cutoff, b, e):
    phredo = phred[::-1]
    l_b = 0
    l_e = 0
    for x in range(len(phred)-2):
        tot_beg = ord(phred[x]) + ord(phred[x+1]) + ord(phred[x+2]) - 99
        tot_eind = ord(phredo[x]) + ord(phredo[x+1]) + ord(phredo[x+2]) - 99
        if tot_beg / 3 < cutoff:
            l_b += 1
        elif tot_beg / 3 > cutoff:
            b = False
        if tot_eind / 3 < cutoff:
            l_e += 1
        elif tot_eind / 3 > cutoff:
            e = False
        if not b and not e:
            break
    return [l_b, l_e]


def trimmen(input1, input2, output1, output2):
    with open(input1) as file1, open(input2) as file2, open(output1, "w") as uitvoer1, open(output2, "w") as uitvoer2:
        for header1, seq1, fr1, phred1, header2, seq2, fr2, phred2 in zip(file1, file1, file1, file1, file2, file2, file2, file2):
            res1 = sliding_window(phred1.strip(), cutoff=35, b=True, e=True)
            res2 = sliding_window(phred2.strip(), cutoff=35, b=True, e=True)
            if len(seq1[res1[0]:len(seq1)-res1[1]-1]) > 30 and len(seq2[res2[0]:len(seq2)-res2[1]-1]) > 30:
                uitvoer1.write(f"{header1}{seq1[res1[0]:len(seq1)-res1[1]-1]}\n{fr1}{phred1[res1[0]:len(seq1)-res1[1]-1]}\n")
                uitvoer2.write(f"{header2}{seq2[res2[0]:len(seq2)-res2[1]-1]}\n{fr2}{phred2[res2[0]:len(seq2)-res2[1]-1]}\n")
trimmen(snakemake.input.file1, snakemake.input.file2, snakemake.output.output1, snakemake.output.output2)
