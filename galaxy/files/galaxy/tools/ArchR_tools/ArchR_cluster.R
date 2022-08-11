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
  "cores", "c", 0, "integer",
  "genome", "g", 1, "character",
  "sample", "s", 1, "character",
  "sampleid", "n", 1, "character",
  "minTSS", "t", 1, "integer",
  "minFrag", "a", 1, "integer",
  "maxFrag", "b", 1, "integer",
  "outArrow", "o", 1, "character"
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

addArchRGenome(opt$genome)

#inputFiles <- getTutorialData("Hematopoiesis")
inputFiles = opt$sample
names(inputFiles) = opt$sampleid
#inputFiles
#quit()

# Instantiate ArchR project
proj <- ArchRProject(
  ArrowFiles = ArrowFiles,
  outputDirectory = "HemeTutorial",
  copyArrows = TRUE #This is recommened so that you maintain an unaltered copy for later usage.
)

# Inform ArchR to ignore predicted doublets
proj <- filterDoublets(ArchRProj = proj)

# Add LSI clustering to project
proj <- addIterativeLSI(ArchRProj = proj, useMatrix = "TileMatrix", name = "IterativeLSI")

# Call clusters using Seurat graph clustering
proj <- addClusters(input = proj, reducedDims = "IterativeLSI")

# Project data using UMAP
proj <- addUMAP(ArchRProj = proj, reducedDims = "IterativeLSI")

# Generate 2D projection colored by 'Sample'
p1 <- plotEmbedding(ArchRProj = proj, colorBy = "cellColData", name = "Sample", embedding = "UMAP")

# Generate 2D projection colored by 'Cluster'
p2 <- plotEmbedding(ArchRProj = proj, colorBy = "cellColData", name = "Clusters", embedding = "UMAP")

# Output data to PDF
plotPDF(p1,p2, name = "Plot-UMAP-Sample-Clusters.pdf", ArchRProj = proj, addDOC = FALSE, width = 5, height = 5)

# Add imputation weights
proj <- addImputeWeights(proj)

# Pick marker genes
markerGenes  <- c(
    "CD34",  #Early Progenitor
    "GATA1", #Erythroid
    "PAX5", "MS4A1", "MME", #B-Cell Trajectory
    "CD14", "MPO", #Monocytes
    "CD3D", "CD8A"#TCells
  )

p <- plotEmbedding(
    ArchRProj = proj,
    colorBy = "GeneScoreMatrix",
    name = markerGenes,
    embedding = "UMAP",
    imputeWeights = getImputeWeights(proj)
)

# Plot embeddings
plotPDF(plotList = p, name = "Plot-UMAP-Marker-Genes-W-Imputation.pdf", ArchRProj = proj, addDOC = FALSE, width = 5, height = 5)

# Output Genome browser snapshot
p <- plotBrowserTrack(
    ArchRProj = proj,
    groupBy = "Clusters",
    geneSymbol = markerGenes,
    upstream = 50000,
    downstream = 50000
)

# PDF of Genome browser
plotPDF(plotList = p, name = "Plot-Tracks-Marker-Genes.pdf", ArchRProj = proj, addDOC = FALSE, width = 5, height = 5)

ArrowFiles <- createArrowFiles(
  inputFiles = inputFiles,
  sampleNames = names(inputFiles),
  outputNames = names(inputFiles),
  QCDir = "QualityControl",

  geneAnnotation = getGeneAnnotation(),
  genomeAnnotation = getGenomeAnnotation(),
  threads = getArchRThreads(),

  minTSS = opt$minTSS, #Dont set this too high because you can always increase later
  minFrags = opt$minFrag,
  maxFrags = opt$maxFrag,
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
