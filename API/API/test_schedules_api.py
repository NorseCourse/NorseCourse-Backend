

from urllib2 import Request, urlopen, URLError
import json
import random




# coursename : [section_id,course_id]
courses = {"PSYC-130-A":[1,505], "PSYC-130-B":[2,505], "PSYC-130-C":[3,505], "PSYC-130-D":[4,505], "PSYC-130-E":[5,505], "MATH-110-A":[6,994], "MATH-115-A":[7,740], "PSYC-240-A":[8,1040], "MATH-115-B":[9,740], "PSYC-240-B":[10,1040], "PSYC-241-A":[11,725], "PSYC-244-A":[12,483], 
			"MATH-123-A":[13,609], "MATH-123-B":[14,609], "MATH-140-A":[15,586], "MATH-140-B":[16,586], "MATH-140-C":[17,586], "MATH-140-D":[18,586], "MATH-140-E":[19,586], "MATH-140-F":[20,586], "MATH-151-A":[21,587], "MATH-151-B":[22,587], "MATH-151-C":[23,587], "MATH-151-D":[24,587], 
			"MATH-152-A":[25,705], "MATH-152-B":[26,705], "MATH-152-C":[27,705], "MATH-220-A":[28,550], "MATH-240-A":[29,896], "MATH-240-B":[30,896], "MATH-321-A":[31,751], "MATH-321-B":[32,751], "MATH-327-A":[33,712], "MATH-351-A":[34,733], "MATH-471-A":[35,1061], "MATH-490-A":[36,779], 
			"MATH-339-A":[37,523], "PSYC-349-A":[38,1059], "PSYC-350-A":[39,821], "PSYC-350-B":[40,821], "PSYC-354-A":[41,918], "PSYC-354L-A01":[42,868], "PSYC-354L-A02":[43,868], "PSYC-353-A":[44,1024], "PSYC-353L-A":[45,491], "PSYC-353L-B":[46,491], "PSYC-465-A":[47,876], 
			"PSYC-465-B":[48,876], "PSYC-490-A":[49,869], "PSYC-270-A":[50,937], "IS-485-A":[51,770], "CHEM-151-A":[52,756], "CHEM-151-B":[53,756], "CHEM-151-C":[54,756], "IS-490-A":[55,1038], "CHEM-151L-01":[56,480], "CHEM-151L-02":[57,480], "CHEM-151L-03":[58,480], "CHEM-151L-04":[59,480], 
			"CHEM-151L-05":[60,480], "CHEM-151L-06":[61,480], "CHEM-151L-07":[62,480], "CHEM-151L-08":[63,480], "CHEM-151L-09":[64,480], "CHEM-201-A":[65,988], "CHEM-201L-01":[66,527], "CHEM-201L-02":[67,527], "CHEM-241-A":[68,773], "CHEM-241-B":[69,773], "CHEM-241L-01":[70,675], 
			"CHEM-241L-02":[71,675], "CHEM-241L-03":[72,675], "CHEM-241L-04":[73,675], "CHEM-241L-05":[74,675], "CHEM-344-A":[75,487], "CHEM-345-A":[76,902], "CHEM-351-A":[77,727], "CHEM-362-A":[78,954], "CHEM-365-A":[79,693], "CHEM-366-A":[80,1046], "CHEM-490L-01":[81,983], 
			"CHEM-372-A":[82,974], "SCI-125-A":[83,887], "MUS-115-A":[84,816], "MUS-115-B":[85,816], "MUS-116-A":[86,631], "MUS-116-B":[87,631], "MUS-116-C":[88,631], "MUS-116-D":[89,631], "MUS-117-A":[90,532], "MUS-117-B":[91,532], "MUS-117-C":[92,532], "MUS-117-D":[93,532], 
			"MUS-118-A":[94,679], "MUS-121-A":[95,521], "MUS-121-B":[96,521], "MUS-121-C":[97,521], "MUS-121-D":[98,521], "MUS-121-E":[99,521], "MUS-121L-A":[100,739], "MUS-121L-B":[101,739], "MUS-121L-C":[102,739], "MUS-121L-D":[103,739], "SCI-110-A":[104,1004], "SCI-240-A":[105,1031], 
			"MUS-121L-E":[106,739], "MUS-121L-F":[107,739], "PHYS-151-A":[108,602], "MUS-130-A":[109,507], "MUS-130-A":[110,507], "MUS-130-A":[111,507], "SCI-121-A":[112,928], "MUS-130-A":[113,507], "SCI-121L-A01":[114,596], "MUS-130-A":[115,507], "SCI-121L-A02":[116,596], "MUS-130-A":[117,507], 
			"PHYS-151L-A01":[118,897], "PHYS-151L-A02":[119,897], "PHYS-151L-A03":[120,897], "PHYS-181-A":[121,651], "PHYS-181L-A01":[122,738], "PHYS-181L-A02":[123,738], "PHYS-281-A":[124,604], "PHYS-281L-A01":[125,957], "PHYS-311-A":[126,825], "PHYS-490-A":[127,686], "PHYS-369-A":[128,562], 
			"MUS-130-A":[129,507], "MUS-130-A":[130,507], "MUS-130-A":[131,507], "MUS-130-A":[132,507], "MUS-130-A":[133,507], "MUS-130-A":[134,507], "NURS-234-A":[135,614], "MUS-130-A":[136,507], "MUS-130-A":[137,507], "MUS-130-A":[138,507], "MUS-130-A":[139,507], "MUS-130-A":[140,507], 
			"MUS-130-A":[141,507], "MUS-130-A":[142,507], "MUS-130-A":[143,507], "MUS-130-A":[144,507], "MUS-130-A":[145,507], "MUS-130-B":[146,507], "MUS-130-C":[147,507], "MUS-130-D":[148,507], "MUS-130-F":[149,507], "MUS-130-G":[150,507], "MUS-130-I":[151,507], "MUS-130-J":[152,507], 
			"MUS-130-K":[153,507], "MUS-130-L":[154,507], "MUS-130-N":[155,507], "MUS-130-O":[156,507], "MUS-130-P":[157,507], "MUS-131-A":[158,1029], "MUS-131L-A":[159,857], "MUS-110-A":[160,979], "MUS-145-A":[161,834], "MUS-227-A":[162,913], "MUS-230-A":[163,484], "MUS-230-A":[164,484], 
			"MUS-230-A":[165,484], "MUS-230-A":[166,484], "MUS-230-A":[167,484], "NURS-235-A":[168,801], "MUS-230-A":[169,484], "NURS-235-B":[170,801], "MUS-230-A":[171,484], "NURS-235-C":[172,801], "NURS-235-D":[173,801], "NURS-235-E":[174,801], "NURS-235L-01":[175,735], "MUS-230-A":[176,484], 
			"NURS-235L-02":[177,735], "NURS-235L-03":[178,735], "MUS-230-A":[179,484], "MUS-230-A":[180,484], "MUS-230-A":[181,484], "NURS-235L-04":[182,735], "MUS-230-A":[183,484], "MUS-230-A":[184,484], "NURS-235L-05":[185,735], "NURS-370-A":[186,573], "NURS-371-A":[187,859], "NURS-374-A":[188,1030], 
			"NURS-376-A":[189,516], "NURS-377-A":[190,615], "NURS-378-A":[191,706], "MUS-230-A":[192,484], "NURS-390-A":[193,806], "MUS-230-A":[194,484], "NURS-420-A":[195,971], "NURS-421-A":[196,707], "NURS-490-A":[197,788], "MUS-230-A":[198,484], "MUS-230-A":[199,484], "MUS-230-A":[200,484], 
			"MUS-230-A":[201,484], "MUS-230-A":[202,484], "MUS-230-B":[203,484], "MUS-230-C":[204,484], "MUS-230-D":[205,484], "MUS-230-F":[206,484], "NURS-234-B":[207,614], "NURS-425-A":[208,657], "MUS-230-G":[209,484], "MUS-230-I":[210,484], "MUS-230-J":[211,484], "MUS-230-K":[212,484], 
			"MUS-230-L":[213,484], "MUS-230-N":[214,484], "MUS-230-O":[215,484], "MUS-230-P":[216,484], "MUS-231-A":[217,830], "NURS-425L-A01":[218,724], "NURS-425L-A02":[219,724], "MUS-231-B":[220,830], "MUS-231-C":[221,830], "MUS-231-D":[222,830], "MUS-231L-A":[223,715], "CS-130-A":[224,767], 
			"MUS-231L-B":[225,715], "CS-130-B":[226,767], "MUS-231L-C":[227,715], "MUS-231L-D":[228,715], "CS-140-A":[229,951], "MUS-231L-E":[230,715], "CS-140-B":[231,951], "MUS-238-A":[232,932], "CS-150-A":[233,893], "CS-150-B":[234,893], "MUS-250-A":[235,850], "CS-160-A":[236,701], 
			"MUS-250-B":[237,850], "CS-165-A":[238,810], "MUS-250-C":[239,850], "CS-253-A":[240,629], "MUS-250-D":[241,850], "MUS-273-A":[242,743], "MUS-273-B":[243,743], "MUS-273-D":[244,743], "MUS-273-E":[245,743], "MUS-273-F":[246,743], "MUS-273-C":[247,743], "MUS-273-G":[248,743], 
			"MUS-273-H":[249,743], "MUS-273-I":[250,743], "MUS-273-J":[251,743], "MUS-273-K":[252,743], "MUS-273-L":[253,743], "CS-360-A":[254,536], "CS-490-A":[255,878], "MUS-273-M":[256,743], "CS-296-A":[257,1055], "MUS-273-N":[258,743], "MUS-273-O":[259,743], "MUS-273-P":[260,743], 
			"MUS-300-A":[261,485], "MUS-300-A":[262,485], "MUS-300-A":[263,485], "CS-120-A":[264,737], "MUS-300-A":[265,485], "MUS-300-A":[266,485], "MUS-300-A":[267,485], "MUS-300-A":[268,485], "MUS-300-A":[269,485], "CS-150-C":[270,893], "CS-160-B":[271,701], "MUS-300-A":[272,485], 
			"MUS-300-A":[273,485], "MUS-300-A":[274,485], "CS-260-A":[275,592], "CS-320-A":[276,984], "MUS-300-A":[277,485], "MUS-300-A":[278,485], "CS-430-A":[279,867], "MUS-300-A":[280,485], "MUS-300-A":[281,485], "MUS-300-A":[282,485], "MUS-300-A":[283,485], "MUS-300-A":[284,485], 
			"MUS-300-A":[285,485], "MUS-300-A":[286,485], "MUS-300-A":[287,485], "MUS-300-A":[288,485], "PHIL-100-A":[289,841], "PHIL-100-B":[290,841], "PHIL-120-A":[291,782], "PHIL-140-A":[292,807], "PHIL-150-A":[293,997], "PHIL-200-A":[294,809], "PHIL-490-A":[295,952], "PHIL-300-A":[296,911], 
			"PHIL-485-A":[297,668], "MUS-330-A":[298,508], "MUS-330-A":[299,508], "MUS-330-A":[300,508], "MUS-330-A":[301,508], "MUS-330-A":[302,508], "MUS-330-A":[303,508], "MUS-330-A":[304,508], "MUS-330-A":[305,508], "MUS-330-A":[306,508], "MUS-330-A":[307,508], "MUS-330-A":[308,508], 
			"MUS-330-A":[309,508], "MUS-330-A":[310,508], "MUS-330-A":[311,508], "MUS-330-A":[312,508], "MUS-330-A":[313,508], "MUS-330-A":[314,508], "MUS-330-A":[315,508], "MUS-330-A":[316,508], "MUS-330-A":[317,508], "MUS-330-A":[318,508], "MUS-330-A":[319,508], "MUS-330-B":[320,508], 
			"MUS-330-C":[321,508], "MUS-330-D":[322,508], "MUS-330-F":[323,508], "MUS-330-G":[324,508], "MUS-330-I":[325,508], "MUS-330-J":[326,508], "MUS-330-K":[327,508], "MUS-330-L":[328,508], "MUS-330-N":[329,508], "MUS-330-O":[330,508], "MUS-330-P":[331,508], "CHIN-101-A":[332,682], 
			"MUS-338-A":[333,989], "CHIN-201-A":[334,924], "MUS-360-A":[335,1011], "MUS-362-A":[336,936], "MUS-362-A":[337,936], "MUS-362-A":[338,936], "MUS-430-A":[339,510], "MUS-430-A":[340,510], "MUS-430-A":[341,510], "MUS-430-A":[342,510], "MUS-430-A":[343,510], "MUS-430-A":[344,510], 
			"MUS-430-A":[345,510], "MUS-430-A":[346,510], "MUS-430-A":[347,510], "MUS-430-A":[348,510], "MUS-430-A":[349,510], "MUS-430-A":[350,510], "MUS-430-A":[351,510], "MUS-430-A":[352,510], "MUS-430-A":[353,510], "CHIN-242-A":[354,501], "FCUL-242-A":[355,750], "MUS-430-A":[356,510], 
			"FREN-101-A":[357,569], "MUS-430-A":[358,510], "FREN-102-A":[359,794], "MUS-430-A":[360,510], "FREN-202-A":[361,912], "MUS-430-A":[362,510], "FREN-342-A":[363,762], "MUS-430-A":[364,510], "MUS-430-A":[365,510], "FREN-347-A":[366,978], "MUS-430-B":[367,510], "MUS-430-C":[368,510], 
			"FREN-490-A":[369,786], "MUS-430-D":[370,510], "GER-101-A":[371,1060], "MUS-430-F":[372,510], "GER-101-B":[373,1060], "MUS-430-G":[374,510], "MUS-430-I":[375,510], "MUS-430-J":[376,510], "GER-102-A":[377,731], "GER-201-A":[378,1000], "MUS-430-K":[379,510], "MUS-430-L":[380,510], 
			"GER-202-A":[381,732], "MUS-430-N":[382,510], "GER-470-A":[383,492], "MUS-430-O":[384,510], "MUS-430-P":[385,510], "MUS-490-A":[386,1035], "MUS-491-A":[387,576], "GER-490-A":[388,1067], "MUS-115-A":[389,816], "ITAL-101-A":[390,713], "MUS-469-A":[391,772], "LING-131-A":[392,1008], 
			"LING-235-A":[393,755], "LING-350-A":[394,544], "RUS-101-A":[395,534], "RUS-201-A":[396,958], "RUS-490-A":[397,720], "SCST-345-A":[398,1064], "SCST-201-A":[399,946], "SCST-101-A":[400,522], "SCST-101-B":[401,522], "SCST-101-C":[402,522], "ENVS-230-A":[403,950], "ENVS-330-A":[404,551], 
			"ENVS-310-A":[405,820], "ENVS-310L-A01":[406,778], "ENVS-133-A":[407,567], "ENVS-133L-A01":[408,568], "ENVS-239-A":[409,665], "ENVS-175-A":[410,526], "ENG-110-A":[411,1041], "ENG-110-B":[412,1041], "RUS-239-A":[413,1077], "FCUL-239-A":[414,1071], "ENG-114-A":[415,783], "ENG-114-B":[416,783], 
			"ENG-130-B":[417,524], "ENG-130-A":[418,524], "ENG-212-A":[419,1043], "ENG-213-A":[420,560], "ENG-230-A":[421,666], "ENG-239-A":[422,795], "ENG-245-A":[423,509], "WGST-245-A":[424,570], "ENG-251-A":[425,610], "AFRS-251-A":[426,1032], "WGST-251-A":[427,1028], "ENG-260-B":[428,774], 
			"ENG-314-A":[429,993], "ENG-353-A":[430,817], "ENG-364-A":[431,621], "ENG-366-A":[432,1047], "ENG-485-A":[433,849], "ENG-490-A":[434,625], "ENG-260-A":[435,774], "ACCTG-110-A":[436,611], "ACCTG-110-B":[437,611], "ACCTG-150-A":[438,1066], "ACCTG-150-B":[439,1066], "ACCTG-150-C":[440,1066], 
			"ACCTG-353-A":[441,632], "ACCTG-358-A":[442,689], "ACCTG-365-A":[443,555], "ACCTG-467-A":[444,919], "ECON-130-A":[445,619], "ECON-130-B":[446,619], "ECON-130-C":[447,619], "ECON-130-D":[448,619], "ECON-247-A":[449,986], "ECON-256-A":[450,711], "ECON-342-A":[451,879], "ECON-262-A":[452,1070], 
			"MGT-150-A":[453,572], "MGT-240-A":[454,696], "MGT-240-B":[455,696], "MGT-240-C":[456,696], "MGT-250-A":[457,765], "MGT-250-B":[458,765], "MGT-351-A":[459,1033], "MGT-351-B":[460,1033], "MGT-352-A":[461,504], "MGT-352-B":[462,504], "MGT-353-A":[463,578], "MGT-353-B":[464,578], "MGT-360-A":[465,520], 
			"MGT-366-A":[466,798], "MGT-364-A":[467,1034], "MGT-490-A":[468,714], "MGT-490-B":[469,714], "MGT-490-C":[470,714], "MGT-490-D":[471,714], "MGT-490-E":[472,714], "MGT-490-F":[473,714], "MGT-490-G":[474,714], "MGT-490-H":[475,714], "FCUL-350-A":[476,709], "RUS-350-A":[477,503], "SPAN-101-A":[478,886], 
			"SPAN-102-A":[479,617], "SPAN-102-B":[480,617], "SPAN-102-C":[481,617], "SPAN-102-D":[482,617], "SPAN-201-A":[483,482], "SPAN-201-B":[484,482], "SPAN-201-C":[485,482], "SPAN-201-D":[486,482], "SPAN-302-A":[487,726], "SPAN-302-B":[488,726], "SPAN-303-A":[489,506], "SPAN-303-B":[490,506], 
			"SPAN-304-A":[491,681], "SPAN-346-A":[492,645], "REL-101-A":[493,559], "SPAN-490-A":[494,1013], "REL-101-B":[495,559], "REL-101-C":[496,559], "REL-101-D":[497,559], "REL-101-E":[498,559], "REL-101-F":[499,559], "REL-101-G":[500,559], "REL-101-H":[501,559], "REL-101-I":[502,559], 
			"REL-101-J":[503,559], "REL-101-K":[504,559], "REL-101-L":[505,559], "REL-211-A":[506,813], "SPAN-450-A":[507,612], "REL-221-A":[508,582], "REL-227-A":[509,785], "COMS-130-A":[510,616], "REL-231-A":[511,838], "COMS-130-B":[512,616], "COMS-132-A":[513,747], "COMS-132-B":[514,747], 
			"COMS-133-A":[515,584], "COMS-133-B":[516,584], "COMS-463-A":[517,488], "REL-235-A":[518,892], "COMS-234-A":[519,904], "COMS-258-A":[520,1006], "REL-241-A":[521,493], "COMS-350-A":[522,818], "REL-241-B":[523,493], "COMS-255-A":[524,718], "COMS-362-A":[525,1075], "COMS-357-A":[526,847], 
			"REL-250-A":[527,925], "SCI-340-A":[528,802], "REL-250-B":[529,925], "REL-251-A":[530,633], "REL-262-A":[531,960], "REL-262-B":[532,960], "BIO-115-A":[533,920], "BIO-115L-A01":[534,824], "BIO-115L-A02":[535,824], "BIO-115L-A03":[536,824], "BIO-115L-A04":[537,824], "BIO-116-A":[538,987], 
			"BIO-116L-A01":[539,702], "BIO-116L-A02":[540,702], "BIO-116L-A03":[541,702], "REL-485-A":[542,685], "REL-364-A":[543,1022], "REL-490-A":[544,1045], "HEB-101-A":[545,598], "BIO-116L-A04":[546,702], "BIO-125-A":[547,667], "BIO-125L-A01":[548,674], "BIO-151-A":[549,921], "BIO-151L-A01":[550,580], 
			"ART-103-A":[551,1037], "BIO-151L-A02,":[552,580], "BIO-151L-A03":[553,580], "ART-108-A":[554,823], "BIO-151L-A04":[555,580], "ART-108-B":[556,823], "ART-110-A":[557,499], "ART-111-A":[558,556], "ART-111-A":[559,556], "ART-118-A":[560,722], "BIO-151L-A05":[561,580], "ART-216-A":[562,676], 
			"BIO-151L-A06":[563,580], "BIO-151L-A07":[564,580], "BIO-151L-A08":[565,580], "BIO-151L-A09":[566,580], "BIO-151L-A10":[567,580], "BIO-151L-A11":[568,580], "BIO-231-A":[569,836], "BIO-243-A":[570,855], "ART-239-A":[571,519], "BIO-243L-A01":[572,557], "BIO-243L-A02":[573,557], "BIO-243L-A03":[574,557], 
			"BIO-243L-A04":[575,557], "BIO-255-A":[576,759], "BIO-255L-A01":[577,558], "ART-251-A":[578,494], "BIO-255L-A02":[579,558], "BIO-255L-A03":[580,558], "ART-300-A":[581,548], "ART-300-A":[582,548], "BIO-255L-A04":[583,558], "ART-368-A":[584,528], "WGST-368-A":[585,1051], "ART-490-A":[586,947], 
			"DAN-100-A":[587,1001], "BIO-256-A":[588,1016], "DAN-100-B":[589,1001], "BIO-256L-A01":[590,852], "BIO-256L-A02":[591,852], "DAN-100-C":[592,1001], "DAN-101-A":[593,599], "DAN-130-A":[594,908], "BIO-301-A":[595,853], "BIO-301L-A01":[596,537], "BIO-301L-A02":[597,537], "BIO-364-A":[598,959], 
			"WGST-131-A":[599,1014], "DAN-300-A":[600,963], "BIO-364L-A01":[601,608], "BIO-365-A":[602,581], "BIO-365L-A":[603,790], "BIO-490-A":[604,999], "THE-300-A":[605,996], "BIO-303-A":[606,860], "BIO-359-A":[607,628], "DAN-360-A":[608,589], "BIO-251-A":[609,495], "BIO-251L-A":[610,982], 
			"DAN-490-A":[611,970], "THE-100-A":[612,553], "THE-100-B":[613,553], "THE-100-C":[614,553], "POLS-139-A":[615,903], "POLS-132-A":[616,626], "POLS-132-B":[617,626], "POLS-362-A":[618,808], "POLS-247-A":[619,1053], "POLS-258-A":[620,948], "POLS-335-A":[621,758], "POLS-355-A":[622,945], 
			"POLS-490-A":[623,1063], "POLS-485-A":[624,940], "ANTH-101-A":[625,479], "ANTH-101-B":[626,479], "ANTH-101-C":[627,479], "ANTH-102-A":[628,1025], "ANTH-104-A":[629,1012], "ANTH-205-A":[630,780], "THE-105-A":[631,627], "THE-105-B":[632,627], "ANTH-210-A":[633,590], "THE-200-A":[634,964], 
			"ANTH-339-A":[635,827], "ANTH-490-A":[636,646], "WGST-130-A":[637,1027], "THE-204-A":[638,907], "THE-204-A":[639,907], "SOC-101-A":[640,554], "SOC-101-B":[641,554], "SOC-101-C":[642,554], "THE-204-B":[643,907], "THE-204-B":[644,907], "SOC-242-A":[645,934], "WGST-242-A":[646,1050], 
			"SOC-270-A":[647,660], "SOC-301-A":[648,885], "SOC-356-A":[649,607], "SOC-468-A":[650,1042], "WGST-468-A":[651,564], "THE-490-A":[652,915], "SOC-490-A":[653,535], "SW-101-A":[654,716], "EDUC-220-A":[655,894], "EDUC-220-B":[656,894], "SW-110-A":[657,565], "EDUC-220-C":[658,894], 
			"SW-201-A":[659,579], "SW-301-A":[660,663], "EDUC-221-A":[661,791], "SW-303-A":[662,694], "EDUC-221-B":[663,791], "SW-401-A":[664,547], "SW-402-A":[665,757], "EDUC-223-A":[666,622], "SW-403-A":[667,481], "SW-490-A":[668,992], "EDUC-226-A":[669,575], "EDUC-240-A":[670,636], 
			"EDUC-242-A":[671,977], "PAID-450-A":[672,591], "PAID-450-A":[673,591], "PAID-450-A":[674,591], "PAID-450-A":[675,591], "PAID-111D-01":[676,515], "PAID-111D-02":[677,515], "PAID-111D-03":[678,515], "PAID-111D-04":[679,515], "PAID-111D-05":[680,515], "PAID-111D-06":[681,515], 
			"PAID-111D-07":[682,515], "EDUC-245-A":[683,1048], "PAID-111D-08":[684,515], "PAID-111D-09":[685,515], "EDUC-255-A":[686,511], "PAID-111D-10":[687,515], "PAID-111D-12":[688,515], "PAID-111D-13":[689,515], "PAID-111D-14":[690,515], "PAID-111D-15":[691,515], "PAID-111D-16":[692,515], 
			"PAID-111D-17":[693,515], "PAID-111D-18":[694,515], "PAID-111D-19":[695,515], "PAID-111D-20":[696,515], "PAID-111D-21":[697,515], "PAID-111D-22":[698,515], "PAID-111D-23":[699,515], "PAID-111D-24":[700,515], "PAID-111D-26":[701,515], "PAID-111D-27":[702,515], "PAID-111D-28":[703,515], 
			"PAID-111D-29":[704,515], "PAID-111D-30":[705,515], "PAID-111D-31":[706,515], "PAID-111D-32":[707,515], "PAID-111D-33":[708,515], "PAID-111D-34":[709,515], "CLAS-250-A":[710,961], "CLAS-240-A":[711,498], "CLAS-300-A":[712,1044], "CLAS-490-A":[713,637], "CLAS-320-A":[714,775], 
			"WGST-320-A":[715,895], "GRK-101-A":[716,638], "GRK-201-A":[717,995], "GRK-490-A":[718,741], "EDUC-260-A":[719,863], "EDUC-265-A":[720,583], "EDUC-270-A":[721,1026], "EDUC-275-A":[722,846], "EDUC-377-A":[723,1057], "EDUC-325-A":[724,763], "EDUC-325-B":[725,763], "EDUC-326-A":[726,490], 
			"EDUC-326-B":[727,490], "EDUC-330-A":[728,955], "EDUC-332-A":[729,719], "EDUC-352-A":[730,542], "EDUC-352-A":[731,542], "EDUC-352-A":[732,542], "EDUC-352-A":[733,542], "LAT-101-A":[734,687], "LAT-101-B":[735,687], "LAT-201-A":[736,927], "GRK-301-A":[737,872], "LAT-301-A":[738,704], 
			"LAT-490-A":[739,899], "ATHTR-265-A":[740,871], "ATHTR-490-A":[741,793], "ATHTR-365-A":[742,680], "ATHTR-465-A":[743,623], "ATHTR-465-A7":[44,623], "HLTH-490-A":[745,1019], "HLTH-249-A":[746,588], "EDUC-353-A":[747,864], "HLTH-126-A":[748,563], "EDUC-371-A":[749,672], "HLTH-125-A":[750,729], 
			"EDUC-371L-A":[751,517], "HLTH-233-A":[752,695], "HLTH-343-A":[753,941], "EDUC-382-A":[754,530], "HLTH-201-A":[755,819], "EDUC-379-A":[756,804], "HLTH-465-A":[757,734], "PE-323-A":[758,829], "PE-251-A":[759,744], "EDUC-378-A":[760,938], "PE-221-A":[761,769], "PE-221-A":[762,769], 
			"EDUC-383-A":[763,931], "PE-226-A":[764,764], "PE-247-A":[765,916], "EDUC-384-A":[766,828], "EDUC-385-A":[767,658], "PE-229-A":[768,752], "EDUC-386-A":[769,784], "EDUC-386-B":[770,784], "PE-345-A":[771,721], "EDUC-387-A":[772,1056], "PE-343-A":[773,655], "EDUC-390-A":[774,543], 
			"EDUC-470-A":[775,529], "PE-456-A":[776,771], "EDUC-486-A":[777,1018], "EDUC-490-A":[778,826], "EDUC-323-A":[779,939], "PE-490-A":[780,981], "PE-190-A":[781,812], "PE-365-A":[782,652], "PE-261-A":[783,998], "EDUC-372-A":[784,926], "PE-260-A":[785,577], "PE-250-A":[786,497], 
			"MUS-244-A":[787,842], "MUS-346-A":[788,1062], "PE-110-B01":[789,541], "PE-110-B01":[790,541], "PE-110-B01":[791,541], "WGST-270-A":[792,673], "WGST-490-A":[793,797], "WGST-290-A":[794,531], "HIST-290-A":[795,843], "PE-110-B01":[796,541], "PE-110-B01":[797,541], "PE-110-B01":[798,541], 
			"PE-110-B01":[799,541], "PE-110-B01":[800,541], "PE-110-B01":[801,541], "PE-110-C01":[802,541], "PE-110-C01":[803,541], "PE-110-C01":[804,541], "PE-110-C01":[805,541], "PE-110-C01":[806,541], "PE-110-C01":[807,541], "ENG-239-A":[808,795], "WGST-239-A":[809,630], "PE-100-B02":[810,710], 
			"PE-100-B02":[811,710], "AFRS-135-A":[812,1073], "HIST-135-A":[813,659], "AFRS-171-A":[814,1039], "HIST-171-A":[815,991], "SPAN-239-A":[816,594], "PE-100-B01":[817,710], "PE-100-B01":[818,710], "AFRS-339-A":[819,966], "PE-100-B05":[820,710], "PE-100-B05":[821,710], "HIST-339-A":[822,884], 
			"PE-100-B04":[823,710], "PE-100-B04":[824,710], "AFRS-490-A":[825,1036], "PE-100-B03":[826,710], "PE-100-B03":[827,710], "PE-100-C03":[828,710], "PE-100-C03":[829,710], "HIST-101-A":[830,944], "HIST-111-A":[831,837], "PE-100-C04":[832,710], "PE-100-C04":[833,710], "PE-100-C02":[834,710], 
			"PE-100-C02":[835,710], "PE-100-C01":[836,710], "PE-100-C01":[837,710], "PE-100-C05":[838,710], "PE-100-C05":[839,710], "HIST-126-A":[840,723], "HIST-149-A":[841,703], "HIST-226-A":[842,644], "HIST-351-A":[843,613], "HIST-362-A":[844,891], "HIST-485-A":[845,650], "HIST-490-A":[846,605], 
			"GS-100-A":[847,754], "GS-100-B":[848,754], "GS-100-C":[849,754], "GS-110-A":[850,525], "GS-110-B":[851,525], "INTS-306-A":[852,898], "ENVS-485-A":[853,953], "ENVS-485-A":[854,953], "THE-305-A":[855,603], "MUS-345-A":[856,1058], "MUS-342-A":[857,533], "MUS-343-A":[858,900], "COMS-490-A":[859,1074], 
			"JOUR-100-A":[860,980], "MUS-115-A":[861,816], "MUS-130-A":[862,507], "MUS-230-A":[863,484], "MUS-230-A":[864,484], "MUS-430-A":[865,510], "THE-103-A":[866,766], "ART-228-A":[867,815], "ART-200-A":[868,717], "ART-200-A":[869,717], "ART-316-A":[870,549]}

