# Asset Pricing Code Repository

This repository contains all of the code that I've used in my asset pricing papers.

## Aims

My aims in publishing my code to the public are:
- To enable others to replicate my work
- To contribute to making the field of asset pricing more accessible

## Inspiration

In publishing this code, I take inspiration from [Open Asset Pricing](https://www.openassetpricing.com/).

## Acknowledgements

This code is built off of the work of Qingyi (Freda) Song Drechsler, whose code on WRDS served as the base of this implementation, and Theis Ingerslev Jensen, Bryan Kelly, and Lasse Heje Pedersen. Their "Is There A Replication Crisis in Finance?" appendix contained many useful definitions which are employed here.

## Implementation Details

I currently only have access to the class account version of WRDS, so I was unable to use the WRDS API. Instead, I utilized web queries, downloaded the data as CSV files, and then used Python to process all of the data.

## Replication Instructions

To replicate my work:
1. Clone this repository.
2. Follow the instructions in the `data_download_instructions.txt` file to download all of the data.
3. Run the code!

## Contact

Please let me know if you have any questions, comments, or concerns. You can reach me at [aidanvyas@rice.edu](mailto:aidanvyas@rice.edu).
