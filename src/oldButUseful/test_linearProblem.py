from unittest import TestCase

from linearProblem import LinearProblem
import pickle as pickle
import intermediateSymmetryFinder as sf

enlight16WithConstraints = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                            26, 27, 28, 29, 30, 31, 2, 18, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 3,
                            19,
                            35, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 4, 20, 36, 52, 68, 69, 70, 71, 72,
                            73,
                            74, 75, 76, 77, 78, 79, 5, 21, 37, 53, 69, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 6,
                            22,
                            38, 54, 70, 86, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 7, 23, 39, 55, 71, 87,
                            103,
                            119, 120, 121, 122, 123, 124, 125, 126, 127, 8, 24, 40, 56, 72, 88, 104, 120, 136, 137, 138,
                            139, 140, 141, 142, 143, 9, 25, 41, 57, 73, 89, 105, 121, 137, 153, 154, 155, 156, 157, 158,
                            159, 10, 26, 42, 58, 74, 90, 106, 122, 138, 154, 170, 171, 172, 173, 174, 175, 11, 27, 43,
                            59,
                            75, 91, 107, 123, 139, 155, 171, 187, 188, 189, 190, 191, 12, 28, 44, 60, 76, 92, 108, 124,
                            140, 156, 172, 188, 204, 205, 206, 207, 13, 29, 45, 61, 77, 93, 109, 125, 141, 157, 173,
                            189,
                            205, 221, 222, 223, 14, 30, 46, 62, 78, 94, 110, 126, 142, 158, 174, 190, 206, 222, 238,
                            239,
                            15, 31, 47, 63, 79, 95, 111, 127, 143, 159, 175, 191, 207, 223, 239, 255, 256, 257, 258,
                            259,
                            260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 257, 271, 272, 273, 274, 275, 276, 277,
                            278,
                            279, 280, 281, 282, 283, 258, 272, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296,
                            297,
                            259, 273, 287, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 260, 274, 288, 302,
                            316,
                            317, 318, 319, 320, 321, 322, 323, 324, 325, 261, 275, 289, 303, 317, 331, 332, 333, 334,
                            335,
                            336, 337, 338, 339, 262, 276, 290, 304, 318, 332, 346, 347, 348, 349, 350, 351, 352, 353,
                            263,
                            277, 291, 305, 319, 333, 347, 361, 362, 363, 364, 365, 366, 367, 264, 278, 292, 306, 320,
                            334,
                            348, 362, 376, 377, 378, 379, 380, 381, 265, 279, 293, 307, 321, 335, 349, 363, 377, 391,
                            392,
                            393, 394, 395, 266, 280, 294, 308, 322, 336, 350, 364, 378, 392, 406, 407, 408, 409, 267,
                            281,
                            295, 309, 323, 337, 351, 365, 379, 393, 407, 421, 422, 423, 268, 282, 296, 310, 324, 338,
                            352,
                            366, 380, 394, 408, 422, 436, 437, 269, 283, 297, 311, 325, 339, 353, 367, 381, 395, 409,
                            423,
                            437, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467,
                            468,
                            469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 452, 453, 454, 455, 456, 457, 458,
                            459,
                            460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477,
                            478,
                            479, 508, 509, 509, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524,
                            525,
                            513, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 514, 528, 542, 543,
                            544,
                            545, 546, 547, 548, 549, 550, 551, 552, 553, 515, 529, 543, 557, 558, 559, 560, 561, 562,
                            563,
                            564, 565, 566, 567, 516, 530, 544, 558, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581,
                            517,
                            531, 545, 559, 573, 587, 588, 589, 590, 591, 592, 593, 594, 595, 518, 532, 546, 560, 574,
                            588,
                            602, 603, 604, 605, 606, 607, 608, 609, 519, 533, 547, 561, 575, 589, 603, 617, 618, 619,
                            620,
                            621, 622, 623, 520, 534, 548, 562, 576, 590, 604, 618, 632, 633, 634, 635, 636, 637, 521,
                            535,
                            549, 563, 577, 591, 605, 619, 633, 647, 648, 649, 650, 651, 522, 536, 550, 564, 578, 592,
                            606,
                            620, 634, 648, 662, 663, 664, 665, 523, 537, 551, 565, 579, 593, 607, 621, 635, 649, 663,
                            677,
                            678, 679, 524, 538, 552, 566, 580, 594, 608, 622, 636, 650, 664, 678, 692, 693, 525, 539,
                            553,
                            567, 581, 595, 609, 623, 637, 651, 665, 679, 693, 707, 708, 709, 710, 711, 712, 713, 714,
                            715,
                            716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733,
                            734,
                            735, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724,
                            725,
                            726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 764, 765, 765, 767, 768, 769, 770, 771,
                            772,
                            773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 769, 785, 786, 787, 788, 789, 790,
                            791,
                            792, 793, 794, 795, 796, 797, 798, 799, 770, 786, 802, 803, 804, 805, 806, 807, 808, 809,
                            810,
                            811, 812, 813, 814, 815, 771, 787, 803, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828,
                            829,
                            830, 831, 772, 788, 804, 820, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847,
                            773,
                            789, 805, 821, 837, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 774, 790, 806,
                            822,
                            838, 854, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 775, 791, 807, 823, 839, 855,
                            871,
                            887, 888, 889, 890, 891, 892, 893, 894, 895, 776, 792, 808, 824, 840, 856, 872, 888, 904,
                            905,
                            906, 907, 908, 909, 910, 911, 777, 793, 809, 825, 841, 857, 873, 889, 905, 921, 922, 923,
                            924,
                            925, 926, 927, 778, 794, 810, 826, 842, 858, 874, 890, 906, 922, 938, 939, 940, 941, 942,
                            943,
                            779, 795, 811, 827, 843, 859, 875, 891, 907, 923, 939, 955, 956, 957, 958, 959, 780, 796,
                            812,
                            828, 844, 860, 876, 892, 908, 924, 940, 956, 972, 973, 974, 975, 781, 797, 813, 829, 845,
                            861,
                            877, 893, 909, 925, 941, 957, 973, 989, 990, 991, 782, 798, 814, 830, 846, 862, 878, 894,
                            910,
                            926, 942, 958, 974, 990, 1006, 1007, 783, 799, 815, 831, 847, 863, 879, 895, 911, 927, 943,
                            959, 975, 991, 1007, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034,
                            1035, 1036, 1037, 1025, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049,
                            1050, 1051, 1026, 1040, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064,
                            1065, 1027, 1041, 1055, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079,
                            1028, 1042, 1056, 1070, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1029,
                            1043, 1057, 1071, 1085, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1030, 1044,
                            1058, 1072, 1086, 1100, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1031, 1045, 1059,
                            1073, 1087, 1101, 1115, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1032, 1046, 1060, 1074,
                            1088, 1102, 1116, 1130, 1144, 1145, 1146, 1147, 1148, 1149, 1033, 1047, 1061, 1075, 1089,
                            1103, 1117, 1131, 1145, 1159, 1160, 1161, 1162, 1163, 1034, 1048, 1062, 1076, 1090, 1104,
                            1118, 1132, 1146, 1160, 1174, 1175, 1176, 1177, 1035, 1049, 1063, 1077, 1091, 1105, 1119,
                            1133, 1147, 1161, 1175, 1189, 1190, 1191, 1036, 1050, 1064, 1078, 1092, 1106, 1120, 1134,
                            1148, 1162, 1176, 1190, 1204, 1205, 1037, 1051, 1065, 1079, 1093, 1107, 1121, 1135, 1149,
                            1163, 1177, 1191, 1205, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229,
                            1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244,
                            1245, 1246, 1247, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231,
                            1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246,
                            1247, 1276, 1277, 1277, 1279]