sections = {1: 'WGST-251-A', 2: 'SW-403-A', 3: 'FREN-102-A', 4: 'MGT-490-H', 5: 'MGT-490-B', 6: 'MGT-490-C', 7: 'FREN-101-A', 8: 'MGT-490-A', 9: 'MGT-490-F', 10: 'MGT-490-G', 11: 'MGT-490-D', 12: 'MGT-490-E', 13: 'ENVS-485-A', 14: 'CS-296-A', 15: 'AFRS-490-A', 16: 'BIO-359-A', 17: 'MATH-151-D', 
			18: 'MATH-151-C', 19: 'MATH-151-B', 20: 'MATH-151-A', 21: 'DAN-490-A', 22: 'PE-110-C01', 23: 'CS-165-A', 24: 'GS-110-B', 25: 'MATH-115-B', 26: 'MATH-115-A', 27: 'REL-227-A', 28: 'PE-190-A', 29: 'EDUC-323-A', 30: 'SCST-201-A', 31: 'MATH-351-A', 32: 'ENG-314-A', 33: 'SPAN-101-A', 
			34: 'ACCTG-365-A', 35: 'SPAN-201-A', 36: 'SPAN-201-C', 37: 'SPAN-201-B', 38: 'SPAN-201-D', 39: 'MUS-342-A', 40: 'RUS-201-A', 41: 'MUS-345-A', 42: 'CLAS-240-A', 43: 'MUS-273-I', 44: 'ANTH-205-A', 45: 'MUS-121-B', 46: 'MUS-121-C', 47: 'MUS-121-A', 48: 'THE-100-A', 49: 'MUS-121-D', 
			50: 'THE-100-B', 51: 'SCI-110-A', 52: 'COMS-362-A', 53: 'CHEM-201-A', 54: 'EDUC-245-A', 55: 'EDUC-242-A', 56: 'CS-320-A', 57: 'CS-120-A', 58: 'MUS-273-E', 59: 'ACCTG-467-A', 60: 'MUS-145-A', 61: 'CS-360-A', 62: 'IS-485-A', 63: 'MUS-244-A', 64: 'HIST-362-A', 65: 'BIO-125-A', 
			66: 'PHIL-120-A', 67: 'POLS-490-A', 68: 'BIO-231-A', 69: 'ART-103-A', 70: 'EDUC-265-A', 71: 'ENG-230-A', 72: 'ATHTR-465-A', 73: 'CLAS-250-A', 74: 'CS-160-A', 75: 'CS-160-B', 76: 'PE-250-A', 77: 'THE-200-A', 78: 'ART-490-A', 79: 'SCST-345-A', 80: 'PE-251-A', 81: 'MUS-362-A', 
			82: 'MUS-360-A', 83: 'AFRS-135-A', 84: 'ENG-239-A', 85: 'ENVS-310L-A01', 86: 'CHEM-151L-08', 87: 'CHEM-151L-09', 88: 'CHEM-151L-06', 89: 'CHEM-151L-07', 90: 'CHEM-151L-04', 91: 'CHEM-151L-05', 92: 'CHEM-151L-02', 93: 'CHEM-151L-03', 94: 'CHEM-151L-01', 95: 'NURS-425L-A01', 
			96: 'NURS-425L-A02', 97: 'ENG-251-A', 98: 'LAT-301-A', 99: 'COMS-350-A', 100: 'EDUC-384-A', 101: 'AFRS-251-A', 102: 'PSYC-241-A', 103: 'ENVS-133-A', 104: 'BIO-364-A', 105: 'EDUC-386-A', 106: 'EDUC-386-B', 107: 'DAN-300-A', 108: 'CHEM-344-A', 109: 'PE-456-A', 110: 'COMS-234-A', 
			111: 'EDUC-221-A', 112: 'EDUC-221-B', 113: 'HLTH-233-A', 114: 'MUS-430-P', 115: 'MUS-430-I', 116: 'PSYC-240-B', 117: 'MUS-430-K', 118: 'MUS-430-J', 119: 'MUS-430-L', 120: 'EDUC-240-A', 121: 'PE-490-A', 122: 'MUS-430-A', 123: 'MUS-430-C', 124: 'MUS-430-B', 125: 'AFRS-339-A', 
			126: 'COMS-357-A', 127: 'MUS-430-G', 128: 'MUS-430-F', 129: 'PAID-450-A', 130: 'ECON-256-A', 131: 'ENG-213-A', 132: 'GER-490-A', 133: 'GER-101-B', 134: 'GER-101-A', 135: 'ENG-130-A', 136: 'GER-102-A', 137: 'ENG-130-B', 138: 'HIST-171-A', 139: 'EDUC-382-A', 140: 'BIO-301-A', 
			141: 'ART-368-A', 142: 'WGST-245-A', 143: 'REL-101-L', 144: 'REL-101-H', 145: 'REL-101-I', 146: 'REL-101-J', 147: 'REL-101-K', 148: 'REL-101-D', 149: 'REL-101-E', 150: 'REL-101-F', 151: 'REL-101-G', 152: 'REL-101-A', 153: 'REL-101-B', 154: 'MUS-330-G', 155: 'CHEM-365-A', 
			156: 'SOC-242-A', 157: 'SOC-468-A', 158: 'EDUC-379-A', 159: 'REL-235-A', 160: 'SW-101-A', 161: 'MUS-115-B', 162: 'MUS-115-A', 163: 'EDUC-353-A', 164: 'CHIN-242-A', 165: 'PHIL-200-A', 166: 'MATH-471-A', 167: 'BIO-255L-A01', 168: 'GRK-201-A', 169: 'MATH-123-A', 170: 'MATH-123-B',
			171: 'MATH-327-A', 172: 'CS-150-A', 173: 'CS-150-B', 174: 'CS-150-C', 175: 'PSYC-240-A', 176: 'SW-301-A', 177: 'REL-211-A', 178: 'GS-110-A', 179: 'SW-303-A', 180: 'MUS-430-O', 181: 'MUS-430-N', 182: 'SW-402-A', 183: 'SOC-101-A', 184: 'SOC-101-B', 185: 'SOC-101-C', 186: 'MUS-430-D', 
			187: 'MATH-339-A', 188: 'PSYC-465-B', 189: 'PSYC-465-A', 190: 'SCI-121-A', 191: 'EDUC-330-A', 192: 'MGT-353-B', 193: 'CLAS-490-A', 194: 'PAID-111D-16', 195: 'PAID-111D-17', 196: 'PAID-111D-10', 197: 'PAID-111D-12', 198: 'PAID-111D-13', 199: 'PAID-111D-18', 200: 'MUS-131L-A', 
			201: 'COMS-130-A', 202: 'COMS-130-B', 203: 'BIO-243-A', 204: 'COMS-133-B', 205: 'COMS-133-A', 206: 'EDUC-486-A', 207: 'CHIN-101-A', 208: 'CHEM-151-B', 209: 'CHEM-151-C', 210: 'JOUR-100-A', 211: 'CHEM-151-A', 212: 'PHYS-181-A', 213: 'NURS-378-A', 214: 'ENG-366-A', 215: 'PHIL-300-A', 
			216: 'EDUC-255-A', 217: 'PHIL-485-A', 218: 'MGT-366-A', 219: 'MUS-130-P', 220: 'NURS-490-A', 221: 'FREN-202-A', 222: 'SPAN-102-A', 223: 'SPAN-102-C', 224: 'SPAN-102-B', 225: 'SPAN-102-D', 226: 'EDUC-371-A', 227: 'BIO-303-A', 228: 'MUS-330-P', 229: 'MUS-330-J', 230: 'MUS-330-K', 
			231: 'THE-490-A', 232: 'MUS-330-I', 233: 'NURS-377-A', 234: 'MUS-330-O', 235: 'MUS-330-L', 236: 'MUS-330-B', 237: 'MUS-330-C', 238: 'MUS-330-A', 239: 'MUS-330-F', 240: 'GRK-490-A', 241: 'MUS-330-D', 242: 'ATHTR-265-A', 243: 'MUS-130-O', 244: 'EDUC-390-A', 245: 'BIO-255L-A04', 
			246: 'HLTH-465-A', 247: 'BIO-255L-A03', 248: 'BIO-255L-A02', 249: 'MGT-364-A', 250: 'MUS-490-A', 251: 'ART-200-A', 252: 'PHYS-281-A', 253: 'WGST-490-A', 254: 'MUS-130-F', 255: 'MATH-240-B', 256: 'MATH-240-A', 257: 'PSYC-270-A', 258: 'PSYC-350-A', 259: 'PSYC-350-B', 260: 'SCST-101-A', 
			261: 'MUS-250-D', 262: 'SCST-101-C', 263: 'SCST-101-B', 264: 'MUS-250-A', 265: 'MUS-250-C', 266: 'MUS-250-B', 267: 'MUS-130-I', 268: 'MUS-130-J', 269: 'MUS-130-K', 270: 'MUS-130-L', 271: 'MUS-130-N', 272: 'BIO-251L-A', 273: 'MUS-130-A', 274: 'MUS-130-B', 275: 'MUS-130-C', 276: 'MUS-130-D', 
			277: 'WGST-320-A', 278: 'POLS-355-A', 279: 'MUS-130-G', 280: 'POLS-362-A', 281: 'HIST-226-A', 282: 'ART-251-A', 283: 'CHIN-201-A', 284: 'PE-261-A', 285: 'HLTH-343-A', 286: 'CS-490-A', 287: 'ANTH-490-A', 288: 'PE-323-A', 289: 'SPAN-304-A', 290: 'FCUL-350-A', 291: 'MUS-231-B', 
			292: 'MUS-231-C', 293: 'MUS-231-A', 294: 'MUS-231-D', 295: 'ENG-245-A', 296: 'MUS-116-C', 297: 'PAID-111D-26', 298: 'PHIL-140-A', 299: 'EDUC-371L-A', 300: 'FREN-490-A', 301: 'RUS-101-A', 302: 'MATH-490-A', 303: 'THE-305-A', 304: 'SCI-340-A', 305: 'PSYC-353L-A', 306: 'PSYC-353L-B', 
			307: 'HLTH-201-A', 308: 'SOC-356-A', 309: 'PE-343-A', 310: 'PHIL-150-A', 311: 'FREN-342-A', 312: 'FREN-347-A', 313: 'SW-401-A', 314: 'THE-300-A', 315: 'ART-110-A', 316: 'PAID-111D-07', 317: 'PAID-111D-06', 318: 'BIO-301L-A01', 319: 'PAID-111D-04', 320: 'PAID-111D-03', 321: 'PAID-111D-02', 
			322: 'PAID-111D-01', 323: 'PHYS-490-A', 324: 'ECON-342-A', 325: 'BIO-116-A', 326: 'PAID-111D-08', 327: 'ENG-260-A', 328: 'ENG-260-B', 329: 'FCUL-239-A', 330: 'POLS-132-A', 331: 'POLS-132-B', 332: 'EDUC-490-A', 333: 'PE-365-A', 334: 'BIO-151-A', 335: 'ATHTR-490-A', 336: 'ACCTG-150-B', 
			337: 'LAT-201-A', 338: 'PSYC-130-C', 339: 'PSYC-130-B', 340: 'PSYC-130-E', 341: 'PSYC-130-D', 342: 'SOC-270-A', 343: 'REL-101-C', 344: 'PE-100-B01', 345: 'SW-110-A', 346: 'NURS-235-D', 347: 'CLAS-300-A', 348: 'MGT-150-A', 349: 'NURS-421-A', 350: 'EDUC-325-A', 351: 'EDUC-325-B', 
			352: 'COMS-463-A', 353: 'ECON-247-A', 354: 'LING-350-A', 355: 'ACCTG-110-A', 356: 'ACCTG-110-B', 357: 'LAT-490-A', 358: 'MATH-110-A', 359: 'ART-316-A', 360: 'REL-221-A', 361: 'CHEM-201L-01', 362: 'REL-250-B', 363: 'NURS-371-A', 364: 'HLTH-126-A', 365: 'ART-216-A', 366: 'REL-364-A', 
			367: 'ITAL-101-A', 368: 'CS-140-B', 369: 'CS-140-A', 370: 'SPAN-346-A', 371: 'NURS-234-B', 372: 'NURS-234-A', 373: 'WGST-290-A', 374: 'HIST-290-A', 375: 'WGST-131-A', 376: 'LING-235-A', 377: 'REL-241-B', 378: 'REL-241-A', 379: 'GRK-301-A', 380: 'SPAN-302-B', 381: 'SPAN-302-A', 
			382: 'PHYS-151-A', 383: 'CS-430-A', 384: 'THE-103-A', 385: 'LAT-101-B', 386: 'LAT-101-A', 387: 'SPAN-490-A', 388: 'POLS-485-A', 389: 'MATH-152-A', 390: 'MATH-152-B', 391: 'MATH-152-C', 392: 'THE-100-C', 393: 'MUS-121-E', 394: 'ART-239-A', 395: 'WGST-368-A', 396: 'ECON-130-D', 
			397: 'ECON-130-A', 398: 'ECON-130-C', 399: 'ECON-130-B', 400: 'PAID-111D-15', 401: 'LING-131-A', 402: 'HIST-339-A', 403: 'MUS-330-N', 404: 'BIO-151L-A10', 405: 'COMS-490-A', 406: 'RUS-490-A', 407: 'PHIL-490-A', 408: 'PAID-111D-32', 409: 'PAID-111D-33', 410: 'PAID-111D-30', 
			411: 'PAID-111D-31', 412: 'PAID-111D-34', 413: 'SPAN-450-A', 414: 'EDUC-260-A', 415: 'HIST-485-A', 416: 'DAN-130-A', 417: 'WGST-239-A', 418: 'PSYC-490-A', 419: 'POLS-335-A', 420: 'BIO-255-A', 421: 'BIO-256-A', 422: 'EDUC-387-A', 423: 'MUS-346-A', 424: 'ENVS-330-A', 425: 'EDUC-223-A', 
			426: 'EDUC-220-A', 427: 'EDUC-220-C', 428: 'EDUC-220-B', 429: 'HIST-351-A', 430: 'THE-105-A', 431: 'THE-105-B', 432: 'BIO-115L-A01', 433: 'BIO-115L-A02', 434: 'BIO-115L-A03', 435: 'BIO-115L-A04', 436: 'BIO-251-A', 437: 'ENG-212-A', 438: 'PE-100-C01', 439: 'PE-100-C03', 440: 'ENG-353-A', 
			441: 'PE-100-C05', 442: 'PE-100-C04', 443: 'ART-108-B', 444: 'ART-108-A', 445: 'EDUC-383-A', 446: 'HIST-490-A', 447: 'MUS-338-A', 448: 'MUS-343-A', 449: 'MUS-231L-E', 450: 'MUS-231L-D', 451: 'MUS-231L-A', 452: 'MUS-231L-C', 453: 'MUS-231L-B', 454: 'PSYC-354L-A02', 455: 'PSYC-354L-A01', 
			456: 'GRK-101-A', 457: 'MATH-140-A', 458: 'MATH-140-C', 459: 'MATH-140-B', 460: 'MATH-140-E', 461: 'MATH-140-D', 462: 'MATH-140-F', 463: 'ART-300-A', 464: 'REL-490-A', 465: 'PHIL-100-A', 466: 'PHIL-100-B', 467: 'ACCTG-353-A', 468: 'ATHTR-465-A7', 469: 'ART-228-A', 470: 'GER-470-A', 
			471: 'BIO-243L-A02', 472: 'BIO-243L-A03', 473: 'BIO-243L-A01', 474: 'BIO-243L-A04', 475: 'SOC-301-A', 476: 'WGST-468-A', 477: 'HIST-101-A', 478: 'DAN-360-A', 479: 'ENVS-133L-A01', 480: 'BIO-364L-A01', 481: 'REL-231-A', 482: 'CHEM-490L-01', 483: 'CHEM-241L-02', 484: 'CHEM-241L-03', 
			485: 'PSYC-349-A', 486: 'CHEM-241L-01', 487: 'CHEM-241L-04', 488: 'CHEM-241L-05', 489: 'PAID-111D-29', 490: 'PAID-111D-28', 491: 'BIO-151L-A01', 492: 'PAID-111D-24', 493: 'PAID-111D-27', 494: 'WGST-270-A', 495: 'PAID-111D-21', 496: 'PAID-111D-20', 497: 'PAID-111D-23', 498: 'PAID-111D-22', 
			499: 'EDUC-226-A', 500: 'INTS-306-A', 501: 'MUS-227-A', 502: 'BIO-301L-A02', 503: 'PAID-111D-05', 504: 'EDUC-385-A', 505: 'MGT-250-A', 506: 'MGT-250-B', 507: 'REL-250-A', 508: 'ENG-364-A', 509: 'EDUC-332-A', 510: 'COMS-258-A', 511: 'NURS-235L-02', 512: 'NURS-235L-03', 513: 'NURS-235L-01', 
			514: 'NURS-235L-04', 515: 'NURS-235L-05', 516: 'GS-100-C', 517: 'GS-100-B', 518: 'GS-100-A', 519: 'BIO-365-A', 520: 'REL-251-A', 521: 'COMS-132-B', 522: 'COMS-132-A', 523: 'DAN-100-A', 524: 'DAN-100-C', 525: 'DAN-100-B', 526: 'EDUC-372-A', 527: 'PAID-111D-09', 528: 'THE-204-B', 
			529: 'THE-204-A', 530: 'HIST-135-A', 531: 'RUS-350-A', 532: 'IS-490-A', 533: 'CHEM-345-A', 534: 'CS-260-A', 535: 'RUS-239-A', 536: 'SOC-490-A', 537: 'WGST-242-A', 538: 'PSYC-244-A', 539: 'ENG-485-A', 540: 'CHEM-366-A', 541: 'ANTH-339-A', 542: 'BIO-151L-A03', 543: 'BIO-151L-A04', 
			544: 'BIO-151L-A05', 545: 'BIO-151L-A06', 546: 'BIO-151L-A07', 547: 'BIO-151L-A08', 548: 'BIO-151L-A09', 549: 'MUS-131-A', 550: 'PE-100-C02', 551: 'BIO-365L-A', 552: 'ENG-110-B', 553: 'ENG-110-A', 554: 'ANTH-210-A', 555: 'ENG-114-B', 556: 'ENG-114-A', 557: 'MUS-300-A', 
			558: 'BIO-116L-A01', 559: 'BIO-116L-A03', 560: 'BIO-116L-A02', 561: 'BIO-116L-A04', 562: 'ENVS-310-A', 563: 'CS-130-B', 564: 'CS-130-A', 565: 'ACCTG-358-A', 566: 'EDUC-470-A', 567: 'MUS-491-A', 568: 'EDUC-378-A', 569: 'MUS-121L-E', 570: 'MUS-121L-D', 571: 'MUS-121L-F', 
			572: 'MUS-121L-A', 573: 'MUS-121L-C', 574: 'MUS-121L-B', 575: 'BIO-256L-A01', 576: 'BIO-256L-A02', 577: 'ACCTG-150-A', 578: 'PE-100-B02', 579: 'MUS-118-A', 580: 'PE-100-B04', 581: 'SCI-121L-A01', 582: 'SCI-121L-A02', 583: 'CHEM-351-A', 584: 'ACCTG-150-C', 585: 'EDUC-352-A', 
			586: 'CHEM-241-B', 587: 'PSYC-130-A', 588: 'CHEM-241-A', 589: 'HIST-126-A', 590: 'AFRS-171-A', 591: 'CHEM-362-A', 592: 'MUS-273-P', 593: 'HIST-149-A', 594: 'MATH-321-A', 595: 'MATH-321-B', 596: 'MUS-273-H', 597: 'DAN-101-A', 598: 'MUS-273-J', 599: 'MUS-273-K', 600: 'MUS-273-L', 
			601: 'MUS-273-M', 602: 'MUS-273-N', 603: 'MUS-273-O', 604: 'MUS-273-A', 605: 'MUS-273-B', 606: 'MUS-273-C', 607: 'MUS-273-D', 608: 'COMS-255-A', 609: 'MUS-273-F', 610: 'MUS-273-G', 611: 'BIO-151L-A02,', 612: 'HEB-101-A', 613: 'ART-111-A', 614: 'MUS-230-G', 615: 'MUS-230-F', 
			616: 'SCI-125-A', 617: 'MUS-230-D', 618: 'ENVS-230-A', 619: 'SPAN-239-A', 620: 'EDUC-270-A', 621: 'MUS-230-O', 622: 'MUS-230-N', 623: 'PE-247-A', 624: 'PHYS-181L-A02', 625: 'PHYS-181L-A01', 626: 'PSYC-354-A', 627: 'FCUL-242-A', 628: 'BIO-125L-A01', 629: 'PE-229-A', 630: 'MUS-117-D', 
			631: 'PE-345-A', 632: 'MUS-117-A', 633: 'MUS-117-C', 634: 'MUS-117-B', 635: 'MGT-352-B', 636: 'MGT-352-A', 637: 'MGT-351-A', 638: 'MGT-351-B', 639: 'PSYC-353-A', 640: 'EDUC-377-A', 641: 'REL-485-A', 642: 'PAID-111D-14', 643: 'CLAS-320-A', 644: 'MUS-116-A', 645: 'MUS-116-B', 
			646: 'MGT-353-A', 647: 'MUS-116-D', 648: 'NURS-376-A', 649: 'NURS-374-A', 650: 'HLTH-249-A', 651: 'NURS-420-A', 652: 'MATH-220-A', 653: 'MUS-469-A', 654: 'ART-118-A', 655: 'HLTH-490-A', 656: 'PAID-111D-19', 657: 'NURS-235-B', 658: 'NURS-235-C', 659: 'NURS-235-A', 660: 'EDUC-275-A', 
			661: 'NURS-235-E', 662: 'MGT-360-A', 663: 'PE-110-B01', 664: 'ENVS-239-A', 665: 'SCI-240-A', 666: 'BIO-151L-A11', 667: 'PHYS-369-A', 668: 'BIO-115-A', 669: 'NURS-370-A', 670: 'SW-490-A', 671: 'ATHTR-365-A', 672: 'MUS-238-A', 673: 'GER-202-A', 674: 'PE-260-A', 675: 'HIST-111-A', 
			676: 'CS-253-A', 677: 'NURS-425-A', 678: 'ENG-490-A', 679: 'PE-226-A', 680: 'CHEM-372-A', 681: 'ANTH-104-A', 682: 'WGST-130-A', 683: 'ECON-262-A', 684: 'ENVS-175-A', 685: 'POLS-247-A', 686: 'GER-201-A', 687: 'HLTH-125-A', 688: 'EDUC-326-B', 689: 'NURS-390-A', 690: 'EDUC-326-A', 
			691: 'CHEM-201L-02', 692: 'POLS-139-A', 693: 'MGT-240-C', 694: 'MGT-240-B', 695: 'MGT-240-A', 696: 'REL-262-B', 697: 'ANTH-102-A', 698: 'REL-262-A', 699: 'MUS-230-C', 700: 'MUS-230-B', 701: 'MUS-230-A', 702: 'ANTH-101-C', 703: 'ANTH-101-B', 704: 'ANTH-101-A', 705: 'MUS-230-L', 
			706: 'MUS-230-K', 707: 'MUS-230-J', 708: 'MUS-230-I', 709: 'SPAN-303-A', 710: 'MUS-230-P', 711: 'PE-100-B03', 712: 'PE-221-A', 713: 'PE-100-B05', 714: 'PHYS-281L-A01', 715: 'PHYS-311-A', 716: 'PHYS-151L-A03', 717: 'PHYS-151L-A02', 718: 'PHYS-151L-A01', 
			719: 'SW-201-A', 720: 'SPAN-303-B', 721: 'MUS-110-A', 722: 'POLS-258-A', 723: 'BIO-490-A'}

