#!/usr/bin/env Rscript

# Command-line interface to ArchR for use with Galaxy (adapted from DESeq2)

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
  "cores", "s", 0, "integer",
  "genome", "g", 1, "character"
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
  addArchRThreads(threads = opt$cores)
} else {
  addArchRThreads(threads = 1)
}

addArchRGenome(opt$genome)

inputFiles <- getTutorialData("Hematopoiesis")
#inputFiles
#quit()

ArrowFiles <- createArrowFiles(
  inputFiles = inputFiles,
  sampleNames = names(inputFiles),
  outputNames = names(inputFiles),
  QCDir = "QualityControl",

  geneAnnotation = getGeneAnnotation(),
  genomeAnnotation = getGenomeAnnotation(),
  threads = getArchRThreads(),

  minTSS = 4, #Dont set this too high because you can always increase later
  minFrags = 1000,
  maxFrags = 1e+05,
  nucLength = 147,
  promoterRegion = c(2000, 100),

  #Don't touch these parameters
  nChunk = 5,
  bcTag = "qname",
  addTileMat = TRUE,
  addGeneScoreMat = TRUE,
  verbose = TRUE,
  cleanTmp = TRUE,

  # Tn5 bias strands
  offsetPlus = 4,
  offsetMinus = -5

)
