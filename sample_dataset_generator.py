import csv
import random
from pathlib import Path

from datasets import load_dataset


def sample_prompts(dataset_name, seed, sample_size,split, field_name):
    ds = load_dataset(dataset_name, split=split)

    rng = random.Random(seed)
    indices = list(range(len(ds)))
    rng.shuffle(indices)

    selected_indices = indices[:sample_size]
    sampled_prompts = [ds[i][field_name] for i in selected_indices]

    return sampled_prompts

if __name__ == "__main__":
    dataset_name   = "euclaise/writingprompts"
    split          = "train"
    field_name  = "prompt"
    sample_size      = 50
    seed           = 12345
    output_csv_file_path     = Path("datasets/sample_prompts.csv")

    sampled_prompts = sample_prompts(dataset_name, seed, sample_size,split, field_name)

    with output_csv_file_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["prompt_id", "prompt_text"])
        # Add an index for traceability in later usage
        for i, txt in enumerate(sampled_prompts, start=1):
            writer.writerow([i, txt])