# phase_load_normalizer

The program is designed to equalize **single-phase** loads and calculate the asymmetry of single-phase loads in a three-phase supply network.

---
### How to use
1. Type or paste a list of single-phase loads from the clipboard.
2. Type or paste from the clipboard a list of three-phase loads, if necessary.
3. Press the button.
4. Easy peasy.
 
* Decimal separator - *dot*.
* The separator between values - *space*.

**Requires an installed xlsxwriter library.**


#### General operating principle
At the first stage, the next value from the sorted list of single-phase loads is placed on the least loaded phase. The second stage is an attempt to minimize the unevenness of the load by swapping the loads between adjacent phases.

#### Saving report
If you can't save the report, check the existence of the _reports_ folder, as well as the access permissions to it.
