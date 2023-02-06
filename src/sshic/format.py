import pandas as pd
import sshic.tools as tl


def run(
        fragments_list_path: str,
        oligos_capture_path: str,
        output_path: str
):

    """
    This function aims at formatting and creating a correspondence between each probe (oligo capture) and
    the fragments aka the read that contains it.
    Complementary information are given such as chromosomes of the probe (basically the same as the fragment),
    the position on the chromosome of the fragment and the probe, and the type (ss, ds, ds_neg etc ..) of the probe

    The resulting dataframe is written in a tsv file, in the same location of that of the fragments_list.txt

    ARGUMENTS
    _______________________
    fragments_list_path : str
        path to the digested fragments list based on a restriction enzyme or a fixed chunk size.
    oligos_capture_path : str
        path to the file containing the oligo-nucleotides capture information
    output_path : str
        desired output_path to save the file
    """

    df_fragments = pd.read_csv(fragments_list_path, sep='\t')
    df_oligos = pd.read_csv(oligos_capture_path, sep=",")
    df_probes_in_frag = pd.DataFrame()
    df_probes_in_frag.index = ['type', 'probe_start', 'probe_end', 'chr', 'frag_id', 'frag_start', 'frag_end']

    for index, row in df_oligos.iterrows():
        chrom, probe_start, probe_end, probe_type, probe, probe_seq = row
        sub_df_fragments = df_fragments[df_fragments['chrom'] == chrom]
        oligo_middle = int(probe_start + (probe_end-probe_start)/2)
        nearest_frag_start = tl.find_nearest(
            array=sub_df_fragments['start_pos'], key=oligo_middle, mode='lower'
        )
        frag_id = sub_df_fragments.index[sub_df_fragments['start_pos'] == nearest_frag_start].tolist()[0]
        frag_start = sub_df_fragments.loc[frag_id, 'start_pos']
        frag_end = sub_df_fragments.loc[frag_id, 'end_pos']
        df_probes_in_frag[probe] = [probe_type, probe_start, probe_end, chrom, frag_id, frag_start, frag_end]

    df_probes_in_frag = df_probes_in_frag.T
    df_probes_in_frag.to_csv(output_path, sep='\t', index_label='probe')
