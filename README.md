# EPLANoptML

Machine learning as a surrogate model for EnergyPLAN and EPLANopt: https://doi.org/10.1016/j.energy.2024.132735
EPLANoptML is an innovative approach that integrates machine learning algorithms with EnergyPLAN and EPLANopt to accelerate energy system optimization at the country level. This model significantly reduces computational time while maintaining high accuracy, enabling more comprehensive exploration of uncertainties in energy system modeling.

## Features

- Integration of machine learning with EnergyPLAN and EPLANopt
- Significant reduction in computational time (64-74% faster than traditional EPLANopt)
- Maintains high accuracy (>99%) in predicting EnergyPLAN outputs
- Enables deeper exploration of energy system uncertainties
- Applicable to national-scale energy system modeling
- Preserves high temporal resolution and extensive sector-coupling

## Requirements

- EnergyPLAN version >=15.1 (Download from [EnergyPLAN website](https://www.energyplan.eu/))
- Python 3.x

## How to Use

Please look at [EPLANopt](https://github.com/matpri/EPLANopt) for more details on how to use this code.

## Related Repositories

This project builds upon and connects with the following repositories:

- [EPLANoptMAC](https://github.com/matpri/EPLANoptMAC): Creates Marginal Abatement Cost (MAC) curves based on EnergyPLAN
- [EPLANopt](https://github.com/matpri/EPLANopt): Energy system optimization model based on EnergyPLAN

## Results

EPLANoptML demonstrates:
- Optimal machine learning model: Neural Network with 500 hidden nodes
- Training efficiency: 99% accuracy achieved after 10 generations
- Computational time savings: 64-74% compared to traditional EPLANopt
- Accuracy maintenance: Close to that of full EPLANopt runs


## How to Cite EPLANoptML

If you use EPLANoptML in your research, please cite the following paper:

Prina MG, Dallapiccola M, Moser D, Sparber W. Machine learning as a surrogate model for EnergyPLAN: speeding up energy system optimization at the country level. Energy 2024:132735. https://doi.org/10.1016/J.ENERGY.2024.132735

## Contributing

We welcome contributions to EPLANoptML. Please feel free to submit pull requests, create issues or contact the authors for any questions.

## Acknowledgements

This work has received funding from the Horizon 2020 program of the European Union under GA. No. 952957 – Project [TRUST-PV](https://trust-pv.eu/).
