#!/usr/bin/env python3
# 单源生成说明书示意图：master(双语+CSS变量) → ①Artifact 内联 ②docs images 独立浅色 SVG(中英各一)
import re, os

ROOT = "/Users/apple/Documents/workspace/work/EVSEProNew"
SCRATCH = "/private/tmp/claude-501/-Users-apple-Documents-workspace-work-EVSEProNew/aaa3a2c3-1c0a-4162-803b-649aa9f62331/scratchpad"
IMG = os.path.join(ROOT, "docs/user-manual/images")
os.makedirs(IMG, exist_ok=True)

# 浅色定稿色值（与 Artifact light tokens 一致）
HEX = {
    "--blue": "#155DFC", "--teal": "#0E7490", "--green": "#009966", "--amber": "#B45309",
    "--violet": "#6D4FC4", "--slate": "#56657A", "--muted": "#5B6B7E", "--ink": "#0B1526",
    "--line": "#E1E8EF", "--card": "#FFFFFF", "--canvas": "#F3F7F9",
    "--blue-tint": "#EAF0FE", "--green-tint": "#E4F4EE", "--amber-tint": "#FBEEDB",
    "--teal-tint": "#E0F1F6", "--violet-tint": "#EFEAFB", "--slate-tint": "#EBEFF3",
}
FONT = '-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", sans-serif'

# ═════════ D1 两条控制通道 ═════════
D1 = '''<svg viewBox="0 0 640 252" xmlns="http://www.w3.org/2000/svg">
  <!-- 手机 -->
  <rect x="40" y="70" width="50" height="100" rx="12" fill="var(--card)" stroke="var(--ink)" stroke-width="1.5"/>
  <rect x="47" y="80" width="36" height="64" rx="4" fill="var(--blue-tint)"/>
  <circle cx="65" cy="158" r="3.5" fill="var(--muted)"/>
  <!-- 充电桩 -->
  <rect x="550" y="58" width="60" height="112" rx="12" fill="var(--card)" stroke="var(--ink)" stroke-width="1.5"/>
  <rect x="559" y="70" width="42" height="30" rx="4" fill="var(--green-tint)"/>
  <circle cx="580" cy="112" r="2.5" fill="var(--green)"/>
  <circle cx="580" cy="134" r="9" fill="var(--canvas)" stroke="var(--ink)" stroke-width="1.5"/>
  <circle cx="580" cy="134" r="3.5" fill="var(--muted)"/>
  <!-- 蓝牙近场：上弧 -->
  <path d="M 96,100 C 220,54 420,54 544,100" fill="none" stroke="var(--blue)" stroke-width="2"/>
  <polygon points="96,100 106,95 106,105" fill="var(--blue)"/>
  <polygon points="544,100 534,95 534,105" fill="var(--blue)"/>
  <!-- 云端远程：下双弧 + 云 -->
  <path d="M 96,140 C 170,186 220,196 264,198" fill="none" stroke="var(--teal)" stroke-width="2" stroke-dasharray="5 5"/>
  <path d="M 376,198 C 440,196 490,186 544,140" fill="none" stroke="var(--teal)" stroke-width="2" stroke-dasharray="5 5"/>
  <polygon points="96,140 106,135 106,145" fill="var(--teal)"/>
  <polygon points="544,140 534,135 534,145" fill="var(--teal)"/>
  <g fill="var(--teal-tint)">
    <circle cx="305" cy="192" r="13"/><circle cx="322" cy="184" r="16"/><circle cx="340" cy="193" r="12"/>
    <rect x="294" y="192" width="56" height="13" rx="6"/>
  </g>
  <g class="zh">
    <rect x="272" y="40" width="96" height="26" rx="13" fill="var(--blue-tint)"/>
    <text x="320" y="57" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--blue)">蓝牙近场</text>
    <text x="320" y="88" text-anchor="middle" font-size="11" fill="var(--muted)">在桩旁 · 手机直连，不依赖家庭网络</text>
    <text x="65" y="196" text-anchor="middle" font-size="12" fill="var(--muted)">手机 App</text>
    <text x="580" y="196" text-anchor="middle" font-size="12" fill="var(--muted)">充电桩</text>
    <text x="320" y="228" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--teal)">云端远程</text>
    <text x="320" y="245" text-anchor="middle" font-size="11" fill="var(--muted)">不在桩旁 · 经充电桩的家庭 Wi-Fi 中转，自动切换</text>
  </g>
  <g class="en">
    <rect x="250" y="40" width="140" height="26" rx="13" fill="var(--blue-tint)"/>
    <text x="320" y="57" text-anchor="middle" font-size="12" font-weight="600" fill="var(--blue)">Bluetooth (nearby)</text>
    <text x="320" y="88" text-anchor="middle" font-size="11" fill="var(--muted)">Next to the charger · direct, no home network needed</text>
    <text x="65" y="196" text-anchor="middle" font-size="12" fill="var(--muted)">Phone app</text>
    <text x="580" y="196" text-anchor="middle" font-size="12" fill="var(--muted)">Charger</text>
    <text x="320" y="228" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--teal)">Cloud (remote)</text>
    <text x="320" y="245" text-anchor="middle" font-size="11" fill="var(--muted)">Away · relayed via the charger's home Wi-Fi, switches automatically</text>
  </g>
</svg>'''