enlight16WithoutConstraints = [0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0, 1, 17, 18, 19, 20, 21, 22, 23, 23, 22,
                               21, 20, 19, 18, 17, 1, 2, 18, 34, 35, 36, 37, 38, 39, 39, 38, 37, 36, 35, 34, 18, 2, 3,
                               19, 35, 51, 52, 53, 54, 55, 55, 54, 53, 52, 51, 35, 19, 3, 4, 20, 36, 52, 68, 69, 70, 71,
                               71, 70, 69, 68, 52, 36, 20, 4, 5, 21, 37, 53, 69, 85, 86, 87, 87, 86, 85, 69, 53, 37, 21,
                               5, 6, 22, 38, 54, 70, 86, 102, 103, 103, 102, 86, 70, 54, 38, 22, 6, 7, 23, 39, 55, 71,
                               87, 103, 119, 119, 103, 87, 71, 55, 39, 23, 7, 7, 23, 39, 55, 71, 87, 103, 119, 119, 103,
                               87, 71, 55, 39, 23, 7, 6, 22, 38, 54, 70, 86, 102, 103, 103, 102, 86, 70, 54, 38, 22, 6,
                               5, 21, 37, 53, 69, 85, 86, 87, 87, 86, 85, 69, 53, 37, 21, 5, 4, 20, 36, 52, 68, 69, 70,
                               71, 71, 70, 69, 68, 52, 36, 20, 4, 3, 19, 35, 51, 52, 53, 54, 55, 55, 54, 53, 52, 51, 35,
                               19, 3, 2, 18, 34, 35, 36, 37, 38, 39, 39, 38, 37, 36, 35, 34, 18, 2, 1, 17, 18, 19, 20,
                               21, 22, 23, 23, 22, 21, 20, 19, 18, 17, 1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1,
                               0, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
                               256, 256, 256, 256, 256, 512, 513, 514, 515, 516, 517, 518, 518, 517, 516, 515, 514, 513,
                               512, 513, 527, 528, 529, 530, 531, 532, 532, 531, 530, 529, 528, 527, 513, 514, 528, 542,
                               543, 544, 545, 546, 546, 545, 544, 543, 542, 528, 514, 515, 529, 543, 557, 558, 559, 560,
                               560, 559, 558, 557, 543, 529, 515, 516, 530, 544, 558, 572, 573, 574, 574, 573, 572, 558,
                               544, 530, 516, 517, 531, 545, 559, 573, 587, 588, 588, 587, 573, 559, 545, 531, 517, 518,
                               532, 546, 560, 574, 588, 602, 602, 588, 574, 560, 546, 532, 518, 518, 532, 546, 560, 574,
                               588, 602, 602, 588, 574, 560, 546, 532, 518, 517, 531, 545, 559, 573, 587, 588, 588, 587,
                               573, 559, 545, 531, 517, 516, 530, 544, 558, 572, 573, 574, 574, 573, 572, 558, 544, 530,
                               516, 515, 529, 543, 557, 558, 559, 560, 560, 559, 558, 557, 543, 529, 515, 514, 528, 542,
                               543, 544, 545, 546, 546, 545, 544, 543, 542, 528, 514, 513, 527, 528, 529, 530, 531, 532,
                               532, 531, 530, 529, 528, 527, 513, 512, 513, 514, 515, 516, 517, 518, 518, 517, 516, 515,
                               514, 513, 512, 708, 709, 710, 711, 712, 713, 714, 714, 713, 712, 711, 710, 709, 708, 708,
                               709, 710, 711, 712, 713, 714, 714, 713, 712, 711, 710, 709, 708, 708, 709, 710, 711, 712,
                               713, 714, 714, 713, 712, 711, 710, 709, 708, 708, 709, 710, 711, 712, 713, 714, 714, 713,
                               712, 711, 710, 709, 708, 764, 764, 764, 764]


