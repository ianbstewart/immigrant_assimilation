# Assimilation
A study of immigrant assimilation using both Facebook advertising data and a traditional survey.

## Install
Running the code requires installing packages with `conda`.
We need Python2.7 for `PySocialWatcher` until it gets upgraded to Python3+ (TBD).

```
conda create -n assimilation_py27 python=2.7 anaconda
conda install -r requirements.txt
```

## Running code

Before running code, the environment should be activated:

```
conda activate assimilation_py27
```

All code should be run from the base directory, e.g.:

```
python example_mine.py
```

To deactivate the environment after running code:

```
deactivate
```

## Relevant papers
- Measuring immigrant assimilation on Facebook: https://arxiv.org/pdf/1801.09430.pdf
- Social ties of immigrant communities: https://research.fb.com/wp-content/uploads/2016/11/the-social-ties-of-immigrant-communities-in-the-united-states.pdf
- Monitoring migrant stock: http://www.zagheni.net/uploads/3/4/4/7/34477700/zagheni_weber_gummadi_2017_accepted_version.pdf

## Resources

- American FactFinder (census data; American Community Survey estimates): https://factfinder.census.gov/
- Pew Hispanic (census data): http://www.pewhispanic.org/2017/05/03/facts-on-u-s-immigrants-current-data/

## Progress to date

- Activated and tested access token (src/data_processing/example_mine.py).
- Mined audience counts for Hispanic people across languages (Spanish/Bilingual/English), age groups (young, middle-aged, old) and states, including the full Hispanic count and only Ex-pats from Mexico (src/data_processing/mine_multiple_locations.py).
- Compared the Ex-pat estimates with ground-truth census data (src/data_processing/compare_facebook_survey_estimates.ipynb).
- Compared the relative audience sizes of different age/language groups and found that younger Hispanic Facebook users (13-28) tended to be more bilingual and use less Spanish than older Hispanic users (28+). (src/data_processing/compare_young_old_lang_use.ipynb).
- Computed correlation in interest percentages and found that Hispanic Ex-pats from Mexico are closer to American interests than to Mexican interests (src/data_processing/compare_facebook_survey_estimates.ipynb): metrics include Pearson's correlation, paired t-test, and KL divergence.

## TODO

- Figure out MPI policy on funding for survey deployment.
- Assess Turk Prime as a platform for survey deployment (alternative to Facebook, in case of funding problems): how much representation of Hispanic people?
- Filter interests to pick out those most likely to be related to assimilation (e.g. music).