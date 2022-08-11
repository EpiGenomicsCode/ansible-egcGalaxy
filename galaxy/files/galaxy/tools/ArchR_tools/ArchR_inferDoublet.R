#!/usr/bin/env Rscript

# Command-line interface to ArchR for use with Galaxy

# R error handling to go to stderr
options(show.error.messages = F, error = function() {
  cat(geterrmessage(), file = stderr()); q("no", 1, F)
})

library("getopt")
library("tools")
options(stringAsFactors = FALSE, useFancyQuotes = FALSE)
args <- commandArgs(trailingOnly = TRUE)

# get options, using the spec as defined by the enclosed list.
# we read the options from the default: commandArgs(TRUE).
spec <- matrix(c(
  "quiet", "q", 0, "logical",
  "help", "h", 0, "logical",
  "cores", "c", 0, "integer",
  "sample", "s", 1, "character",
  "kCells", "k", 1, "integer",
  "knnMethod", "m", 1, "character",
  "LSIMethod", "l", 1, "integer"
), byrow = TRUE, ncol = 4)
opt <- getopt(spec)

# if help was asked for print a friendly message
# and exit with a non-zero error code
if (!is.null(opt$help)) {
  cat(getopt(spec, usage = TRUE))
  q(status = 1)
}

verbose <- is.null(opt$quiet)

suppressPackageStartupMessages({
  library("ArchR")
})

if (opt$cores > 1) {
  library("parallel")
  addArchRThreads(threads = opt$cores, force=TRUE)
} else {
  addArchRThreads(threads = 1, force=TRUE)
}

inputFiles = opt$sample
sampleName <- h5read(inputFiles, paste0("Metadata/Sample"))
#file.path("QualityControl", sampleName)
dir.create(file.path("QualityControl", sampleName), recursive = TRUE, showWarnings = TRUE)
#inputFiles
#sampleName

doubScores <- addDoubletScores(
  input = inputFiles,
  k = opt$kCells, #Refers to how many cells near a "pseudo-doublet" to count.
  knnMethod = opt$knnMethod, #Refers to the embedding to use for nearest neighbor search.
  LSIMethod = opt$LSIMethod,
)
