#jet2016postVFP/run.done  jet2016preVFP/run.done  jet2017/run.done  jet2018/run.done  muon2016postVFP/run.done  muon2016preVFP/run.done
#ARR_OBJ=(muon electron jet)
mkdir -p logs/

##
OBJ=jet
YEAR=2016preVFP
#python3 runPlot.py ${OBJ} ${YEAR} &> logs/${OBJ}__${YEAR}.log&
##
OBJ=jet
YEAR=2017
#python3 runPlot.py ${OBJ} ${YEAR} &> logs/${OBJ}__${YEAR}.log&

OBJ=jet
YEAR=2018
#python3 runPlot.py ${OBJ} ${YEAR} &> logs/${OBJ}__${YEAR}.log&


OBJ=electron
YEAR=2016preVFP
python3 runPlot.py ${OBJ} ${YEAR} &> logs/${OBJ}__${YEAR}.log&

