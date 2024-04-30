# OOPS: GEM5 Prediction

## Project Overview

Design space exploration in computer architecture is expensive, requiring large amounts of design effort and simulation time. In order to perform first-pass power and performance evaluations of proposed CPU configurations, we developed and trained a number of DL models to narrow down useful configurations for future exploration.

## DL Models

We trained 4 different DL models - InvertibleMLP, InvertibleMLP with One-Hot Encoding, Encoder / Decoder Design, and Encoder / Decoder Design with One-Hot Encoding

## Directory

**Data Collection** - Folder contains scripts used to collect and manage our data collection for training, as well as the dataset itself in csv form.
**HTMLs (saved images and stuff)** - Folder contains our trained Jupyter Notebooks with outputs saved as HTML for reference
**Jupyter Notebooks** - Folder contains our code in Jupyter used to implement our various DL models
