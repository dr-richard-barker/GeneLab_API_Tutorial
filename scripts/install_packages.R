# Create a directory for R packages if it doesn't exist
r_libs_path <- file.path(Sys.getenv("HOME"), "r-packages")
if (!dir.exists(r_libs_path)) {
  dir.create(r_libs_path, recursive = TRUE)
}

# Set the user library path
.libPaths(c(r_libs_path, .libPaths()))

# Optional: Set a default CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Install BiocManager if it's not already installed
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager", lib = r_libs_path)

# CRAN packages
cran_packages <- c("readr", "gplots", "ggplot2", "stringr")
# Bioconductor packages
bioc_packages <- c("org.Hs.eg.db", "edgeR", "DESeq2", "clusterProfiler", "enrichplot", "SBGNview")

# Install CRAN packages
for (pkg in cran_packages) {
    if (!requireNamespace(pkg, quietly = TRUE))
        install.packages(pkg, lib = r_libs_path)
}

# Install Bioconductor packages
for (pkg in bioc_packages) {
    if (!requireNamespace(pkg, quietly = TRUE))
        BiocManager::install(pkg, lib = r_libs_path, ask = FALSE)
}

print("All R packages are installed.")