ges = ['INTCL', 'HEPT', 'HIST', 'HB', 'HE', 'HBSSM', 'QUANT', 'NWL', 'REL', 'BL', 'SKL', 'NWNL', 'WEL']


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

# numReqC = int(input("How many required courses?"))
# numPrefC = int(input("How many preferred courses?"))
# numReqS = int(input("How many required sections?"))
# numPrefS = int(input("How many preferred sections?"))
# numReqGE = int(input("How many required ge?"))
# numPrefGE = int(input("How many preferred ge?"))
# minC = int(input("min credits?"))
# maxC = int(input("max credits?"))

def getCriteria():
	numReqC = random.choice(range(5))
	numPrefC = random.choice(range(5-numReqC))
	numReqS = random.choice(range(5-(numReqC+numPrefC)))
	numPrefS = random.choice(range(5-(numReqC+numPrefC+numReqS)))
	numReqGE = random.choice(range(5-(numReqC+numPrefC+numReqS+numPrefS)))
	numPrefGE = random.choice(range(5-(numReqC+numPrefC+numReqS+numPrefS+numReqGE)))
	minC = random.choice(range(10,13))
	maxC = random.choice(range(16,21))
	while maxC-minC < 4:
		minC = random.choice(range(10,13))
		maxC = random.choice(range(16,21))
	return (numReqC,numPrefC,numReqS,numPrefS,numReqGE,numPrefGE,minC,maxC)

