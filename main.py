"""
A special thank you to Qingyi (Freda) Song Drechsler whose code on WRDS served
as the base of this implementation.
And to Theis Ingerslev Jensen, Bryan Kelly, and Lasse Heje Pedersen whose
"Is There A Replication Crisis in Finance?" appendix contained many
useful definitions which are employed here.
"""

# Import the necessary libraries.
import time
from process_data import process_data
from replicate_fama_french import replicate_fama_french


def main():
    """
    This script processes the raw WRDS data and replicates the Fama-French
    factors.
    """

    # Track the overall execution time.
    start_time = time.time()

    # Process the data.
    process_data()
    print("Processed Data.")

    # Replicate the Fama-French factors.
    replicate_fama_french()
    print("Replicated Fama-French Factors.")

    # Print total execution time.
    elapsed_time = time.time() - start_time
    print(f"Total time elapsed is {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    main()
