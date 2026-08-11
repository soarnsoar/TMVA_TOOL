mkdir -p logs
ARR_SCRIPT=(
submit_run_single_SCAN_BDT_JET_16a.py


)

for script in ${ARR_SCRIPT[@]};do
    ${script} &> logs/${script}.jetonlysub.log &
    sleep 30
done