# ═════════ D2 七种状态流转 ═════════
D2 = '''<svg viewBox="0 0 680 290" xmlns="http://www.w3.org/2000/svg">
  <!-- 主流程盒 -->
  <rect x="16" y="40" width="126" height="42" rx="10" fill="var(--card)" stroke="var(--line)" stroke-width="1.5"/>
  <rect x="180" y="40" width="84" height="42" rx="10" fill="var(--blue-tint)" stroke="var(--blue)" stroke-width="1.5"/>
  <rect x="302" y="40" width="96" height="42" rx="10" fill="var(--blue)"/>
  <rect x="436" y="40" width="96" height="42" rx="10" fill="var(--green-tint)" stroke="var(--green)" stroke-width="1.5"/>
  <!-- 主流程箭头 -->
  <line x1="142" y1="61" x2="171" y2="61" stroke="var(--muted)" stroke-width="1.5"/><polygon points="180,61 171,57 171,65" fill="var(--muted)"/>
  <line x1="264" y1="61" x2="293" y2="61" stroke="var(--muted)" stroke-width="1.5"/><polygon points="302,61 293,57 293,65" fill="var(--muted)"/>
  <line x1="398" y1="61" x2="427" y2="61" stroke="var(--muted)" stroke-width="1.5"/><polygon points="436,61 427,57 427,65" fill="var(--muted)"/>
  <!-- 再次充电回环 -->
  <path d="M 484,34 C 460,8 374,8 350,34" fill="none" stroke="var(--green)" stroke-width="1.5" stroke-dasharray="4 4"/>
  <polygon points="350,34 353,24 359,31" fill="var(--green)"/>
  <!-- 等待中 -->
  <rect x="180" y="136" width="100" height="38" rx="10" fill="var(--teal-tint)" stroke="var(--teal)" stroke-width="1.5"/>
  <line x1="222" y1="82" x2="222" y2="127" stroke="var(--teal)" stroke-width="1.5" stroke-dasharray="4 4"/><polygon points="222,136 218,127 226,127" fill="var(--teal)"/>
  <path d="M 280,155 H 350 V 91" fill="none" stroke="var(--teal)" stroke-width="1.5" stroke-dasharray="4 4"/><polygon points="350,82 346,91 354,91" fill="var(--teal)"/>
  <!-- 桩侧暂停 -->
  <rect x="252" y="226" width="190" height="44" rx="10" fill="var(--amber-tint)" stroke="var(--amber)" stroke-width="1.5"/>
  <line x1="330" y1="82" x2="330" y2="217" stroke="var(--amber)" stroke-width="1.5"/><polygon points="330,226 326,217 334,217" fill="var(--amber)"/>
  <line x1="368" y1="226" x2="368" y2="91" stroke="var(--muted)" stroke-width="1.5"/><polygon points="368,82 364,91 372,91" fill="var(--muted)"/>
  <!-- 车辆已暂停 -->
  <rect x="488" y="226" width="120" height="44" rx="10" fill="var(--slate-tint)" stroke="var(--slate)" stroke-width="1.5"/>
  <path d="M 398,74 C 470,84 505,140 533,217" fill="none" stroke="var(--slate)" stroke-width="1.5" stroke-dasharray="4 4"/>
  <polygon points="535,226 529,218 537,216" fill="var(--slate)"/>
  <path d="M 560,226 C 580,150 560,110 512,88" fill="none" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="4 4"/>
  <polygon points="504,84 514,83 511,91" fill="var(--muted)"/>
  <g class="zh">
    <text x="79" y="65" text-anchor="middle" font-size="12" fill="var(--ink)">未连接充电枪</text>
    <text x="222" y="65" text-anchor="middle" font-size="12" font-weight="600" fill="var(--blue)">就绪</text>
    <text x="350" y="65" text-anchor="middle" font-size="12" font-weight="600" fill="#FFFFFF">充电中</text>
    <text x="484" y="65" text-anchor="middle" font-size="12" font-weight="600" fill="var(--green)">已完成</text>
    <text x="161" y="53" text-anchor="middle" font-size="10" fill="var(--muted)">插枪</text>
    <text x="283" y="53" text-anchor="middle" font-size="10" fill="var(--muted)">开始</text>
    <text x="417" y="53" text-anchor="middle" font-size="10" fill="var(--muted)">结束</text>
    <text x="417" y="16" text-anchor="middle" font-size="10.5" fill="var(--green)">再次充电</text>
    <text x="230" y="159" text-anchor="middle" font-size="12" font-weight="600" fill="var(--teal)">等待中</text>
    <text x="214" y="112" text-anchor="end" font-size="10.5" fill="var(--muted)">已设预约</text>
    <text x="315" y="170" text-anchor="middle" font-size="10.5" fill="var(--muted)">到点自动开始</text>
    <text x="347" y="252" text-anchor="middle" font-size="12" fill="var(--amber)">充电已被充电桩暂停</text>
    <text x="322" y="204" text-anchor="end" font-size="10.5" fill="var(--muted)">桩侧保护 / 预约暂停</text>
    <text x="376" y="204" text-anchor="start" font-size="10.5" fill="var(--muted)">恢复充电</text>
    <text x="548" y="252" text-anchor="middle" font-size="12" fill="var(--slate)">车辆已暂停</text>
    <text x="508" y="150" text-anchor="start" font-size="10.5" fill="var(--muted)">车端要求</text>
    <text x="584" y="150" text-anchor="start" font-size="10.5" fill="var(--muted)">停止充电</text>
  </g>
  <g class="en">
    <text x="79" y="57" text-anchor="middle" font-size="10" fill="var(--ink)">NO CABLE</text>
    <text x="79" y="70" text-anchor="middle" font-size="10" fill="var(--ink)">CONNECTED</text>
    <text x="222" y="65" text-anchor="middle" font-size="11" font-weight="600" fill="var(--blue)">READY</text>
    <text x="350" y="65" text-anchor="middle" font-size="11" font-weight="600" fill="#FFFFFF">CHARGING</text>
    <text x="484" y="65" text-anchor="middle" font-size="11" font-weight="600" fill="var(--green)">COMPLETE</text>
    <text x="161" y="53" text-anchor="middle" font-size="9.5" fill="var(--muted)">plug in</text>
    <text x="283" y="53" text-anchor="middle" font-size="9.5" fill="var(--muted)">start</text>
    <text x="417" y="53" text-anchor="middle" font-size="9.5" fill="var(--muted)">ends</text>
    <text x="417" y="16" text-anchor="middle" font-size="10.5" fill="var(--green)">Charge Again</text>
    <text x="230" y="159" text-anchor="middle" font-size="11" font-weight="600" fill="var(--teal)">WAITING</text>
    <text x="214" y="112" text-anchor="end" font-size="10" fill="var(--muted)">schedule set</text>
    <text x="328" y="170" text-anchor="middle" font-size="10" fill="var(--muted)">starts at set time</text>
    <text x="347" y="252" text-anchor="middle" font-size="10" fill="var(--amber)">Charging paused by the charger</text>
    <text x="322" y="204" text-anchor="end" font-size="10" fill="var(--muted)">protection / schedule</text>
    <text x="376" y="204" text-anchor="start" font-size="10" fill="var(--muted)">Resume</text>
    <text x="548" y="252" text-anchor="middle" font-size="10" fill="var(--slate)">VEHICLE PAUSED</text>
    <text x="508" y="150" text-anchor="start" font-size="10" fill="var(--muted)">vehicle request</text>
    <text x="592" y="180" text-anchor="start" font-size="10" fill="var(--muted)">Stop</text>
  </g>
</svg>'''

