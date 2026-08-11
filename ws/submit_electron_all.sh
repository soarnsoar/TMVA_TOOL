mkdir -p logs
ARR_SCRIPT=(
submit_run_single_SCAN_BDT_ELECTRON_16a.py  submit_run_single_SCAN_BDT_ELECTRON_16b.py  submit_run_single_SCAN_BDT_ELECTRON_17.py  submit_run_single_SCAN_BDT_ELECTRON_18.py


)

for script in ${ARR_SCRIPT[@]};do
    ${script} &> logs/${script}.electrononlysub.log &
    sleep 30
done
