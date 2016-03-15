

from urllib2 import Request, urlopen, URLError
import json



# coursename : [section_id,course_id]
courses = {'EDUC-352-A': [826, 556], 'HLTH-126-A': [682, 665], 'HLTH-490-A': [525, 749], 'CHEM-474-A': [780, 690], 'PHYS-152-A': [363, 863], 'WGST-361-A': [351, 692], 'CS-130-B': [793, 814], 'REL-364-A': [841, 669], 'ANTH-380-A': [870, 531], 'LAT-202-A': [337, 885], 'ITAL-102-A': [32, 876], 'COMS-342-A': [15, 609], 'SW-403-A': [279, 513], 'FREN-102-A': [7, 645], 'FREN-102-B': [10, 645], 'MGT-490-I': [77, 894], 'PHIL-310-A': [298, 694], 'PAID-112D-30': [594, 596], 'PAID-112D-33': [597, 596], 'PAID-112D-32': [596, 596], 'MGT-490-B': [72, 894], 'MGT-490-C': [835, 894], 'FREN-101-A': [6, 642], 'MGT-490-A': [71, 894], 'MGT-490-F': [74, 894], 'MGT-490-G': [75, 894], 'MGT-490-D': [73, 894], 'EDUC-344-A': [227, 610], 'PE-100-B01': [732, 585], 'PHYS-491-A': [375, 612], 'ENVS-485-A': [105, 837], 'CHEM-202L-A03': [185, 528], 'CHEM-202L-A02': [184, 528], 'CHEM-202L-A01': [183, 528], 'REL-222-A': [132, 488], 'WGST-131-A': [255, 747], 'BIO-152L-A03': [402, 545], 'ANTH-209-A': [252, 845], 'LING-133-A': [830, 743], 'DAN-199-A': [253, 825], 'COMS-320-A': [31, 750], 'WGST-342-A': [20, 679], 'SPAN-302-B': [95, 519], 'SPAN-302-A': [94, 519], 'RUS-102-A': [37, 485], 'EDUC-328-A': [225, 686], 'EDUC-328-B': [242, 686], 'SOC-350-A': [267, 502], 'PHYS-152L-A02': [366, 864], 'PHYS-152L-A03': [825, 864], 'MATH-151-A': [128, 719], 'PHYS-152L-A01': [365, 864], 'LING-493-A': [850, 846], 'SPAN-460-A': [101, 660], 'AFRS-172-A': [308, 653], 'LAT-102-A': [335, 884], 'LAT-102-B': [336, 884], 'HIST-493-A': [856, 868], 'BIO-152L-A04': [403, 545], 'SPAN-490-A': [104, 523], 'DAN-205-A': [256, 766], 'PAID-112D-09': [554, 596], 'PE-110-C01': [811, 584], 'POLS-485-A': [331, 857], 'CS-165-A': [794, 827], 'MATH-115-D': [120, 646], 'MATH-115-C': [119, 646], 'MATH-115-B': [118, 646], 'MATH-152-B': [131, 722], 'CHEM-371-A': [778, 850], 'ART-493-B': [833, 542], 'PE-190-B': [704, 874], 'GRK-490-A': [828, 733], 'BIO-250-A': [417, 729], 'EDUC-323-A': [223, 698], 'ECON-248-A': [51, 565], 'SCST-202-A': [82, 499], 'ENG-147-A': [305, 573], 'SCI-111-A': [210, 496], 'THE-100-B': [860, 860], 'ART-239-A': [201, 848], 'ENVS-134L-A02': [92, 622], 'ENVS-134L-A03': [109, 622], 'ENVS-134L-A01': [91, 622], 'ATHTR-372-A': [674, 635], 'CHEM-114-A': [164, 493], 'MATH-110-B': [113, 711], 'COMS-347-A': [23, 800], 'NURS-471L-A01': [450, 931], 'NURS-378-A': [447, 795], 'CHEM-141-A': [167, 702], 'DAN-100-B': [862, 761], 'ECON-130-A': [47, 564], 'ECON-130-B': [48, 564], 'SPAN-201-A': [87, 517], 'SPAN-201-C': [89, 517], 'SPAN-201-B': [88, 517], 'SPAN-201-D': [93, 517], 'MGT-490-H': [76, 894], 'MUS-330-I': [670, 555], 'AFRS-147-A': [303, 881], 'COMS-348-A': [24, 652], 'LING-131-A': [33, 620], 'PAID-112D-31': [595, 596], 'RUS-243-A': [422, 543], 'ANTH-303-A': [842, 782], 'MUS-332L-D': [691, 903], 'MUS-332L-C': [690, 903], 'MUS-332L-B': [689, 903], 'MUS-332L-A': [688, 903], 'POLS-380-A': [869, 920], 'EDUC-255-A': [433, 592], 'MUS-273-I': [618, 921], 'CS-260-A': [356, 826], 'BIO-358-A': [424, 801], 'PAID-112D-17': [567, 596], 'PAID-112D-08': [553, 596], 'SPAN-346-A': [99, 521], 'ART-210-A': [200, 817], 'HLTH-358-A': [524, 742], 'PAID-112D-04': [542, 596], 'PAID-112D-05': [543, 596], 'PAID-112D-06': [545, 596], 'PHIL-490-A': [299, 835], 'THE-100-A': [859, 860], 'PAID-112D-01': [538, 596], 'PAID-112D-02': [539, 596], 'PAID-112D-03': [540, 596], 'INTS-130-D': [534, 805], 'ACCTG-468-A': [43, 539], 'SCI-110-A': [812, 495], 'COMS-490-A': [27, 619], 'PAID-112D-16': [566, 596], 'POLS-366-A': [314, 916], 'MUS-273-A': [818, 921], 'POLS-375-A': [868, 919], 'BIO-112L-A': [823, 569], 'PSYC-493-A': [849, 484], 'WGST-337-A': [152, 678], 'SOC-472-A': [269, 503], 'THE-352-A': [289, 762], 'SCI-250-B': [514, 789], 'SCI-250-A': [512, 789], 'ENVS-215L-A01': [103, 712], 'HIST-235-A': [428, 862], 'PAID-112D-15': [565, 596], 'THE-127-A': [277, 768], 'CHEM-202-A': [182, 527], 'JOUR-100-A': [858, 831], 'EDUC-260-A': [434, 570], 'MUS-273-H': [617, 921], 'MUS-145-A': [544, 714], 'HIST-485-A': [324, 708], 'MUS-341-B': [694, 906], 'DAN-130-A': [254, 764], 'MUS-341-A': [693, 906], 'MUS-247-A': [316, 910], 'IS-485-A': [213, 873], 'PSYC-349-A': [787, 671], 'EDUC-367-A': [232, 808], 'PSYC-490-A': [398, 483], 'PHYS-282L-A': [371, 664], 'ENVS-493-A': [855, 624], 'PHIL-493-A': [854, 836], 'ART-104-A': [162, 663], 'ENVS-490-A': [107, 638], 'POLS-363-A': [311, 914], 'PHIL-120-A': [295, 807], 'POLS-490-A': [317, 922], 'PAID-450-A': [836, 775], 'BIO-252-A': [419, 551], 'MUS-135-A': [541, 604], 'EDUC-380-A': [839, 784], 'ART-103-A': [160, 662], 'EDUC-265-A': [435, 590], 'PHYS-312-A': [372, 867], 'BIO-232-A': [411, 732], 'PSYC-243-A': [385, 929], 'ENG-230-B': [330, 597], 'MUS-330-F': [668, 555], 'MUS-344-A': [697, 909], 'ENG-230-A': [329, 597], 'FCUL-251-A': [84, 785], 'PSYC-249-A': [388, 605], 'EDUC-223-A': [219, 625], 'EDUC-246-A': [220, 644], 'CS-160-A': [352, 548], 'MGT-371-A': [60, 740], 'PE-250-A': [715, 559], 'MUS-439-A': [768, 803], 'HIST-239-A': [364, 834], 'EDUC-388-A': [769, 822], 'ART-490-A': [209, 541], 'MUS-122-C': [462, 899], 'ART-490-B': [211, 541], 'PSYC-242-A': [386, 672], 'MUS-122-D': [463, 899], 'POLS-493-A': [846, 923], 'MATH-253-B': [139, 731], 'MATH-253-A': [138, 731], 'CHEM-490-A': [194, 535], 'MUS-360-A': [706, 925], 'BIO-354L-A01': [423, 683], 'POLS-364-A': [313, 915], 'ENG-212-A': [328, 581], 'CHEM-242L-03': [189, 525], 'BIO-493-A': [853, 563], 'CHEM-242L-02': [188, 525], 'BIO-490-A': [429, 562], 'REL-493-A': [848, 576], 'ENG-312-A': [347, 600], 'ATHTR-468-A': [675, 636], 'DAN-264-A': [272, 767], 'ART-202-A': [196, 726], 'PE-100-C01': [782, 585], 'PSYC-356L-A01': [394, 611], 'PE-100-C03': [786, 585], 'PE-100-C02': [784, 585], 'PE-100-C05': [792, 585], 'PE-100-C04': [790, 585], 'LAT-302-A': [338, 599], 'ART-108-B': [174, 533], 'ART-108-A': [173, 533], 'THE-491-A': [838, 776], 'PSYC-356L-A02': [395, 611], 'ATHTR-370-A': [673, 634], 'MUS-343-A': [695, 908], 'MUS-343-B': [696, 908], 'ENG-354-A': [349, 603], 'INTS-130-A': [497, 805], 'INTS-130-B': [502, 805], 'INTS-130-C': [533, 805], 'SOC-261-A': [262, 657], 'INTS-130-E': [535, 805], 'INTS-130-F': [536, 805], 'INTS-130-G': [537, 805], 'MUS-122L-A': [464, 900], 'CHEM-152L-06': [181, 522], 'ART-491-A': [237, 721], 'CHEM-152L-01': [171, 522], 'PSYC-243-B': [387, 929], 'ART-300-A': [204, 540], 'REL-490-A': [163, 494], 'ENVS-134-A': [90, 606], 'CHEM-242L-01': [187, 525], 'PHIL-100-A': [292, 794], 'PHIL-100-B': [300, 794], 'PHIL-100-C': [301, 794], 'MUS-273-C': [612, 921], 'CHEM-242L-04': [190, 525], 'NURS-477-A': [496, 936], 'NURS-382-A': [503, 796], 'ENG-210-A': [326, 578], 'WGST-147-A': [307, 734], 'ENG-231-A': [327, 587], 'ART-228-A': [238, 537], 'SPAN-339-A': [98, 838], 'COMS-380-A': [867, 623], 'HIST-172-A': [312, 654], 'ENG-334-A': [348, 601], 'PE-456-A': [720, 879], 'HLTH-234-A': [683, 758], 'EDUC-221-A': [215, 595], 'EDUC-221-B': [216, 595], 'HIST-101-A': [318, 773], 'EDUC-222-B': [218, 608], 'EDUC-222-A': [217, 608], 'HLTH-233-A': [523, 736], 'NURS-386-A': [504, 798], 'MUS-430-P': [754, 582], 'MUS-430-I': [744, 582], 'PSYC-240-B': [384, 928], 'PSYC-240-A': [383, 928], 'MUS-430-J': [745, 582], 'MUS-430-L': [749, 582], 'MUS-430-O': [753, 582], 'PE-490-A': [526, 895], 'MUS-430-A': [738, 582], 'HLTH-352-A': [698, 739], 'MUS-430-C': [740, 582], 'NURS-473-A': [451, 933], 'MUS-330-P': [681, 555], 'MATH-339-A': [145, 851], 'MUS-430-F': [742, 582], 'MUS-132L-A': [519, 707], 'CHEM-301-A': [191, 695], 'GRK-102-A': [334, 724], 'REL-232-A': [149, 561], 'REL-232-B': [150, 561], 'SPAN-350-A': [100, 658], 'ANTH-401-A': [257, 529], 'ECON-255-A': [53, 566], 'MUS-330-K': [672, 555], 'ART-208-A': [199, 727], 'MUS-122L-B': [465, 900], 'MUS-122L-C': [466, 900], 'MUS-122L-D': [467, 900], 'MUS-122L-E': [468, 900], 'MUS-122L-F': [763, 900], 'ART-200-A': [179, 534], 'IS-450-A': [281, 854], 'ART-206-A': [197, 815], 'SW-305-A': [276, 509], 'PAID-112D-19': [569, 596], 'PAID-112D-18': [568, 596], 'ENG-130-A': [370, 858], 'GER-102-A': [21, 704], 'GER-102-B': [22, 704], 'PAID-112D-14': [563, 596], 'PAID-112D-13': [561, 596], 'PAID-112D-12': [558, 596], 'PAID-112D-11': [557, 596], 'PAID-112D-10': [556, 596], 'PHIL-220-A': [296, 806], 'THE-199-A': [282, 824], 'MUS-363-A': [709, 640], 'PHYS-114L-A': [377, 861], 'MUS-330-B': [665, 555], 'EDUC-226-A': [834, 841], 'MUS-330-C': [666, 555], 'AFRS-239-A': [287, 856], 'MUS-330-A': [821, 555], 'REL-101-H': [122, 560], 'REL-101-I': [125, 560], 'REL-101-J': [127, 560], 'REL-101-D': [114, 560], 'HIST-150-A': [321, 675], 'REL-101-F': [117, 560], 'REL-101-G': [121, 560], 'REL-101-A': [106, 560], 'REL-101-B': [108, 560], 'REL-101-C': [111, 560], 'PE-231-A': [711, 875], 'CHEM-365-A': [193, 613], 'MUS-330-D': [667, 555], 'CLAS-310-A': [341, 753], 'WGST-485-A': [814, 810], 'SCI-250L-A01': [515, 833], 'NURS-471-A': [449, 930], 'NURS-388-A': [505, 799], 'MATH-141-A': [123, 718], 'MATH-141-B': [124, 718], 'MATH-141-C': [126, 718], 'MGT-150-B': [57, 783], 'REL-316-A': [822, 492], 'COMS-330-A': [25, 774], 'BIO-248L-A04': [416, 550], 'BIO-248L-A03': [415, 550], 'BIO-248L-A02': [414, 550], 'BIO-248L-A01': [413, 550], 'PE-342-A': [529, 877], 'LING-490-A': [36, 752], 'COMS-132-B': [13, 617], 'COMS-132-A': [11, 617], 'DAN-100-A': [861, 761], 'SW-101-A': [271, 506], 'BIO-362-A': [426, 615], 'PAID-112D-07': [546, 596], 'IS-493-A': [847, 847], 'FCUL-142-A': [1, 781], 'LING-245-A': [35, 666], 'SOC-345-A': [265, 501], 'AFRS-235-A': [427, 907], 'ENG-211-A': [354, 580], 'NURS-384-A': [448, 797], 'PHIL-110-A': [293, 811], 'IS-490-A': [214, 746], 'REL-239-A': [286, 853], 'THE-200-A': [283, 769], 'GER-490-A': [827, 717], 'MUST-380-A': [857, 688], 'GRK-202-A': [340, 728], 'SOC-490-A': [270, 505], 'EDUC-331-A': [797, 689], 'MUS-268-A': [766, 918], 'PE-366L-A02': [532, 883], 'ENG-485-A': [820, 859], 'CHEM-114L-A01': [165, 497], 'REL-230-B': [147, 489], 'REL-230-A': [133, 489], 'CHEM-114L-A02': [166, 497], 'REL-233-A': [151, 491], 'CS-150-A': [344, 547], 'CS-150-B': [346, 547], 'HIST-321-A': [436, 716], 'CHEM-242-A': [186, 524], 'CHEM-242-B': [824, 524], 'MUS-430-K': [746, 582], 'ACCTG-354-A': [42, 479], 'PSYC-353-A': [390, 932], 'GER-346-A': [29, 812], 'WGST-351-A': [264, 691], 'ART-379-A': [208, 754], 'THE-222-A': [284, 804], 'ENG-110-A': [325, 558], 'SW-402-A': [278, 512], 'ART-339-A': [206, 849], 'MATH-115-A': [116, 646], 'SOC-101-A': [259, 500], 'SOC-101-B': [260, 500], 'SOC-101-C': [261, 500], 'MUS-430-B': [739, 582], 'REL-256-A': [158, 567], 'NURS-477L-A02': [499, 937], 'NURS-477L-A01': [498, 937], 'HLTH-125-A': [677, 647], 'CHEM-361-A': [192, 530], 'MUS-430-G': [743, 582], 'MATH-454-A': [143, 745], 'PHYS-114-A': [376, 840], 'PHYS-182-A': [367, 865], 'MUS-266-A': [765, 917], 'FCUL-243-A': [2, 546], 'MGT-353-B': [66, 889], 'CLAS-490-A': [333, 670], 'MGT-353-A': [65, 889], 'THE-206-A': [198, 816], 'RUS-202-A': [78, 487], 'DAN-105-A': [251, 765], 'SCST-251-A': [83, 786], 'MUS-491-A': [244, 843], 'MUS-332-B': [685, 901], 'PAID-112D-27': [589, 596], 'PE-130-A': [701, 809], 'EDUC-378-B': [235, 589], 'EDUC-378-A': [236, 589], 'MUS-332-C': [686, 901], 'EDUC-278-A': [222, 697], 'EDUC-376-A': [233, 557], 'IS-230-A': [212, 872], 'BIO-358L-A01': [425, 802], 'COMS-130-A': [8, 616], 'COMS-130-B': [9, 616], 'ACCTG-357-A': [46, 526], 'BIO-250L-A01': [418, 735], 'ATHTR-268-A': [520, 632], 'PE-100-B02': [748, 585], 'THE-327-A': [288, 771], 'PE-100-B04': [756, 585], 'PE-100-B05': [758, 585], 'EDUC-486-A': [239, 699], 'BIO-295-A': [865, 778], 'ATHTR-490-A': [527, 637], 'BIO-152L-A10': [409, 545], 'BIO-152L-A11': [410, 545], 'SW-304-A': [275, 510], 'PE-346-A': [719, 757], 'MATH-439-A': [146, 852], 'MUS-132-A': [518, 706], 'BIO-152L-A01': [400, 545], 'MUS-300-A': [646, 583], 'CHEM-141L-A01': [168, 703], 'PSYC-130-C': [380, 926], 'WGST-243-A': [3, 693], 'BIO-152L-A02': [401, 545], 'BIO-152L-A05': [404, 545], 'PE-190-A': [703, 874], 'CHEM-152-A': [169, 504], 'AFRS-247-A': [315, 902], 'CHEM-152-B': [170, 504], 'PE-244-A': [713, 878], 'SPAN-101-A': [85, 515], 'ENG-361-A': [350, 607], 'MATH-365-A': [142, 738], 'PE-366L-A01': [531, 883], 'CLAS-240-A': [342, 629], 'BIO-152L-A09': [408, 545], 'MUS-273-J': [619, 921], 'MUS-273-K': [620, 921], 'MUS-273-L': [621, 921], 'MUS-273-M': [622, 921], 'MUS-273-N': [623, 921], 'BIO-152L-A08': [407, 545], 'PSYC-350-A': [389, 935], 'MUS-273-B': [819, 921], 'ECON-490-A': [52, 577], 'MUS-273-D': [613, 921], 'MUS-273-E': [614, 921], 'MUS-273-F': [615, 921], 'MUS-273-G': [616, 921], 'EDUC-252-A': [221, 627], 'MATH-328-A': [141, 630], 'MUS-130-P': [517, 553], 'NURS-493-A': [844, 594], 'MUS-356-A': [864, 913], 'NURS-236-A': [440, 790], 'NURS-236-B': [501, 790], 'NURS-490-A': [500, 938], 'MGT-362-A': [67, 890], 'FREN-202-A': [14, 650], 'SW-110-A': [800, 715], 'SPAN-102-A': [86, 516], 'MGT-365-A': [69, 892], 'EDUC-371-A': [439, 821], 'MUS-230-N': [609, 579], 'MATH-152-A': [130, 722], 'CHIN-102-A': [4, 709], 'FREN-201-A': [12, 648], 'EDUC-270-A': [437, 591], 'PSYC-353L-A02': [392, 710], 'COMS-357-A': [30, 618], 'PSYC-353L-A01': [391, 710], 'ENVS-215-A': [102, 681], 'MUS-330-J': [671, 555], 'MUS-230-O': [610, 579], 'PAID-112D-28': [591, 596], 'PAID-112D-29': [592, 596], 'MUS-330-N': [678, 555], 'MUS-330-O': [680, 555], 'MUS-330-L': [676, 555], 'CLAS-300-A': [332, 628], 'PAID-112D-22': [574, 596], 'PAID-112D-23': [576, 596], 'PAID-112D-20': [570, 596], 'PAID-112D-21': [571, 596], 'PAID-112D-26': [587, 596], 'ANTH-101-A': [245, 481], 'PAID-112D-24': [582, 596], 'PAID-112D-25': [585, 596], 'SCST-102-B': [80, 498], 'SCST-102-C': [81, 498], 'SCST-102-A': [79, 498], 'MUS-130-N': [513, 553], 'MUS-117-D': [459, 898], 'MUS-115-A': [767, 586], 'MUS-117-A': [456, 898], 'MUS-117-C': [458, 898], 'MUS-117-B': [457, 898], 'CS-130-A': [788, 814], 'MGT-352-B': [64, 888], 'MGT-352-A': [63, 888], 'MGT-351-A': [61, 887], 'MGT-351-B': [62, 887], 'ECON-366-A': [55, 571], 'CS-330-A': [357, 614], 'MGT-364-A': [68, 891], 'MUS-490-A': [760, 927], 'GER-101-A': [19, 701], 'WGST-490-A': [361, 687], 'FREN-345-A': [16, 680], 'HIST-225-A': [323, 651], 'MATH-240-A': [137, 725], 'ART-295-A': [866, 748], 'ART-252-A': [202, 538], 'REL-485-A': [285, 855], 'PHYS-361-A': [373, 870], 'MUS-130-I': [507, 553], 'MUS-130-J': [508, 553], 'MUS-130-K': [509, 553], 'MUS-130-L': [510, 553], 'MATH-322-A': [140, 737], 'MUS-130-O': [516, 553], 'MUS-130-A': [490, 553], 'MUS-130-B': [491, 553], 'MUS-130-C': [492, 553], 'MUS-130-D': [493, 553], 'CS-491-A': [359, 643], 'MUS-130-F': [494, 553], 'MUS-130-G': [506, 553], 'HLTH-344-A': [687, 759], 'COMS-233-A': [28, 641], 'CHIN-202-A': [5, 713], 'MUS-116-A': [454, 896], 'MUS-116-B': [455, 896], 'PSYC-468-B': [397, 480], 'PSYC-468-A': [396, 480], 'PHIL-130-A': [135, 819], 'CS-370-A': [358, 830], 'PHIL-130-B': [148, 819], 'CS-353-A': [360, 829], 'ANTH-490-A': [258, 532], 'HIST-162-A': [322, 639], 'CLAS-360-A': [343, 656], 'PE-229-A': [710, 755], 'HIST-112-A': [319, 741], 'BIO-354-A': [421, 554], 'MATH-220-A': [134, 730], 'MATH-220-B': [136, 730], 'MUST-220-A': [291, 655], 'MGT-367-A': [70, 893], 'MUS-122-A': [460, 899], 'MUS-430-N': [750, 582], 'MUS-338-A': [692, 621], 'ECON-268-A': [54, 572], 'MUS-351-A': [699, 911], 'MUS-351-B': [700, 911], 'ANTH-103-A': [248, 511], 'ENG-368-A': [353, 626], 'MUS-122-B': [461, 899], 'EDUC-275-A': [438, 593], 'PHYS-493-A': [851, 575], 'MUS-122-E': [762, 899], 'PE-110-B01': [779, 584], 'CLAS-275-A': [813, 780], 'NURS-237-A': [442, 791], 'ENVS-239-A': [110, 839], 'ACCTG-490-A': [44, 659], 'ACCTG-490-B': [45, 659], 'EDUC-371L-A': [441, 842], 'BIO-248-A': [412, 549], 'FREN-490-A': [18, 696], 'ATHTR-368-A': [522, 633], 'MATH-490-A': [144, 772], 'PHYS-282-A': [369, 661], 'POLS-130-A': [302, 897], 'SW-490-A': [280, 514], 'AS-389-A': [840, 787], 'NURS-373-A': [446, 793], 'NURS-375-A': [511, 813], 'MATH-493-A': [843, 574], 'DAN-230-A': [268, 760], 'SW-204-A': [274, 508], 'EDUC-391-A': [770, 823], 'PE-260-A': [528, 880], 'PSYC-356-A': [393, 939], 'PE-344-A': [718, 756], 'EDUC-232-A': [432, 588], 'EDUC-232-B': [444, 588], 'BIO-252L-A01': [420, 552], 'CS-253-A': [795, 828], 'ECON-142-B': [50, 763], 'ECON-142-A': [49, 763], 'CHEM-152L-05': [180, 522], 'CHEM-152L-04': [176, 522], 'ENG-490-A': [355, 667], 'SOC-351-A': [263, 649], 'REL-112-A': [129, 482], 'CHEM-152L-03': [175, 522], 'CHEM-152L-02': [172, 522], 'PE-226-A': [705, 723], 'NURS-376-A': [443, 788], 'REL-243-A': [157, 490], 'MUS-376-A': [712, 924], 'ANTH-104-A': [249, 518], 'MUS-430-D': [741, 582], 'ART-110-A': [177, 720], 'HIST-395-A': [863, 869], 'ACCTG-250-A': [41, 674], 'WGST-130-A': [362, 668], 'MUS-227-A': [547, 744], 'PHYS-490-A': [374, 871], 'CHEM-493-A': [852, 536], 'PHIL-110-B': [294, 811], 'POLS-247-A': [309, 904], 'THE-360-A': [290, 770], 'ANTH-208-A': [250, 751], 'GER-201-A': [26, 705], 'BIO-112-A': [430, 568], 'MUS-111-A': [815, 677], 'REL-101-E': [115, 560], 'ENG-260-A': [345, 598], 'MUS-330-G': [669, 555], 'HLTH-125-B': [679, 647], 'ART-310-A': [205, 818], 'POLS-132-A': [304, 682], 'POLS-132-B': [306, 682], 'MUS-332-A': [684, 901], 'BIO-152-A': [399, 544], 'PE-366-A': [530, 882], 'EDUC-490-A': [240, 700], 'ACCTG-150-A': [38, 673], 'ACCTG-150-C': [40, 673], 'ACCTG-150-B': [39, 673], 'PSYC-130-A': [378, 926], 'HIST-126-A': [320, 844], 'PSYC-130-B': [379, 926], 'PSYC-130-E': [382, 926], 'PSYC-130-D': [381, 926], 'BIO-152L-A07': [406, 545], 'BIO-152L-A06': [405, 545], 'REL-261-A': [159, 486], 'AFRS-345-A': [266, 832], 'REL-261-B': [161, 486], 'MGT-240-B': [59, 779], 'MGT-240-A': [58, 779], 'MUS-230-G': [602, 579], 'MUS-230-F': [598, 579], 'MUS-230-D': [593, 579], 'MUS-230-C': [590, 579], 'MUS-230-B': [588, 579], 'MUS-230-A': [817, 579], 'ANTH-101-C': [247, 481], 'ANTH-101-B': [246, 481], 'MGT-150-A': [56, 783], 'MUS-230-L': [829, 579], 'MUS-230-K': [608, 579], 'MUS-230-J': [607, 579], 'MUS-230-I': [606, 579], 'DAN-491-A': [837, 777], 'MUS-353-A': [702, 912], 'MUS-230-P': [611, 579], 'ART-493-A': [832, 542], 'PE-100-B03': [752, 585], 'FREN-346-A': [17, 684], 'ACCTG-110-A': [34, 602], 'ACCTG-110-B': [831, 602], 'LAT-490-A': [339, 886], 'MATH-110-A': [112, 711], 'ENG-493-A': [845, 676], 'MUS-237-A': [816, 905], 'SW-201-A': [273, 507], 'SPAN-303-B': [97, 520], 'PHYS-182L-A01': [368, 866], 'SPAN-303-A': [96, 520], 'EDUC-329-A': [226, 685], 'NURS-372-A': [445, 792], 'POLS-258-A': [310, 631], 'EDUC-329-B': [243, 685], 'PHIL-230-A': [297, 820], 'NURS-473L-A01': [495, 934]}
sections = {1: 'FCUL-142-A', 2: 'FCUL-243-A', 3: 'WGST-243-A', 4: 'CHIN-102-A', 5: 'CHIN-202-A', 6: 'FREN-101-A', 7: 'FREN-102-A', 8: 'COMS-130-A', 9: 'COMS-130-B', 10: 'FREN-102-B', 11: 'COMS-132-A', 12: 'FREN-201-A', 13: 'COMS-132-B', 14: 'FREN-202-A', 15: 'COMS-342-A', 16: 'FREN-345-A', 17: 'FREN-346-A', 18: 'FREN-490-A', 19: 'GER-101-A', 20: 'WGST-342-A', 21: 'GER-102-A', 22: 'GER-102-B', 23: 'COMS-347-A', 24: 'COMS-348-A', 25: 'COMS-330-A', 26: 'GER-201-A', 27: 'COMS-490-A', 28: 'COMS-233-A', 29: 'GER-346-A', 30: 'COMS-357-A', 31: 'COMS-320-A', 32: 'ITAL-102-A', 33: 'LING-131-A', 34: 'ACCTG-110-A', 35: 'LING-245-A', 36: 'LING-490-A', 37: 'RUS-102-A', 38: 'ACCTG-150-A', 39: 'ACCTG-150-B', 40: 'ACCTG-150-C', 41: 'ACCTG-250-A', 42: 'ACCTG-354-A', 43: 'ACCTG-468-A', 44: 'ACCTG-490-A', 45: 'ACCTG-490-B', 46: 'ACCTG-357-A', 47: 'ECON-130-A', 48: 'ECON-130-B', 49: 'ECON-142-A', 50: 'ECON-142-B', 51: 'ECON-248-A', 52: 'ECON-490-A', 53: 'ECON-255-A', 54: 'ECON-268-A', 55: 'ECON-366-A', 56: 'MGT-150-A', 57: 'MGT-150-B', 58: 'MGT-240-A', 59: 'MGT-240-B', 60: 'MGT-371-A', 61: 'MGT-351-A', 62: 'MGT-351-B', 63: 'MGT-352-A', 64: 'MGT-352-B', 65: 'MGT-353-A', 66: 'MGT-353-B', 67: 'MGT-362-A', 68: 'MGT-364-A', 69: 'MGT-365-A', 70: 'MGT-367-A', 71: 'MGT-490-A', 72: 'MGT-490-B', 73: 'MGT-490-D', 74: 'MGT-490-F', 75: 'MGT-490-G', 76: 'MGT-490-H', 77: 'MGT-490-I', 78: 'RUS-202-A', 79: 'SCST-102-A', 80: 'SCST-102-B', 81: 'SCST-102-C', 82: 'SCST-202-A', 83: 'SCST-251-A', 84: 'FCUL-251-A', 85: 'SPAN-101-A', 86: 'SPAN-102-A', 87: 'SPAN-201-A', 88: 'SPAN-201-B', 89: 'SPAN-201-C', 90: 'ENVS-134-A', 91: 'ENVS-134L-A01', 92: 'ENVS-134L-A02', 93: 'SPAN-201-D', 94: 'SPAN-302-A', 95: 'SPAN-302-B', 96: 'SPAN-303-A', 97: 'SPAN-303-B', 98: 'SPAN-339-A', 99: 'SPAN-346-A', 100: 'SPAN-350-A', 101: 'SPAN-460-A', 102: 'ENVS-215-A', 103: 'ENVS-215L-A01', 104: 'SPAN-490-A', 105: 'ENVS-485-A', 106: 'REL-101-A', 107: 'ENVS-490-A', 108: 'REL-101-B', 109: 'ENVS-134L-A03', 110: 'ENVS-239-A', 111: 'REL-101-C', 112: 'MATH-110-A', 113: 'MATH-110-B', 114: 'REL-101-D', 115: 'REL-101-E', 116: 'MATH-115-A', 117: 'REL-101-F', 118: 'MATH-115-B', 119: 'MATH-115-C', 120: 'MATH-115-D', 121: 'REL-101-G', 122: 'REL-101-H', 123: 'MATH-141-A', 124: 'MATH-141-B', 125: 'REL-101-I', 126: 'MATH-141-C', 127: 'REL-101-J', 128: 'MATH-151-A', 129: 'REL-112-A', 130: 'MATH-152-A', 131: 'MATH-152-B', 132: 'REL-222-A', 133: 'REL-230-A', 134: 'MATH-220-A', 135: 'PHIL-130-A', 136: 'MATH-220-B', 137: 'MATH-240-A', 138: 'MATH-253-A', 139: 'MATH-253-B', 140: 'MATH-322-A', 141: 'MATH-328-A', 142: 'MATH-365-A', 143: 'MATH-454-A', 144: 'MATH-490-A', 145: 'MATH-339-A', 146: 'MATH-439-A', 147: 'REL-230-B', 148: 'PHIL-130-B', 149: 'REL-232-A', 150: 'REL-232-B', 151: 'REL-233-A', 152: 'WGST-337-A', 157: 'REL-243-A', 158: 'REL-256-A', 159: 'REL-261-A', 160: 'ART-103-A', 161: 'REL-261-B', 162: 'ART-104-A', 163: 'REL-490-A', 164: 'CHEM-114-A', 165: 'CHEM-114L-A01', 166: 'CHEM-114L-A02', 167: 'CHEM-141-A', 168: 'CHEM-141L-A01', 169: 'CHEM-152-A', 170: 'CHEM-152-B', 171: 'CHEM-152L-01', 172: 'CHEM-152L-02', 173: 'ART-108-A', 174: 'ART-108-B', 175: 'CHEM-152L-03', 176: 'CHEM-152L-04', 177: 'ART-110-A', 179: 'ART-200-A', 180: 'CHEM-152L-05', 181: 'CHEM-152L-06', 182: 'CHEM-202-A', 183: 'CHEM-202L-A01', 184: 'CHEM-202L-A02', 185: 'CHEM-202L-A03', 186: 'CHEM-242-A', 187: 'CHEM-242L-01', 188: 'CHEM-242L-02', 189: 'CHEM-242L-03', 190: 'CHEM-242L-04', 191: 'CHEM-301-A', 192: 'CHEM-361-A', 193: 'CHEM-365-A', 194: 'CHEM-490-A', 196: 'ART-202-A', 197: 'ART-206-A', 198: 'THE-206-A', 199: 'ART-208-A', 200: 'ART-210-A', 201: 'ART-239-A', 202: 'ART-252-A', 204: 'ART-300-A', 205: 'ART-310-A', 206: 'ART-339-A', 208: 'ART-379-A', 209: 'ART-490-A', 210: 'SCI-111-A', 211: 'ART-490-B', 212: 'IS-230-A', 213: 'IS-485-A', 214: 'IS-490-A', 215: 'EDUC-221-A', 216: 'EDUC-221-B', 217: 'EDUC-222-A', 218: 'EDUC-222-B', 219: 'EDUC-223-A', 220: 'EDUC-246-A', 221: 'EDUC-252-A', 222: 'EDUC-278-A', 223: 'EDUC-323-A', 225: 'EDUC-328-A', 226: 'EDUC-329-A', 227: 'EDUC-344-A', 232: 'EDUC-367-A', 233: 'EDUC-376-A', 235: 'EDUC-378-B', 236: 'EDUC-378-A', 237: 'ART-491-A', 238: 'ART-228-A', 239: 'EDUC-486-A', 240: 'EDUC-490-A', 242: 'EDUC-328-B', 243: 'EDUC-329-B', 244: 'MUS-491-A', 245: 'ANTH-101-A', 246: 'ANTH-101-B', 247: 'ANTH-101-C', 248: 'ANTH-103-A', 249: 'ANTH-104-A', 250: 'ANTH-208-A', 251: 'DAN-105-A', 252: 'ANTH-209-A', 253: 'DAN-199-A', 254: 'DAN-130-A', 255: 'WGST-131-A', 256: 'DAN-205-A', 257: 'ANTH-401-A', 258: 'ANTH-490-A', 259: 'SOC-101-A', 260: 'SOC-101-B', 261: 'SOC-101-C', 262: 'SOC-261-A', 263: 'SOC-351-A', 264: 'WGST-351-A', 265: 'SOC-345-A', 266: 'AFRS-345-A', 267: 'SOC-350-A', 268: 'DAN-230-A', 269: 'SOC-472-A', 270: 'SOC-490-A', 271: 'SW-101-A', 272: 'DAN-264-A', 273: 'SW-201-A', 274: 'SW-204-A', 275: 'SW-304-A', 276: 'SW-305-A', 277: 'THE-127-A', 278: 'SW-402-A', 279: 'SW-403-A', 280: 'SW-490-A', 281: 'IS-450-A', 282: 'THE-199-A', 283: 'THE-200-A', 284: 'THE-222-A', 285: 'REL-485-A', 286: 'REL-239-A', 287: 'AFRS-239-A', 288: 'THE-327-A', 289: 'THE-352-A', 290: 'THE-360-A', 291: 'MUST-220-A', 292: 'PHIL-100-A', 293: 'PHIL-110-A', 294: 'PHIL-110-B', 295: 'PHIL-120-A', 296: 'PHIL-220-A', 297: 'PHIL-230-A', 298: 'PHIL-310-A', 299: 'PHIL-490-A', 300: 'PHIL-100-B', 301: 'PHIL-100-C', 302: 'POLS-130-A', 303: 'AFRS-147-A', 304: 'POLS-132-A', 305: 'ENG-147-A', 306: 'POLS-132-B', 307: 'WGST-147-A', 308: 'AFRS-172-A', 309: 'POLS-247-A', 310: 'POLS-258-A', 311: 'POLS-363-A', 312: 'HIST-172-A', 313: 'POLS-364-A', 314: 'POLS-366-A', 315: 'AFRS-247-A', 316: 'MUS-247-A', 317: 'POLS-490-A', 318: 'HIST-101-A', 319: 'HIST-112-A', 320: 'HIST-126-A', 321: 'HIST-150-A', 322: 'HIST-162-A', 323: 'HIST-225-A', 324: 'HIST-485-A', 325: 'ENG-110-A', 326: 'ENG-210-A', 327: 'ENG-231-A', 328: 'ENG-212-A', 329: 'ENG-230-A', 330: 'ENG-230-B', 331: 'POLS-485-A', 332: 'CLAS-300-A', 333: 'CLAS-490-A', 334: 'GRK-102-A', 335: 'LAT-102-A', 336: 'LAT-102-B', 337: 'LAT-202-A', 338: 'LAT-302-A', 339: 'LAT-490-A', 340: 'GRK-202-A', 341: 'CLAS-310-A', 342: 'CLAS-240-A', 343: 'CLAS-360-A', 344: 'CS-150-A', 345: 'ENG-260-A', 346: 'CS-150-B', 347: 'ENG-312-A', 348: 'ENG-334-A', 349: 'ENG-354-A', 350: 'ENG-361-A', 351: 'WGST-361-A', 352: 'CS-160-A', 353: 'ENG-368-A', 354: 'ENG-211-A', 355: 'ENG-490-A', 356: 'CS-260-A', 357: 'CS-330-A', 358: 'CS-370-A', 359: 'CS-491-A', 360: 'CS-353-A', 361: 'WGST-490-A', 362: 'WGST-130-A', 363: 'PHYS-152-A', 364: 'HIST-239-A', 365: 'PHYS-152L-A01', 366: 'PHYS-152L-A02', 367: 'PHYS-182-A', 368: 'PHYS-182L-A01', 369: 'PHYS-282-A', 370: 'ENG-130-A', 371: 'PHYS-282L-A', 372: 'PHYS-312-A', 373: 'PHYS-361-A', 374: 'PHYS-490-A', 375: 'PHYS-491-A', 376: 'PHYS-114-A', 377: 'PHYS-114L-A', 378: 'PSYC-130-A', 379: 'PSYC-130-B', 380: 'PSYC-130-C', 381: 'PSYC-130-D', 382: 'PSYC-130-E', 383: 'PSYC-240-A', 384: 'PSYC-240-B', 385: 'PSYC-243-A', 386: 'PSYC-242-A', 387: 'PSYC-243-B', 388: 'PSYC-249-A', 389: 'PSYC-350-A', 390: 'PSYC-353-A', 391: 'PSYC-353L-A01', 392: 'PSYC-353L-A02', 393: 'PSYC-356-A', 394: 'PSYC-356L-A01', 395: 'PSYC-356L-A02', 396: 'PSYC-468-A', 397: 'PSYC-468-B', 398: 'PSYC-490-A', 399: 'BIO-152-A', 400: 'BIO-152L-A01', 401: 'BIO-152L-A02', 402: 'BIO-152L-A03', 403: 'BIO-152L-A04', 404: 'BIO-152L-A05', 405: 'BIO-152L-A06', 406: 'BIO-152L-A07', 407: 'BIO-152L-A08', 408: 'BIO-152L-A09', 409: 'BIO-152L-A10', 410: 'BIO-152L-A11', 411: 'BIO-232-A', 412: 'BIO-248-A', 413: 'BIO-248L-A01', 414: 'BIO-248L-A02', 415: 'BIO-248L-A03', 416: 'BIO-248L-A04', 417: 'BIO-250-A', 418: 'BIO-250L-A01', 419: 'BIO-252-A', 420: 'BIO-252L-A01', 421: 'BIO-354-A', 422: 'RUS-243-A', 423: 'BIO-354L-A01', 424: 'BIO-358-A', 425: 'BIO-358L-A01', 426: 'BIO-362-A', 427: 'AFRS-235-A', 428: 'HIST-235-A', 429: 'BIO-490-A', 430: 'BIO-112-A', 432: 'EDUC-232-A', 433: 'EDUC-255-A', 434: 'EDUC-260-A', 435: 'EDUC-265-A', 436: 'HIST-321-A', 437: 'EDUC-270-A', 438: 'EDUC-275-A', 439: 'EDUC-371-A', 440: 'NURS-236-A', 441: 'EDUC-371L-A', 442: 'NURS-237-A', 443: 'NURS-376-A', 444: 'EDUC-232-B', 445: 'NURS-372-A', 446: 'NURS-373-A', 447: 'NURS-378-A', 448: 'NURS-384-A', 449: 'NURS-471-A', 450: 'NURS-471L-A01', 451: 'NURS-473-A', 454: 'MUS-116-A', 455: 'MUS-116-B', 456: 'MUS-117-A', 457: 'MUS-117-B', 458: 'MUS-117-C', 459: 'MUS-117-D', 460: 'MUS-122-A', 461: 'MUS-122-B', 462: 'MUS-122-C', 463: 'MUS-122-D', 464: 'MUS-122L-A', 465: 'MUS-122L-B', 466: 'MUS-122L-C', 467: 'MUS-122L-D', 468: 'MUS-122L-E', 490: 'MUS-130-A', 491: 'MUS-130-B', 492: 'MUS-130-C', 493: 'MUS-130-D', 494: 'MUS-130-F', 495: 'NURS-473L-A01', 496: 'NURS-477-A', 497: 'INTS-130-A', 498: 'NURS-477L-A01', 499: 'NURS-477L-A02', 500: 'NURS-490-A', 501: 'NURS-236-B', 502: 'INTS-130-B', 503: 'NURS-382-A', 504: 'NURS-386-A', 505: 'NURS-388-A', 506: 'MUS-130-G', 507: 'MUS-130-I', 508: 'MUS-130-J', 509: 'MUS-130-K', 510: 'MUS-130-L', 511: 'NURS-375-A', 512: 'SCI-250-A', 513: 'MUS-130-N', 514: 'SCI-250-B', 515: 'SCI-250L-A01', 516: 'MUS-130-O', 517: 'MUS-130-P', 518: 'MUS-132-A', 519: 'MUS-132L-A', 520: 'ATHTR-268-A', 522: 'ATHTR-368-A', 523: 'HLTH-233-A', 524: 'HLTH-358-A', 525: 'HLTH-490-A', 526: 'PE-490-A', 527: 'ATHTR-490-A', 528: 'PE-260-A', 529: 'PE-342-A', 530: 'PE-366-A', 531: 'PE-366L-A01', 532: 'PE-366L-A02', 533: 'INTS-130-C', 534: 'INTS-130-D', 535: 'INTS-130-E', 536: 'INTS-130-F', 537: 'INTS-130-G', 538: 'PAID-112D-01', 539: 'PAID-112D-02', 540: 'PAID-112D-03', 541: 'MUS-135-A', 542: 'PAID-112D-04', 543: 'PAID-112D-05', 544: 'MUS-145-A', 545: 'PAID-112D-06', 546: 'PAID-112D-07', 547: 'MUS-227-A', 553: 'PAID-112D-08', 554: 'PAID-112D-09', 556: 'PAID-112D-10', 557: 'PAID-112D-11', 558: 'PAID-112D-12', 561: 'PAID-112D-13', 563: 'PAID-112D-14', 565: 'PAID-112D-15', 566: 'PAID-112D-16', 567: 'PAID-112D-17', 568: 'PAID-112D-18', 569: 'PAID-112D-19', 570: 'PAID-112D-20', 571: 'PAID-112D-21', 574: 'PAID-112D-22', 576: 'PAID-112D-23', 582: 'PAID-112D-24', 585: 'PAID-112D-25', 587: 'PAID-112D-26', 588: 'MUS-230-B', 589: 'PAID-112D-27', 590: 'MUS-230-C', 591: 'PAID-112D-28', 592: 'PAID-112D-29', 593: 'MUS-230-D', 594: 'PAID-112D-30', 595: 'PAID-112D-31', 596: 'PAID-112D-32', 597: 'PAID-112D-33', 598: 'MUS-230-F', 602: 'MUS-230-G', 606: 'MUS-230-I', 607: 'MUS-230-J', 608: 'MUS-230-K', 609: 'MUS-230-N', 610: 'MUS-230-O', 611: 'MUS-230-P', 612: 'MUS-273-C', 613: 'MUS-273-D', 614: 'MUS-273-E', 615: 'MUS-273-F', 616: 'MUS-273-G', 617: 'MUS-273-H', 618: 'MUS-273-I', 619: 'MUS-273-J', 620: 'MUS-273-K', 621: 'MUS-273-L', 622: 'MUS-273-M', 623: 'MUS-273-N', 646: 'MUS-300-A', 665: 'MUS-330-B', 666: 'MUS-330-C', 667: 'MUS-330-D', 668: 'MUS-330-F', 669: 'MUS-330-G', 670: 'MUS-330-I', 671: 'MUS-330-J', 672: 'MUS-330-K', 673: 'ATHTR-370-A', 674: 'ATHTR-372-A', 675: 'ATHTR-468-A', 676: 'MUS-330-L', 677: 'HLTH-125-A', 678: 'MUS-330-N', 679: 'HLTH-125-B', 680: 'MUS-330-O', 681: 'MUS-330-P', 682: 'HLTH-126-A', 683: 'HLTH-234-A', 684: 'MUS-332-A', 685: 'MUS-332-B', 686: 'MUS-332-C', 687: 'HLTH-344-A', 688: 'MUS-332L-A', 689: 'MUS-332L-B', 690: 'MUS-332L-C', 691: 'MUS-332L-D', 692: 'MUS-338-A', 693: 'MUS-341-A', 694: 'MUS-341-B', 695: 'MUS-343-A', 696: 'MUS-343-B', 697: 'MUS-344-A', 698: 'HLTH-352-A', 699: 'MUS-351-A', 700: 'MUS-351-B', 701: 'PE-130-A', 702: 'MUS-353-A', 703: 'PE-190-A', 704: 'PE-190-B', 705: 'PE-226-A', 706: 'MUS-360-A', 709: 'MUS-363-A', 710: 'PE-229-A', 711: 'PE-231-A', 712: 'MUS-376-A', 713: 'PE-244-A', 715: 'PE-250-A', 718: 'PE-344-A', 719: 'PE-346-A', 720: 'PE-456-A', 732: 'PE-100-B01', 738: 'MUS-430-A', 739: 'MUS-430-B', 740: 'MUS-430-C', 741: 'MUS-430-D', 742: 'MUS-430-F', 743: 'MUS-430-G', 744: 'MUS-430-I', 745: 'MUS-430-J', 746: 'MUS-430-K', 748: 'PE-100-B02', 749: 'MUS-430-L', 750: 'MUS-430-N', 752: 'PE-100-B03', 753: 'MUS-430-O', 754: 'MUS-430-P', 756: 'PE-100-B04', 758: 'PE-100-B05', 760: 'MUS-490-A', 762: 'MUS-122-E', 763: 'MUS-122L-F', 765: 'MUS-266-A', 766: 'MUS-268-A', 767: 'MUS-115-A', 768: 'MUS-439-A', 769: 'EDUC-388-A', 770: 'EDUC-391-A', 778: 'CHEM-371-A', 779: 'PE-110-B01', 780: 'CHEM-474-A', 782: 'PE-100-C01', 784: 'PE-100-C02', 786: 'PE-100-C03', 787: 'PSYC-349-A', 788: 'CS-130-A', 790: 'PE-100-C04', 792: 'PE-100-C05', 793: 'CS-130-B', 794: 'CS-165-A', 795: 'CS-253-A', 797: 'EDUC-331-A', 800: 'SW-110-A', 811: 'PE-110-C01', 812: 'SCI-110-A', 813: 'CLAS-275-A', 814: 'WGST-485-A', 815: 'MUS-111-A', 816: 'MUS-237-A', 817: 'MUS-230-A', 818: 'MUS-273-A', 819: 'MUS-273-B', 820: 'ENG-485-A', 821: 'MUS-330-A', 822: 'REL-316-A', 823: 'BIO-112L-A', 824: 'CHEM-242-B', 825: 'PHYS-152L-A03', 826: 'EDUC-352-A', 827: 'GER-490-A', 828: 'GRK-490-A', 829: 'MUS-230-L', 830: 'LING-133-A', 831: 'ACCTG-110-B', 832: 'ART-493-A', 833: 'ART-493-B', 834: 'EDUC-226-A', 835: 'MGT-490-C', 836: 'PAID-450-A', 837: 'DAN-491-A', 838: 'THE-491-A', 839: 'EDUC-380-A', 840: 'AS-389-A', 841: 'REL-364-A', 842: 'ANTH-303-A', 843: 'MATH-493-A', 844: 'NURS-493-A', 845: 'ENG-493-A', 846: 'POLS-493-A', 847: 'IS-493-A', 848: 'REL-493-A', 849: 'PSYC-493-A', 850: 'LING-493-A', 851: 'PHYS-493-A', 852: 'CHEM-493-A', 853: 'BIO-493-A', 854: 'PHIL-493-A', 855: 'ENVS-493-A', 856: 'HIST-493-A', 857: 'MUST-380-A', 858: 'JOUR-100-A', 859: 'THE-100-A', 860: 'THE-100-B', 861: 'DAN-100-A', 862: 'DAN-100-B', 863: 'HIST-395-A', 864: 'MUS-356-A', 865: 'BIO-295-A', 866: 'ART-295-A', 867: 'COMS-380-A', 868: 'POLS-375-A', 869: 'POLS-380-A', 870: 'ANTH-380-A'}


