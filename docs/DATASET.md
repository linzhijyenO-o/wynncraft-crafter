# wynnbd — Wynncraft 物品图鉴 · Ingredient 数据集

> English README: [../README.md](../README.md) · 项目主页：中文版 [../README.zh-CN.md](../README.zh-CN.md)

把 <https://wynncraft.com/help/item-guide> 里的**全部材料（Ingredient）**抓下来，并把每件物品的**所有属性规范化成统一标签**，可直接用于筛选、建库、做自研计算器。

- 物品总数：**972**
- 标签种类：**749**（共 10,172 条标签赋值，平均每件 10.5 个）
- 词条键：**72**（2,016 条 物品×词条 记录）
- 掉落源：**1,193** 个（2,986 条 物品×掉落 记录）
- 抓取时间：2026-10-24

---

## 1. 数据是怎么来的（重要）

`/help/item-guide` 是 Nuxt 客户端渲染页面，直接请求 HTML 只能拿到导航和页脚，**数据不在 HTML 里**。

翻页后的真实请求是官方 API，网页和本数据集完全同源：

```
POST https://api.wynncraft.com/v3/item/search?page=N
Content-Type: application/json

{"type": ["ingredient"]}
```

返回 `controller: {count: 972, pages: 49}`，每页 20 条。`scripts/fetch_ingredients.ps1` 就是按这个接口把 49 页合并成一个 JSON（原始响应不改写，存 `raw/`）。

筛选侧的元数据（tier 取值、全部词条键、职业等）来自 `GET https://api.wynncraft.com/v3/item/metadata`，存 `raw/item_metadata.json`。

---

## 2. 目录结构

```
wynnbd/
├─ README.md                          ← 你正在看的这份
├─ raw/                               原始数据（不做任何改写）
│  ├─ ingredients_raw.json            49 页合并后的接口响应（972 条）
│  ├─ item_metadata.json              筛选项元数据（117 个词条键、tier 表等）
│  └─ fetch_log.txt                   抓取日志
├─ data/                              规范化产物
│  ├─ ingredients.json                主数据（嵌套 + tags，含 icon/掉落坐标）
│  ├─ ingredients.csv                 主表（宽表，一行一件，Excel 可直接开）
│  ├─ ingredient_identifications.csv  词条长表（一行一个 物品×词条）
│  ├─ ingredient_drops.csv            掉落长表（一行一个 物品×掉落源）
│  ├─ tags.json                       标签词表（命名空间 + 每个标签的物品数）
│  ├─ tag_index.json                  标签 → 物品 id 列表（反查）
│  ├─ drop_index.json                 掉落源 → 物品 id 列表（反查）
│  ├─ tags.md                         标签字典（中文说明，人读）
│  └─ ingredients.md                  按职业分组的全量清单（人读）
├─ crafter/                           自制装备制作器（Web，Python 后端）
│  ├─ README.md                       用法、计算口径、搜索算法说明
│  ├─ start.cmd                       一键启动（自动开浏览器）
│  ├─ backend/                        engine.py 计算引擎 / server.py HTTP 服务
│  └─ frontend/                       单页前端（原生 HTML/CSS/JS）
└─ scripts/
   ├─ fetch_ingredients.ps1           抓取（可重复运行）
   ├─ build_dataset.py                规范化 + 导出
   └─ run_all.ps1                     一键执行上面两步
```

> `crafter/` 直接读 `data/ingredients.json`，用法见 [crafter/README.md](../crafter/README.md)。

---

## 3. 字段字典（`ingredients.json` / `ingredients.csv`）

单位已统一：耐久按「千」还原成整数、持续时间用秒、使用次数用次。

| 字段 | 类型 | 单位/取值 | 说明 |
| --- | --- | --- | --- |
| `id` | string | — | 接口 `internalName`，也是唯一主键（972 个互不相同） |
| `name` | string | — | 显示名 `displayName` |
| `type` | string | 恒为 `ingredient` | 物品大类 |
| `tier.code` | string | `TIER_0`~`TIER_3` | 接口原值 |
| `tier.level` | int | 0–3 | 数值化阶级，便于排序/过滤 |
| `tier.name` | string | Normal / Unique / Rare / Legendary | 阶级英文名 |
| `tier.color` | string | `#rrggbb` | 游戏内阶级配色 |
| `crafting_level` | int | 1–119 | 可用于配方的最低制作等级 |
| `professions` | string[] | 8 种职业 | 该材料能用在哪些职业的配方里 |
| `emblem` | string | 恒为 `square` | 图标底框 |
| `icon` | object | — | 原样保留：`format` 为 `attribute`（原版模型 + CustomModelData）或 `skin`（材质哈希） |
| `item_ids` | object | 见下 | **只作用于成品（装备）**的属性 |
| `consumable_ids` | object | 见下 | **只作用于消耗品（卷轴/药水）**的属性 |
| `position_modifiers` | object | % | 放在配方格不同相对位置的加成 |
| `identifications` | object[] | 见下 | 物品提供的属性词条（ID） |
| `drops` | object[] | 见下 | 掉落来源 |
| `drop_entries_raw` | int | — | 接口原始掉落条数（去重前，便于回溯） |
| `tags` | string[] | `命名空间:值` | 全部标签，见第 4 节 |

**`item_ids`**（接口 `itemOnlyIDs`）

