import logging
import unittest

from knowseq.classifiers import knn
from knowseq.utils import csv_to_dataframe, csv_to_list
from knowseq.utils.plotting import plot_samples_heatmap, plot_confusion_matrix, plot_boxplot


class KnnClassifierTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(module)s - %(message)s")

    def test_kenn_classifier(self):
        golden_degs_df = csv_to_dataframe(path_components=["../test_fixtures", "golden", "degs_matrix_breast.csv"],
                                          index_col=0, header=0).transpose()

        quality_labels = csv_to_dataframe(path_components=["../test_fixtures", "golden", "qa_labels_breast.csv"],
                                          header=None).iloc[:, 0]

        fs_ranking = csv_to_list(path_components=["../test_fixtures", "golden", "fs_ranking_mrmr_breast.csv"])
        fs_ranking_list = [row[0] for row in fs_ranking if row]

        knn_res = knn(golden_degs_df, quality_labels, fs_ranking_list)

        plot_boxplot(golden_degs_df, quality_labels, fs_ranking_list, top_n_features=3)
        plot_confusion_matrix(knn_res["confusion_matrix"], unique_labels=knn_res["unique_labels"].tolist())
        plot_samples_heatmap(golden_degs_df, quality_labels, fs_ranking_list, top_n_features=4)

        # TODO: assert


if __name__ == '__main__':
    unittest.main()