def checkGood(c):
	c = c.split("-")
	if c[1][-1] == "L":
		return False
	return True

def main():
	(numReqC,numPrefC,numReqS,numPrefS,numReqGE,numPrefGE,minC,maxC) = getCriteria()
	print("\n\n################################################################\n")

	reqC = []
	for x in range(numReqC):
		temp = random.choice(courses.keys())
		while not checkGood(temp):
			temp = random.choice(courses.keys())
		reqC.append(temp)
	prefC = []
	for x in range(numPrefC):
		temp = random.choice(courses.keys())
		while not checkGood(temp):
			temp = random.choice(courses.keys())
		prefC.append(temp)
	reqS = []
	for x in range(numReqS):
		temp = sections[random.choice(sections.keys())]
		while not checkGood(temp):
			temp = sections[random.choice(sections.keys())]
		reqS.append(temp)
	prefS = []
	for x in range(numPrefS):
		temp = sections[random.choice(sections.keys())]
		while not checkGood(temp):
			temp = sections[random.choice(sections.keys())]
		prefS.append(temp)
	reqG = []
	for x in range(numReqGE):
		reqG.append(random.choice(ges))
	prefG = []
	for x in range(numReqGE):
		prefG.append(random.choice(ges))

	times = [8,16]

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
		if schedule['error'] != "No errors":

			print("*******************************THERE WAS AN ERROR")
			print(schedule['error'])
			print("req Courses: ",reqC)
			print("pref Courses: ",prefC)
			print("req Sections: ",reqS)
			print("pref Sections: ",prefS)
			print("req GE",reqG)
			print("pref GE",prefG)
			print("min Credits",minC)
			print("max Credits",maxC)
			print("time block: ",times)
			print("\n")

main()










