import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import src.constants as constants
from src.make_latex_tables import average_velocities_table_to_latex, halpha_regions_table_to_latex
from src.bpt_plotting import bpt_plot
from src.kinematics_calculations import RegionCalculations
from src.fit_line_profiles import plot_profiles
from src.line_profile_info import RegionParameters

# Path to the directory you wish to save the ouput plots, tables and results.
constants.OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Output_Files')

# Path to the directory containing your input data files (Optional).
constants.DATA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Data_Files')

# # Set up example region to simultaneously fit multiple emission lines
example_region = RegionParameters(region_name='HCG31-A',
                                  blue_spec_file='HCG31-A_B.fc.fits',
                                  red_spec_file='HCG31-A_R.fc.fits',
                                  blue_spec_error_file='HCG31-A_B_ErrorFlux.fc.fits',
                                  red_spec_error_file='HCG31-A_R_ErrorFlux.fc.fits',
                                  scale_flux=1e14,
                                  center_list={'low': [4002.52322, 4021.71577, 3973.37160],
                                               'high': [4005.19802, 4025.48311, 3982.74252]},
                                  sigma_list={'low': [41.8827261, 18.8630715,  92.9064515],
                                              'high': [44.0996336, 16.9739078,  101.497488]},
                                  lin_slope={'low': -2.4358e-07, 'high': -1.0036e-07},
                                  lin_int={'low': 0.00218375, 'high': 0.00172978},
                                  num_comps={'low': 3, 'high': 3},
                                  component_labels=['Narrow 1', 'Narrow 2', 'Broad'],
                                  component_colors=['b', 'r', 'g'],
                                  plotting_x_range=[3600, 4300],
                                  sigma_instr_blue=5.2,
                                  sigma_inst_red=6.2,
                                  distance=1.67e26,
                                  em_lines_for_avg_vel_calc=['H-Alpha', 'H-Beta_Blue', 'OIII-5007A', 'NII-6584A', 'SII-6717A'],
                                  plot_residuals=False,
                                  show_systemic_velocity=False,
                                  systemic_velocity=None
                                  )

example_region.add_em_line(name='H-Alpha', plot_color='y', order=20, filter='red', min_idx=2931, max_idx=3360, rest_wavelength=6562.82, num_comps=3, amp_list=[13.5290844, 1.9384663, 6.3288925], zone='low', sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': np.inf, 's': np.inf}, copy_from=None)
example_region.add_em_line(name='OIII-5007A', plot_color='c', order=4, filter='red', min_idx=2300, max_idx=3440, rest_wavelength=5006.84, num_comps=3, amp_list=[9.750481, 1.283694, 5.119205], zone='high', sigma_tsquared=10.39, comp_limits={'a': np.inf, 'c': np.inf, 's': np.inf}, copy_from=None)
example_region.add_em_line(name='OIII-4959A', plot_color='g', order=4, filter='red', min_idx=1080, max_idx=2000, rest_wavelength=4958.91, num_comps=3, amp_list=[3.2072457, 0.4285652, 1.7044356], zone='high', sigma_tsquared=10.39, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='OIII-5007A')
example_region.add_em_line(name='H-Beta', plot_color='b', order=36, filter='blue', min_idx=370, max_idx=1613, rest_wavelength=4861.33, num_comps=3, amp_list=[3.9230061, 0.3794315, 2.1102948], zone='low', sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Alpha')
example_region.add_em_line(name='NII-6584A', plot_color='violet', order=20, filter='red', min_idx=3361, max_idx=3885, rest_wavelength=6583.41, num_comps=3, amp_list=[1.7845879, 0.446267, 0.9448954], zone='low', sigma_tsquared=11.87, comp_limits={'a': np.inf, 'c': np.inf, 's': np.inf}, copy_from=None)
example_region.add_em_line(name='NII-6548A', plot_color='violet', order=20, filter='red', min_idx=2563, max_idx=2930, rest_wavelength=6548.03, num_comps=3, amp_list=[0.0324588, 1.0586795, 0.5316711], zone='low', sigma_tsquared=11.87, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='NII-6584A')
example_region.add_em_line(name='SII-6717A', plot_color='r', order=22, filter='red', min_idx=508, max_idx=985, rest_wavelength=6716.47, num_comps=3, amp_list=[1.0651477, 0.1889682, 0.5398219], zone='low', sigma_tsquared=5.19, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Alpha')
example_region.add_em_line(name='SII-6731A', plot_color='#58D68D', order=22, filter='red', min_idx=986, max_idx=1290, rest_wavelength=6730.85, num_comps=3, amp_list=[0.0324219, 0.6733394, 0.2678776], zone='low', sigma_tsquared=5.19, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='SII-6717A')
example_region.add_em_line(name='H-Gamma', plot_color='r', order=27, filter='blue', min_idx=1625, max_idx=2183, rest_wavelength=4340.47, num_comps=3, amp_list=[1.8354956, 0.1155452, 0.8171744], zone='low', sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Beta')
example_region.add_em_line(name='H-Delta', plot_color='c', order=22, filter='blue', min_idx=2390, max_idx=2810, rest_wavelength=4101.74, num_comps=3, amp_list=[0.9831404, 0.0538247, 0.420242], zone='low', sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Beta')
example_region.add_em_line(name='SIII-9069A', plot_color='#27AE60', order=35, filter='red', min_idx=485, max_idx=881, rest_wavelength=9068.9, num_comps=3, amp_list=[1.462683, 0.5170754, 0.5116994], zone='low', sigma_tsquared=5.19, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='OIII-5007A')


def main():
    regions_parameters = [example_region]

    region_array = []
    rp_bpt_points, rp_bpt_points_s, rp_bpt_points_o, rp_bpt_points_p = [], [], [], []
    for rp in regions_parameters:
        region = RegionCalculations(rp, xAxis='vel', initVals='vel')
        region_array.append(region.lineInArray)
        rp_bpt_points.append(region.bptPoints)
        rp_bpt_points_s.append(region.bptPoints_s)
        rp_bpt_points_o.append(region.bptPoints_o)
        rp_bpt_points_p.append(region.bptPoints_p)

        plot_profiles(['H-Alpha', 'OIII-5007A', 'H-Beta', 'NII-6584A', 'SII-6717A'], rp, nameForComps='SII-6717A',
                      title=rp.regionName + ' Strongest Emission Lines', sortedIndex=[0, 1, 2, 3, 4], logscale=True,
                      ymin=None)

    bpt_plot(regions_parameters, rp_bpt_points, plot_type='n')
    bpt_plot(regions_parameters, rp_bpt_points_s, plot_type='s')
    bpt_plot(regions_parameters, rp_bpt_points_o, plot_type='o')
    bpt_plot(regions_parameters, rp_bpt_points_p, plot_type='p')
    halpha_regions_table_to_latex(region_array, paperSize='a4', orientation='portrait', longTable=False)
    average_velocities_table_to_latex(regions_parameters, paperSize='a4', orientation='landscape', longTable=False)

    plt.show()


if __name__ == '__main__':
    main()
