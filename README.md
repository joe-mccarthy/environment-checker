# Environment Checker

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/joe-mccarthy/environment-checker/build-test.yml?style=for-the-badge)
![Coveralls](https://img.shields.io/coverallsCoverage/github/joe-mccarthy/environment-checker?style=for-the-badge) 
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg?style=for-the-badge)](https://www.python.org/downloads/release/python-380/)
![GitHub License](https://img.shields.io/github/license/joe-mccarthy/environment-checker?style=for-the-badge)

Simple script that's called from a cron job that will take a reading from a bme 280 sensor or open weather api and record the result in a csv file with the calculated dew point.

## Getting Started

Ensure that you have the bme_280 sensors correctly connected and have made a note of the address of the sensor. If you're planning on using the Open Weather API ensure that you have your API key ready.

### Prerequisites

- Python 3.8 or higher

### Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/joe-mccarthy/environment-checker.git
cd environment-checker
pip install -r requirements.txt
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

1. Fork the Project
1. Create your Feature Branch (git checkout -b feature/AmazingFeature)
1. Commit your Changes (git commit -m 'Add some AmazingFeature')
1. Push to the Branch (git push origin feature/AmazingFeature)
1. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