# ═════════ D3 设备分享双泳道 ═════════
D3 = '''<svg viewBox="0 0 640 292" xmlns="http://www.w3.org/2000/svg">
  <rect x="120" y="16" width="100" height="26" rx="13" fill="var(--violet-tint)"/>
  <rect x="395" y="16" width="150" height="26" rx="13" fill="var(--blue-tint)"/>
  <!-- 在线分享 -->
  <rect x="375" y="82" width="190" height="32" rx="8" fill="var(--card)" stroke="var(--line)" stroke-width="1.5"/>
  <path d="M 375,98 H 305 V 126 H 274" fill="none" stroke="var(--muted)" stroke-width="1.5"/>
  <polygon points="265,126 274,122 274,130" fill="var(--muted)"/>
  <rect x="75" y="118" width="190" height="32" rx="8" fill="var(--violet-tint)" stroke="var(--violet)" stroke-width="1.5"/>
  <path d="M 265,142 H 322 V 172 H 371" fill="none" stroke="var(--muted)" stroke-width="1.5"/>
  <polygon points="380,172 371,168 371,176" fill="var(--muted)"/>
  <rect x="375" y="156" width="190" height="32" rx="8" fill="var(--green-tint)" stroke="var(--green)" stroke-width="1.5"/>
  <!-- 分隔 -->
  <line x1="20" y1="212" x2="620" y2="212" stroke="var(--line)" stroke-width="1" stroke-dasharray="4 4"/>
  <!-- 近场分享码 -->
  <rect x="75" y="244" width="190" height="32" rx="8" fill="var(--blue-tint)" stroke="var(--blue)" stroke-width="1.5"/>
  <line x1="265" y1="260" x2="371" y2="260" stroke="var(--muted)" stroke-width="1.5"/>
  <polygon points="380,260 371,256 371,264" fill="var(--muted)"/>
  <rect x="375" y="244" width="190" height="32" rx="8" fill="var(--card)" stroke="var(--line)" stroke-width="1.5"/>
  <g class="zh">
    <text x="170" y="33" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--violet)">物主</text>
    <text x="470" y="33" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--blue)">家人（共享用户）</text>
    <text x="20" y="70" font-size="11" font-weight="700" letter-spacing="2" fill="var(--muted)">在线分享</text>
    <text x="470" y="102" text-anchor="middle" font-size="12" fill="var(--ink)">打开 我的 → 设备分享</text>
    <text x="340" y="92" text-anchor="middle" font-size="10.5" fill="var(--muted)">出示邀请码</text>
    <text x="170" y="138" text-anchor="middle" font-size="12" fill="var(--violet)">扫描邀请码 · 选有效期</text>
    <text x="470" y="204" text-anchor="middle" font-size="10.5" fill="var(--muted)">云端签发 · 每台设备最多 10 个在线分享</text>
    <text x="470" y="176" text-anchor="middle" font-size="12" fill="var(--green)">设备出现在首页 ·「共享」</text>
    <text x="20" y="234" font-size="11" font-weight="700" letter-spacing="2" fill="var(--muted)">近场分享码</text>
    <text x="170" y="264" text-anchor="middle" font-size="12" fill="var(--blue)">桩旁生成分享码（1小时–30天）</text>
    <text x="322" y="252" text-anchor="middle" font-size="10.5" fill="var(--amber)">不经云端 · 码即钥匙</text>
    <text x="470" y="264" text-anchor="middle" font-size="12" fill="var(--ink)">扫码或粘贴导入</text>
  </g>
  <g class="en">
    <text x="170" y="33" text-anchor="middle" font-size="12" font-weight="600" fill="var(--violet)">Owner</text>
    <text x="470" y="33" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--blue)">Family (shared user)</text>
    <text x="20" y="70" font-size="10.5" font-weight="700" letter-spacing="1.5" fill="var(--muted)">ONLINE SHARE</text>
    <text x="470" y="102" text-anchor="middle" font-size="10.5" fill="var(--ink)">Open Me → Device sharing</text>
    <text x="340" y="92" text-anchor="middle" font-size="10" fill="var(--muted)">shows invite code</text>
    <text x="170" y="138" text-anchor="middle" font-size="10.5" fill="var(--violet)">Scan invite code · pick validity</text>
    <text x="470" y="204" text-anchor="middle" font-size="10" fill="var(--muted)">cloud-issued · up to 10 per device</text>
    <text x="470" y="176" text-anchor="middle" font-size="10.5" fill="var(--green)">Device appears on Home · "Shared"</text>
    <text x="20" y="234" font-size="10.5" font-weight="700" letter-spacing="1.5" fill="var(--muted)">NEARBY SHARE CODE</text>
    <text x="170" y="264" text-anchor="middle" font-size="10.5" fill="var(--blue)">Generate next to the charger (1 h–30 d)</text>
    <text x="322" y="252" text-anchor="middle" font-size="10" fill="var(--amber)">offline · the code is a key</text>
    <text x="470" y="264" text-anchor="middle" font-size="10.5" fill="var(--ink)">Scan or paste to import</text>
  </g>
</svg>'''

