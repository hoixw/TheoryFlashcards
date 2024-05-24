from utils import build_flashcards
from argparse import ArgumentParser

CAR_DICT = {
    "Alertness": [32417, 32421, 32422, 32408, 32429, 32428, 32424, 32415, 32423, 32425, 32431, 32409, 32406, 32411, 32410, 32414, 32427, 32407, 32420, 32418, 32416, 32419, 32413, 32412, 32426, 32430],
    "Attitude": [32493, 32474, 32480, 32492, 32483, 32491, 32463, 32476, 32467, 32488, 32479, 32462, 32481, 32477, 32469, 32498, 32497, 32468, 32471, 32465, 32485, 32495, 32475, 32478, 32484, 32496, 32460, 32473, 32482, 32486, 32489, 32470, 32464, 32461, 32487, 32490, 32494, 32466, 32472],
    "Safety & Your Vehicle": [34864, 34899, 34908, 34898, 34852, 34848, 34903, 34877, 34872, 34905, 34891, 34907, 34869, 34868, 34916, 34885, 34888, 34902, 34873, 34865, 34843, 34867, 34896, 34870, 34917, 34886, 34876, 34857, 34851, 34853, 34910, 34862, 34912, 34875, 34880, 34860, 34914, 34889, 34855, 34882, 34854, 34850, 34915, 34884, 34858, 34847, 34881, 34874, 34901, 34878, 34863, 34909, 34911, 34842, 34861, 34897, 34849, 34871, 34841, 34895, 34887, 34883, 34859, 34892, 34846, 34879, 34904, 34906, 34893, 34894, 34844, 34890, 34845, 34900, 34913, 34856, 34866],
    "Safety Margins": [34982, 34986, 34983, 34957, 34970, 34987, 34984, 34958, 34962, 34989, 34973, 34969, 34972, 34965, 34960, 34975, 34968, 34974, 34961, 34979, 34988, 34978, 34967, 34963, 34985, 34981, 34971, 34956, 34959, 34977, 34976, 34980, 34964, 34966],
    "Hazard Awareness": [33730, 33761, 33748, 33721, 33762, 33716, 33747, 33751, 33729, 33711, 33739, 33746, 33742, 33728, 33708, 33753, 33767, 33707, 33715, 33743, 33712, 33759, 33709, 33737, 33764, 33694, 33763, 33714, 33701, 33724, 33696, 33760, 33722, 33741, 33735, 33700, 33733, 33765, 33750, 33718, 33738, 33693, 33720, 33695, 33755, 33691, 33719, 33752, 33744, 33704, 33726, 33756, 33740, 33717, 33697, 33710, 33713, 33699, 33731, 33705, 33698, 33690, 33734, 33754, 33745, 33757, 33727, 33723, 33706, 33692, 33703, 33749, 33725, 33736, 33758, 33702, 33766, 33732],
    "Vulnerable Road Users": [35667, 35652, 35666, 35630, 35670, 35669, 35558, 35657, 35655, 35662, 35626, 35684, 35661, 35682, 35627, 35675, 35645, 35671, 35647, 35659, 35663, 35680, 35685, 35640, 35631, 35653, 35691, 35638, 35673, 35690, 35632, 35628, 35674, 35635, 35677, 35643, 35683, 35679, 35650, 35625, 35660, 35676, 35649, 35654, 35636, 35642, 35637, 35559, 35634, 35629, 35665, 35644, 35646, 35672, 35681, 35668, 35678, 35689, 35648, 35639, 35561, 35641, 35664, 35656, 35658, 35651, 35688, 35633, 35687, 35686, 35560],
    "Other Types of Vehicle": [34235, 34251, 34244, 34242, 34232, 34234, 34236, 34243, 34249, 34239, 34245, 34252, 34237, 34246, 34250, 34253, 34247, 34248, 34233, 34241, 34238, 34240],
    "Vehicle Handling": [35363, 35351, 35383, 35347, 35350, 35354, 35365, 35366, 35359, 35380, 35368, 35377, 35375, 35342, 35367, 35369, 35362, 35358, 35386, 35349, 35345, 35346, 35378, 35385, 35373, 35353, 35356, 35374, 35376, 35360, 35357, 35361, 35381, 35348, 35384, 35371, 35379, 35372, 35343, 35355, 35382, 35364, 35352, 35370, 35344],
    "Motorway Rules": [34087, 34091, 34082, 34088, 34093, 34111, 34123, 34126, 34104, 34092, 34119, 34105, 34113, 34103, 34097, 34108, 34027, 34117, 34077, 34089, 34095, 34121, 34124, 34026, 34118, 34101, 34122, 34115, 34128, 34125, 34129, 34131, 34080, 34112, 34079, 34083, 34098, 34109, 34127, 34090, 34086, 34107, 34096, 34084, 34106, 34078, 34094, 34102, 34116, 34085, 34120, 34100, 34114, 34081, 34099, 34110, 34130],
    "Rules of the Road": [34712, 34704, 34731, 34738, 34708, 34732, 34752, 34698, 34716, 34723, 34733, 34714, 34749, 34725, 34713, 34702, 34760, 34756, 34701, 34744, 34715, 34703, 34743, 34748, 34728, 34735, 34700, 34722, 34737, 34726, 34719, 34761, 34707, 34724, 34709, 34745, 34711, 34747, 34753, 34717, 34740, 34710, 34720, 34695, 34730, 34718, 34721, 34739, 34757, 34736, 34754, 34696, 34727, 34729, 34734, 34758, 34742, 34746, 34697, 34706, 34755, 34750, 34741, 34759, 34699, 34751, 34705],
    "Road and Traffic Signs": [34563, 34558, 34568, 34580, 34540, 34609, 34561, 34530, 34597, 34516, 34599, 34574, 34616, 34548, 34589, 34550, 34588, 34594, 34515, 34551, 34638, 34533, 34578, 34514, 34555, 34581, 34585, 34532, 34527, 34626, 34557, 34633, 34590, 34641, 34531, 34534, 34579, 34615, 34620, 34522, 34544, 34556, 34521, 34547, 34552, 34559, 34631, 34545, 34605, 34622, 34553, 34570, 34603, 34543, 34592, 34600, 34565, 34567, 34602, 34538, 34528, 34630, 34632, 34537, 34564, 34628, 34549, 34624, 34618, 34541, 34572, 34596, 34617, 34523, 34519, 34595, 34575, 34607, 34542, 34613, 34536, 34598, 34510, 34637, 34621, 34569, 34593, 34586, 34529, 34525, 34518, 34636, 34604, 34634, 34576, 34611, 34625, 34606, 34566, 34640, 34511, 34612, 34584, 34608, 34520, 34627, 34591, 34560, 34587, 34562, 34614, 34512, 34639, 34526, 34554, 34577, 34539, 34524, 34583, 34582, 34535, 34546, 34623, 34513, 34571, 34601, 34573, 34635, 34642, 34610, 34517, 34629, 34619],
    "Documents": [33612, 33602, 33607, 33609, 33624, 33613, 33606, 33627, 33605, 33619, 33625, 33603, 33611, 33623, 33614, 33620, 33621, 33617, 33626, 33604, 33628, 33616, 33615, 33608, 33618, 33610, 33622, 33601],
    "Incidents, Accidents, Emergencies": [33878, 33895, 33909, 33902, 33912, 33899, 33879, 33826, 33888, 33901, 33896, 33910, 33877, 33900, 33869, 33908, 33873, 33887, 33875, 33892, 33891, 33881, 33872, 33876, 33874, 33914, 33827, 33884, 33913, 33880, 33890, 33882, 33871, 33904, 33883, 33894, 33885, 33898, 33906, 33903, 33893, 33889, 33897, 33886, 33870, 33907, 33905, 33911],
    "Vehicle Loading": [35399, 35388, 35407, 35401, 35393, 35391, 35400, 35402, 35392, 35389, 35398, 35390, 35406, 35397, 35405, 35396, 35408, 35394, 35404, 35395, 35403],
}

