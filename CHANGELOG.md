# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added sonar integration and badge for the readme

### Changed

- Changelog typo
- [#1](https://github.com/joe-mccarthy/environment-checker/pull/1) Update dependencies via dependabot

## [1.0.0] - 2024-08-23

### Added

- Created the project changelog.
- Created unit tests
- Added module docstring
- Added method docstring
- Added badges
- Get temperature, pressure, humidity from OpenWeatherMapAPI
- Get temperature, pressure, humidity from BME280 sensor
- Calculate the dew point for current readings
- Check csv file exists
- Creates missing csv file and creates headers
- Appends current readings to the csv file
- No API key assumes using BME280 sensor with defaults

### Changed

- Variables are passed as cli arguments
- Updated the project readme

### Removed

- Removed hard coded variables

[unreleased]: https://github.com/joe-mccarthy/environment-checker/compare/1.0.0...HEAD
[1.0.0]: https://github.com/joe-mccarthy/environment-checker/releases/tag/1.0.0
