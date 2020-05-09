# Corona-Bhavishya

Efforts towards predicting numbers based on lockdown and movement characteristics of masses

## Notes for Jupyter Notebooks

1. The Python file corresponding to a Jupyter Notebook follow the same naming
2. Various flags are used in the Jupyter Notebook (and hence, the Python File) for choosing what models should be run. Check the `# Flags` commented section [here](https://github.com/DivyanshuSaxena/Corona-Bhavishya/blob/master/non_neural_predictions.py#L18).
3. **Committing a Jupyter Notebook**  
Please note that a Jupyter Notebook must be committed after striping its output and metadata, to avoid unnecessary changes to the repo, and to keep it small in size. Use [nbstripout](https://github.com/kynan/nbstripout) for adding a git hook, as follows:  
    * Install `nbstripout` using pip or conda

      ```console
      >>> pip install --upgrade nbstripout
      ```

      or

      ```console
      >>> conda install -c conda-forge nbstripout
      ```

    * Use `nbstripout` for the current repo using:

      ```console
      >>> nbstripout --install
      ```

    For further instructions, check documentation [here](https://github.com/kynan/nbstripout/blob/master/README.rst).

## Parameters

- [X] Time Series Data of district (window)
- [X] Population Density
- [X] Lockdown Level  
    0: No_Lockdown  
    1: Pre-lockdown (Large_Public_Spaces)  
    2: Green_Zone (Essentials_with_public_transports)  
    3: Orange_Zone (Essentials_with_private_transports)  
    4: Red_Zone (Only_Essentials)  
    5: Only_Emergency_services  
- [ ] Parameters of SIR Model

## Todo

- [X] Make data cumulative
- [X] Plot a simple LinearRegression on the data
- [X] Fit a non-linear curve
- [X] Get District wise data for states
- [X] Get data for states and probably, international data as well
- [X] Try Neural Models (RNN, LSTM maybe)
- [ ] Add different parameters data (Multivariate LSTM)
- [ ] Check Loss functions, and use the best fit
- [ ] Multiple models for consequent predictions - subsequent usage of these multiple models
- [ ] Predict for data on India

## Sources

The list of sources for data used for models in the current repo:

1. [Covindia](https://covindia.com/)
2. [COVID-19 Tracker | India](https://github.com/covid19india/api)
