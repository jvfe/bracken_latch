import subprocess
from pathlib import Path
from typing import List

from latch import large_task, map_task, small_task, workflow
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchDir, LatchFile

from .docs import wf_docs
from .wf_types import BrackenSample, ClassificationLevel, ReadLength, Sample


@small_task
def create_bracken_inputs(
    samples: List[Sample],
    kraken_database: LatchDir,
    read_length: ReadLength,
    classification_level: ClassificationLevel,
    threshold: int,
) -> List[BrackenSample]:
    return [
        BrackenSample(
            sample_name=sample.name,
            data=sample.data,
            database=kraken_database,
            read_length=read_length.value,
            classification_level=classification_level.value,
            threshold=threshold,
        )
        for sample in samples
    ]


@large_task
def run_bracken(sample: BrackenSample) -> LatchFile:

    sample_name = sample.name

    output_name = f"{sample_name}_bracken.tsv"
    output_path = Path(output_name).resolve()

    remote_output = f"{sample_name}/{output_name}"

    _bracken_cmd = [
        "/root/Bracken-2.8/bracken",
        "-d",
        sample.database.local_path,
        "-i",
        sample.data.local_path,
        "-o",
        str(output_path),
        "-r",
        sample.read_length,
        "-l",
        sample.classification_level,
        "-t",
        str(sample.threshold),
    ]

    subprocess.run(_bracken_cmd, check=True)

    return LatchFile(str(output_path), f"latch:///bracken/{remote_output}")


@workflow(wf_docs)
def bracken(
    samples: List[Sample],
    kraken_database: LatchDir,
    read_length: ReadLength = ReadLength._100,
    classification_level: ClassificationLevel = ClassificationLevel.S,
    threshold: int = 10,
) -> List[LatchFile]:
    """Bayesian Reestimation of Abundance with Kraken

    Bracken
    ------

     Bracken[^1] (Bayesian Reestimation of Abundance with KrakEN) is a highly accurate
     statistical method that computes the abundance of species in DNA sequences from
     a metagenomics sample. Braken uses the taxonomy labels assigned by Kraken, a
     highly accurate metagenomics classification algorithm, to estimate the number
     of reads originating from each species present in a sample.

    [^1]: Lu J, Breitwieser FP, Thielen P, Salzberg SL. (2017)
    Bracken: estimating species abundance in metagenomics data.
    PeerJ Computer Science 3:e104, https://doi.org/10.7717/peerj-cs.104
    """

    bracken_inputs = create_bracken_inputs(
        samples=samples,
        kraken_database=kraken_database,
        read_length=read_length,
        classification_level=classification_level,
        threshold=threshold,
    )

    return map_task(run_bracken)(sample=bracken_inputs)


LaunchPlan(
    bracken,
    "Shotgun metagenomics data",
    {
        "samples": [
            Sample(
                name="SRR579291",
                data=LatchFile("s3://latch-public/test-data/4318/SRR579291.tsv"),
            ),
            Sample(
                name="SRR579292",
                data=LatchFile("s3://latch-public/test-data/4318/SRR579292.tsv"),
            ),
        ],
        "kraken_database": LatchDir(
            "s3://latch-public/test-data/4318/standard_kraken_db/"
        ),
    },
)
