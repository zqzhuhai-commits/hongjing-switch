# 红色警戒 Switch 中文版

基于 [Vanilla Conquer Switch](https://github.com/capsterx-switch/Vanilla-Conquer/tree/v0-r6) 的红色警戒 1 中文资源补丁和 NSP 启动前端。

**[下载 v0.3 正式版](https://github.com/zqzhuhai-commits/hongjing-switch/releases/tag/v0.3)**

## v0.3 内容

- 修复英文资源优先加载导致的中文菜单覆盖问题。
- 加入 90 个中文 SHP 资源，包含右侧建筑、单位按钮图片。
- 两个资料片菜单名称改为“反击任务”“余波任务”。
- NRO 显示名称为“红色警戒”，带自定义图标；附带同名 NSP 前端。

用户已反馈本版可以运行。仍可能有少量英文，尚未完成所有界面、任务和硬件版本的测试。此项目为社区自制程序，非任天堂或 EA 官方发行。

## 安装和升级

需要能够运行自制程序的 Switch，以及你自己的红色警戒 1 游戏数据。本包不是完整游戏数据包。

1. 完全结束游戏，备份 SD 卡 `switch/redalert/EXPAND2.MIX` 和 `switch/redalert/RedAlert.nro`。
2. 下载 Release 中的 `RedAlert-CHS-v03-and-NSP.zip` 并解压。
3. 将其中 `RedAlert-CHS-v03/patch/` 的 **两个文件一起**覆盖到 SD 卡 `switch/redalert/`。
4. 保留原有 `REDALERT.MIX`、`HIRES1.MIX`、`MAIN.MIX` 等游戏数据。
5. 已安装的 NSP 可以继续使用；首次使用可安装包内的 `红色警戒.nsp`。
6. 放回 SD 卡后启动游戏。

也可在 Windows 运行包内的 `Install-CHS.cmd`。安装器会检查匹配版本并备份；Windows 自动安装器未实机测试，支持手动安装。

**NSP 固定目标：`sdmc:/switch/redalert/RedAlert.nro`。** 文件名需要为 `RedAlert.nro`；启动界面显示名仍为中文。NSP 仅负责启动，不能删除 NRO 或游戏数据。

本补丁基于已核验的输入版本制作。全新安装者请准备兼容的游戏数据，不要把补丁误认为完整游戏。自动安装器遇到不匹配的文件会停止。

## 校验和回滚

Release 的 `SHA256SUMS.txt` 提供每个附件的 SHA-256。完整包 SHA-256：

```text
0124e702e4ebaf132683facbb0c9eed9cc9932378e3572d75e1ff5d41f9835ab
```

回滚时完全结束游戏，将备份的 `EXPAND2.MIX` 和 `RedAlert.nro` 一起恢复。请勿只更新或回滚其中一个文件。

## 源码和资源来源

- 游戏引擎：Vanilla Conquer Switch，`v0-r6` / `dbebd4181658cd8232c495bd12760a1d1bc00f99`。许可原文见 `licenses/Vanilla-Conquer.txt`。
- NSP 前端：[switch-nsp-forwarder 0.0.8](https://github.com/TooTallNate/switch-nsp-forwarder/tree/0.0.8)，MIT。
- 中文文本、字体和图片来自用户提供的中文版资源；游戏资源权利属于相应权利人，不随工具源码改授许可。
- 两项新增菜单字形基于 [Noto Sans CJK](https://github.com/notofonts/noto-cjk) 栅格化。
- Release 附带 `Source-v0.3.zip`，包含固定版本的引擎和前端源码，以及本项目补丁脚本和修改说明；没有主机密钥。

`tools/build_chs_v03.py` 是资源补丁处理脚本，需要原输入文件和 v0.2 中间资源；它不是从干净源码一键交叉编译整个游戏的脚本。当前发布的 NRO 基于上游预编译文件，仅定长替换两个菜单字符串，名称及图标来自此前制作版本。

## 问题反馈

请提交界面截图、启动方式、系统/自制环境版本，以及是否同时更新了两个补丁文件。发现其他英文时请标出位置。
