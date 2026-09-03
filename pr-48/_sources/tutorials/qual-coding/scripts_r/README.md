# Setup

The scripts in this folder are:

* `skeleton_qual_coding.R`
* `skeleton_qual_coding.Rmd`

They require R and a small number of R packages.

## Required R packages

Install the required packages once in R:

```r
install.packages(c(
  "httr",
  "jsonlite",
  "rmarkdown"
))
```

The packages are used for:

* `httr` — sending requests to the API
* `jsonlite` — reading and writing JSON
* `rmarkdown` — rendering the `.Rmd` file to HTML

If you are only running `skeleton_qual_coding.R`, `rmarkdown` is not required.

## Set your OpenRouter API key

The scripts expect your OpenRouter API key to be available as the environment
variable `OPENROUTER_API_KEY`.

You can obtain an API key from:

https://openrouter.ai

### macOS / Linux

In Terminal:

```bash
export OPENROUTER_API_KEY="sk-or-..."
```

### Windows PowerShell

```powershell
$env:OPENROUTER_API_KEY="sk-or-..."
```

### Windows Command Prompt

```cmd
set OPENROUTER_API_KEY=sk-or-...
```

This sets the API key only for the current terminal session.

Do not put your real API key directly in the R script or commit it to Git.

## Run the R script

From the folder containing the scripts, run:

```bash
Rscript skeleton_qual_coding.R
```

Alternatively, open the script in RStudio and run it there.

## Packages needed for the full pipeline

The skeleton scripts above use only the packages listed earlier.

The full pipeline — including Excel files, photos, multiple models, and
reliability statistics — requires several additional packages:

```r
install.packages(c(
  "readxl",
  "writexl",
  "base64enc",
  "irr"
))
```

These packages are used for:

* `readxl` — reading Excel files
* `writexl` — writing Excel files
* `base64enc` — encoding images for API requests
* `irr` — Cohen's kappa and other agreement statistics
