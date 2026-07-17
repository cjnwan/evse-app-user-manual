#!/bin/zsh
SIM=A250D68A-3623-4304-8AD8-7889C5034726
BID=com.shenqi.evsepro
shot() {
  local name=$1 link=$2 seed=$3
  xcrun simctl terminate $SIM $BID 2>/dev/null
  sleep 1
  export SIMCTL_CHILD_EVSE_QA_HIDE_DEBUG_UI=1
  export SIMCTL_CHILD_EVSE_LAUNCH_DEEPLINK="$link"
  if [[ -n "$seed" ]]; then export SIMCTL_CHILD_EVSE_HOME_MOCK_SEED=1; else unset SIMCTL_CHILD_EVSE_HOME_MOCK_SEED; fi
  xcrun simctl launch $SIM $BID >/dev/null
  sleep 7
  xcrun simctl io $SIM screenshot "shots/$name.png" >/dev/null 2>&1 && echo "$name done"
}
shot home_grid    "evsepro://main/home" seed
shot now_charging "evsepro://dev/wallbox?state=2"
shot now_ready    "evsepro://dev/wallbox?state=1"
shot now_complete "evsepro://dev/wallbox?state=6"
shot schedule_tab "evsepro://dev/wallbox?tab=1"
shot history      "evsepro://dev/wallboxhistory"
shot settings     "evsepro://dev/wallboxsettings"
shot rateplan     "evsepro://dev/rateplan"
shot profile      "evsepro://main/profile"
shot energy       "evsepro://dev/wallbox?segment=2"
