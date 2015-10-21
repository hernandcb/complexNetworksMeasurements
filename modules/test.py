import time
import os
import glob
import networkit as nk
import dimension.fractalDimension as fd
import robustness.robustness as robustness
from config import apconfig

real_networks_folder = apconfig.get_real_networks_full_path()
random_networks_folder = apconfig.get_random_networks_full_path()

networks = {
    "dolphins": real_networks_folder + 'Dolphin social network/dolphins.gml' # ,
    # "football": real_networks_folder + 'American College football/football.gml',
    # "celegans": real_networks_folder + 'CElegans/celegans.gml',
    # "email": real_networks_folder + 'Email network/email.gml',
    # "eColi": real_networks_folder + 'EColi/EColi.gml',
    # "power": real_networks_folder + 'Power grid/power.gml'
}

methods = {
    "fractalDimension": fd.fractal_dimension,
    "robustness" : robustness.plot_robustness_analysis
}


def test(filename, measure, iterations=80, results_file=None):
    g = nk.readGraph(filename, nk.Format.GML)
    g.setName(os.path.basename(filename).split(".", 1)[0])

    if g.isDirected():
        g = g.toUndirected()

    for i in range(iterations):
        print(measure(g), file=results_file)


def test_real_networks():
    current_time = time.strftime("%d-%m-%Y_%H%M%S")
    current_folder = os.getcwd()
    base_results_folder = apconfig.get_results_folder_path()

    for network in networks.values():
        network_name = os.path.basename(network).split(".", 1)[0]

        # Create folder if not exists
        if not os.path.exists(base_results_folder + network_name):
            os.makedirs(base_results_folder + network_name)

        os.chdir(base_results_folder + network_name)

        for method in methods:
            results_file_name = network_name + "_" + method + "_" + current_time + ".results"

            with open(results_file_name, 'a') as file:
                test(network, method, results_file=file)

        os.chdir(current_folder)


def test_random_networks():
    current_folder = os.getcwd()
    current_time = time.strftime("%d-%m-%Y_%H%M%S")

    results_folder = apconfig.get_random_results_folder_path()
    if not os.path.exists(results_folder):
            os.makedirs(results_folder)

    os.chdir(results_folder)

    networks_list = get_files(random_networks_folder, ".gml")

    for network in networks_list:
        network_name = os.path.basename(network).rsplit(".", 1)[0]

        for method in methods:
            results_file_name = network_name + "_" + method + "_" + current_time + ".results"

            with open(results_file_name, 'a') as file:
                test(network, method, results_file=file)

    os.chdir(current_folder)


def get_files(folder="", extension=""):
    """
    This method returns a list with the names of all the files contained in
    the folder received by parameter.

    folder: The folder where gml files are looked for. The current folder is the
     default value
    extension: A file extension. i.e. ".txt", If no value is passed all the
     files in the folder are returned
    """
    return sorted(glob.glob(folder + "*" + extension), reverse=True)


def main():
    # test_random_networks()
    test_real_networks()


if __name__ == '__main__':
    main()
