import sys
from rdflib import Graph


def convert(input_data, output_data):
    g = Graph()
    with open(input_data, 'r', encoding='utf-8') as nt_f:
        g.parse(nt_f, format='nt')

    with open(output_data, 'w', encoding='utf-8') as f:
        # Iterate over triples and write to TSV file
        for s, p, o in g:
            # Skip triples where p contains any of the specified substrings
            if "type" in p or "endDate" in p or "startDate" in p or "hasPosition" in p or "hasHistology" in p or "performanceStatus" in p or "patientToxicity" in p or "toxicity" in p or "toxicityID" in p or "patientDrug" in p:
                continue
            # Replace part of the string with ''
            s = s.replace("http://example.org/lungCancer/entity/", "")
            p = p.replace("http://example.org/lungCancer/vocab/", "").replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#",'')
            o = o.replace("http://example.org/lungCancer/entity/", "").replace("http://example.org/lungCancer/vocab/", "")
            f.write(f"{s}\t{p}\t{o}\n")

    return output_data


def main(*args):
    data = args[0]
    out = args[1]
    convert(data, out)


if __name__ == '__main__':
    main(*sys.argv[1:])


