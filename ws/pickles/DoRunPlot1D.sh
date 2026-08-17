#jet2016postVFP/run.done  jet2016preVFP/run.done  jet2017/run.done  jet2018/run.done  muon2016postVFP/run.done  muon2016preVFP/run.done
#ARR_OBJ=(muon electron jet)
mkdir -p logs/
ARR_OBJ=(muon electron jet)
ARR_YEAR=(2016preVFP 2016postVFP 2017 2018)
for OBJ in ${ARR_OBJ[@]};do
    for YEAR in ${ARR_YEAR[@]};do
	python3 runPlot1D.py ${OBJ} ${YEAR} &> logs/1D_${OBJ}__${YEAR}.log&
    done
done
