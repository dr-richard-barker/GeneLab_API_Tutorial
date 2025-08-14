# .Rprofile
# Create a directory for R packages if it doesn't exist
r_libs_path <- file.path(Sys.getenv("HOME"), "r-packages")
if (!dir.exists(r_libs_path)) {
  dir.create(r_libs_path, recursive = TRUE)
}

# Set the user library path
.libPaths(c(r_libs_path, .libPaths()))

# Optional: Set a default CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org"))
