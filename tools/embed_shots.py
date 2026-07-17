#!/usr/bin/env python3
# 截图嵌入：Artifact(base64 内嵌) + 双语 Markdown(文件引用)
import base64, os

ROOT = "/Users/apple/Documents/workspace/work/EVSEProNew"
SCRATCH = "/private/tmp/claude-501/-Users-apple-Documents-workspace-work-EVSEProNew/aaa3a2c3-1c0a-4162-803b-649aa9f62331/scratchpad"
IMG = os.path.join(ROOT, "docs/user-manual/images/screenshots")

def uri(name):
    b = open(os.path.join(IMG, name + ".jpg"), "rb").read()
    return "data:image/jpeg;base64," + base64.b64encode(b).decode()

CAP = {  # name: (zh, en)
    "home_grid":    ("首页 · 设备网格", "Home · device grid"),
    "pairing_start":("「添加新设备」选择配对方式", '"Add a new device" — choose a method'),
    "signin":       ("登录页", "Sign-in"),
    "now_ready":    ("就绪", "READY"),
    "now_charging": ("充电中", "Charging"),
    "now_waiting":  ("等待中", "WAITING"),
    "now_complete": ("已完成", "COMPLETE"),
    "schedule_tab": ("「计划」标签 · 一次性", 'Schedule tab · One-time'),
    "history":      ("「记录」标签", "History tab"),
    "settings":     ("设备设置页（物主视角）", "Device settings (owner view)"),
    "rateplan":     ("电价方案编辑器", "Rate plan editor"),
    "profile":      ("「我的」页", '"Me" page'),
}

def shot(name):
    zh, en = CAP[name]
    return ('\n    <figure class="shot">\n      <img src="%s" alt="%s / %s" loading="lazy">\n'
            '      <figcaption><span class="zh">%s</span><span class="en">%s</span></figcaption>\n    </figure>\n'
            % (uri(name), zh, en, zh, en))

def gallery(names):
    cells = []
    for n in names:
        zh, en = CAP[n]
        cells.append('      <div><img src="%s" alt="%s / %s" loading="lazy"><p class="lbl">'
                     '<span class="zh">%s</span><span class="en">%s</span></p></div>' % (uri(n), zh, en, zh, en))
    return '\n    <figure class="shot-grid">\n%s\n    </figure>\n' % "\n".join(cells)

art = os.path.join(SCRATCH, "evsepro-user-manual.html")
html = open(art).read()

# CSS（挂在示意图样式之后）
css_anchor = "  figure.diagram figcaption { font-size: 12.5px; color: var(--muted); text-align: center; padding: 8px 0 4px; }"
assert css_anchor in html
html = html.replace(css_anchor, css_anchor + """

  /* ── 界面截图 ── */
  figure.shot { margin: 6px auto 22px; text-align: center; }
  figure.shot img { width: 100%; max-width: 300px; border-radius: 22px; border: 1px solid var(--line); box-shadow: var(--shadow); }
  figure.shot figcaption { font-size: 12.5px; color: var(--muted); padding-top: 8px; }
  figure.shot-grid { margin: 6px 0 22px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  @media (max-width: 640px) { figure.shot-grid { grid-template-columns: repeat(2, 1fr); } }
  figure.shot-grid > div { text-align: center; }
  figure.shot-grid img { width: 100%; border-radius: 16px; border: 1px solid var(--line); box-shadow: var(--shadow); }
  figure.shot-grid .lbl { font-size: 12px; color: var(--muted); padding-top: 6px; margin: 0; }""", 1)

# 打印防断
pb = "    .tw, .note, .card, ol.steps > li, tr, figure.diagram { break-inside: avoid; }"
assert pb in html
html = html.replace(pb, "    .tw, .note, .card, ol.steps > li, tr, figure.diagram, figure.shot, figure.shot-grid > div { break-inside: avoid; }", 1)

def insert_after(anchor, payload):
    global html
    assert anchor in html, "missing artifact anchor: %r" % anchor[:70]
    html = html.replace(anchor, anchor + payload, 1)

# §2.3 配对步骤条示意图后 → 添加新设备截图
insert_after('<figcaption><span class="zh">添加充电桩流程</span><span class="en">Add-a-charger flow</span></figcaption>\n    </figure>',
             shot("pairing_start"))
# §3.1 首页网格
insert_after('<p class="en">Next to the device with Bluetooth connectable, the card shows "Online" regardless of internet.</p>',
             shot("home_grid"))
# §4.1 状态表后 → 四态画廊
insert_after('<tr><td>"COMPLETE"</td><td>Session finished normally</td><td>"Charge Again"</td></tr>\n    </table></div>',
             gallery(["now_ready", "now_charging", "now_waiting", "now_complete"]))