url_dict = {
	'minNumCredits': None,
	'maxNumCredits': None,
	'requiredCourses': None,
	'preferredCourses': None,
	'requiredSections': None,
	'preferredSections': None,
	'requiredGenEds': None,
	'preferredGenEds': None,
	# use list of ints [9,13]
	'times':None
}

url_extenstion = {
	'minNumCredits': "minCredits=",
	'maxNumCredits': "maxCredits=",
	'requiredCourses': "requiredCourses=",
	'preferredCourses': "preferredCourses=",
	'requiredSections': "requiredSections=",
	'preferredSections': "preferredSections=",
	'requiredGenEds': "requiredGenEds=",
	'preferredGenEds': "preferredGenEds=",
	'times':"requiredTimeBlock="
}



# put in values

reqC = ["MATH-328-A","CS-353-A","PHIL-110-B"]
prefC = []
reqS = []
prefS = []
reqG = ['HB']
prefG = []
minC = 12
maxC =18
times = [8,13]



requiredCourses = ""
if reqC != []:
	for c in reqC:
		requiredCourses += str(courses[c][1]) + "%2C"
	url_dict['requiredCourses'] = requiredCourses[:-3]

preferredCourses = ""
if prefC != []:
	for c in prefC:
		preferredCourses += str(courses[c][1]) + "%2C"
	url_dict['preferredCourses'] = preferredCourses[:-3]

