import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)


# TODO ask if we only use x$counts, since I only implemented that part
# TODO: change labels type (should not be str but a vector of strings)
# TODO: parallel reading? concurrent.futures
def read_dge(count_files: pd.Series, path: str = None, labels: str = None):
    """
    Reads and merges a set of text files containing gene expression counts.

    Args:
        count_files: Pandas Series of filenames that contain sample information.
        path: String giving the directory containing the files. Set to None by default (current working directory).
        labels: Names to associate with the files. Set to None by default (file names).

    Returns:
        Pandas Dataframe, containing a row for each unique tag found in the input files and a column for each
        input file.

    Raises:
        Exception: If row names are not unique within the row-names.
    """

    # Assign path and labels if given
    samples_data_list = [os.path.join(path, str(file)) for file in count_files] if path else count_files
    samples_data = pd.Series(samples_data_list)

    samples_labels = labels if labels else count_files.apply(lambda file: str(file).split(".")[0])
    samples = pd.DataFrame(samples_data.array, index=samples_labels, columns=["files"])

    # TODO: improve performance
    # Collate counts for unique tags
    counts = pd.DataFrame()
    for sample in samples["files"]:
        file_name = os.path.basename(sample)
        file_data = pd.read_csv(sample, sep=r"\t", index_col=0, names=(file_name,), engine="python", dtype="Int64")
        if file_data.index.has_duplicates:
            raise Exception("There are duplicated row names in files param. Row names must be unique.")
        counts = counts.join(file_data, how="outer")

    counts = counts.fillna(0)  # TODO: find a way of replacing NaN while joining

    # Alert user if htseq-style meta genes found
    meta_tags = counts[counts.index.str.startswith("_")].index
    if len(meta_tags):
        logging.info(f"Meta tags detected: {meta_tags.values}")

    return counts
