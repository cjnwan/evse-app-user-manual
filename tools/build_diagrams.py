#!/usr/bin/env python3
# 说明书示意图单源刷新：master（双语 g.zh/g.en + CSS 变量色）→
#   ① images/*.{zh,en}.svg 独立浅色文件（md 引用）
#   ② index.html 内联块按 viewBox 定位整块替换（随语言/明暗切换）
# 幂等：可重复运行；新增图时先手动把 <figure class="diagram">…</figure> 插进 index.html 一次，
# 之后由本脚本刷新。改完 master 必须 rsvg-convert 渲染目检（手排坐标易压框）。
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 仓根
IMG = os.path.join(ROOT, "images")
INDEX = os.path.join(ROOT, "index.html")

HEX = {
    "--blue": "#155DFC", "--teal": "#0E7490", "--green": "#009966", "--amber": "#B45309",
    "--violet": "#6D4FC4", "--slate": "#56657A", "--muted": "#5B6B7E", "--ink": "#0B1526",
    "--line": "#E1E8EF", "--card": "#FFFFFF", "--canvas": "#F3F7F9",
    "--blue-tint": "#EAF0FE", "--green-tint": "#E4F4EE", "--amber-tint": "#FBEEDB",
    "--teal-tint": "#E0F1F6", "--violet-tint": "#EFEAFB", "--slate-tint": "#EBEFF3",
}
FONT = '-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", sans-serif'

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

