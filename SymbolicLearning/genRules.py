import sys
import pandas as pd

def genRules(input_data):
    with open(input_data, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # Read all lines into a list

        # Iterate through lines and remove lines until 'Rule' is found
        while lines and not lines[0].strip().startswith('Rule'):
            lines.pop(0)  # Remove the first line

        # Find the index of the line containing "Mining done" or "Total time"
        mining_index = None
        for i, line in enumerate(lines):
            if "Mining done" in line:
                mining_index = i
                break

        if mining_index is not None:
            del lines[mining_index:]

    return lines

def save_as_csv(lines, output_filename):
    data = []

    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) > 1:
            first_column_parts = parts[0].split(' => ')
            if len(first_column_parts) > 1:
                data.append(first_column_parts + parts[1:])

    df = pd.DataFrame(data, columns=['Body', 'Head', 'Head Coverage', 'Std Confidence', 'PCA Confidence', 'Positive Examples',
                               'Body size', 'PCA Body size', 'Functional variable'])

    result = df.to_dict('list')
    df.to_csv(output_filename, index=False)
    return result


def main(*args):
    data = args[0]
    out = args[1]
    lines = genRules(data)
    results = save_as_csv(lines, out)
    print(results)


if __name__ == '__main__':
    main(*sys.argv[1:])

