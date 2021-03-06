#
#
#------------------------------------
SOLUTION, xtri3n_hook-1, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	LOADS, force_load-2
	LOADS, force_load-3
	BOUNDARIES, boundary-1
	BOUNDARIES, boundary-2
#------------------------------------
RESULTS, xtri3n_hook-1
#------------------------------------
	DISPLACEMENT, plot, 1
	STRESS, plot, 1
	STRAIN, plot, 1
#
#
#
#
#
MATERIAL, Isotropic, 1010_carbon_steel (N mm kg), 205000.0, 0.29, 7.87e-09
#
#
#
SECTION, PlaneSect, 0, 1010_carbon_steel (N mm kg), 20.0
#
#
#
BOUNDARY, Displacement, boundary-1, 1, 0., 1
BOUNDARY, Displacement, boundary-2, 2, 0., 2
#
#
#
LOAD, Force, force_load-1, 3, 3500, 0., -1, 0.
LOAD, Force, force_load-2, 4, 1250, 0., -1, 0.
LOAD, Force, force_load-3, 5, 350, 0., -1, 0.
#
#
#
SET_NODES, 1, 1, 5 - 7, 11, 12, 71
SET_NODES, 2, 2 - 4, 70
SET_NODES, 3, 46, 47, 96
SET_NODES, 4, 45, 48, 49, 95
SET_NODES, 5, 44, 97
SET_NODES, 999, 1 - 301
#
#
#
SET_ELEMENTS, 999, 1 - 488
SET_ELEMENTS, 1, 1 - 488
#
#
#
NODE, 1, 6.75994205, 100.401855, 0.0
NODE, 2, 3.33813429, 105.111565, 0.0
NODE, 3, -7.49309254, 108.630844, 0.0
NODE, 4, -13.0296946, 106.831894, 0.0
NODE, 5, -17.3559322, 102.936531, 0.0
NODE, 6, -19.7237606, 97.6183014, 0.0
NODE, 7, -17.3559322, 86.4785461, 0.0
NODE, 8, -13.0296946, 82.5831833, 0.0
NODE, 9, -7.49309254, 80.7842331, 0.0
NODE, 10, -1.70345616, 81.392746, 0.0
NODE, 11, 6.75994205, 89.0132294, 0.0
NODE, 12, 7.97030592, 94.7075424, 0.0
NODE, 13, -36.0296936, 94.7074356, 0.0
NODE, 14, -36.0295525, 54.7074318, 0.0
NODE, 15, -35.1460495, 49.4201965, 0.0
NODE, 16, -32.5915794, 44.7074318, 0.0
NODE, 17, -25.217104, 35.25, 0.0
NODE, 18, -24.0791798, 25.2224979, 0.0
NODE, 19, -23.2354774, 30.3965588, 0.0
NODE, 20, -27.5, 21.25, 0.0
NODE, 21, -44.8954506, 9.72231483, 0.0
NODE, 22, 47.3200836, -50.806694, 0.0
NODE, 23, 42.3110504, -66.31633, 0.0
NODE, 24, 38.2755051, -73.4179764, 0.0
NODE, 25, 27.5149364, -85.6592712, 0.0
NODE, 26, 13.8569479, -94.5530167, 0.0
NODE, 27, -1.69065368, -99.4429398, 0.0
NODE, 28, -17.9806309, -99.9682312, 0.0
NODE, 29, -33.8109703, -96.090126, 0.0
NODE, 30, -41.1850128, -92.5769501, 0.0
NODE, 31, -54.1700706, -82.7266922, 0.0
NODE, 32, -64.025116, -69.7452698, 0.0
NODE, 33, -70.0229645, -54.5905571, 0.0
NODE, 34, -71.7210312, -38.3808136, 0.0
NODE, 35, -68.9940186, -22.3121243, 0.0
NODE, 36, -66.0214844, -14.7040377, 0.0
NODE, 37, -57.132782, -1.04276943, 0.0
NODE, 38, 47.9703064, -34.521225, 0.0
NODE, 39, 34.184021, -29.7606735, 0.0
NODE, 40, 39.602829, -27.2832203, 0.0
NODE, 41, 45.2347984, -29.2279987, 0.0
NODE, 42, 31.9703064, -35.2924652, 0.0
NODE, 43, 31.0773315, -43.4820023, 0.0
NODE, 44, 24.1833839, -58.3395844, 0.0
NODE, 45, 18.5064163, -64.3093414, 0.0
NODE, 46, 4.01399946, -71.9411163, 0.0
NODE, 47, -4.12032652, -73.2444611, 0.0
NODE, 48, -20.2716713, -70.522644, 0.0
NODE, 49, -27.5296001, -66.625412, 0.0
NODE, 50, -38.7204399, -54.6655121, 0.0
NODE, 51, -42.1273994, -47.1649361, 0.0
NODE, 52, -43.7713051, -30.8685646, 0.0
NODE, 53, -41.9309921, -22.8386707, 0.0
NODE, 54, -33.3542252, -8.88469791, 0.0
NODE, 55, -27.0208721, -3.6164372, 0.0
NODE, 56, 4.49872398, 17.2710915, 0.0
NODE, 57, 7.71081352, 20.2710915, 0.0
NODE, 58, 20.326704, 44.7074318, 0.0
NODE, 59, 23.0463505, 51.9893417, 0.0
NODE, 60, 23.9703064, 59.7074318, 0.0
NODE, 61, 23.9703064, 94.7074356, 0.0
NODE, 62, -35.0074921, 102.472023, 0.0
NODE, 63, -27.2429352, 115.920708, 0.0
NODE, 64, -21.0297241, 120.688286, 0.0
NODE, 65, -13.7942829, 123.68531, 0.0
NODE, 66, 1.73489428, 123.68531, 0.0
NODE, 67, 8.97033691, 120.688286, 0.0
NODE, 68, 15.183547, 115.920708, 0.0
NODE, 69, 22.948103, 102.472023, 0.0
NODE, 70, -1.70345628, 108.022331, 0.0
NODE, 71, -19.7237606, 91.7967758, 0.0
NODE, 72, 3.33813429, 84.3035126, 0.0
NODE, 73, -36.0296669, 86.7074356, 0.0
NODE, 74, -36.0296364, 78.7074356, 0.0
NODE, 75, -36.0296097, 70.7074356, 0.0
NODE, 76, -36.0295792, 62.7074318, 0.0
NODE, 77, -28.9043407, 39.9787178, 0.0
NODE, 78, -39.0969658, 13.5648766, 0.0
NODE, 79, -33.2984848, 17.4074383, 0.0
NODE, 80, 48.2007446, -42.6861382, 0.0
NODE, 81, 45.3446503, -58.7323875, 0.0
NODE, 82, 33.3128128, -79.9057007, 0.0
NODE, 83, 20.989336, -90.5720596, 0.0
NODE, 84, 6.24995804, -97.5283585, 0.0
NODE, 85, -9.81772327, -100.261292, 0.0
NODE, 86, -26.0280952, -98.5691986, 0.0
NODE, 87, -48.0135651, -88.09478, 0.0
NODE, 88, -59.540432, -76.5721664, 0.0
NODE, 89, -67.5410156, -62.3725166, 0.0
NODE, 90, -71.4249573, -46.5436134, 0.0
NODE, 91, -70.9056778, -30.2534409, 0.0
NODE, 92, -62.0431633, -7.57018185, 0.0
NODE, 93, -51.3813477, 4.75722647, 0.0
NODE, 94, 28.4403801, -51.286644, 0.0
NODE, 95, 11.6762857, -68.9153442, 0.0
NODE, 96, -12.3443899, -72.7641144, 0.0
NODE, 97, -33.7770653, -61.2555771, 0.0
NODE, 98, -43.8378143, -39.1063766, 0.0
NODE, 99, -38.4033661, -15.3940868, 0.0
NODE, 100, -21.7676048, -0.135182619, 0.0
NODE, 101, -16.5143394, 3.34607196, 0.0
NODE, 102, -11.2610741, 6.82732677, 0.0
NODE, 103, -6.00780773, 10.3085814, 0.0
NODE, 104, -0.754541993, 13.7898359, 0.0
NODE, 105, 10.2339916, 25.1583595, 0.0
NODE, 106, 12.7571697, 30.0456276, 0.0
NODE, 107, 15.2803478, 34.9328957, 0.0
NODE, 108, 17.8035259, 39.8201637, 0.0
NODE, 109, 23.9703064, 85.9574356, 0.0
NODE, 110, 23.9703064, 77.2074356, 0.0
NODE, 111, 23.9703064, 68.4574356, 0.0
NODE, 112, -32.0104904, 109.707481, 0.0
NODE, 113, -6.02969408, 124.707542, 0.0
NODE, 114, 19.9511032, 109.707481, 0.0
NODE, 115, 4.19099808, 22.438406, 0.0
NODE, 116, -19.6144848, 34.1619949, 0.0
NODE, 117, -21.8019371, 20.0602894, 0.0
NODE, 118, -19.1832314, 27.1811905, 0.0
NODE, 119, -30.3454666, 50.0242348, 0.0
NODE, 120, 14.3784657, 44.6685486, 0.0
NODE, 121, 9.77644634, 34.5028877, 0.0
NODE, 122, 8.16717911, 30.1216679, 0.0
NODE, 123, 12.0937214, 39.5185318, 0.0
NODE, 124, 11.2705202, 98.2736282, 0.0
NODE, 125, 9.76342583, 83.4439316, 0.0
NODE, 126, 8.23267746, 104.852127, 0.0
NODE, 127, -17.6940022, 107.813919, 0.0
NODE, 128, -11.763649, 77.088028, 0.0
NODE, 129, 3.07848883, 77.3714676, 0.0
NODE, 130, -4.76046753, 75.6166458, 0.0
NODE, 131, -23.5119438, 86.6569366, 0.0
NODE, 132, -23.9889641, 94.9416962, 0.0
NODE, 133, -4.35281754, 112.102966, 0.0
NODE, 134, -11.5260153, 111.318214, 0.0
NODE, 135, 2.71648932, 109.83876, 0.0
NODE, 136, -18.6276054, 79.7961197, 0.0
NODE, 137, -22.0279102, 102.054634, 0.0
NODE, 138, 11.6100054, 91.2098618, 0.0
NODE, 139, 39.8492661, -33.4918556, 0.0
NODE, 140, -26.6093388, 45.110775, 0.0
NODE, 141, -23.0292244, 40.0070038, 0.0
NODE, 142, -16.6725025, 9.81460476, 0.0
NODE, 143, -11.321208, 13.098527, 0.0
NODE, 144, -22.0713863, 6.6860981, 0.0
NODE, 145, -6.0022068, 16.3138103, 0.0
NODE, 146, -28.8856621, 4.22592545, 0.0
NODE, 147, -0.756465614, 19.456974, 0.0
NODE, 148, -37.2633095, 6.54184246, 0.0
NODE, 149, -32.0638504, 11.1892672, 0.0
NODE, 150, -27.1947002, 15.4722309, 0.0
NODE, 151, -0.570453286, 24.7486744, 0.0
NODE, 152, 6.40248966, 38.9694328, 0.0
NODE, 153, 3.63914609, 33.2332497, 0.0
NODE, 154, 8.75046349, 44.1863937, 0.0
NODE, 155, 16.4192142, 50.2829704, 0.0
NODE, 156, -20.5924702, 45.3054199, 0.0
NODE, 157, -21.8174839, 13.0388136, 0.0
NODE, 158, -16.4271374, 16.2552986, 0.0
NODE, 159, -10.9594975, 19.1572266, 0.0
NODE, 160, -5.64418364, 22.0127792, 0.0
NODE, 161, -26.4066162, 10.122467, 0.0
NODE, 162, -24.0547276, 50.4269485, 0.0
NODE, 163, -35.1870537, -1.12987864, 0.0
NODE, 164, -17.0805912, 40.1393585, 0.0
NODE, 165, 4.24200344, 27.509779, 0.0
NODE, 166, 3.14189601, 43.7643509, 0.0
NODE, 167, -5.1016202, 27.5228539, 0.0
NODE, 168, 0.363218933, 38.7001877, 0.0
NODE, 169, 10.8499432, 49.3724022, 0.0
NODE, 170, -17.8873119, 50.4858665, 0.0
NODE, 171, -13.6527424, 35.3970528, 0.0
NODE, 172, -27.7377911, 55.4408875, 0.0
NODE, 173, -15.5170813, 22.4421997, 0.0
NODE, 174, -10.2805796, 24.8381271, 0.0
NODE, 175, 17.3741932, 56.6907883, 0.0
NODE, 176, -43.2390938, 1.58641863, 0.0
NODE, 177, -14.7288895, 45.3811569, 0.0
NODE, 178, -2.43705511, 43.6666145, 0.0
NODE, 179, -0.268202126, 29.2979126, 0.0
NODE, 180, 5.37382603, 48.8781509, 0.0
NODE, 181, -3.63750935, 33.5093803, 0.0
NODE, 182, -10.895505, 40.7223816, 0.0
NODE, 183, -15.3823109, 30.9267883, 0.0
NODE, 184, -14.1092968, 27.2213459, 0.0
NODE, 185, 12.6180983, 54.0778618, 0.0
NODE, 186, -21.1355171, 55.759037, 0.0
NODE, 187, -10.1227732, 30.7555542, 0.0
NODE, 188, -11.9043741, 50.1235771, 0.0
NODE, 189, 17.449028, 64.0620422, 0.0
NODE, 190, -0.121678799, 48.4618225, 0.0
NODE, 191, -5.35983086, 39.3243065, 0.0
NODE, 192, -14.7547922, 55.6015549, 0.0
NODE, 193, -8.73367214, 35.9417343, 0.0
NODE, 194, -24.4700108, 61.1703339, 0.0
NODE, 195, 10.8889761, 59.9777031, 0.0
NODE, 196, -10.0726337, 45.624012, 0.0
NODE, 197, -49.3116798, -3.6967597, 0.0
NODE, 198, -6.02301168, 48.4501266, 0.0
NODE, 199, 1.99666214, 53.470417, 0.0
NODE, 200, -7.91243553, 55.1742058, 0.0
NODE, 201, -30.5809917, 60.260334, 0.0
NODE, 202, -17.8815975, 61.1392517, 0.0
NODE, 203, 11.1972036, 67.5958405, 0.0
NODE, 204, -6.95760727, 43.5574875, 0.0
NODE, 205, -41.2359505, -6.73320055, 0.0
NODE, 206, -2.80963707, 52.6489601, 0.0
NODE, 207, 7.60981989, 54.1414337, 0.0
NODE, 208, -11.5289745, 60.8308945, 0.0
NODE, 209, -20.8446445, 67.0223465, 0.0
NODE, 210, -28.7036324, 67.2739029, 0.0
NODE, 211, 6.01560831, 64.3453751, 0.0
NODE, 212, 17.3447247, 72.0811768, 0.0
NODE, 213, 3.94298148, 59.0937881, 0.0
NODE, 214, -6.07207584, 60.8731842, 0.0
NODE, 215, -14.156662, 66.4135056, 0.0
NODE, 216, -0.824638665, 64.914978, 0.0
NODE, 217, -7.9202857, 65.6862411, 0.0
NODE, 218, -16.4447384, 72.5236893, 0.0
NODE, 219, 4.9174614, 70.1477737, 0.0
NODE, 220, -23.2348652, 73.6231003, 0.0
NODE, 221, 10.5404167, 75.1234512, 0.0
NODE, 222, -9.98326874, 71.1962357, 0.0
NODE, 223, -1.9465239, 57.6959229, 0.0
NODE, 224, -29.8381348, 75.4986115, 0.0
NODE, 225, 16.9380627, 80.1475372, 0.0
NODE, 226, -4.79817247, 69.801857, 0.0
NODE, 227, -25.0470638, 79.7189865, 0.0
NODE, 228, -54.6947899, -7.81700134, 0.0
NODE, 229, 15.0669451, 103.632782, 0.0
NODE, 230, -17.7733898, 115.053345, 0.0
NODE, 231, 10.1089811, 111.69162, 0.0
NODE, 232, -29.7754059, 91.0870438, 0.0
NODE, 233, -29.0250511, 100.499863, 0.0
NODE, 234, -8.80573845, 117.344765, 0.0
NODE, 235, -24.2956295, 108.508324, 0.0
NODE, 236, 0.620350182, 117.151321, 0.0
NODE, 237, 17.8393402, 94.7607117, 0.0
NODE, 238, 16.0242271, 87.1038971, 0.0
NODE, 239, -30.038641, 83.0627441, 0.0
NODE, 240, -47.7849007, -12.8485003, 0.0
NODE, 241, -0.477465659, 71.5705414, 0.0
NODE, 242, -57.0329323, -13.9106331, 0.0
NODE, 243, 42.7863846, -38.9356766, 0.0
NODE, 244, 19.911068, -82.0971603, 0.0
NODE, 245, -55.8512764, -69.1764603, 0.0
NODE, 246, 34.4225616, -66.3430252, 0.0
NODE, 247, 13.5126667, -86.8868866, 0.0
NODE, 248, 37.5065041, -52.7021065, 0.0
NODE, 249, -27.8852463, -90.4354401, 0.0
NODE, 250, -64.0383453, -35.2248268, 0.0
NODE, 251, -62.2846565, -28.1783085, 0.0
NODE, 252, -46.4591103, -79.9847412, 0.0
NODE, 253, 38.2199364, -60.6564331, 0.0
NODE, 254, -6.35994577, -92.7470093, 0.0
NODE, 255, -63.7727547, -49.3596954, 0.0
NODE, 256, -20.6720047, -92.0316849, 0.0
NODE, 257, -34.569458, -87.8831787, 0.0
NODE, 258, -13.3970804, -93.0774384, 0.0
NODE, 259, -62.0817223, -56.3081741, 0.0
NODE, 260, -40.8299522, -84.3654251, 0.0
NODE, 261, -59.4457626, -62.9405136, 0.0
NODE, 262, 40.6904221, -44.6433372, 0.0
NODE, 263, -51.5629196, -74.9009171, 0.0
NODE, 264, 8.38675213, -90.8564148, 0.0
NODE, 265, -64.5129547, -42.3455467, 0.0
NODE, 266, 1.36860549, -90.356163, 0.0
NODE, 267, -59.787159, -20.9866467, 0.0
NODE, 268, 26.1949425, -78.6624222, 0.0
NODE, 269, 29.8516541, -72.8048401, 0.0
NODE, 270, -52.5692177, -27.3050308, 0.0
NODE, 271, -43.0399857, -63.5457153, 0.0
NODE, 272, 20.5128536, -72.9515915, 0.0
NODE, 273, -51.0807419, -44.5745773, 0.0
NODE, 274, -35.7280273, -71.1283722, 0.0
NODE, 275, -51.050087, -35.7000389, 0.0
NODE, 276, -48.3620529, -54.4540367, 0.0
NODE, 277, 0.768415987, -80.8058777, 0.0
NODE, 278, -17.8797646, -78.3998871, 0.0
NODE, 279, -9.11715603, -80.6928711, 0.0
NODE, 280, -26.8911228, -76.4298401, 0.0
NODE, 281, 26.4986324, -65.6561203, 0.0
NODE, 282, 11.0517788, -78.4037704, 0.0
NODE, 283, -51.8210411, -19.5778961, 0.0
NODE, 284, -51.892189, -62.6751328, 0.0
NODE, 285, -29.3777847, -83.860817, 0.0
NODE, 286, -15.6608143, -86.0365601, 0.0
NODE, 287, -44.365242, -72.5934372, 0.0
NODE, 288, -4.64264727, -86.4383698, 0.0
NODE, 289, -57.7701454, -39.3672676, 0.0
NODE, 290, -57.5424919, -33.1550941, 0.0
NODE, 291, -58.7053909, -45.3667908, 0.0
NODE, 292, 7.01764345, -85.4618225, 0.0
NODE, 293, -40.37994, -77.640007, 0.0
NODE, 294, -34.6293793, -80.2179413, 0.0
NODE, 295, -56.5817528, -51.2535439, 0.0
NODE, 296, -9.83552837, -87.7984467, 0.0
NODE, 297, -55.6726952, -57.5262794, 0.0
NODE, 298, -23.0611229, -84.5323715, 0.0
NODE, 299, -49.3423233, -68.578331, 0.0
NODE, 300, 31.5452328, -59.1639862, 0.0
NODE, 301, 37.2747421, -39.1690674, 0.0
#
#
#
ELEMENT, TRI3N, 1, 0, 129, 125, 72
ELEMENT, TRI3N, 2, 0, 130, 9, 128
ELEMENT, TRI3N, 3, 0, 175, 155, 59
ELEMENT, TRI3N, 4, 0, 185, 155, 175
ELEMENT, TRI3N, 5, 0, 164, 156, 141
ELEMENT, TRI3N, 6, 0, 152, 121, 123
ELEMENT, TRI3N, 7, 0, 160, 159, 145
ELEMENT, TRI3N, 8, 0, 115, 56, 57
ELEMENT, TRI3N, 9, 0, 173, 158, 159
ELEMENT, TRI3N, 10, 0, 161, 157, 150
ELEMENT, TRI3N, 11, 0, 161, 150, 149
ELEMENT, TRI3N, 12, 0, 146, 100, 144
ELEMENT, TRI3N, 13, 0, 176, 148, 21
ELEMENT, TRI3N, 14, 0, 176, 163, 148
ELEMENT, TRI3N, 15, 0, 242, 228, 92
ELEMENT, TRI3N, 16, 0, 290, 250, 289
ELEMENT, TRI3N, 17, 0, 283, 267, 270
ELEMENT, TRI3N, 18, 0, 251, 91, 250
ELEMENT, TRI3N, 19, 0, 291, 289, 265
ELEMENT, TRI3N, 20, 0, 290, 289, 275
ELEMENT, TRI3N, 21, 0, 259, 255, 33
ELEMENT, TRI3N, 22, 0, 297, 261, 284
ELEMENT, TRI3N, 23, 0, 245, 32, 88
ELEMENT, TRI3N, 24, 0, 287, 274, 271
ELEMENT, TRI3N, 25, 0, 293, 287, 252
ELEMENT, TRI3N, 26, 0, 257, 29, 249
ELEMENT, TRI3N, 27, 0, 294, 257, 285
ELEMENT, TRI3N, 28, 0, 249, 29, 86
ELEMENT, TRI3N, 29, 0, 258, 85, 254
ELEMENT, TRI3N, 30, 0, 298, 278, 280
ELEMENT, TRI3N, 31, 0, 296, 279, 286
ELEMENT, TRI3N, 32, 0, 247, 83, 244
ELEMENT, TRI3N, 33, 0, 272, 244, 268
ELEMENT, TRI3N, 34, 0, 268, 244, 25
ELEMENT, TRI3N, 35, 0, 281, 272, 269
ELEMENT, TRI3N, 36, 0, 281, 44, 45
ELEMENT, TRI3N, 37, 0, 262, 22, 80
ELEMENT, TRI3N, 38, 0, 301, 139, 42
ELEMENT, TRI3N, 39, 0, 139, 41, 40
ELEMENT, TRI3N, 40, 0, 139, 40, 39
ELEMENT, TRI3N, 41, 0, 172, 119, 162
ELEMENT, TRI3N, 42, 0, 220, 209, 218
ELEMENT, TRI3N, 43, 0, 239, 74, 224
ELEMENT, TRI3N, 44, 0, 233, 232, 132
ELEMENT, TRI3N, 45, 0, 233, 112, 62
ELEMENT, TRI3N, 46, 0, 235, 63, 112
ELEMENT, TRI3N, 47, 0, 234, 230, 134
ELEMENT, TRI3N, 48, 0, 235, 230, 63
ELEMENT, TRI3N, 49, 0, 134, 4, 3
ELEMENT, TRI3N, 50, 0, 234, 65, 230
ELEMENT, TRI3N, 51, 0, 236, 113, 234
ELEMENT, TRI3N, 52, 0, 231, 135, 126
ELEMENT, TRI3N, 53, 0, 236, 135, 231
ELEMENT, TRI3N, 54, 0, 231, 229, 114
ELEMENT, TRI3N, 55, 0, 229, 126, 124
ELEMENT, TRI3N, 56, 0, 229, 69, 114
ELEMENT, TRI3N, 57, 0, 237, 109, 61
ELEMENT, TRI3N, 58, 0, 238, 225, 109
ELEMENT, TRI3N, 59, 0, 162, 140, 156
ELEMENT, TRI3N, 60, 0, 140, 119, 16
ELEMENT, TRI3N, 61, 0, 119, 15, 16
ELEMENT, TRI3N, 62, 0, 139, 39, 42
ELEMENT, TRI3N, 63, 0, 262, 80, 243
ELEMENT, TRI3N, 64, 0, 300, 248, 94
ELEMENT, TRI3N, 65, 0, 292, 266, 264
ELEMENT, TRI3N, 66, 0, 228, 197, 37
ELEMENT, TRI3N, 67, 0, 237, 69, 229
ELEMENT, TRI3N, 68, 0, 235, 137, 127
ELEMENT, TRI3N, 69, 0, 233, 13, 232
ELEMENT, TRI3N, 70, 0, 135, 70, 2
ELEMENT, TRI3N, 71, 0, 132, 71, 6
ELEMENT, TRI3N, 72, 0, 221, 129, 219
ELEMENT, TRI3N, 73, 0, 224, 75, 210
ELEMENT, TRI3N, 74, 0, 239, 224, 227
ELEMENT, TRI3N, 75, 0, 210, 76, 201
ELEMENT, TRI3N, 76, 0, 172, 14, 119
ELEMENT, TRI3N, 77, 0, 141, 17, 116
ELEMENT, TRI3N, 78, 0, 149, 148, 146
ELEMENT, TRI3N, 79, 0, 148, 78, 21
ELEMENT, TRI3N, 80, 0, 243, 38, 139
ELEMENT, TRI3N, 81, 0, 248, 43, 94
ELEMENT, TRI3N, 82, 0, 269, 24, 246
ELEMENT, TRI3N, 83, 0, 282, 247, 244
ELEMENT, TRI3N, 84, 0, 264, 26, 247
ELEMENT, TRI3N, 85, 0, 254, 85, 27
ELEMENT, TRI3N, 86, 0, 296, 254, 288
ELEMENT, TRI3N, 87, 0, 294, 274, 293
ELEMENT, TRI3N, 88, 0, 299, 271, 284
ELEMENT, TRI3N, 89, 0, 261, 32, 245
ELEMENT, TRI3N, 90, 0, 255, 90, 33
ELEMENT, TRI3N, 91, 0, 250, 91, 34
ELEMENT, TRI3N, 92, 0, 242, 240, 228
ELEMENT, TRI3N, 93, 0, 197, 176, 93
ELEMENT, TRI3N, 94, 0, 300, 253, 248
ELEMENT, TRI3N, 95, 0, 282, 244, 272
ELEMENT, TRI3N, 96, 0, 298, 256, 286
ELEMENT, TRI3N, 97, 0, 299, 287, 271
ELEMENT, TRI3N, 98, 0, 289, 250, 265
ELEMENT, TRI3N, 99, 0, 205, 54, 163
ELEMENT, TRI3N, 100, 0, 144, 101, 142
ELEMENT, TRI3N, 101, 0, 150, 117, 20
ELEMENT, TRI3N, 102, 0, 145, 143, 103
ELEMENT, TRI3N, 103, 0, 160, 147, 151
ELEMENT, TRI3N, 104, 0, 147, 56, 115
ELEMENT, TRI3N, 105, 0, 153, 121, 152
ELEMENT, TRI3N, 106, 0, 168, 152, 166
ELEMENT, TRI3N, 107, 0, 123, 108, 120
ELEMENT, TRI3N, 108, 0, 155, 58, 59
ELEMENT, TRI3N, 109, 0, 238, 237, 138
ELEMENT, TRI3N, 110, 0, 238, 125, 225
ELEMENT, TRI3N, 111, 0, 225, 212, 110
ELEMENT, TRI3N, 112, 0, 235, 233, 137
ELEMENT, TRI3N, 113, 0, 234, 134, 133
ELEMENT, TRI3N, 114, 0, 236, 231, 67
ELEMENT, TRI3N, 115, 0, 115, 57, 105
ELEMENT, TRI3N, 116, 0, 122, 106, 121
ELEMENT, TRI3N, 117, 0, 116, 17, 19
ELEMENT, TRI3N, 118, 0, 118, 116, 19
ELEMENT, TRI3N, 119, 0, 143, 142, 102
ELEMENT, TRI3N, 120, 0, 117, 18, 20
ELEMENT, TRI3N, 121, 0, 118, 19, 18
ELEMENT, TRI3N, 122, 0, 118, 18, 117
ELEMENT, TRI3N, 123, 0, 119, 14, 15
ELEMENT, TRI3N, 124, 0, 140, 16, 77
ELEMENT, TRI3N, 125, 0, 120, 108, 58
ELEMENT, TRI3N, 126, 0, 130, 129, 10
ELEMENT, TRI3N, 127, 0, 121, 106, 107
ELEMENT, TRI3N, 128, 0, 123, 121, 107
ELEMENT, TRI3N, 129, 0, 165, 105, 122
ELEMENT, TRI3N, 130, 0, 122, 105, 106
ELEMENT, TRI3N, 131, 0, 123, 107, 108
ELEMENT, TRI3N, 132, 0, 154, 152, 123
ELEMENT, TRI3N, 133, 0, 124, 1, 12
ELEMENT, TRI3N, 134, 0, 138, 124, 12
ELEMENT, TRI3N, 135, 0, 125, 11, 72
ELEMENT, TRI3N, 136, 0, 129, 72, 10
ELEMENT, TRI3N, 137, 0, 126, 2, 1
ELEMENT, TRI3N, 138, 0, 126, 1, 124
ELEMENT, TRI3N, 139, 0, 127, 5, 4
ELEMENT, TRI3N, 140, 0, 134, 127, 4
ELEMENT, TRI3N, 141, 0, 128, 9, 8
ELEMENT, TRI3N, 142, 0, 136, 128, 8
ELEMENT, TRI3N, 143, 0, 130, 10, 9
ELEMENT, TRI3N, 144, 0, 189, 175, 60
ELEMENT, TRI3N, 145, 0, 170, 162, 156
ELEMENT, TRI3N, 146, 0, 207, 169, 185
ELEMENT, TRI3N, 147, 0, 131, 7, 71
ELEMENT, TRI3N, 148, 0, 132, 131, 71
ELEMENT, TRI3N, 149, 0, 137, 132, 6
ELEMENT, TRI3N, 150, 0, 232, 13, 73
ELEMENT, TRI3N, 151, 0, 133, 3, 70
ELEMENT, TRI3N, 152, 0, 135, 133, 70
ELEMENT, TRI3N, 153, 0, 134, 3, 133
ELEMENT, TRI3N, 154, 0, 230, 65, 64
ELEMENT, TRI3N, 155, 0, 135, 2, 126
ELEMENT, TRI3N, 156, 0, 236, 67, 66
ELEMENT, TRI3N, 157, 0, 136, 8, 7
ELEMENT, TRI3N, 158, 0, 136, 7, 131
ELEMENT, TRI3N, 159, 0, 137, 6, 5
ELEMENT, TRI3N, 160, 0, 137, 5, 127
ELEMENT, TRI3N, 161, 0, 138, 12, 11
ELEMENT, TRI3N, 162, 0, 138, 11, 125
ELEMENT, TRI3N, 163, 0, 301, 42, 43
ELEMENT, TRI3N, 164, 0, 139, 38, 41
ELEMENT, TRI3N, 165, 0, 141, 77, 17
ELEMENT, TRI3N, 166, 0, 141, 140, 77
ELEMENT, TRI3N, 167, 0, 166, 152, 154
ELEMENT, TRI3N, 168, 0, 182, 177, 164
ELEMENT, TRI3N, 169, 0, 142, 101, 102
ELEMENT, TRI3N, 170, 0, 143, 102, 103
ELEMENT, TRI3N, 171, 0, 145, 103, 104
ELEMENT, TRI3N, 172, 0, 159, 143, 145
ELEMENT, TRI3N, 173, 0, 157, 144, 142
ELEMENT, TRI3N, 174, 0, 144, 100, 101
ELEMENT, TRI3N, 175, 0, 147, 145, 104
ELEMENT, TRI3N, 176, 0, 159, 158, 143
ELEMENT, TRI3N, 177, 0, 161, 146, 144
ELEMENT, TRI3N, 178, 0, 146, 55, 100
ELEMENT, TRI3N, 179, 0, 147, 104, 56
ELEMENT, TRI3N, 180, 0, 151, 147, 115
ELEMENT, TRI3N, 181, 0, 176, 21, 93
ELEMENT, TRI3N, 182, 0, 163, 146, 148
ELEMENT, TRI3N, 183, 0, 149, 79, 78
ELEMENT, TRI3N, 184, 0, 149, 78, 148
ELEMENT, TRI3N, 185, 0, 150, 20, 79
ELEMENT, TRI3N, 186, 0, 150, 79, 149
ELEMENT, TRI3N, 187, 0, 174, 173, 159
ELEMENT, TRI3N, 188, 0, 165, 151, 115
ELEMENT, TRI3N, 189, 0, 181, 179, 153
ELEMENT, TRI3N, 190, 0, 154, 123, 120
ELEMENT, TRI3N, 191, 0, 179, 167, 151
ELEMENT, TRI3N, 192, 0, 153, 122, 121
ELEMENT, TRI3N, 193, 0, 169, 120, 155
ELEMENT, TRI3N, 194, 0, 204, 198, 196
ELEMENT, TRI3N, 195, 0, 155, 120, 58
ELEMENT, TRI3N, 196, 0, 175, 59, 60
ELEMENT, TRI3N, 197, 0, 186, 172, 162
ELEMENT, TRI3N, 198, 0, 156, 140, 141
ELEMENT, TRI3N, 199, 0, 158, 157, 142
ELEMENT, TRI3N, 200, 0, 157, 117, 150
ELEMENT, TRI3N, 201, 0, 158, 117, 157
ELEMENT, TRI3N, 202, 0, 158, 142, 143
ELEMENT, TRI3N, 203, 0, 160, 145, 147
ELEMENT, TRI3N, 204, 0, 174, 159, 160
ELEMENT, TRI3N, 205, 0, 181, 167, 179
ELEMENT, TRI3N, 206, 0, 174, 160, 167
ELEMENT, TRI3N, 207, 0, 161, 149, 146
ELEMENT, TRI3N, 208, 0, 161, 144, 157
ELEMENT, TRI3N, 209, 0, 186, 162, 170
ELEMENT, TRI3N, 210, 0, 162, 119, 140
ELEMENT, TRI3N, 211, 0, 163, 54, 55
ELEMENT, TRI3N, 212, 0, 163, 55, 146
ELEMENT, TRI3N, 213, 0, 164, 141, 116
ELEMENT, TRI3N, 214, 0, 187, 174, 167
ELEMENT, TRI3N, 215, 0, 165, 115, 105
ELEMENT, TRI3N, 216, 0, 165, 122, 153
ELEMENT, TRI3N, 217, 0, 180, 154, 169
ELEMENT, TRI3N, 218, 0, 204, 182, 191
ELEMENT, TRI3N, 219, 0, 167, 160, 151
ELEMENT, TRI3N, 220, 0, 179, 151, 165
ELEMENT, TRI3N, 221, 0, 193, 191, 182
ELEMENT, TRI3N, 222, 0, 168, 153, 152
ELEMENT, TRI3N, 223, 0, 207, 199, 180
ELEMENT, TRI3N, 224, 0, 169, 154, 120
ELEMENT, TRI3N, 225, 0, 177, 170, 156
ELEMENT, TRI3N, 226, 0, 200, 188, 198
ELEMENT, TRI3N, 227, 0, 171, 164, 116
ELEMENT, TRI3N, 228, 0, 183, 116, 118
ELEMENT, TRI3N, 229, 0, 194, 172, 186
ELEMENT, TRI3N, 230, 0, 201, 14, 172
ELEMENT, TRI3N, 231, 0, 173, 118, 117
ELEMENT, TRI3N, 232, 0, 173, 117, 158
ELEMENT, TRI3N, 233, 0, 187, 183, 184
ELEMENT, TRI3N, 234, 0, 184, 173, 174
ELEMENT, TRI3N, 235, 0, 189, 60, 111
ELEMENT, TRI3N, 236, 0, 195, 175, 189
ELEMENT, TRI3N, 237, 0, 197, 93, 37
ELEMENT, TRI3N, 238, 0, 205, 163, 176
ELEMENT, TRI3N, 239, 0, 177, 156, 164
ELEMENT, TRI3N, 240, 0, 196, 188, 177
ELEMENT, TRI3N, 241, 0, 178, 168, 166
ELEMENT, TRI3N, 242, 0, 190, 166, 180
ELEMENT, TRI3N, 243, 0, 179, 165, 153
ELEMENT, TRI3N, 244, 0, 181, 153, 168
ELEMENT, TRI3N, 245, 0, 206, 200, 198
ELEMENT, TRI3N, 246, 0, 180, 166, 154
ELEMENT, TRI3N, 247, 0, 191, 168, 178
ELEMENT, TRI3N, 248, 0, 193, 181, 191
ELEMENT, TRI3N, 249, 0, 182, 164, 171
ELEMENT, TRI3N, 250, 0, 193, 171, 187
ELEMENT, TRI3N, 251, 0, 183, 171, 116
ELEMENT, TRI3N, 252, 0, 184, 183, 118
ELEMENT, TRI3N, 253, 0, 184, 118, 173
ELEMENT, TRI3N, 254, 0, 187, 184, 174
ELEMENT, TRI3N, 255, 0, 213, 207, 195
ELEMENT, TRI3N, 256, 0, 185, 169, 155
ELEMENT, TRI3N, 257, 0, 192, 170, 188
ELEMENT, TRI3N, 258, 0, 202, 186, 192
ELEMENT, TRI3N, 259, 0, 187, 167, 181
ELEMENT, TRI3N, 260, 0, 187, 171, 183
ELEMENT, TRI3N, 261, 0, 208, 202, 192
ELEMENT, TRI3N, 262, 0, 188, 170, 177
ELEMENT, TRI3N, 263, 0, 212, 203, 189
ELEMENT, TRI3N, 264, 0, 203, 195, 189
ELEMENT, TRI3N, 265, 0, 190, 178, 166
ELEMENT, TRI3N, 266, 0, 199, 190, 180
ELEMENT, TRI3N, 267, 0, 191, 181, 168
ELEMENT, TRI3N, 268, 0, 204, 196, 182
ELEMENT, TRI3N, 269, 0, 202, 194, 186
ELEMENT, TRI3N, 270, 0, 192, 186, 170
ELEMENT, TRI3N, 271, 0, 193, 182, 171
ELEMENT, TRI3N, 272, 0, 193, 187, 181
ELEMENT, TRI3N, 273, 0, 215, 202, 208
ELEMENT, TRI3N, 274, 0, 210, 194, 209
ELEMENT, TRI3N, 275, 0, 219, 211, 203
ELEMENT, TRI3N, 276, 0, 195, 185, 175
ELEMENT, TRI3N, 277, 0, 196, 177, 182
ELEMENT, TRI3N, 278, 0, 198, 178, 190
ELEMENT, TRI3N, 279, 0, 228, 37, 92
ELEMENT, TRI3N, 280, 0, 240, 197, 228
ELEMENT, TRI3N, 281, 0, 206, 190, 199
ELEMENT, TRI3N, 282, 0, 198, 188, 196
ELEMENT, TRI3N, 283, 0, 207, 180, 169
ELEMENT, TRI3N, 284, 0, 223, 214, 200
ELEMENT, TRI3N, 285, 0, 217, 215, 208
ELEMENT, TRI3N, 286, 0, 200, 192, 188
ELEMENT, TRI3N, 287, 0, 201, 76, 14
ELEMENT, TRI3N, 288, 0, 201, 172, 194
ELEMENT, TRI3N, 289, 0, 208, 192, 200
ELEMENT, TRI3N, 290, 0, 218, 209, 215
ELEMENT, TRI3N, 291, 0, 212, 189, 111
ELEMENT, TRI3N, 292, 0, 241, 226, 216
ELEMENT, TRI3N, 293, 0, 204, 191, 178
ELEMENT, TRI3N, 294, 0, 204, 178, 198
ELEMENT, TRI3N, 295, 0, 205, 99, 54
ELEMENT, TRI3N, 296, 0, 205, 176, 197
ELEMENT, TRI3N, 297, 0, 206, 198, 190
ELEMENT, TRI3N, 298, 0, 216, 213, 211
ELEMENT, TRI3N, 299, 0, 207, 185, 195
ELEMENT, TRI3N, 300, 0, 213, 195, 211
ELEMENT, TRI3N, 301, 0, 223, 200, 206
ELEMENT, TRI3N, 302, 0, 215, 209, 202
ELEMENT, TRI3N, 303, 0, 227, 220, 136
ELEMENT, TRI3N, 304, 0, 209, 194, 202
ELEMENT, TRI3N, 305, 0, 210, 75, 76
ELEMENT, TRI3N, 306, 0, 210, 201, 194
ELEMENT, TRI3N, 307, 0, 211, 195, 203
ELEMENT, TRI3N, 308, 0, 226, 222, 217
ELEMENT, TRI3N, 309, 0, 212, 111, 110
ELEMENT, TRI3N, 310, 0, 225, 221, 212
ELEMENT, TRI3N, 311, 0, 223, 199, 213
ELEMENT, TRI3N, 312, 0, 213, 199, 207
ELEMENT, TRI3N, 313, 0, 223, 216, 214
ELEMENT, TRI3N, 314, 0, 214, 208, 200
ELEMENT, TRI3N, 315, 0, 217, 208, 214
ELEMENT, TRI3N, 316, 0, 222, 218, 215
ELEMENT, TRI3N, 317, 0, 219, 216, 211
ELEMENT, TRI3N, 318, 0, 226, 217, 216
ELEMENT, TRI3N, 319, 0, 217, 214, 216
ELEMENT, TRI3N, 320, 0, 222, 130, 128
ELEMENT, TRI3N, 321, 0, 218, 128, 136
ELEMENT, TRI3N, 322, 0, 220, 218, 136
ELEMENT, TRI3N, 323, 0, 221, 219, 203
ELEMENT, TRI3N, 324, 0, 241, 129, 130
ELEMENT, TRI3N, 325, 0, 227, 224, 220
ELEMENT, TRI3N, 326, 0, 220, 210, 209
ELEMENT, TRI3N, 327, 0, 221, 125, 129
ELEMENT, TRI3N, 328, 0, 221, 203, 212
ELEMENT, TRI3N, 329, 0, 222, 128, 218
ELEMENT, TRI3N, 330, 0, 222, 215, 217
ELEMENT, TRI3N, 331, 0, 223, 206, 199
ELEMENT, TRI3N, 332, 0, 223, 213, 216
ELEMENT, TRI3N, 333, 0, 224, 74, 75
ELEMENT, TRI3N, 334, 0, 224, 210, 220
ELEMENT, TRI3N, 335, 0, 225, 110, 109
ELEMENT, TRI3N, 336, 0, 225, 125, 221
ELEMENT, TRI3N, 337, 0, 241, 216, 219
ELEMENT, TRI3N, 338, 0, 226, 130, 222
ELEMENT, TRI3N, 339, 0, 227, 136, 131
ELEMENT, TRI3N, 340, 0, 239, 131, 232
ELEMENT, TRI3N, 341, 0, 242, 92, 36
ELEMENT, TRI3N, 342, 0, 240, 205, 197
ELEMENT, TRI3N, 343, 0, 237, 229, 124
ELEMENT, TRI3N, 344, 0, 231, 114, 68
ELEMENT, TRI3N, 345, 0, 230, 64, 63
ELEMENT, TRI3N, 346, 0, 230, 127, 134
ELEMENT, TRI3N, 347, 0, 231, 126, 229
ELEMENT, TRI3N, 348, 0, 231, 68, 67
ELEMENT, TRI3N, 349, 0, 239, 232, 73
ELEMENT, TRI3N, 350, 0, 232, 131, 132
ELEMENT, TRI3N, 351, 0, 233, 62, 13
ELEMENT, TRI3N, 352, 0, 233, 132, 137
ELEMENT, TRI3N, 353, 0, 236, 234, 133
ELEMENT, TRI3N, 354, 0, 234, 113, 65
ELEMENT, TRI3N, 355, 0, 235, 127, 230
ELEMENT, TRI3N, 356, 0, 235, 112, 233
ELEMENT, TRI3N, 357, 0, 236, 66, 113
ELEMENT, TRI3N, 358, 0, 236, 133, 135
ELEMENT, TRI3N, 359, 0, 237, 61, 69
ELEMENT, TRI3N, 360, 0, 237, 124, 138
ELEMENT, TRI3N, 361, 0, 238, 109, 237
ELEMENT, TRI3N, 362, 0, 238, 138, 125
ELEMENT, TRI3N, 363, 0, 239, 73, 74
ELEMENT, TRI3N, 364, 0, 239, 227, 131
ELEMENT, TRI3N, 365, 0, 240, 53, 99
ELEMENT, TRI3N, 366, 0, 240, 99, 205
ELEMENT, TRI3N, 367, 0, 241, 219, 129
ELEMENT, TRI3N, 368, 0, 241, 130, 226
ELEMENT, TRI3N, 369, 0, 267, 36, 35
ELEMENT, TRI3N, 370, 0, 283, 270, 53
ELEMENT, TRI3N, 371, 0, 262, 248, 22
ELEMENT, TRI3N, 372, 0, 243, 80, 38
ELEMENT, TRI3N, 373, 0, 244, 83, 25
ELEMENT, TRI3N, 374, 0, 268, 25, 82
ELEMENT, TRI3N, 375, 0, 263, 88, 31
ELEMENT, TRI3N, 376, 0, 297, 276, 295
ELEMENT, TRI3N, 377, 0, 246, 24, 23
ELEMENT, TRI3N, 378, 0, 253, 23, 81
ELEMENT, TRI3N, 379, 0, 292, 282, 277
ELEMENT, TRI3N, 380, 0, 247, 26, 83
ELEMENT, TRI3N, 381, 0, 300, 94, 44
ELEMENT, TRI3N, 382, 0, 248, 81, 22
ELEMENT, TRI3N, 383, 0, 256, 86, 28
ELEMENT, TRI3N, 384, 0, 294, 280, 274
ELEMENT, TRI3N, 385, 0, 265, 34, 90
ELEMENT, TRI3N, 386, 0, 290, 270, 251
ELEMENT, TRI3N, 387, 0, 270, 267, 251
ELEMENT, TRI3N, 388, 0, 251, 35, 91
ELEMENT, TRI3N, 389, 0, 252, 31, 87
ELEMENT, TRI3N, 390, 0, 260, 87, 30
ELEMENT, TRI3N, 391, 0, 253, 246, 23
ELEMENT, TRI3N, 392, 0, 253, 81, 248
ELEMENT, TRI3N, 393, 0, 266, 27, 84
ELEMENT, TRI3N, 394, 0, 288, 254, 266
ELEMENT, TRI3N, 395, 0, 259, 33, 89
ELEMENT, TRI3N, 396, 0, 295, 291, 255
ELEMENT, TRI3N, 397, 0, 256, 249, 86
ELEMENT, TRI3N, 398, 0, 258, 256, 28
ELEMENT, TRI3N, 399, 0, 257, 30, 29
ELEMENT, TRI3N, 400, 0, 298, 280, 285
ELEMENT, TRI3N, 401, 0, 258, 28, 85
ELEMENT, TRI3N, 402, 0, 286, 279, 278
ELEMENT, TRI3N, 403, 0, 261, 259, 89
ELEMENT, TRI3N, 404, 0, 295, 273, 291
ELEMENT, TRI3N, 405, 0, 260, 252, 87
ELEMENT, TRI3N, 406, 0, 260, 30, 257
ELEMENT, TRI3N, 407, 0, 261, 89, 32
ELEMENT, TRI3N, 408, 0, 284, 271, 276
ELEMENT, TRI3N, 409, 0, 301, 262, 243
ELEMENT, TRI3N, 410, 0, 262, 43, 248
ELEMENT, TRI3N, 411, 0, 263, 245, 88
ELEMENT, TRI3N, 412, 0, 263, 31, 252
ELEMENT, TRI3N, 413, 0, 292, 247, 282
ELEMENT, TRI3N, 414, 0, 264, 84, 26
ELEMENT, TRI3N, 415, 0, 265, 250, 34
ELEMENT, TRI3N, 416, 0, 265, 90, 255
ELEMENT, TRI3N, 417, 0, 266, 254, 27
ELEMENT, TRI3N, 418, 0, 266, 84, 264
ELEMENT, TRI3N, 419, 0, 267, 242, 36
ELEMENT, TRI3N, 420, 0, 267, 35, 251
ELEMENT, TRI3N, 421, 0, 269, 268, 82
ELEMENT, TRI3N, 422, 0, 272, 268, 269
ELEMENT, TRI3N, 423, 0, 269, 82, 24
ELEMENT, TRI3N, 424, 0, 281, 269, 246
ELEMENT, TRI3N, 425, 0, 270, 52, 53
ELEMENT, TRI3N, 426, 0, 283, 53, 240
ELEMENT, TRI3N, 427, 0, 271, 97, 50
ELEMENT, TRI3N, 428, 0, 276, 271, 50
ELEMENT, TRI3N, 429, 0, 272, 45, 95
ELEMENT, TRI3N, 430, 0, 282, 272, 95
ELEMENT, TRI3N, 431, 0, 273, 51, 98
ELEMENT, TRI3N, 432, 0, 275, 273, 98
ELEMENT, TRI3N, 433, 0, 274, 49, 97
ELEMENT, TRI3N, 434, 0, 274, 97, 271
ELEMENT, TRI3N, 435, 0, 275, 98, 52
ELEMENT, TRI3N, 436, 0, 275, 52, 270
ELEMENT, TRI3N, 437, 0, 276, 50, 51
ELEMENT, TRI3N, 438, 0, 276, 51, 273
ELEMENT, TRI3N, 439, 0, 277, 46, 47
ELEMENT, TRI3N, 440, 0, 279, 277, 47
ELEMENT, TRI3N, 441, 0, 278, 96, 48
ELEMENT, TRI3N, 442, 0, 280, 278, 48
ELEMENT, TRI3N, 443, 0, 279, 47, 96
ELEMENT, TRI3N, 444, 0, 279, 96, 278
ELEMENT, TRI3N, 445, 0, 280, 48, 49
ELEMENT, TRI3N, 446, 0, 280, 49, 274
ELEMENT, TRI3N, 447, 0, 300, 281, 246
ELEMENT, TRI3N, 448, 0, 281, 45, 272
ELEMENT, TRI3N, 449, 0, 282, 95, 46
ELEMENT, TRI3N, 450, 0, 282, 46, 277
ELEMENT, TRI3N, 451, 0, 283, 240, 242
ELEMENT, TRI3N, 452, 0, 283, 242, 267
ELEMENT, TRI3N, 453, 0, 284, 261, 245
ELEMENT, TRI3N, 454, 0, 299, 245, 263
ELEMENT, TRI3N, 455, 0, 285, 257, 249
ELEMENT, TRI3N, 456, 0, 298, 286, 278
ELEMENT, TRI3N, 457, 0, 286, 256, 258
ELEMENT, TRI3N, 458, 0, 296, 288, 279
ELEMENT, TRI3N, 459, 0, 287, 263, 252
ELEMENT, TRI3N, 460, 0, 293, 252, 260
ELEMENT, TRI3N, 461, 0, 288, 266, 277
ELEMENT, TRI3N, 462, 0, 288, 277, 279
ELEMENT, TRI3N, 463, 0, 291, 265, 255
ELEMENT, TRI3N, 464, 0, 289, 273, 275
ELEMENT, TRI3N, 465, 0, 290, 275, 270
ELEMENT, TRI3N, 466, 0, 290, 251, 250
ELEMENT, TRI3N, 467, 0, 295, 255, 259
ELEMENT, TRI3N, 468, 0, 291, 273, 289
ELEMENT, TRI3N, 469, 0, 292, 277, 266
ELEMENT, TRI3N, 470, 0, 292, 264, 247
ELEMENT, TRI3N, 471, 0, 294, 293, 260
ELEMENT, TRI3N, 472, 0, 293, 274, 287
ELEMENT, TRI3N, 473, 0, 294, 260, 257
ELEMENT, TRI3N, 474, 0, 294, 285, 280
ELEMENT, TRI3N, 475, 0, 297, 295, 259
ELEMENT, TRI3N, 476, 0, 295, 276, 273
ELEMENT, TRI3N, 477, 0, 296, 286, 258
ELEMENT, TRI3N, 478, 0, 296, 258, 254
ELEMENT, TRI3N, 479, 0, 297, 259, 261
ELEMENT, TRI3N, 480, 0, 297, 284, 276
ELEMENT, TRI3N, 481, 0, 298, 285, 249
ELEMENT, TRI3N, 482, 0, 298, 249, 256
ELEMENT, TRI3N, 483, 0, 299, 284, 245
ELEMENT, TRI3N, 484, 0, 299, 263, 287
ELEMENT, TRI3N, 485, 0, 300, 44, 281
ELEMENT, TRI3N, 486, 0, 300, 246, 253
ELEMENT, TRI3N, 487, 0, 301, 243, 139
ELEMENT, TRI3N, 488, 0, 301, 43, 262
#
#
#
