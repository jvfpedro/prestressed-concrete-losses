# prestressed-concrete-losses

This is a study project for the *Civil Engineering* course. The goal of this code is to automate the calculation of prestressed concrete losses in beams, following standard Civil Engineering regulations.

The project assists in the dimensioning and verification of structures by calculating both immediate losses (occurring during prestressing) and time-dependent progressive losses.

## Features
- **Immediate Losses:** calculates losses due to friction, anchorage slip (considering different slip hypotheses), and immediate elastic shortening of concrete.
- **Progressive Losses:** calculates time-dependent losses including concrete shrinkage (considering humidity and notional size) and concrete creep.
- **Relaxation:** calculates the loss due to the relaxation of the prestressing steel.
- **Automated Verification:** outputs the results in kN for quick structural analysis.

## Technologies Used
- Python 3
- Math module (standard library for complex equations and exponential functions)

## File Structure
The project is organized into three main scripts, each handling a specific type of loss:

- **`perdas_imediatas.py`**:
  - Friction losses.
  - Anchorage slip losses.
  - Immediate elastic shortening.
- **`perdas_prog_ret_flu.py`**:
  - Concrete shrinkage (time-dependent).
  - Concrete creep (time-dependent).
- **`perdas_prog_relax.py`**:
  - Steel relaxation losses.

## Installation and Setup
1. Ensure you have Python 3 installed on your machine.
2. Clone this repository or download the `.py` files.

## Author

João Vitor Ferreira Pedro
[Civil Engineer - UFSC]
[https://github.com/jvfpedro] [jvfpedro@gmail.com]

Daniel Tavares dos Anjos
[collaborator]
[https://github.com/danieltanjos]
