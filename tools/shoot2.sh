#!/bin/zsh
SIM=A250D68A-3623-4304-8AD8-7889C5034726
BID=com.shenqi.evsepro
NAME='%E8%BD%A6%E5%BA%93%E5%85%85%E7%94%B5%E6%A1%A9'   # 车库充电桩
shot() {
  local name=$1 link=$2
  xcrun simctl terminate $SIM $BID 2>/dev/null
  sleep 1
  export SIMCTL_CHILD_EVSE_QA_HIDE_DEBUG_UI=1
  export SIMCTL_CHILD_EVSE_LAUNCH_DEEPLINK="$link"
  xcrun simctl launch $SIM $BID >/dev/null
  sleep 7
  xcrun simctl io $SIM screenshot "shots/$name.png" >/dev/null 2>&1 && echo "$name done"
}
shot now_charging "evsepro://dev/wallbox?state=2&name=$NAME"
shot now_ready    "evsepro://dev/wallbox?state=1&sched=0&name=$NAME"
shot now_complete "evsepro://dev/wallbox?state=6&sched=0&name=$NAME"
shot now_waiting  "evsepro://dev/wallbox?state=3&name=$NAME"
shot rateplan     "evsepro://dev/rateplan"
