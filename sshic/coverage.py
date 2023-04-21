import os
import re
import sys
import argparse
import numpy as np
import pandas as pd

#   Set as None to avoid SettingWithCopyWarning
pd.options.mode.chained_assignment = None


def coverage(
    hic_contacts_path: str,
    fragments_path: str,
    output_dir: str,
):

    """
    Calculate the coverage per fragment and save the result to a bedgraph file in the output directory.

    Parameters
    ----------
    hic_contacts_path : str
        Path to the sparse_contacts_input.txt file (generated by hicstuff).
    fragments_path : str
        Path to the fragments_input.txt file (generated by hicstuff).
    output_dir : str
        Path to the output directory.
    """

    sample_filename = hic_contacts_path.split("/")[-1]
    sample_id = re.search(r"AD\d+", sample_filename).group()
    output_path = os.path.join(output_dir, sample_id + f"_coverage_per_fragment.bedgraph")

    df_fragments = pd.read_csv(fragments_path, sep='\t')
    df_fragments.rename(columns={'chrom': 'chr', 'start_pos': 'start', 'end_pos': 'end'}, inplace=True)
    df_fragments['id'] = df_fragments.index.values
    df_hic_contacts = pd.read_csv(hic_contacts_path, header=0, sep="\t", names=['frag_a', 'frag_b', 'contacts'])

    df_coverage = df_fragments[['chr', 'start', 'end']]
    df_coverage['contacts'] = np.nan

    df_merged_a = df_hic_contacts.merge(df_fragments[['id', 'chr', 'start', 'end']],
                                        left_on='frag_a',
                                        right_on='id',
                                        suffixes=('', '_a')).drop(columns=['frag_a', 'frag_b'])

    df_merged_b = df_hic_contacts.merge(df_fragments[['id', 'chr', 'start', 'end']],
                                        left_on='frag_b',
                                        right_on='id',
                                        suffixes=('', '_b')).drop(columns=['frag_a', 'frag_b'])

    df_grouped_a = df_merged_a.groupby(by=['id', 'chr', 'start', 'end'], as_index=False).sum()
    df_grouped_b = df_merged_b.groupby(by=['id', 'chr', 'start', 'end'], as_index=False).sum()

    df_grouped = pd.concat(
        (df_grouped_a, df_grouped_b)).groupby(by=['id', 'chr', 'start', 'end'], as_index=False).sum()

    df_grouped.index = df_grouped.id
    df_grouped.drop(columns=['id'], inplace=True)

    df_grouped.to_csv(output_path, sep='\t', index=False, header=False)


def main(argv=None):
    """
    Main function to parse command-line arguments and execute the coverage function.

    Parameters
    ----------
    argv : Optional[List[str]]
        List of command-line arguments. Default is None.
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print('Please enter arguments correctly')
        exit(0)

    parser = argparse.ArgumentParser(description='Coverage contacts per reads')
    parser.add_argument('-f', '--fragments', type=str, required=True,
                        help='Path to the fragments_input.txt file (generated by hicstuff)')
    parser.add_argument('-c', '--contacts', type=str, required=True,
                        help='Path to the sparse_contacts_input.txt file (generated by hicstuff)')
    parser.add_argument('-o', 'output-dir', type=str, required=True,
                        help='Path to the output directory')
    parser.add_argument('--output-format', type=str, required=True,
                        help='format for the output file coverage (tsv, csv, txt, bedgraph etc ...')

    args = parser.parse_args(argv)

    coverage(
        fragments_path=args.fragments,
        hic_contacts_path=args.contacts,
        output_dir=args.output_dir
    )


if __name__ == "__main__":
    main(sys.argv[1:])
