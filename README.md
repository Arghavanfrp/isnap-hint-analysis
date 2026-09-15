# Behavioural Analysis of Hint Use in iSnap

This repository contains the reproducible analysis code used for the MSc Data
Science dissertation examining hint use, learner challenge, and session-level
persistence in the iSnap programming learning environment.

## Study overview

The analysis focuses on the `guess1Lab` task in the iSnap Spring 2016 dataset.
Event-level records are aggregated into sessions and sessions with at least one
hint request are compared with sessions containing no hint requests.

The eight outcome measures are:

- number of recorded events;
- aggregated recorded duration;
- run actions;
- block-grab actions;
- block-snap actions;
- input edits;
- recorded error events; and
- category changes.

The analysis is exploratory. These measures are not treated as direct evidence
of learner difficulty, learning success, or long-term retention.

## Data availability

The raw dataset is not included in this repository. It was obtained from
Carnegie Mellon University's DataShop and must be accessed from its original
source subject to the applicable terms of use.

Do not commit the raw dataset or the generated session-level file. Although the
source identifiers are anonymised, the session-level output is excluded as an
additional privacy safeguard.

## Reproducing the analysis

1. Obtain the iSnap Spring 2016 event-log dataset from DataShop.
2. Save the tab-separated export locally.
3. Create a Python environment and install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run the analysis, passing the location of the dataset explicitly:

   ```bash
   python analysis.py /path/to/dataset.txt
   ```

The command writes private intermediate data to `outputs/private/` and an
aggregate results file to `outputs/summary.json`. Generated output directories
are ignored by Git.

## Expected analytical sample

For the dataset used in the dissertation, the script should identify:

- 28,435 events associated with `guess1Lab`;
- 66 sessions from 65 anonymised learners;
- 32 hint sessions and 34 non-hint sessions; and
- 309 hint requests.

## Repository contents

- `analysis.py` — filtering, session-level feature construction, descriptive
  statistics, and two-sided Mann–Whitney U comparisons.
- `figures/` — final aggregate figures used in the dissertation.
- `requirements.txt` — Python dependencies.

## Ethical and interpretive note

The analysis uses anonymised behavioural records. Results are reported at an
aggregate level, and the repository does not redistribute raw or session-level
learner data. Hint use is interpreted as a support-seeking event rather than a
direct measure of failure or difficulty.