D5 = '''<svg viewBox="0 0 640 372" xmlns="http://www.w3.org/2000/svg">
  <!-- 拓扑行 -->
  <rect x="30" y="40" width="84" height="44" rx="10" fill="var(--card)" stroke="var(--line)" stroke-width="1.5"/>
  <rect x="158" y="40" width="110" height="44" rx="10" fill="var(--teal-tint)" stroke="var(--teal)" stroke-width="1.5"/>
  <rect x="312" y="40" width="96" height="44" rx="10" fill="var(--card)" stroke="var(--line)" stroke-width="1.5"/>
  <rect x="470" y="12" width="120" height="40" rx="10" fill="var(--slate-tint)" stroke="var(--slate)" stroke-width="1.5"/>
  <rect x="470" y="76" width="120" height="40" rx="10" fill="var(--blue)"/>
  <line x1="114" y1="62" x2="149" y2="62" stroke="var(--muted)" stroke-width="1.5"/><polygon points="158,62 149,58 149,66" fill="var(--muted)"/>
  <line x1="268" y1="62" x2="303" y2="62" stroke="var(--muted)" stroke-width="1.5"/><polygon points="312,62 303,58 303,66" fill="var(--muted)"/>
  <path d="M 408,55 C 430,45 445,38 461,34" fill="none" stroke="var(--muted)" stroke-width="1.5"/><polygon points="470,32 461,30 462,38" fill="var(--muted)"/>
  <path d="M 408,69 C 430,79 445,86 461,90" fill="none" stroke="var(--muted)" stroke-width="1.5"/><polygon points="470,92 461,86 462,94" fill="var(--muted)"/>
  <path d="M 213,84 C 240,140 380,140 461,104" fill="none" stroke="var(--teal)" stroke-width="1.5" stroke-dasharray="4 4"/>
  <polygon points="470,100 460,101 464,108" fill="var(--teal)"/>
  <!-- 分配条：1A ≈ 16.25px，总 32A=520px（x30-550）；段间 2px gap -->
  <rect x="30"  y="230" width="128" height="32" rx="6" fill="var(--slate-tint)" stroke="var(--slate)" stroke-width="1"/>
  <rect x="160" y="230" width="390" height="32" rx="6" fill="var(--blue)"/>
  <rect x="30"  y="300" width="323" height="32" rx="6" fill="var(--amber-tint)" stroke="var(--amber)" stroke-width="1"/>
  <rect x="355" y="300" width="195" height="32" rx="6" fill="var(--blue)"/>
  <line x1="550" y1="222" x2="550" y2="340" stroke="var(--line)" stroke-width="1" stroke-dasharray="3 3"/>
  <g class="zh">
    <text x="72" y="67" text-anchor="middle" font-size="12" fill="var(--ink)">电网</text>
    <text x="213" y="67" text-anchor="middle" font-size="12" font-weight="600" fill="var(--teal)">CT 采集盒</text>
    <text x="360" y="67" text-anchor="middle" font-size="12" fill="var(--ink)">家庭配电</text>
    <text x="530" y="37" text-anchor="middle" font-size="12" fill="var(--slate)">家用电器</text>
    <text x="530" y="101" text-anchor="middle" font-size="12" font-weight="600" fill="#FFFFFF">充电桩</text>
    <text x="330" y="152" text-anchor="middle" font-size="10.5" fill="var(--teal)">实时电流读数</text>
    <text x="30" y="203" font-size="12.5" font-weight="600" fill="var(--ink)">「入户上限」32 A 内动态分配</text>
    <text x="550" y="203" text-anchor="end" font-size="10.5" fill="var(--muted)">← 32 A →</text>
    <text x="30" y="224" font-size="10.5" fill="var(--muted)">家里用电少 → 充电全速</text>
    <text x="94" y="250" text-anchor="middle" font-size="11" fill="var(--slate)">家庭 8 A</text>
    <text x="355" y="250" text-anchor="middle" font-size="11.5" font-weight="600" fill="#FFFFFF">充电 24 A</text>
    <text x="30" y="294" font-size="10.5" fill="var(--muted)">家里用电多 → 桩自动让电</text>
    <text x="191" y="320" text-anchor="middle" font-size="11" fill="var(--amber)">家庭 20 A</text>
    <text x="452" y="320" text-anchor="middle" font-size="11.5" font-weight="600" fill="#FFFFFF">充电 12 A</text>
    <text x="30" y="362" font-size="10.5" fill="var(--muted)">充电段不低于「最低充电电流」（6 A 起）；再不足则暂停，负荷下降后自动恢复。</text>
  </g>
  <g class="en">
    <text x="72" y="67" text-anchor="middle" font-size="11" fill="var(--ink)">Grid</text>
    <text x="213" y="67" text-anchor="middle" font-size="10.5" font-weight="600" fill="var(--teal)">CT sensing box</text>
    <text x="360" y="67" text-anchor="middle" font-size="10" fill="var(--ink)">Distribution</text>
    <text x="530" y="37" text-anchor="middle" font-size="10.5" fill="var(--slate)">Appliances</text>
    <text x="530" y="101" text-anchor="middle" font-size="10.5" font-weight="600" fill="#FFFFFF">Charger</text>
    <text x="330" y="152" text-anchor="middle" font-size="10" fill="var(--teal)">live current readings</text>
    <text x="30" y="203" font-size="12" font-weight="600" fill="var(--ink)">Dynamic allocation within the 32 A "Max into house" cap</text>
    <text x="550" y="203" text-anchor="end" font-size="10" fill="var(--muted)">← 32 A →</text>
    <text x="30" y="224" font-size="10" fill="var(--muted)">House quiet → full-speed charging</text>
    <text x="94" y="250" text-anchor="middle" font-size="10.5" fill="var(--slate)">Home 8 A</text>
    <text x="355" y="250" text-anchor="middle" font-size="11" font-weight="600" fill="#FFFFFF">Charging 24 A</text>
    <text x="30" y="294" font-size="10" fill="var(--muted)">House busy → the charger yields</text>
    <text x="191" y="320" text-anchor="middle" font-size="10.5" fill="var(--amber)">Home 20 A</text>
    <text x="452" y="320" text-anchor="middle" font-size="11" font-weight="600" fill="#FFFFFF">Charging 12 A</text>
    <text x="30" y="362" font-size="10" fill="var(--muted)">The charging share never drops below "Min charging current" (6 A+); below that it pauses and auto-resumes.</text>
  </g>
</svg>'''



DIAGRAMS = {
    "channels": D1,
    "states":   D2,
    "sharing":  D3,
    "pairing":  D4,
    "dlb":      D5,
}

def standalone(svg, lang):
    other = "en" if lang == "zh" else "zh"
    out = re.sub(r'  <g class="%s">.*?</g>\n' % other, "", svg, flags=re.S)
    for k, v in HEX.items():
        out = out.replace("var(%s)" % k, v)
    return out.replace('<svg ', "<svg font-family='%s' " % FONT, 1)

def main():
    for name, svg in DIAGRAMS.items():
        for lang in ("zh", "en"):
            path = os.path.join(IMG, "%s.%s.svg" % (name, lang))
            open(path, "w").write(standalone(svg, lang))
            print("wrote", os.path.relpath(path, ROOT))
    h = open(INDEX).read()
    for name, svg in DIAGRAMS.items():
        vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
        marker = '<svg viewBox="%s"' % vb
        if marker not in h:
            print("SKIP inline (not present yet):", name)
            continue
        s = h.index(marker)
        e = h.index("</svg>", s) + len("</svg>")
        h = h[:s] + svg + h[e:]
        print("inline refreshed:", name)
    open(INDEX, "w").write(h)

if __name__ == "__main__":
    main()