# ═════════ D4 配对步骤条 ═════════
D4 = '''<svg viewBox="0 0 680 168" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="64" width="88" height="40" rx="10" fill="var(--card)" stroke="var(--line)" stroke-width="1.5"/>
  <rect x="128" y="64" width="100" height="40" rx="10" fill="var(--card)" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="4 4"/>
  <rect x="252" y="64" width="92" height="40" rx="10" fill="var(--blue)"/>
  <rect x="368" y="64" width="92" height="40" rx="10" fill="var(--card)" stroke="var(--line)" stroke-width="1.5"/>
  <rect x="484" y="64" width="88" height="40" rx="10" fill="var(--card)" stroke="var(--line)" stroke-width="1.5"/>
  <rect x="592" y="64" width="72" height="40" rx="10" fill="var(--green-tint)" stroke="var(--green)" stroke-width="1.5"/>
  <line x1="104" y1="84" x2="119" y2="84" stroke="var(--muted)" stroke-width="1.5"/><polygon points="128,84 119,80 119,88" fill="var(--muted)"/>
  <line x1="228" y1="84" x2="243" y2="84" stroke="var(--muted)" stroke-width="1.5"/><polygon points="252,84 243,80 243,88" fill="var(--muted)"/>
  <line x1="344" y1="84" x2="359" y2="84" stroke="var(--muted)" stroke-width="1.5"/><polygon points="368,84 359,80 359,88" fill="var(--muted)"/>
  <line x1="460" y1="84" x2="475" y2="84" stroke="var(--muted)" stroke-width="1.5"/><polygon points="484,84 475,80 475,88" fill="var(--muted)"/>
  <line x1="572" y1="84" x2="583" y2="84" stroke="var(--muted)" stroke-width="1.5"/><polygon points="592,84 583,80 583,88" fill="var(--muted)"/>
  <path d="M 60,104 C 100,146 250,146 292,110" fill="none" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="4 4"/>
  <polygon points="295,106 288,113 296,116" fill="var(--muted)"/>
  <path d="M 320,104 C 360,150 480,150 522,110" fill="none" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="4 4"/>
  <polygon points="525,106 518,113 526,116" fill="var(--muted)"/>
  <g class="zh">
    <text x="60" y="89" text-anchor="middle" font-size="12" fill="var(--ink)">选择方式</text>
    <text x="178" y="89" text-anchor="middle" font-size="12" fill="var(--ink)">扫描二维码</text>
    <text x="178" y="54" text-anchor="middle" font-size="10" fill="var(--muted)">可选</text>
    <text x="298" y="89" text-anchor="middle" font-size="12" font-weight="600" fill="#FFFFFF">蓝牙认领</text>
    <text x="298" y="54" text-anchor="middle" font-size="10" fill="var(--blue)">需在桩旁</text>
    <text x="414" y="89" text-anchor="middle" font-size="12" fill="var(--ink)">连接 WiFi</text>
    <text x="414" y="54" text-anchor="middle" font-size="10" fill="var(--muted)">需登录 · 可跳过</text>
    <text x="528" y="89" text-anchor="middle" font-size="12" fill="var(--ink)">命名设备</text>
    <text x="628" y="89" text-anchor="middle" font-size="12" font-weight="600" fill="var(--green)">全部就绪</text>
    <text x="176" y="145" text-anchor="middle" font-size="10.5" fill="var(--muted)">直接蓝牙配对</text>
    <text x="421" y="149" text-anchor="middle" font-size="10.5" fill="var(--muted)">「跳过 — 仅使用蓝牙」</text>
  </g>
  <g class="en">
    <text x="60" y="88" text-anchor="middle" font-size="10" fill="var(--ink)">Choose method</text>
    <text x="178" y="88" text-anchor="middle" font-size="10" fill="var(--ink)">Scan QR code</text>
    <text x="178" y="54" text-anchor="middle" font-size="9.5" fill="var(--muted)">optional</text>
    <text x="298" y="88" text-anchor="middle" font-size="10" font-weight="600" fill="#FFFFFF">Bluetooth claim</text>
    <text x="298" y="54" text-anchor="middle" font-size="9.5" fill="var(--blue)">next to charger</text>
    <text x="414" y="88" text-anchor="middle" font-size="10" fill="var(--ink)">Connect to WiFi</text>
    <text x="414" y="54" text-anchor="middle" font-size="9.5" fill="var(--muted)">sign-in · skippable</text>
    <text x="528" y="88" text-anchor="middle" font-size="10" fill="var(--ink)">Name device</text>
    <text x="628" y="88" text-anchor="middle" font-size="10" font-weight="600" fill="var(--green)">All set</text>
    <text x="176" y="145" text-anchor="middle" font-size="10" fill="var(--muted)">straight to Bluetooth</text>
    <text x="421" y="149" text-anchor="middle" font-size="10" fill="var(--muted)">"Skip — use Bluetooth only"</text>
  </g>
</svg>'''

