import sys
import math
import base64
import inspect
import os
import io
from submission_sample import SimpleAgent, dotdict, MCTS
import numpy as np
from tqdm import tqdm
from parl.utils import logger
from connectx_try import encode_weight, load_buffer, System, extract
from connect4_game import Connect4Game
from pathlib import Path
from connectx_try import load_data, getCurrentPlayer, getStep, store_data
from feature import DatasetManager
from random import uniform
import random
from time import sleep
from collections import defaultdict
from statistics import quantiles

sample_s_path = '/home/student/PARL/benchmark/torch/AlphaZero/best_200.pth.tar'
sample_b_path = '/home/student/PARL/benchmark/torch/AlphaZero/saved_model/checkpoint_1.pth.tar'

game = Connect4Game()
strong_timellimit = 5
weak_timelimit = 0.5
strong_puct = 1
weak_puct = 0.1
sample_system = System(game, sample_s_path, sample_b_path, turn=1, strong_timelimit=strong_timellimit,
                        weak_timelimit=weak_timelimit, strong_puct=strong_puct, weak_puct=weak_puct)

paths1 = sorted(Path('./label/important/important/short').glob('*.board'))
paths2 = sorted(Path('./label/important/trivial/short').glob('*.board'))
paths3 = sorted(Path('./label/trivial/important/short').glob('*.board'))
paths4 = sorted(Path('./label/trivial/trivial/short').glob('*.board'))

paths = [paths1, paths2, paths3, paths4]
analist = 1
print(len(paths1), len(paths2), len(paths3), len(paths4))