| 键 | 对应接口字段 | 换算 |
| --- | --- | --- |
| `durability` | `durabilityModifier` | ÷1000（接口里是 -185000 这种千分位值） |
| `strength` / `dexterity` / `intelligence` / `defence` / `agility` | `*Requirement` | 原值（成品上的最低属性需求） |

**`consumable_ids`**（接口 `consumableOnlyIDs`）：`duration` 秒（负数为减益）、`charges` 使用次数。

**`position_modifiers`**（接口 `ingredientPositionModifiers`）：`left` `right` `above` `under` `touching`（相邻）`not_touching`（不相邻），单位 %。

**`identifications[]`**

| 键 | 说明 |
| --- | --- |
| `id` | 词条键，如 `rawHealth`、`thorns`（共 72 种） |
| `label` | 由词条键自动派生的可读名，如 `Raw Health` |
| `min` / `raw` / `max` | 接口原值：区间最小值 / 基准值 / 最大值（固定值三者相等） |

**`drops[]`**：`name` 掉落源名称；`has_coords` 是否有坐标；`coords` 为 `[[x, y, z, 权重?], ...]`。

---

## 4. 标签体系

所有标签写成 `命名空间:值`；带数值的写成 `命名空间:分量:数值`。

| 命名空间 | 中文 | 类别 | 标签数 | 示例 |
| --- | --- | --- | ---: | --- |
| `type` | 物品大类 | 枚举 | 1 | `type:ingredient` |
| `tier` | 阶级 | 枚举 | 4 | `tier:3` |
| `tier-name` | 阶级名 | 枚举 | 4 | `tier-name:Legendary` |
| `profession` | 制作职业 | 枚举 | 8 | `profession:armouring` |
| `crafting-level` | 制作等级 | 枚举 | 119 | `crafting-level:119` |
| `emblem` | 徽记 | 枚举 | 1 | `emblem:square` |
| `id` | 词条 ID | 枚举 | 72 | `id:rawHealth` |
| `item` | 成品属性 | 数值 | 306 | `item:durability:-185` |
| `consumable` | 消耗品属性 | 数值 | 138 | `consumable:duration:-300` |
| `position` | 相邻加成 | 数值 | 96 | `position:left:+85` |

- **枚举型**（categorical）适合当筛选维度；**数值型**（value）本质是属性表摊平，方便一句 `contains` 直接筛。
- 数值为 0 的属性**不生成标签**（避免噪声），需要 0 值请看结构化字段。
- 完整的 749 条标签、每条的物品数与占比见 `data/tags.md`；机读版见 `data/tags.json`。
- 反查：`data/tag_index.json`（标签 → 物品）、`data/drop_index.json`（掉落源 → 物品）。

一件典型物品（Rayscorched Plating）的标签：

```
type:ingredient  tier:3  tier-name:Legendary  profession:armouring  crafting-level:119
emblem:square  item:durability:-185  item:intelligence:-15  item:defence:+35
id:rawHealth  id:rawDefence  id:2ndSpellCost
```

---

## 5. 数据校验

| 检查 | 结果 |
| --- | --- |
| 条数与接口声明一致 | 972 = 972（49 页 × 20） |
| `id` 唯一性 | 通过，无重复 |
| 每条都有 tier / crafting_level / professions | 通过 |
| 阶级分布 | Normal 233 / Unique 250 / Rare 294 / Legendary 195 |
| 制作等级范围 | 1–119 |
| 无词条的物品 | 33 件（接口本身就没有 `identifications`） |
| 无掉落信息的物品 | 148 件（接口未给 `droppedBy`，多为特殊来源） |
| 重复掉落条目 | 原始 3,148 条中有 158 条完全重复（同名同坐标），规范化时已去重，`drop_entries_raw` 保留原数 |

> 注：接口里 tier 只有 `TIER_0`~`TIER_3`，对应游戏内的 Normal / Unique / Rare / Legendary（材料的阶级名沿用游戏内写法，不叫 Common）。

---

## 6. 复现

需要 PowerShell + Python 3。

```powershell
cd D:\C++\wynnbd
.\scripts\run_all.ps1
```

或分步：

```powershell
.\scripts\fetch_ingredients.ps1      # 抓取 -> raw/
python .\scripts\build_dataset.py    # 规范化 -> data/
```

抓取脚本带重试与 250ms 间隔；接口若改版，只需改 `fetch_ingredients.ps1` 里的 `$apiSearch` 与请求体。

如果系统禁止运行脚本（`AuthorizationManager 检查失败` / `UnauthorizedAccess`），先在当前窗口放开：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
```

两个 `.ps1` 存的是 **UTF-8 with BOM**，否则 Windows PowerShell 5.1 会按 GBK 读，中文注释就乱码了；改脚本时别把 BOM 丢了。

---

## 7. 备注

- 网页标题写的是 “5000+ usable items”，那是全部物品（武器 2414 / 护甲 2121 / 饰品 932 / 书 172 / 护符 4 / 材料 972）；本数据集只取 `type=ingredient`。
- 材料图标有两种格式：`attribute`（原版物品 + CustomModelData，可用资源包渲染）与 `skin`（材质哈希，需走官方 CDN / textures 接口）。
- 掉落坐标来自接口原始数据，可直接拼成 `https://map.wynncraft.com?coords=x,y,z`。
