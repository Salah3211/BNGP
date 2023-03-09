def indel(file, output):
    with open(file, "r") as f, open(output, "w") as output:
        inserties = 0
        deleties = 0
        snips = 0
        dictionary = {}
        for line in f:
            if "#"not in line and line != "\n":
                mutatie = [line.strip("").split("\t")[3], line.strip("").split("\t")[4]]
                len_col1 = len(mutatie[0])
                lijst = [len(mutatie[1])]
                if "," in mutatie[1]:
                    lijst = [len(mutatie[1].split(",")[0]) + len(mutatie[1].split(",")[1])]
                for len_col2 in lijst:
                    if len_col1 < len_col2:
                            inserties += 1
                    elif len_col2 < len_col1:
                            deleties += 1
                    elif len_col1 == 1 and len_col2 == 1:
                            snips += 1
                            basen = mutatie[1].split(",")
                            for base in basen:
                                key = mutatie[0] + " -> " + base
                                if key in dictionary.keys():
                                    dictionary[key] = dictionary[key] + 1
                                else:
                                    dictionary[key] = 1
        output.write(f"Aantal inserties: {inserties}\nAantal deleties: {deleties}\nAantal snips: {snips}\n")
        output.write(f"Verhouding deleties/inserties: {inserties/deleties}\nSNP mutaties\n")
        for key, value in dictionary.items():
            output.write(f"{key}: {value}\n")

indel(snakemake.input.a, snakemake.output.b)

