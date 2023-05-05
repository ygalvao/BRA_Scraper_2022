# BRA Scraper 2022

BRA Scraper 2022 is a web scraper designed to download election data from the 2022 Brazilian Federal Elections (2nd round). It specifically targets the Registro Digital de Votos (RDV), Boletim de Urna (BU), and logs of the Electronic Voting Machines (EVMs) for a specified state in Brazil.

## Requirements

- Python 3.8 or later
- Mozilla Firefox
- GeckoDriver

## Installation

1. Install the required Python packages:

```
pip install -r requirements.txt
```

2. Download the [GeckoDriver](https://github.com/mozilla/geckodriver/releases) that matches your Mozilla Firefox version and add it to your system's PATH.

## Usage

Run the scraper using the following command:

```
python web_scraper.py
```

### Command-line arguments

You can pass the following command-line arguments to configure the scraper's behavior during execution:

1. `--show-browser`: If present, the browser will be visible during the scraping process (not headless).
2. `--headless`: If present, the browser will be hidden (headless) during the scraping process. This argument is ignored if `--show-browser` is also present.
3. `--reverse`: If present, the order of the municipalities will be reversed during the scraping process.
4. `--scope`: If present, it should be followed by the desired scope value (e.g., `--scope Rio de Janeiro`). If not present, the user will be prompted to enter the desired scope.
5. `--yes_for_all`: If present, it will automatically assume a "yes" response for all confirmation prompts, causing the "confirm" function in "basic_functions.py" to return "True" every time it is called.

Example usage with command-line arguments:

```
python web_scraper.py --scope "Rio de Janeiro" --yes-for-all
```
or

```
python web_scraper.py --headless --reverse --scope "Rio de Janeiro"
```

With these command-line arguments, users have the flexibility to configure the scraper's behavior during execution, such as choosing between a headless or visible browser, reversing the order of municipalities, setting the desired scope, and bypassing confirmation prompts by automatically assuming "yes" for all.

## License

This project is licensed under the MIT License. Check the LICENSE file for more information.