DIAGRAMS = {
    "channels": (D1, "两条控制通道", "The two control channels"),
    "states":   (D2, "实时页七种状态流转", "Now-page state flow"),
    "sharing":  (D3, "设备分享的两种方式", "Two ways to share a device"),
    "pairing":  (D4, "添加充电桩流程", "Add-a-charger flow"),
}

def standalone(svg, lang):
    out = svg
    other = "en" if lang == "zh" else "zh"
    out = re.sub(r'  <g class="%s">.*?</g>\n' % other, "", out, flags=re.S)
    for var, hexv in HEX.items():
        out = out.replace("var(%s)" % var, hexv)
    out = out.replace('<svg ', '<svg font-family=\'%s\' ' % FONT, 1)
    return out

# ① 独立文件（中英各一，浅色定稿）
for name, (svg, _zh, _en) in DIAGRAMS.items():
    for lang in ("zh", "en"):
        path = os.path.join(IMG, "%s.%s.svg" % (name, lang))
        open(path, "w").write(standalone(svg, lang))
        print("wrote", path)

# ② Artifact 内联
art = os.path.join(SCRATCH, "evsepro-user-manual.html")
html = open(art).read()

def figure(name):
    svg, zh, en = DIAGRAMS[name]
    return ('\n    <figure class="diagram" role="img" aria-label="%s / %s">\n%s\n'
            '      <figcaption><span class="zh">%s</span><span class="en">%s</span></figcaption>\n    </figure>\n'
            % (zh, en, svg, zh, en))

