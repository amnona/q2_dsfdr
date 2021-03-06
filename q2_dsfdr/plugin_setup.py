import qiime2.plugin
from qiime2.plugin import (SemanticType, Str, Int, Float, Choices,
                          MetadataCategory, Plugin)
from q2_types.feature_table import (
    FeatureTable, Frequency)
from q2_types.sample_data import AlphaDiversity, SampleData
from dsfdr.dsfdr import dsfdr
import pandas as pd

_citation = ('Jiang L, Amir A, Morton JT, Heller R, Arias-Castro E, Knight R. 2017. '
             'Discrete False-Discovery Rate Improves Identification of Differentially Abundant Microbes'
             'mSystems.00092-17 '
             'https://doi.org/10.1128/mSystems.00092-17')

_short_description = "Plugin for multiple comparisons in sparse Microbiome Data"

plugin = qiime2.plugin.Plugin(
    name='dsfdr',
    version="0.0.1",
    website='https://github.com/serenejiang/q2_dsfdr',
    package='q2_dsfdr',
    short_description=_short_description,
    description=('This is a QIIME 2 plugin supporting multiple comparisons on sparse microbiome feature tables and metadata'),
    citation_text=_citation
)


def permutation_fdr(table : pd.DataFrame,
                    metadata: qiime2.MetadataCategory,
                    statistical_test: str = 'meandiff',
                    transform_function: str = 'rank',
                    alpha: float = 0.05,
                    permutations: int=1000) -> pd.Series:

        metadata_series = metadata.to_series()[table.index]
        ret_reject, ret_tstat, ret_pvals = dsfdr(table.values.T,
			   metadata_series.values,
               transform_function,
               statistical_test,
			   alpha, permutations)
        return pd.Series(ret_reject, index=table.columns)


_statistical_tests = ['meandiff', 'mannwhiteny', 'kruwallis', 'stdmeandiff',
                      'spearman', 'pearson', 'nonzerospearman', 'nonzeropearson']

_transform_functions = ['rank', 'log', 'pa', 'norm']


plugin.methods.register_function(
    function=permutation_fdr,
    inputs={'table': FeatureTable[Frequency]},
    outputs=[('reject', SampleData[AlphaDiversity])],
    parameters={
        'metadata': MetadataCategory,
        'statistical_test': Str % Choices(_statistical_tests),
        'transform_function': Str % Choices(_transform_functions),
        'permutations': Int,
        'alpha': Float,
    },
    name='Discrete FDR',
    description=("Discrete FDR")
)
