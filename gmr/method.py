import random
from pathlib import Path

from rich.progress import track

from gmr.model.msa import Msa
from gmr.model.rank import Rank
from gmr.model.taxonomy import Taxonomy
from gmr.util import info, task, exit_error, warn


def assert_msa_of_same_length(user_msa, gtdb_msa):
    user_msa_len = len(user_msa.data[next(iter(user_msa.data))])
    gtdb_msa_len = len(gtdb_msa.data[next(iter(gtdb_msa.data))])
    if user_msa_len != gtdb_msa_len:
        exit_error(f"User MSA and GTDB MSA are not of the same length: {user_msa_len} != {gtdb_msa_len}")


def assert_output_directory_empty(output_dir: Path):
    if output_dir.exists():
        exit_error(f"Output directory already exists: {output_dir}")


def assert_gids_unique(user_msa, gtdb_msa):
    user_msa_gids = set(user_msa.data.keys())
    gtdb_msa_gids = set(gtdb_msa.data.keys())
    if len(user_msa_gids.intersection(gtdb_msa_gids)) > 0:
        exit_error(f"User MSA and GTDB MSA have overlapping genome IDs.")


def assert_gtdb_gids_in_taxonomy(gtdb_msa, gtdb_tax):
    gtdb_msa_gids = set(gtdb_msa.data.keys())
    gtdb_tax_gids = set(gtdb_tax.data.keys())
    if not gtdb_msa_gids.issubset(gtdb_tax_gids):
        exit_error(f"GTDB MSA genome IDs are not a subset of GTDB taxonomy genome IDs.")


def generate_msas(user_msa, gtdb_msa, d_rank_to_gids, dir_out, sample_n):
    combos_seen = set()
    n_skips_sequential = 0
    cur_msa_id = 0

    for _ in track(range(sample_n), description='Generating MSAs...'):

        cur_msa = dict()
        for rank, gids in d_rank_to_gids.items():
            gid = random.choice(gids)
            cur_msa[gid] = gtdb_msa.data[gid]
        gtdb_keys = frozenset(cur_msa.keys())

        # Check if we have already seen this combination
        if gtdb_keys in combos_seen:
            # Check if we're stuck in a loop
            if n_skips_sequential >= 10:
                return cur_msa_id
            n_skips_sequential += 1
            continue
        combos_seen.add(gtdb_keys)

        # Otherwise, write the MSA to disk
        msa_path = dir_out / f'msa_{cur_msa_id}.faa'
        with msa_path.open('w') as f:

            # Write the GTDB sequences
            for gid, seq in cur_msa.items():
                f.write(f'>{gid}\n{seq}\n')

            # Write the user sequences
            for gid, seq in user_msa.data.items():
                f.write(f'>{gid}\n{seq}\n')

        cur_msa_id += 1
        n_skips_sequential = 0

    return cur_msa_id


def run_gmr(
        user_msa: Path,
        gtdb_msa: Path,
        gtdb_tax: Path,
        output_dir: Path,
        rank: Rank,
        sample_n: int,
):
    # Set paths
    out_dir_msa = output_dir / 'msa'

    assert_output_directory_empty(output_dir)
    out_dir_msa.mkdir(parents=True)

    task(f'Reading user MSA from: {user_msa}')
    user_msa_obj = Msa.from_path(user_msa)
    info(f'Found {len(user_msa_obj.data):,} sequences in user MSA.')

    task(f'Reading GTDB MSA from: {gtdb_msa}')
    gtdb_msa_obj = Msa.from_path(gtdb_msa)
    info(f'Found {len(gtdb_msa_obj.data):,} sequences in GTDB MSA.')

    assert_msa_of_same_length(user_msa_obj, gtdb_msa_obj)
    assert_gids_unique(user_msa_obj, gtdb_msa_obj)

    task(f'Reading GTDB taxonomy from: {gtdb_tax}')
    gtdb_tax_obj = Taxonomy.from_path(gtdb_tax)
    info(f'Found {len(gtdb_tax_obj.data):,} genomes in the GTDB taxonomy taxonomy file.')

    assert_gtdb_gids_in_taxonomy(gtdb_msa_obj, gtdb_tax_obj)

    task(f'Obtaining genomes that belong to each {rank}.')
    d_rank_to_gids = gtdb_tax_obj.get_rank_to_gids(rank, gtdb_msa_obj.gids())
    info(f'Found {len(d_rank_to_gids):,} {rank.to_plural()} in the GTDB taxonomy that exist in the GTDB MSA.')

    task(f'Generating at most {sample_n:,} unique MSAs by randomly sampling one genome per {rank}.')
    n_msa_generated = generate_msas(user_msa_obj, gtdb_msa_obj, d_rank_to_gids, out_dir_msa, sample_n)
    if n_msa_generated < sample_n:
        warn(f"Unable to find any unique combinations after 10 attempts, exiting early.")
    info(f'Wrote {n_msa_generated:,} unique MSAs to: {out_dir_msa}/msa_[ID].faa')

    return
