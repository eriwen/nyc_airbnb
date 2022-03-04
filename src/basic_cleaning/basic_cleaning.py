#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import os
import pandas as pd
import wandb

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading artifact")
    raw_input_file = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(raw_input_file)

    logger.info("Filtering data by price range")
    df = df[(df.price >= args.min_price) & (df.price <= args.max_price)]

    df.to_csv(args.output_artifact, index=False)

    logger.info("Logging artifact")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

    os.remove(args.output_artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This step cleans the data")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )
    parser.add_argument(
        "--output_artifact", type=str, help="The name for the output artifact", required=True
    )
    parser.add_argument(
        "--output_type", type=str, help="The type for the output artifact", required=True
    )
    parser.add_argument(
        "--output_description",
        type=str,
        help="A description for the output artifact",
        required=True,
    )
    parser.add_argument(
        "--min_price",
        type=int,
        help="The minimum price to consider",
        required=True,
    )
    parser.add_argument(
        "--max_price",
        type=int,
        help="The maximum price to consider",
        required=True,
    )

    args = parser.parse_args()

    go(args)