def constructLinProblem(problemName):
    pickledProblem = pickle.load(open("../pickle/" + problemName + ".p", "rb"))
    return LinearProblem(pickledProblem.Aeq.tocoo(), pickledProblem.Aineq.tocoo(), pickledProblem.beq,
                         pickledProblem.bineq, pickledProblem.f, pickledProblem.lb, pickledProblem.ub)


class TestLinearProblem(TestCase):
    def test_findEqSymmetriesEnlight16(self):
        linProblem = constructLinProblem("enlight16")
        symmetries = linProblem.findEqSymmetriesIntermediate()
        # TODO: Think about why the constraint orbits has changed?
        self.assertEqual(symmetries[0:512][1], enlight16WithConstraints[0:512])

    def test_superposedSymmetriesWithConstraintsEnlight16(self):
        linProblem = constructLinProblem("enlight16")

        symmetriesIntermediate = linProblem.findEqSymmetriesIntermediate()
        symmetriesSuperposition = linProblem.findEqSymmetriesSuperposition()

        # TODO[michaelr]: Should this actually go to 512?
        self.assertEqual(symmetriesSuperposition[1][0:256], enlight16WithConstraints[0:256])
        self.assertEqual(symmetriesIntermediate[1][0:512], enlight16WithConstraints[0:512])

    def test_superposedSymmetriesWithConstraintsCov1075(self):
        linProblem = constructLinProblem("cov1075")
        symmetriesIneqIntermediate = linProblem.findIneqSymmetriesIntermediate()
        symmetriesIneqSuperposition = linProblem.findIneqSymmetriesSuperposition()
        self.assertEqual(symmetriesIneqIntermediate[1], symmetriesIneqSuperposition[1])

    def test_filthy(self):
        linProblem = constructLinProblem("enlight16")
        symmetries = sf.findSymmetries(linProblem)

        # TODO[michaelr]: Why is this only equal up to 512?
        self.assertEqual(symmetries[0:linProblem.numVarsEq], enlight16WithConstraints[0:linProblem.numVarsEq])