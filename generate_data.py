"""
Generate a synthetic tabular dataset for crop yield prediction.

Columns: temperature (°C), humidity (%), rainfall (mm per season),
soil_quality (1–10), fertilizer (kg/ha N-equivalent), crop_yield (t/ha).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def generate_crop_yield_data(
    n_samples: int = 5000,
    random_seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(random_seed)

    temperature = rng.uniform(15.0, 38.0, n_samples)
    humidity = rng.uniform(35.0, 95.0, n_samples)
    rainfall = rng.uniform(50.0, 450.0, n_samples)
    soil_quality = rng.uniform(3.0, 10.0, n_samples)
    fertilizer = rng.uniform(0.0, 160.0, n_samples)

    # Nonlinear, agriculture-inspired mapping + Gaussian noise
    temp_opt = 26.0
    temp_term = np.exp(-0.018 * (temperature - temp_opt) ** 2)
    hum_term = np.clip(1.0 - np.abs(humidity - 65.0) / 90.0, 0.2, 1.0)
    rain_opt = 200.0
    rain_term = np.exp(-0.0009 * (rainfall - rain_opt) ** 2)
    fert_diminishing = 0.11 * fertilizer - 0.00035 * fertilizer**2

    crop_yield = (
        10.0
        + 22.0 * temp_term
        + 7.5 * hum_term
        + 14.0 * rain_term
        + 2.1 * soil_quality
        + fert_diminishing
        + rng.normal(0.0, 2.8, n_samples)
    )
    crop_yield = np.clip(crop_yield, 4.0, 85.0)

    return pd.DataFrame(
        {
            "temperature": np.round(temperature, 1),
            "humidity": np.round(humidity, 1),
            "rainfall": np.round(rainfall, 1),
            "soil_quality": np.round(soil_quality, 2),
            "fertilizer": np.round(fertilizer, 1),
            "crop_yield": np.round(crop_yield, 2),
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic crop yield dataset")
    parser.add_argument("-n", "--samples", type=int, default=5000, help="Number of rows")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("dataset.csv"),
        help="Output CSV path",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    df = generate_crop_yield_data(n_samples=args.samples, random_seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Wrote {len(df)} rows to {args.output.resolve()}")


if __name__ == "__main__":
    main()
