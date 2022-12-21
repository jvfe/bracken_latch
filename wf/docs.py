from latch.types.metadata import (
    LatchAuthor,
    LatchMetadata,
    LatchParameter,
    Params,
    Section,
    Text,
)

PARAMS = {
    "samples": LatchParameter(
        display_name="Bracken samples",
        description="Kraken2 TSV reports",
        batch_table_column=True,
    ),
    "kraken_database": LatchParameter(
        display_name="Kraken2 database",
        description=(
            "The database used for the Kraken2 classification. "
            "Must also contain Bracken database-kmer files"
        ),
    ),
    "read_length": LatchParameter(
        display_name="Read length", description="Ideal length of reads in your sample"
    ),
    "classification_level": LatchParameter(
        display_name="Taxonomic rank",
    ),
    "threshold": LatchParameter(display_name="Minimum read threshold"),
}

FLOW = [
    Section("Samples", Params("samples")),
    Section("Kraken2 options", Params("kraken_database")),
    Section(
        "Bracken options",
        Text(
            "Bracken uses the taxonomy labels assigned by Kraken "
            "to estimate the number of reads originating from each species present "
            "in a sample"
        ),
        Params("read_length"),
        Text(
            "Specifies the taxonomic rank to analyze. "
            "Each classification at this specified rank will receive "
            "an estimated number of reads belonging to that rank after abundance estimation."
        ),
        Params("classification_level"),
        Text(
            "Specifies the minimum number of reads required for a classification "
            "at the specified rank. Any classifications with less than the specified threshold "
            "will not receive additional reads from higher taxonomy levels when distributing reads "
            "for abundance estimation."
        ),
        Params("threshold"),
    ),
]

WORKFLOW_NAME = "bracken"

wf_docs = LatchMetadata(
    display_name=WORKFLOW_NAME.title(),
    documentation=f"https://github.com/jvfe/{WORKFLOW_NAME}_latch/blob/main/README.md",
    author=LatchAuthor(
        name="jvfe",
        github="https://github.com/jvfe",
    ),
    repository=f"https://github.com/jvfe/{WORKFLOW_NAME}_latch",
    license="MIT",
    parameters=PARAMS,
    tags=["NGS", "taxonomy"],
    flow=FLOW,
)
