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
    actual_start_time = time.time()

    # Process data.
    start_time = time.time()
    process_data()
    end_time = time.time()
    print("Processed data.")
    print("Time Elapsed: ", end_time - start_time)

    # Replicate the Fama-French factors.
    start_time = time.time()
    replicate_fama_french()
    end_time = time.time()
    print("Replicated Fama-French.")
    print("Time Elapsed: ", end_time - start_time)

    # Print total execution time.
    actual_end_time = time.time()
    print("Total Time Elapsed: ", actual_end_time - actual_start_time)


if __name__ == "__main__":
    main()