# CSS
css_anchor = "  footer { color: var(--muted); font-size: 13px; padding-top: 8px; }"
assert css_anchor in html
html = html.replace(css_anchor, """  /* ── 示意图 ── */
  figure.diagram { margin: 6px 0 20px; background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 18px 14px 10px; }
  figure.diagram svg { width: 100%; height: auto; display: block; }
  figure.diagram text { font-family: inherit; }
  figure.diagram figcaption { font-size: 12.5px; color: var(--muted); text-align: center; padding: 8px 0 4px; }

""" + css_anchor, 1)
# 打印防断
pb = "    .tw, .note, .card, ol.steps > li, tr { break-inside: avoid; }"
assert pb in html
html = html.replace(pb, "    .tw, .note, .card, ol.steps > li, tr, figure.diagram { break-inside: avoid; }", 1)

# D1 → §1.3 末尾
a1 = 'marked <span class="b b-near">Nearby</span> throughout.</li>\n    </ul>\n  </section>'
assert a1 in html
html = html.replace(a1, a1.replace("</section>", figure("channels") + "  </section>"), 1)
# D2 → §4.1 标题后
a2 = '<h3><span class="zh">七种状态一览</span><span class="en">The seven states</span></h3>'
assert a2 in html
html = html.replace(a2, a2 + figure("states"), 1)
# D3 → §9 两种方式表格后（英文表格结束处）
a3 = '<tr><td>Nearby share code</td><td>Any charger (incl. offline-only)</td><td class="num">1 h / 24 h / 7 d / 30 d</td><td>Expires automatically; recipient can remove it locally</td></tr>\n    </table></div>'
assert a3 in html
html = html.replace(a3, a3 + figure("sharing"), 1)
# D4 → §2.3 引言后
a4 = '<p class="en">On Home tap "Add a device" or "+":</p>'
assert a4 in html
html = html.replace(a4, a4 + figure("pairing"), 1)

