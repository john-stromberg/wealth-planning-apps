# Wealth Planning Apps

Each project is maintained as an independent project. Use its own README,
dependency definitions, tests, entry points, and license.

| Project | Original repository |
| --- | --- |
| [wealth-planning-calculator](projects/wealth-planning-calculator/) | [GitHub](https://github.com/john-stromberg/wealth-planning-calculator) |
| [cashflow-optimizer](projects/cashflow-optimizer/) | [GitHub](https://github.com/john-stromberg/cashflow-optimizer) |
| [client-wealth-dashboard](projects/client-wealth-dashboard/) | [GitHub](https://github.com/john-stromberg/client-wealth-dashboard) |
| [financial-data-pipeline](projects/financial-data-pipeline/) | [GitHub](https://github.com/john-stromberg/financial-data-pipeline) |

The source commit and tree for each import are recorded in [IMPORTS.json](IMPORTS.json);
the complete imported commit histories are retained. Run each project from its own
directory. There is no shared installation or unified API.

The existing pinned dependencies were validated with Python 3.11. The
Streamlit projects constrain PyArrow below 26 because PyArrow 26 requires
NumPy 2, while these projects pin NumPy 1.24.

Project-level GitHub Actions files are preserved as references. GitHub only runs
workflows located under this repository's root `.github/workflows/` directory.
