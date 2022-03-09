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

suppressPackageStartupMessages({
  library("ArchR")
})

inputFiles <- getTutorialData("Hematopoiesis")
inputFiles

addArchRGenome("hg19")

ArrowFiles <- createArrowFiles(
  inputFiles = inputFiles,
  sampleNames = names(inputFiles),
  filterTSS = 4, #Dont set this too high because you can always increase later
  filterFrags = 1000,
  addTileMat = TRUE,
  addGeneScoreMat = TRUE
)