open(art, "w").write(html)
print("artifact patched, len =", len(html))

# ③ Markdown（中英各插 4 图）
def patch_md(path, pairs):
    src = open(path).read()
    for anchor, insert, before in pairs:
        assert anchor in src, "MISSING ANCHOR in %s: %r" % (path, anchor[:60])
        src = src.replace(anchor, (insert + anchor) if before else (anchor + insert), 1)
    open(path, "w").write(src)
    print("patched", path)

zh_md = os.path.join(ROOT, "docs/user-manual/EVSEPro-使用功能说明书.md")
patch_md(zh_md, [
    ("- 少数操作是蓝牙近场专属（屏幕亮度、温度单位、启动方式、负载均衡配置、固件升级、解绑），手册中以 🔵 标注。",
     "\n\n![两条控制通道示意图](images/channels.zh.svg)", False),
    ("\n> 配对过程若提示「该充电桩已被认领」",
     "\n![添加充电桩流程](images/pairing.zh.svg)\n", True),
    ("### 4.1 七种状态一览\n", "\n![实时页状态流转图](images/states.zh.svg)\n", False),
    ("\n### 9.1 物主视角：发起分享", "\n![设备分享的两种方式](images/sharing.zh.svg)\n", True),
])

en_md = os.path.join(ROOT, "docs/user-manual/EVSEPro-User-Manual.en.md")
patch_md(en_md, [
    ("- A few operations are Bluetooth-only (screen brightness, temperature unit, start method, load-balancing configuration, firmware update, unpairing) — marked 🔵 throughout.",
     "\n\n![The two control channels](images/channels.en.svg)", False),
    ("\n> If pairing reports the charger",
     "\n![Add-a-charger flow](images/pairing.en.svg)\n", True),
    ("### 4.1 The seven states\n", "\n![Now-page state flow](images/states.en.svg)\n", False),
    ("\n### 9.1 Owner: initiating", "\n![Two ways to share a device](images/sharing.en.svg)\n", True),
])

print("ALL DONE")