sdata = [0.40262096704026185, 0.30489389851081894, 0.15899086020794223, 0.6320184825526673, 0.12525985239942317, 0.4996407446315872, 0.630621522202852, 0.13352881992645382, 0.43093636248608436, 0.541682089965038, 0.13249934902285737, 0.36056421861269666, 0.07599876711021451, 0.269150647805529, 0.5478617178583653, 0.5411429356162761, 0.16342964728218928, 0.6098091607699622, 0.13337020881253175, 0.6389842004709394, 0.6398167627685231, 0.33177997362734, 0.6388970797390423, 0.4865735761038784, 0.41186930313986936, 0.49590322406996784, 0.23583749819591454, 0.15899086020794223, 0.26619864326591, 0.3970025455054818, 0.40261871182043585, 0.33816371507292775, 0.47761379111571856, 0.3643636039293784, 0.07637482663758846, 0.15899086020794223, 0.2769598796177393, 0.15899086020794223, 0.15667227433940076, 0.2956183061822514, 0.10813223215122465, 0.4381082792097012, 0.14382654902408842, 0.5097021594704112, 0.3479548145883685, 0.08084266713875493, 0.34639962335862096, 0.639992561449382, 0.3467485818856937, 0.5284890357869776, 0.2595660364516391, 0.2919798260190925, 0.15726682151024587, 0.15726682151024587, 0.5221668231734959, 0.18553791337927752, 0.17701508130668983, 0.144054476658319, 0.15840997960300682, 0.15264361949471641, 0.1593295181874294, 0.3317771528733352, 0.37001396723244645, 0.31311378694787584, 0.26828997184706543, 0.3462852687470538, 0.583154258362552, 0.09048621073058197, 0.09048621073058197, 0.3504412792083117, 0.5748501705513623, 0.31184972012744916, 0.09048621073058197, 0.3508542499660391, 0.4926245703628279, 0.3270299731924502, 0.5833075040517676, 0.609021072070623, 0.24160089876858173, 0.09048621073058197, 0.11582231291987681, 0.08649538798010185, 0.21941164255822207, 0.09048621073058197, 0.47368916263126015, 0.43154011824698635, 0.5474711566676727, 0.27694233027960913, 0.15726682151024587, 0.09048621073058197, 0.3430452718066918, 0.16562266907003703, 0.15726682151024587, 0.09048621073058197, 0.160157990654962, 0.43179555478663384, 0.15726682151024587, 0.2849595685961246, 0.31633902349257265, 0.18477005205086067, 0.09048621073058197, 0.517158574205429, 0.471480576446149, 0.0030262592179335, 9.601525194113947e-06, 0.0253213096614752, 0.028466995805990224, 0.1411457359639492, 0.0030262592179335, 0.0010616434435306132, 0.9096073984096472, 2.429868089848242e-08, 0.1586563219297386, 0.18288769787014053, 0.036715321847482954, 0.12977442622100602, 0.022309509588176582, 0.03292829507869384, 0.1312190001808035, 6.82142396414065e-05, 1.2859320482618843e-05, 0.0018088771520766045, 0.1512213745387077, 0.016476606044236633, 5.2248193185278066e-08, 0.6153615160798893, 0.0002376943122249031, 2.1182358977966942e-10, 0.00023113349485498702, 0.0014274112563376206, 0.0011429919300303482, 0.3887341125461793, 0.5534805502906457, 0.17752761906440492, 8.463959319072957e-05, 0.43355633283749506, 0.007174073200665987, 4.908692606221621e-05, 0.09147805686634294, 0.15805229403905058, 2.3020486133873416e-06, 1.2636245421049353e-06, 0.14876937858940828, 1.6462725881183359e-07, 4.42459887409541e-06, 0.000356424156742321, 1.3566241003957204e-05, 4.930095635899079e-05, 0.08271428085710139, 0.09967048466617227, 0.0005592650522066833, 8.463959319072957e-05, 0.0562444913872517, 9.769973416950961e-09, 0.1411457359639492, 1.854535351725417e-05, 0.040373705022056464, 0.004220296944187396, 0.6663706403329138, 3.364421052651778e-06, 0.053929531528864205, 1.583101152391464e-09, 0.18240947868254043, 4.268710745236604e-07, 2.235526977756308e-08, 1.0986471087903738e-06, 2.8712833000099647e-10, 0.18300575814568748, 0.16272244821116097, 8.722068196789225e-06, 0.07035373392725093, 1.3615101806863095e-05, 3.0920161128733526e-06, 4.078803746466519e-05, 0.0030262592179335, 9.59728672143001e-06, 0.13727543895375965, 1.1613586113412567e-05, 2.0571626767207362e-05, 1.0918411987859144e-08, 0.314382999342324, 0.03783569242584917, 0.2816048299903686, 0.326431907774531, 2.6594585733619162e-09, 0.13357445779760177, 0.16401161720016905, 0.24194848567485341, 0.032514502738738425, 0.49730357527145336, 0.16401284790327048, 0.3170570420620317, 0.3675139741005663, 0.12246102126225425, 0.002376476636808036, 0.07053262269316975, 2.3168618680244892e-05, 0.000697142858553832, 0.2032761291290504, 0.5969234452543682, 0.23082933362187297, 2.567783581355343e-06, 0.6303481861618032, 0.11772165493715372, 0.05675112136492544, 1.307189889644178e-05, 0.06274314251145832, 0.06812047368844475, 0.00014226762505899158, 0.12445569346962346, 0.009022742060395786, 0.00036646853382990227, 0.005861190711902396, 0.08116827319978114, 0.0860128679621066, 0.10386383762498394, 0.0860128679621066, 0.1256662677388653, 0.0490745886481372, 5.085861465659036e-07, 0.1229554624539261, 0.014142658127432243, 1.2095407184062877e-05, 0.11167421594134497, 0.10681212996212741, 0.058121154520023754, 0.2877222025261087, 0.0035832831886332883, 0.009126478911169614, 0.274656997802609, 0.0005304397381260628, 0.4757429723950489, 0.0030262592179335, 0.006850560923573711, 0.05099720456267405, 0.2746437487769216, 0.48685274037012427, 0.05099720456267405, 0.13072097253880818, 2.1607751130545693e-05, 5.198615365372915e-05, 0.7364551612025956, 0.4589943507230948, 0.05099720456267405, 0.13079605122800783, 2.1607751130545693e-05, 5.328001630232393e-05, 0.13910000870728784, 0.0030262592179335, 1.3569183306003651e-05, 0.1256324084327117, 0.12457546189871974, 0.05099720456267405, 0.2809017444152536, 0.0915241866897575, 2.6275870368408505e-11, 0.0, 0.3494111293991841, 0.05099720456267405, 0.0002764727771329945, 0.48889518506496155, 1.1071572125445074e-05, 0.0860128679621066, 0.12566371576078258, 0.05099720456267405, 0.00011316736273471405, 0.029105468973575344, 0.2622641624909144, 0.00012849102573341044, 0.0860128679621066, 1.984004057931088e-07, 0.47582543106023556, 0.05099720456267405, 0.0003732812401145224, 5.813739401304474e-05, 0.0860128679621066, 1.1803160944623414e-06, 0.0009214750141941863, 0.3142165957017581, 7.890384063955481e-06, 0.09537480160441231, 0.05099720456267405, 4.582843088854815e-05, 3.5226174105673635e-07]
wdata = [0.6400000000000002, 0.17480404489801382, 0.17477183519229708, 0.17446473189891004, 0.6400000000000002, 0.14598203081436273, 0.14606560558060583, 0.14633531441179404, 0.17498045735935794, 0.1747252288643843, 0.17443511906681497, 0.17454878553458558, 0.1461749245593294, 0.17486852631478372, 0.14644871683031174, 0.1747272094525572, 0.17474060318741053, 0.14595400936593164, 0.17502679220991824, 0.17499066259305723, 0.14585556166616306, 0.1748406587089167, 0.1462769233514923, 0.1747252288643843, 0.17468448057838487, 0.17474048882933252, 0.17469948176149885, 0.1459415616917732, 0.1744238944812299, 0.6400000000000002, 0.6400000000000002, 0.1684604851500302, 0.14642380494525498, 0.17480131510329858, 0.14634777886629785, 0.14626532814586482, 0.1462066126049427, 0.17449392895215168, 0.1459004402084068, 0.6400000000000002, 0.14574494227961504, 0.1460095686919164, 0.1742812313310997, 0.400470803303166, 0.6400000000000002, 0.1752882673163781, 0.0013065651932224497, 0.24147362678644205, 0.0013065651932224497, 0.21882009504157368, 0.0012831279269932196, 0.0012588704696325811, 0.21931380963410416, 0.21930434891556266, 0.21872741569872792, 0.0012885664401795652, 2.2686008462002862e-07, 0.0012803518967286745, 0.0012541520471425125, 0.0012299844344955044, 0.21935290471972474, 0.001255476638162456, 0.24081049301143018, 0.0012715920655740752, 0.21875563396922842, 0.0013065651932224497, 0.24058439470413337, 1.1261699155440396e-07, 0.001267555620885732, 0.0012957300856849896, 0.0013021445330534318, 0.0012715920655740752, 0.0012674362601344492, 0.0012957300856849896, 0.001266927551353916, 0.0013065651932224497, 0.240583846554309, 0.23416055254523935, 8.091705900103996e-08, 3.1233334245373e-07, 0.1543736724632437, 0.21873528800334996, 0.0012960247870570762, 0.0012765758846843979, 0.001276428739457988, 0.001304004235051711, 0.21877512612813796, 0.0013065651932224497, 0.21915664298965581, 3.4174010762888507e-07, 0.0012537129730286144, 0.15401782420526616, 0.14611969211353584, 0.001305636426282222, 0.0012773395470742723, 0.0013077609677019854, 0.15429483559065366, 4.33613939476718e-08, 0.0013275197013298415, 3.444240910732699e-07, 0.0013206344034400166, 0.0013022302087521385, 0.0012798756734973438, 0.14570321942156625, 0.14655376943107212, 0.1748222178639029, 0.14597872070472487, 0.14560953598121723, 0.17484505612743395, 0.14609251685671792, 0.17516938343070104, 0.14542179238671604, 0.17463313464925848, 0.14588029085025614, 0.17473737988275437, 0.17464343493607223, 0.17452315083306172, 0.14560027800909434, 0.1745771826384422, 0.17517684749582943, 0.17458991152587186, 0.17438367165943308, 0.17480131510329858, 0.6400000000000002, 0.14610220966942417, 0.17452910957939732, 0.14608438033670448, 0.17464433607438995, 0.17472456651742344, 0.17473628751875575, 0.1461000202434963, 0.17482916451603883, 0.17493699557211345, 0.40048865236109865, 0.14643680347532678, 0.17471877850714268, 0.146084208336557, 0.14626810238207852, 0.17474905880720254, 0.1749274525373177, 0.1461484101535531, 0.17509714944502663, 0.17461989737598008, 0.14591630022645719, 0.17502344826531444, 0.17471544248902657, 0.1746911657570754, 0.14629248237068668, 0.17476709421917452, 0.17467968289161925, 0.14627479530674686, 0.17505118452158003, 0.17479447225516623, 0.14606504747066845, 0.17433826320668638, 0.14601758469163476, 0.17495003042511853, 0.14593144841853348, 0.1749218584193492, 0.14639849493429663, 0.6400000000000002, 0.17470053169954303, 0.6400000000000002, 0.17457534479022435, 0.14652131140593389, 0.17488903742721718, 0.14630153547896177, 0.1748471357872154, 0.6400000000000002, 0.14578516337990038, 0.17487598989128345, 0.145909253499911, 0.14579732558365754, 0.17484510223567337, 0.14570542179863477, 0.17490804814321864, 0.1746649908196379, 0.17417798776080676, 0.17494617613667515, 0.14649583099259966, 0.1746941423562782, 0.1751822360908844, 0.1745819695125048, 0.6400000000000002, 0.17421907378083296, 0.14638613892441818, 0.17490916740593312, 0.1743509223231109, 0.17441504003414196, 0.14588481212630028, 0.17446232568469194, 0.14613440136426104, 0.17496744490429805, 0.1747322238051572, 0.1458996183159483, 0.6400000000000002, 0.14572315176788062, 0.17460474038461762, 0.14543927096085668, 0.1746795589776458, 0.0012781042450146574, 0.21870521610193783, 0.001973641175223236, 0.0012460862560787066, 0.14597278822365822, 0.23395793738514525, 0.0012979097384312945, 0.21881609199634672, 0.21896486845334023, 0.2184060766803225, 0.0012322977689047886, 0.0012664238675299565, 0.0012770548810484173, 1.6380536645987931e-07, 0.0012460862560787066, 0.0012512394532095982, 0.0012460862560787066, 0.0012512394532095982, 0.0012638003408253307, 0.14633047594965826, 0.0012659089635369794, 0.0013065651932224497, 1.5924453915294733e-07, 0.0012744704231994052, 0.0012799724445045255, 0.0012715920655740752, 0.0012552168440794007, 0.21925212562541901, 1.1261699155440396e-07, 0.001267098010389597, 0.2191579009894256, 0.001252303108299865, 0.2196578953841332, 0.24101028046575362, 0.24052284661072826, 0.001267098010389597, 1.210213140034888e-07, 0.24055992670387463, 0.0012796131340748495, 0.21895087588256384, 0.0013012895832944815, 4.6366330767044766e-08, 0.0012921685413697847, 0.21878005248234475, 0.0012796131340748495, 0.2410285471701173, 0.2189547550256697, 0.0012683171279630867, 0.21965838315199324, 7.97840259247895e-08, 0.0012460862560787066, 0.0012512394532095982, 0.21867932353818031, 0.00128040842530431, 0.0012460862560787066, 0.0, 0.0, 0.0013012668897150659, 0.21863245880705878, 0.21948914347868964, 0.0012559060430792498, 0.24827057573813524, 0.0012460862560787066, 0.0012512394532095982, 0.21874876133777182, 1.0351138006514658e-07, 0.0012835938560274744, 0.0012460862560787066, 0.1460401317321578, 0.0012460862560787066, 1.951079343942563e-07, 0.24074112119167085, 0.21881186352501475, 0.2405295977356602, 0.24109692591032794, 0.0012460862560787066, 7.951950630413763e-08, 0.0012885664401795652, 2.4925677045484206e-07, 0.23397039218948898, 0.0012949669674640028, 0.24064513460962228, 1.339162110036707e-07, 0.001320443671759661]
print(quantiles(sdata, n=4))
print(quantiles(wdata, n=4))
#sdata = []
#wdata = []
'''
for  i in range(len(paths)):
    for p in paths[i]:
        imp, board, branch, fpath, importance = load_data(p)
        new_simp = sample_system.getMyImportance(board, 1, fpath, getStep(board))
        new_wimp = sample_system.getMyImportance(board, -1, fpath, getStep(board))
        #print(new_simp, new_wimp)
        sdata.append(new_simp)
        wdata.append(new_wimp)

print(sdata)
print(wdata)
sq1 = math.ceil(np.percentile(sdata, 25))
sq2 = math.ceil(np.percentile(sdata, 50))
sq3 = math.ceil(np.percentile(sdata, 75))
print(sq1, sq2, sq3, np.mean(sdata))

wq1 = math.ceil(np.percentile(wdata, 25))
wq2 = math.ceil(np.percentile(wdata, 50))
wq3 = math.ceil(np.percentile(wdata, 75))

print(wq1, wq2, wq3, np.mean(wdata))
'''