requiredSections = ""
if reqS != []:
	for c in reqS:
		requiredSections += str(courses[c][0]) + "%2C"
	url_dict['requiredSections'] = requiredSections[:-3]

preferredSections = ""
if prefS != []:
	for c in prefS:
		preferredSections += str(courses[c][0]) + "%2C"
	url_dict['preferredSections'] = preferredSections[:-3]

if prefG != []:
	pg = ""
	for x in prefG:
		pg += x + "%2C"
	url_dict['preferredGenEds'] = pg[:-3]
if reqG != []:
	rg = ""
	for x in reqG:
		rg += x + "%2C"
	url_dict['requiredGenEds'] = rg[:-3]
url_dict['minNumCredits'] = minC
url_dict['maxNumCredits'] = maxC
url_dict['times'] = times



######################################################################
######################################################################
############################# Build URL ##############################
######################################################################
######################################################################

url = "https://norsecourse.com:5000/api/schedules?" 

added = False
for thing in url_dict:
	if url_dict[thing] != None:
		if added:
			url += "&"
		added = True
		url += url_extenstion[thing]
		if thing == "times":
			url += str(url_dict[thing][0]) + "%3A00%2C" + str(url_dict[thing][1]) + "%3A00"
		else:
			url += str(url_dict[thing])



print(url)
request = Request(url)

response = urlopen(request)
result = response.read()
api = json.loads(result)

for schedule in api:
	if schedule['error'] == "No errors":
		print("SCHEDULE OPTION")
		sect_ids = schedule['schedule']
		for s in sect_ids:
			if s in sections:
				print(sections[s])
			else:
				print("section id:",s)
		print("\n\n")
	else:
		print("THERE WAS AN ERROR")
		print(schedule['error'])
		print("\n\n")












