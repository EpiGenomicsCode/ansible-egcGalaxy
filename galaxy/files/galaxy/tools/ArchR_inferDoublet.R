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

doubScores <- addDoubletScores(
  input = ArrowFiles,
  k = 10, #Refers to how many cells near a "pseudo-doublet" to count.
  knnMethod = "UMAP", #Refers to the embedding to use for nearest neighbor search.
  LSIMethod = 1
)
