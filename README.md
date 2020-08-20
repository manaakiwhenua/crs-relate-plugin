[![manaakiwhenua-standards](https://github.com/manaakiwhenua/local-outlier-factor-plugin/workflows/manaakiwhenua-standards/badge.svg)](https://github.com/manaakiwhenua/manaakiwhenua-standards)

# crs-relate-plugin

A plugin for performing DE-9IM relationship tests between WKT geometries and their stated coordinate reference system (CRS).

For example, this can be used to assert whether a recorded geometry in a local circuit projection, is in fact within that CRS's defined extent.

The code could be generalised to perform the relationship test between arbitrary geometries, but this plugin is deliberately focused on asserting relationships between geometries and CRSs.

## Building for release

Requires wheel.

`python setup.py sdist bdist_wheel`

This can be included in a requirements.txt as: `git+https://github.com/manaakiwhenua/local-outlier-factor-plugin.git@master`

`master` branch is for release, changes should be proposed in a separate branch and a PR submitted for merging into master, including rebuilding the source distributions.

(TODO: replace with a Github Action)
