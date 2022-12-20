# Instructions

status: draft


## Setup

1. Install dependencies
    ```bash
    poetry install
    ```
2. Start the application
    ´´´bash
    poetry run invoke start
    ```

## Testing

- Run tests
    ```bash
    poetry run invoke test
    ```
- Generate coverage report
    ```bash
    poetry run invoke coverage-report
    ```
- Perform pylint code quality inspection
    ```bash
    poetry run invoke lint
    ```
- Execute autopep8 format
    ```bash
    poetry run invoke format
    ```
