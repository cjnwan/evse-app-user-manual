# 再生产工具链

说明书三类资产的生成/更新脚本（源自 2026-07 首版制作，路径按需调整）。

| 脚本 | 用途 |
|---|---|
| `build_diagrams.py` | 5 张示意图单源刷新（双通道/七状态/分享泳道/配对步骤条/DLB 原理）：master（双语文本 + CSS 变量）→ ① index.html 内联按 viewBox 整块替换（随语言/明暗切换）② `images/*.{zh,en}.svg` 独立浅色文件。**幂等可重复运行**；改图只改 master，跑一遍两种形态同步；新图需先手动把 figure 插入 index.html 一次。**改完必须渲染目检**（`rsvg-convert` 出 PNG 过眼，手排坐标容易压框）。 |
| `shoot.sh` / `shoot2.sh` | 模拟器中文截图批（deeplink 免点按配方）。 |
| `shoot_en.sh` | 英文批（先 `defaults write <bid> EVSEAppLanguage en`）。 |
| `shoot_dlb.sh` / `shoot_dlb_en.sh` | DLB 能耗段中/英截图：`dev/wallbox?dlb=1`（mock 种 DLB 演示遥测块 + 注入 `bs40-22-eu-dlb-solar` 能力）；第二张带 `EVSE_QA_SCROLL_Y=620` 滚到分配卡，成图后 PIL `crop((0, 465, 1206, 1520))` 出特写。 |
| `embed_shots.py` | 截图 → 640w JPEG q82 → `images/screenshots/` + index.html base64 内嵌 + md 引用。 |

## 截图配方要点（App 仓 DEBUG 构建）

- 环境变量（`SIMCTL_CHILD_` 前缀）：`EVSE_LAUNCH_DEEPLINK`（直达路由）、`EVSE_QA_HIDE_DEBUG_UI=1`（藏调试 UI，官方截图必带）、`EVSE_HOME_MOCK_SEED=1`（首页种 4 张 mock 卡）。
- 设备壳各态：`evsepro://dev/wallbox?state=N&sched=0&name=<urlencoded>`（N=0..6；name 覆盖壳标题；sched=0 摘预约）。
- 记录页种数据：`evsepro://dev/wallboxhistory`；设置页全能力：`evsepro://dev/wallboxsettings`；电价：`evsepro://dev/rateplan`。
- 状态栏清理：`xcrun simctl status_bar <sim> override --time 9:41 --batteryLevel 100 --cellularBars 4 --wifiBars 3`。
- 真机截图无法传环境变量 → 用 Release 包拍，或接受后处理。

## 维护铁律

- 中文 md 为权威；改动顺序 = 中文 md → 英文 md → index.html（三处内容人工同步，勿只改一处）。
- 英文引文一律取 App `en.lproj/Localizable.strings` 同 key 真值，禁止自译；界面词以 App 实际文案为准。
- 通道术语固定：「蓝牙近场 / Bluetooth (nearby)」「云端远程 / Cloud (remote)」。