MOTORBIKE_DICT = {
    "Alertness": [32377, 32374, 32386, 32381, 32392, 32393, 32373, 32391, 32395, 32405, 32385, 32390, 32380, 32375, 32387, 32382, 32399, 32389, 32384, 32378, 32398, 32379, 32394, 32404, 32402, 32388, 32396, 32383, 32397, 32376, 32401, 32400, 32403], 
    "Attitude": [32434, 32441, 32432, 32451, 32449, 32440, 32445, 32450, 32456, 32453, 32436, 32433, 32446, 32443, 32438, 32454, 32442, 32455, 32459, 32447, 32458, 32435, 32452, 32439, 32448, 32457, 32437, 32444], 
    "Safety & Your Motorcycle": [34762, 34763, 34806, 34764, 34811, 34840, 34791, 34789, 34777, 34798, 34786, 34815, 34771, 34816, 34832, 34774, 34808, 34810, 34807, 34799, 34765, 34766, 34821, 34836, 34803, 34827, 34783, 34782, 34819, 34779, 34809, 34773, 34785, 34787, 34817, 34814, 34780, 34772, 34768, 34812, 34834, 34805, 34835, 34826, 34802, 34801, 34796, 34839, 34784, 34767, 34804, 34831, 34778, 34824, 34837, 34828, 34770, 34838, 34781, 34829, 34792, 34797, 34830, 34833, 34795, 34793, 34813, 34820, 34790, 34800, 34794, 34788, 34769, 34775, 34823, 34822, 34818, 34776, 34825],
    "Safety Margins": [34952, 34922, 34942, 34925, 34938, 34945, 34944, 34951, 34933, 34926, 34929, 34953, 34943, 34932, 34934, 34923, 34931, 34946, 34949, 34936, 34954, 34928, 34947, 34930, 34937, 34950, 34918, 34955, 34941, 34919, 34924, 34920, 34927, 34948, 34935, 34940, 34939, 34921], 
    "Hazard Awareness": [33650, 33670, 33656, 33680, 33685, 33651, 33667, 33642, 33645, 33675, 33669, 33658, 33672, 33678, 33682, 33643, 33648, 33652, 33676, 33664, 33641, 33665, 33688, 33681, 33661, 33639, 33653, 33660, 33671, 33646, 33657, 33662, 33677, 33654, 33683, 33674, 33687, 33686, 33659, 33655, 33673, 33684, 33647, 33666, 33663, 33668, 33689, 33679, 33644, 33649, 33640], 
    "Vulnerable Road Users": [35581, 35609, 35572, 35620, 35608, 35614, 35607, 35574, 35617, 35554, 35622, 35623, 35594, 35596, 35578, 35565, 35584, 35585, 35590, 35597, 35602, 35591, 35562, 35569, 35624, 35557, 35612, 35580, 35586, 35587, 35593, 35600, 35599, 35619, 35603, 35595, 35563, 35576, 35575, 35583, 35616, 35598, 35611, 35592, 35573, 35566, 35604, 35564, 35556, 35570, 35618, 35567, 35606, 35613, 35555, 35588, 35621, 35571, 35601, 35582, 35568, 35610, 35589, 35577, 35605, 35615, 35579], 
    "Other Types of Vehicles": [34224, 34218, 34220, 34228, 34222, 34215, 34221, 34217, 34231, 34219, 34223, 34216, 34227, 34230, 34225, 34226, 34229], 
    "Motorcycle Handling": [33982, 33962, 33950, 33970, 33979, 33971, 33953, 33972, 33990, 33980, 33947, 33987, 33985, 33963, 33969, 33973, 33986, 33951, 33977, 33956, 33960, 33955, 33943, 33949, 33984, 33968, 33974, 33965, 33948, 33957, 33942, 33978, 33991, 33981, 33954, 33964, 33946, 33952, 33976, 33959, 33967, 33961, 33941, 33945, 33983, 33988, 33944, 33975, 33966, 33958, 33989], 
    "Motorway Rules": [34032, 34030, 34024, 34028, 34052, 34075, 34039, 34033, 34053, 34046, 34065, 34047, 34041, 34049, 34066, 34045, 34060, 34057, 34063, 34062, 34051, 34072, 34073, 34044, 34058, 34040, 34059, 34071, 34031, 34048, 34043, 34054, 34050, 34034, 34064, 34038, 34056, 34036, 34055, 34067, 34037, 34068, 34076, 34070, 34025, 34029, 34069, 34061, 34074, 34042, 34035], 
    "Rules of the Road": [34676, 34648, 34685, 34668, 34647, 34663, 34686, 34693, 34683, 34694, 34682, 34643, 34671, 34677, 34678, 34660, 34680, 34658, 34684, 34672, 34690, 34664, 34652, 34645, 34667, 34674, 34654, 34657, 34649, 34653, 34681, 34651, 34679, 34688, 34670, 34689, 34691, 34662, 34666, 34687, 34665, 34659, 34644, 34656, 34650, 34655, 34673, 34692, 34675, 34646, 34661, 34669], 
    "Road and Traffic Signs": [34461, 34494, 34427, 34413, 34388, 34386, 34379, 34471, 34496, 34502, 34429, 34440, 34408, 34442, 34398, 34497, 34492, 34397, 34501, 34506, 34426, 34403, 34436, 34415, 34423, 34485, 34460, 34382, 34399, 34468, 34508, 34450, 34455, 34478, 34444, 34464, 34418, 34383, 34378, 34404, 34451, 34477, 34449, 34406, 34438, 34482, 34434, 34433, 34479, 34487, 34392, 34393, 34446, 34476, 34395, 34448, 34498, 34377, 34469, 34410, 34411, 34495, 34484, 34456, 34509, 34387, 34470, 34401, 34431, 34424, 34465, 34453, 34443, 34402, 34462, 34390, 34504, 34467, 34475, 34507, 34458, 34499, 34409, 34454, 34430, 34380, 34500, 34463, 34381, 34486, 34457, 34439, 34445, 34481, 34400, 34385, 34435, 34428, 34452, 34414, 34483, 34384, 34394, 34441, 34489, 34505, 34473, 34432, 34474, 34417, 34391, 34422, 34466, 34405, 34490, 34396, 34416, 34412, 34493, 34447, 34376, 34480, 34491, 34425, 34421, 34419, 34389, 34488, 34420, 34503, 34437, 34459, 34407, 34472], 
    "Documents": [33570, 33585, 33574, 33587, 33580, 33575, 33584, 33569, 33599, 33589, 33588, 33571, 33573, 33581, 33586, 33592, 33590, 33577, 33598, 33591, 33576, 33593, 33572, 33583, 33594, 33579, 33582, 33595, 33597, 33600, 33596, 33578], 
    "Incidents, Accidents, Emergencies": [33822, 33825, 33862, 33819, 33858, 33849, 33853, 33854, 33820, 33868, 33841, 33839, 33865, 33823, 33847, 33850, 33861, 33846, 33857, 33840, 33843, 33867, 33852, 33845, 33824, 33864, 33848, 33818, 33860, 33855, 33856, 33866, 33851, 33844, 33842, 33821, 33863, 33859], 
    "Motorcycle Loading": [34022, 34011, 34004, 34019, 34021, 33992, 34007, 33994, 33997, 34005, 34020, 34008, 33996, 34015, 33993, 34001, 33998, 34013, 34009, 33995, 34012, 33999, 34010, 34023, 34014, 34016, 34006, 34017, 34002, 34000, 34018, 34003]
}


MAIN_DICT = {"car": CAR_DICT, "motorbike": MOTORBIKE_DICT}

parser = ArgumentParser()
parser.add_argument("vehicles", nargs="*", help="List of test types to construct flashcards for.\nOptions are car, motorbike, lorry, bus, adi. If none provided, all will be constructed.")

args = parser.parse_args()

if args.vehicles == []:
    for test, testdict in MAIN_DICT.items():
        build_flashcards(testdict, test)

elif len(args.vehicles) > 5:
    raise ValueError("Too many arguments provided")

else:
    for arg in args.vehicles:
        if arg in ["car", "motorbike", "lorry", "bus", "adi"]:
            build_flashcards(MAIN_DICT[arg], arg)
        else:
            raise ValueError(f"""Invalid argument provided: {arg}. 
                             Valid options are: car, lorry, bus, adi, motorbike""")

