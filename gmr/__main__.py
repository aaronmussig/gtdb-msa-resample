import sys
from pathlib import Path

import typer
from typing_extensions import Annotated

from gmr import __version__
from gmr.method import run_gmr
from gmr.model.rank import Rank
from gmr.util import info

app = typer.Typer()


@app.command()
def run(
        user_msa: Annotated[Path, typer.Argument(help="MSA that contains the USER genomes aligned to the GTDB MSA.")],
        gtdb_msa: Annotated[Path, typer.Argument(help="MSA that contains the GTDB genomes aligned to the GTDB MSA (e.g: https://data.gtdb.ecogenomic.org/releases/latest/genomic_files_reps/bac120_msa_reps.faa.gz).")],
        gtdb_tax: Annotated[Path, typer.Argument(help="GTDB taxonomy file (e.g: https://data.gtdb.ecogenomic.org/releases/latest/bac120_taxonomy.tsv).")],
        output_dir: Annotated[Path, typer.Argument(help="Output directory.")],  # The path to the output file.
        rank: Annotated[Rank, typer.Argument(help="Rank from which genomes will be sampled from.")],
        sample_n: Annotated[int, typer.Argument(help="Number of unique MSAs to generate.")],
):
    # Output the program version
    info(f'gmr v{__version__}')

    # Run the program
    run_gmr(
        user_msa=user_msa,
        gtdb_msa=gtdb_msa,
        gtdb_tax=gtdb_tax,
        output_dir=output_dir,
        rank=rank,
        sample_n=sample_n,
    )

    # Program finish
    info('Done.')
    sys.exit(0)


if __name__ == "__main__":
    app()
