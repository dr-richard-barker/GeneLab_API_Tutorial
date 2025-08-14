import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import os

def test_rpy2_installation():
    """
    Tests if rpy2 is installed and can interface with R.
    """
    try:
        # Create a local directory for R packages
        r_libs_path = os.path.join(os.path.expanduser('~'), 'r-packages')
        os.makedirs(r_libs_path, exist_ok=True)

        # Set the R_LIBS_USER environment variable
        os.environ['R_LIBS_USER'] = r_libs_path

        # Import R's 'utils' package
        utils = importr('utils')

        # Select a CRAN mirror
        utils.chooseCRANmirror(ind=1)

        # Install a package
        packnames = ('ggplot2',)
        from rpy2.robjects.vectors import StrVector
        utils.install_packages(StrVector(packnames), lib=r_libs_path)

        print("Successfully installed ggplot2 from R using rpy2.")
        print("rpy2 is working correctly.")

    except Exception as e:
        print(f"An error occurred while testing rpy2: {e}")

if __name__ == "__main__":
    test_rpy2_installation()
