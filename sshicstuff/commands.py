from docopt import docopt

import sshicstuff.subsample as sshcs
import sshicstuff.genomaker as sshcg
import sshicstuff.filter as sshcf
import sshicstuff.version as sshcv
import sshicstuff.associate as sshca


class AbstractCommand:
    """Base class for the commands"""

    def __init__(self, command_args, global_args):
        """
        Initialize the commands.

        :param command_args: arguments of the command
        :param global_args: arguments of the program
        """
        self.args = docopt(self.__doc__, argv=command_args)
        self.global_args = global_args

    def execute(self):
        """Execute the commands"""
        raise NotImplementedError


class Subsample(AbstractCommand):
    """
    Subsample and compress FASTQ file using seqtk.

    usage:
        subsample [-s SEED] [-z SIZE] [-c] [-F] <input>

    arguments:
        <input>                   Input FASTQ or FASTQ.gz file

    options:
        -s SEED, --seed SEED      Seed for the random number generator [default: 100]
        -z SIZE, --size SIZE      Number of reads to subsample [default: 4000000]
        -c, --compress            Compress the output file with gzip [default: True]
        -F, --force               Force the overwriting of the output file if the file exists [default: False]
    """
    def execute(self):
        sshcs.subsample(
            self.args["<input>"],
            seed=int(self.args["--seed"]),
            size=int(self.args["--size"]),
            compress=self.args["--compress"]

        )


class Genomaker(AbstractCommand):
    """
    Create a chromosome artificial that is the concatenation of the annealing oligos and the enzyme sequence.
    You can specify the rules for the concatenation.

    usage:
        genomaker [-f FRAGMENT_SIZE] [-s SPACER] [-l LINE_LENGTH] <annealing_input> <genome_input> <enzyme>

    arguments:
        <annealing_input>         Path to the annealing oligo positions CSV file
        <genome_input>            Path to the genome FASTA file
        <enzyme>                  Sequence of the enzyme

    options:
        -f FRAGMENT_SIZE, --fragment-size FRAGMENT_SIZE     Size of the fragments [default: 150]
        -s SPACER, --spacer SPACER                          Spacer sequence [default: N]
        -l LINE_LENGTH, --line-length LINE_LENGTH           Length of the lines in the FASTA file [default: 60]
    """

    def execute(self):
        sshcg.insert_artifical_chr(
            self.args["<annealing_input>"],
            self.args["<genome_input>"],
            self.args["<enzyme>"],
            fragment_size=int(self.args["--fragment-size"]),
            fasta_spacer=self.args["--spacer"],
            fasta_line_length=int(self.args["--line-length"])
        )


class Associate(AbstractCommand):
    """
    Simple and basic script to find and associate for each oligo/probe name
    a fragment id from the fragment list generated by hicstuff.

    usage:
        associate <oligos_capture_input> <fragments_input> [-s SHIFT] [-F]

    Arguments:
        <oligos_capture_input>              Path to the oligos capture file
        <fragments_input>                   Path to the fragments file

    Options:
        -s SHIFT, --shift SHIFT             Shift the fragment id by this value [default: 0]
        -F, --force                         Force the overwriting of the oligos file even if
                                            the columns are already present [default: True]
    """

    def execute(self):
        sshca.associate_oligo_to_frag(
            oligos_capture_path=self.args["<oligos_capture_input>"],
            fragments_path=self.args["<fragments_input>"],
            frag_id_shift=int(self.args["--shift"]),
            force=self.args["--force"]
        )


class Hiconly(AbstractCommand):
    """
    Filter the sparse matrix by removing all the ss DNA specific contacts.
    Retain only the contacts between non-ss DNA fragments.

    usage:
        hiconly <sparse_matrix_input> <oligos_capture_input> [-o OUTPUT] [-n FLANKING-NUMBER]

    Arguments:
        <sparse_matrix_input>                           Path to the sparse matrix file
        <oligos_capture_input>                          Path to the oligos capture file

    Options:
        -o OUTPUT, --output OUTPUT                      Path to the output file
        -n FLANKING-NUMBER, --flanking-number NUMBER    number of flanking fragment around the fragment containing the
                                                        oligo to consider and remove
        -F, --force                                     Force the overwriting of the oligos file
                                                        if the file exists [default: False]
    """
    def execute(self):
        sshcf.onlyhic(
            sample_sparse_mat=self.args["<sparse_matrix_input>"],
            oligos_capture_path=self.args["<oligos_capture_input>"],
            output_path=self.args["--output"],
            n_flanking_fragment=int(self.args["--flanking"])
        )


class Filter(AbstractCommand):
    pass


class Coverage(AbstractCommand):
    pass


class Profile(AbstractCommand):
    pass


class Rebin(AbstractCommand):
    pass


class Stats(AbstractCommand):
    pass


class Compare(AbstractCommand):
    pass


class Aggregate(AbstractCommand):
    pass


class Pipeline(AbstractCommand):
    pass