# §5 预约要点后
insert_after('"Stop charging" cancels the wait.</div>', shot("schedule_tab"))
# §6 电价 bullet 后
insert_after('<li>The currency symbol follows the system language and region.</li>\n    </ul>', shot("rateplan"))
# §7.1 记录主页 bullet 后
insert_after('"Export full history (CSV)" for bulk export.</li>\n    </ul>', shot("history"))
# §11.1 设置表后
insert_after('<tr><td>Unpair this device</td><td><span class="b b-owner">Owner</span> <span class="b b-near">Nearby</span></td><td>See below</td></tr>\n    </table></div>',
             shot("settings"))
# §12 章首 + §12.1 登录
insert_after('<h2><span class="zh">账号与个性化</span><span class="en">Account &amp; personalization</span></h2>', shot("profile"))
insert_after('The app has no old-password → new-password form.</li>\n    </ul>', shot("signin"))

open(art, "w").write(html)
print("artifact patched, size = %.1f MB" % (len(html) / 1e6))

# ── Markdown ──
def md_img(name, width=300, lang="zh"):
    zh, en = CAP[name]
    cap = zh if lang == "zh" else en
    return '\n<p align="center"><img src="images/screenshots/%s.jpg" width="%d" alt="%s"><br><sub>%s</sub></p>\n' % (name, width, cap, cap)

def md_gallery(names, lang="zh"):
    imgs = " ".join('<img src="images/screenshots/%s.jpg" width="165" alt="%s">' % (n, CAP[n][0 if lang=="zh" else 1]) for n in names)
    labels = " · ".join(CAP[n][0 if lang=="zh" else 1] for n in names)
    return '\n<p align="center">%s<br><sub>%s</sub></p>\n' % (imgs, labels)

def patch(path, pairs):
    src = open(path).read()
    for anchor, payload in pairs:
        assert anchor in src, "missing md anchor in %s: %r" % (path, anchor[:60])
        src = src.replace(anchor, anchor + payload, 1)
    open(path, "w").write(src)
    print("patched", path)

G = ["now_ready", "now_charging", "now_waiting", "now_complete"]
zh_md = os.path.join(ROOT, "docs/user-manual/EVSEPro-使用功能说明书.md")
patch(zh_md, [
    ("![添加充电桩流程](images/pairing.zh.svg)", md_img("pairing_start", lang="zh")),
    ("人就在设备旁且蓝牙可连时，卡片直接显示「在线」，与是否联网无关。", md_img("home_grid", lang="zh")),
    ("| 「已完成」 | 本次充电正常结束 | 「再次充电」☁️ |", md_gallery(G, "zh")),
    ("- 到点前设备显示「等待中」状态，可随时手动「停止充电」取消本次等待。", md_img("schedule_tab", lang="zh")),
    ("- 货币符号跟随系统语言与地区自动决定。", md_img("rateplan", lang="zh")),
    ("- 「分享」把本页渲染成长图分享；「导出完整历史（CSV）」批量导出。", md_img("history", lang="zh")),
    ("> 屏幕亮度、温度单位、启动方式为蓝牙近场专属设置，远程修改会提示「靠近后重试」——这是帮助中心「远程改不了屏幕亮度等设置？」的官方答案。", md_img("settings", lang="zh")),
    ("## 12 账号与个性化 {#account}", md_img("profile", lang="zh")),
    ("- **忘记密码**：输入邮箱 → 「发送重置链接」→ 到邮件里完成重置（链接有效期 30 分钟，注意检查垃圾邮件文件夹）。App 内不提供旧密码改新密码的表单。", md_img("signin", lang="zh")),
])

en_md = os.path.join(ROOT, "docs/user-manual/EVSEPro-User-Manual.en.md")
patch(en_md, [
    ("![Add-a-charger flow](images/pairing.en.svg)", md_img("pairing_start", lang="en")),
    ("If you're next to the device and Bluetooth can connect, the card shows \"Online\" regardless of internet.", md_img("home_grid", lang="en")),
    ('| "COMPLETE" | Session finished normally | "Charge Again" ☁️ |', md_gallery(G, "en")),
    ('- Before the start time the device shows "WAITING"; "Stop charging" cancels that wait.', md_img("schedule_tab", lang="en")),
    ("- The currency symbol follows the system language and region.", md_img("rateplan", lang="en")),
    ('- "Share" renders the page as an image; "Export full history (CSV)" for bulk export.', md_img("history", lang="en")),
    ('> Screen brightness, temperature unit and start method are Bluetooth-only; remote attempts get "Move closer and try again".', md_img("settings", lang="en")),
    ("## 12 Account & personalization {#account}", md_img("profile", lang="en")),
    ("- **Forgot password**: enter the email → \"Send reset link\" → finish in the email (link valid 30 minutes; check spam). The app has no old-password → new-password form.", md_img("signin", lang="en")),
])

print("ALL DONE")
