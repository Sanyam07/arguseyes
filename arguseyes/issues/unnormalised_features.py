import numpy as np

from arguseyes.issues._issue import IssueDetector, Issue


class UnnormalisedFeatures(IssueDetector):

    def _detect(self, pipeline) -> Issue:
        X_train = pipeline.X_train
        _, num_columns = X_train.shape

        unnormalised_feature_found = False
        non_binary_features = []
        non_zero_mean_features = []
        non_unit_variance_features = []

        for column_index in range(0, num_columns):
            column = X_train[:, column_index]
            if not self._is_binary(column):
                non_binary_features.append(column_index)
                if not self._has_zero_mean(column):
                    non_zero_mean_features.append(column_index)
                    unnormalised_feature_found = True
                if not self._has_unit_variance(column):
                    non_unit_variance_features.append(column_index)
                    unnormalised_feature_found = True

        issue_details = {
            'non_binary_features': non_binary_features,
            'non_zero_mean_features': non_zero_mean_features,
            'non_unit_variance_features': non_unit_variance_features
        }

        return Issue('unnormalised_features', unnormalised_feature_found, issue_details)

    @staticmethod
    def _is_binary(column):
        unique_values = np.unique(column)
        return len(unique_values) == 2 and 0.0 in unique_values and 1.0 in unique_values

    @staticmethod
    def _has_zero_mean(column):
        return np.isclose(np.mean(column), 0.0)

    @staticmethod
    def _has_unit_variance(column):
        return np.isclose(np.var(column), 1.0)
