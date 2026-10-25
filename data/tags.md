# Wynncraft Ingredient 标签字典

- 生成时间：2026-10-24T20:09:57+08:00
- 数据来源：`POST https://api.wynncraft.com/v3/item/search  body: {"type":["ingredient"]}`
- 物品总数：972
- 标签种类：749

## 一、命名空间

所有标签统一写成 `命名空间:值`，值内部若还有分量则写成 `命名空间:分量:数值`。

`categorical` 是枚举型标签（可当分类维度），`value` 是带数值的明细标签（本质是属性表被摊平）。

| 命名空间 | 中文 | 含义 | 类别 | 标签数 |
| --- | --- | --- | --- | --- |
| `type` | 物品大类 | 对象类型；目前抓取范围内恒为 ingredient | categorical | 1 |
| `tier` | 阶级 | 0=Normal 1=Unique 2=Rare 3=Legendary | categorical | 4 |
| `tier-name` | 阶级名 | 与 tier 一一对应的英文名 | categorical | 4 |
| `profession` | 制作职业 | 该材料可用于哪些职业的配方 | categorical | 8 |
| `crafting-level` | 制作等级 | 可用于配方的最低制作等级 1-119 | categorical | 119 |
| `emblem` | 徽记 | 物品图标底框样式 | categorical | 1 |
| `id` | 词条 ID | identifications 的键，即物品提供的属性词条 | categorical | 72 |
| `item` | 成品属性 | 只作用于成品(装备)的属性，格式 item:属性:数值 | value | 306 |
| `consumable` | 消耗品属性 | 只作用于消耗品(卷轴/药水)的属性，格式 consumable:属性:数值 | value | 138 |
| `position` | 相邻加成 | 配方格相对位置的效果加成(%)，格式 position:位置:数值 | value | 96 |

## 物品大类（type）

> 对象类型；目前抓取范围内恒为 ingredient

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `type:ingredient` | 材料 | 972 | 100.0% |

## 阶级（tier）

> 0=Normal 1=Unique 2=Rare 3=Legendary

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `tier:2` | Rare | 294 | 30.2% |
| `tier:1` | Unique | 250 | 25.7% |
| `tier:0` | Normal | 233 | 24.0% |
| `tier:3` | Legendary | 195 | 20.1% |

## 阶级名（tier-name）

> 与 tier 一一对应的英文名

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `tier-name:Rare` | 阶级英文名 | 294 | 30.2% |
| `tier-name:Unique` | 阶级英文名 | 250 | 25.7% |
| `tier-name:Normal` | 阶级英文名 | 233 | 24.0% |
| `tier-name:Legendary` | 阶级英文名 | 195 | 20.1% |

## 制作职业（profession）

> 该材料可用于哪些职业的配方

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `profession:armouring` | 防具锻造 | 255 | 26.2% |
| `profession:tailoring` | 裁缝 | 252 | 25.9% |
| `profession:weaponsmithing` | 武器锻造 | 226 | 23.3% |
| `profession:woodworking` | 木工 | 207 | 21.3% |
| `profession:alchemism` | 炼金 | 186 | 19.1% |
| `profession:cooking` | 烹饪 | 160 | 16.5% |
| `profession:scribing` | 铭文 | 148 | 15.2% |
| `profession:jeweling` | 珠宝 | 138 | 14.2% |

## 制作等级（crafting-level）

> 可用于配方的最低制作等级 1-119

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `crafting-level:105` | 制作等级 105 | 32 | 3.3% |
| `crafting-level:90` | 制作等级 90 | 24 | 2.5% |
| `crafting-level:100` | 制作等级 100 | 23 | 2.4% |
| `crafting-level:115` | 制作等级 115 | 21 | 2.2% |
| `crafting-level:83` | 制作等级 83 | 18 | 1.9% |
| `crafting-level:103` | 制作等级 103 | 17 | 1.7% |
| `crafting-level:104` | 制作等级 104 | 17 | 1.7% |
| `crafting-level:60` | 制作等级 60 | 17 | 1.7% |
| `crafting-level:85` | 制作等级 85 | 17 | 1.7% |
| `crafting-level:117` | 制作等级 117 | 15 | 1.5% |
| `crafting-level:25` | 制作等级 25 | 15 | 1.5% |
| `crafting-level:55` | 制作等级 55 | 15 | 1.5% |
| `crafting-level:78` | 制作等级 78 | 15 | 1.5% |
| `crafting-level:92` | 制作等级 92 | 15 | 1.5% |
| `crafting-level:63` | 制作等级 63 | 14 | 1.4% |
| `crafting-level:70` | 制作等级 70 | 14 | 1.4% |
| `crafting-level:75` | 制作等级 75 | 14 | 1.4% |
| `crafting-level:80` | 制作等级 80 | 14 | 1.4% |
| `crafting-level:95` | 制作等级 95 | 14 | 1.4% |
| `crafting-level:118` | 制作等级 118 | 13 | 1.3% |
| `crafting-level:15` | 制作等级 15 | 13 | 1.3% |
| `crafting-level:45` | 制作等级 45 | 13 | 1.3% |
| `crafting-level:77` | 制作等级 77 | 13 | 1.3% |
| `crafting-level:102` | 制作等级 102 | 12 | 1.2% |
| `crafting-level:30` | 制作等级 30 | 12 | 1.2% |
| `crafting-level:65` | 制作等级 65 | 12 | 1.2% |
| `crafting-level:99` | 制作等级 99 | 12 | 1.2% |
| `crafting-level:10` | 制作等级 10 | 11 | 1.1% |
| `crafting-level:96` | 制作等级 96 | 11 | 1.1% |
| `crafting-level:98` | 制作等级 98 | 11 | 1.1% |
| `crafting-level:1` | 制作等级 1 | 10 | 1.0% |
| `crafting-level:20` | 制作等级 20 | 10 | 1.0% |
| `crafting-level:53` | 制作等级 53 | 10 | 1.0% |
| `crafting-level:62` | 制作等级 62 | 10 | 1.0% |
| `crafting-level:76` | 制作等级 76 | 10 | 1.0% |
| `crafting-level:113` | 制作等级 113 | 9 | 0.9% |
| `crafting-level:116` | 制作等级 116 | 9 | 0.9% |
| `crafting-level:23` | 制作等级 23 | 9 | 0.9% |
| `crafting-level:35` | 制作等级 35 | 9 | 0.9% |
| `crafting-level:37` | 制作等级 37 | 9 | 0.9% |
| `crafting-level:43` | 制作等级 43 | 9 | 0.9% |
| `crafting-level:50` | 制作等级 50 | 9 | 0.9% |
| `crafting-level:72` | 制作等级 72 | 9 | 0.9% |
| `crafting-level:73` | 制作等级 73 | 9 | 0.9% |
| `crafting-level:8` | 制作等级 8 | 9 | 0.9% |
| `crafting-level:97` | 制作等级 97 | 9 | 0.9% |
| `crafting-level:119` | 制作等级 119 | 8 | 0.8% |
| `crafting-level:33` | 制作等级 33 | 8 | 0.8% |
| `crafting-level:36` | 制作等级 36 | 8 | 0.8% |
| `crafting-level:56` | 制作等级 56 | 8 | 0.8% |
| `crafting-level:64` | 制作等级 64 | 8 | 0.8% |
| `crafting-level:7` | 制作等级 7 | 8 | 0.8% |
| `crafting-level:81` | 制作等级 81 | 8 | 0.8% |
| `crafting-level:84` | 制作等级 84 | 8 | 0.8% |
| `crafting-level:87` | 制作等级 87 | 8 | 0.8% |
| `crafting-level:89` | 制作等级 89 | 8 | 0.8% |
| `crafting-level:14` | 制作等级 14 | 7 | 0.7% |
| `crafting-level:26` | 制作等级 26 | 7 | 0.7% |
| `crafting-level:27` | 制作等级 27 | 7 | 0.7% |
| `crafting-level:42` | 制作等级 42 | 7 | 0.7% |
| `crafting-level:5` | 制作等级 5 | 7 | 0.7% |
| `crafting-level:106` | 制作等级 106 | 6 | 0.6% |
| `crafting-level:107` | 制作等级 107 | 6 | 0.6% |
| `crafting-level:108` | 制作等级 108 | 6 | 0.6% |
| `crafting-level:114` | 制作等级 114 | 6 | 0.6% |
| `crafting-level:22` | 制作等级 22 | 6 | 0.6% |
| `crafting-level:28` | 制作等级 28 | 6 | 0.6% |
| `crafting-level:3` | 制作等级 3 | 6 | 0.6% |
| `crafting-level:31` | 制作等级 31 | 6 | 0.6% |
| `crafting-level:32` | 制作等级 32 | 6 | 0.6% |
| `crafting-level:34` | 制作等级 34 | 6 | 0.6% |
| `crafting-level:41` | 制作等级 41 | 6 | 0.6% |
| `crafting-level:44` | 制作等级 44 | 6 | 0.6% |
| `crafting-level:57` | 制作等级 57 | 6 | 0.6% |
| `crafting-level:58` | 制作等级 58 | 6 | 0.6% |
| `crafting-level:59` | 制作等级 59 | 6 | 0.6% |
| `crafting-level:6` | 制作等级 6 | 6 | 0.6% |
| `crafting-level:66` | 制作等级 66 | 6 | 0.6% |
| `crafting-level:82` | 制作等级 82 | 6 | 0.6% |
| `crafting-level:86` | 制作等级 86 | 6 | 0.6% |
| `crafting-level:91` | 制作等级 91 | 6 | 0.6% |
| `crafting-level:93` | 制作等级 93 | 6 | 0.6% |
| `crafting-level:16` | 制作等级 16 | 5 | 0.5% |
| `crafting-level:18` | 制作等级 18 | 5 | 0.5% |
| `crafting-level:21` | 制作等级 21 | 5 | 0.5% |
| `crafting-level:40` | 制作等级 40 | 5 | 0.5% |
| `crafting-level:47` | 制作等级 47 | 5 | 0.5% |
| `crafting-level:74` | 制作等级 74 | 5 | 0.5% |
| `crafting-level:88` | 制作等级 88 | 5 | 0.5% |
| `crafting-level:101` | 制作等级 101 | 4 | 0.4% |
| `crafting-level:109` | 制作等级 109 | 4 | 0.4% |
| `crafting-level:46` | 制作等级 46 | 4 | 0.4% |
| `crafting-level:61` | 制作等级 61 | 4 | 0.4% |
| `crafting-level:68` | 制作等级 68 | 4 | 0.4% |
| `crafting-level:9` | 制作等级 9 | 4 | 0.4% |
| `crafting-level:94` | 制作等级 94 | 4 | 0.4% |
| `crafting-level:112` | 制作等级 112 | 3 | 0.3% |
| `crafting-level:12` | 制作等级 12 | 3 | 0.3% |
| `crafting-level:13` | 制作等级 13 | 3 | 0.3% |
| `crafting-level:2` | 制作等级 2 | 3 | 0.3% |
| `crafting-level:24` | 制作等级 24 | 3 | 0.3% |
| `crafting-level:38` | 制作等级 38 | 3 | 0.3% |
| `crafting-level:39` | 制作等级 39 | 3 | 0.3% |
| `crafting-level:4` | 制作等级 4 | 3 | 0.3% |
| `crafting-level:48` | 制作等级 48 | 3 | 0.3% |
| `crafting-level:49` | 制作等级 49 | 3 | 0.3% |
| `crafting-level:51` | 制作等级 51 | 3 | 0.3% |
| `crafting-level:54` | 制作等级 54 | 3 | 0.3% |
| `crafting-level:67` | 制作等级 67 | 3 | 0.3% |
| `crafting-level:71` | 制作等级 71 | 3 | 0.3% |
| `crafting-level:11` | 制作等级 11 | 2 | 0.2% |
| `crafting-level:110` | 制作等级 110 | 2 | 0.2% |
| `crafting-level:52` | 制作等级 52 | 2 | 0.2% |
| `crafting-level:79` | 制作等级 79 | 2 | 0.2% |
| `crafting-level:111` | 制作等级 111 | 1 | 0.1% |
| `crafting-level:17` | 制作等级 17 | 1 | 0.1% |
| `crafting-level:19` | 制作等级 19 | 1 | 0.1% |
| `crafting-level:29` | 制作等级 29 | 1 | 0.1% |
| `crafting-level:69` | 制作等级 69 | 1 | 0.1% |

## 徽记（emblem）

> 物品图标底框样式

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `emblem:square` | 图标底框 square | 972 | 100.0% |

## 词条 ID（id）

> identifications 的键，即物品提供的属性词条

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `id:walkSpeed` | Walk Speed | 124 | 12.8% |
| `id:rawHealth` | Raw Health | 107 | 11.0% |
| `id:mainAttackDamage` | Main Attack Damage | 89 | 9.2% |
| `id:rawDefence` | Raw Defence | 89 | 9.2% |
| `id:spellDamage` | Spell Damage | 82 | 8.4% |
| `id:healthRegenRaw` | Health Regen Raw | 79 | 8.1% |
| `id:rawMainAttackDamage` | Raw Main Attack Damage | 74 | 7.6% |
| `id:rawStrength` | Raw Strength | 73 | 7.5% |
| `id:fireDamage` | Fire Damage | 61 | 6.3% |
| `id:earthDamage` | Earth Damage | 58 | 6.0% |
| `id:rawAgility` | Raw Agility | 58 | 6.0% |
| `id:rawSpellDamage` | Raw Spell Damage | 52 | 5.3% |
| `id:manaRegen` | Mana Regen | 50 | 5.1% |
| `id:thunderDamage` | Thunder Damage | 50 | 5.1% |
| `id:waterDamage` | Water Damage | 50 | 5.1% |
| `id:fireDefence` | Fire Defence | 48 | 4.9% |
| `id:gatherXpBonus` | Gather Xp Bonus | 48 | 4.9% |
| `id:lifeSteal` | Life Steal | 48 | 4.9% |
| `id:healthRegen` | Health Regen | 47 | 4.8% |
| `id:rawDexterity` | Raw Dexterity | 47 | 4.8% |
| `id:poison` | Poison | 46 | 4.7% |
| `id:waterDefence` | Water Defence | 46 | 4.7% |
| `id:airDamage` | Air Damage | 44 | 4.5% |
| `id:lootBonus` | Loot Bonus | 44 | 4.5% |
| `id:combatExperience` | Combat Experience | 43 | 4.4% |
| `id:earthDefence` | Earth Defence | 41 | 4.2% |
| `id:rawIntelligence` | Raw Intelligence | 38 | 3.9% |
| `id:airDefence` | Air Defence | 37 | 3.8% |
| `id:thorns` | Thorns | 34 | 3.5% |
| `id:manaSteal` | Mana Steal | 33 | 3.4% |
| `id:reflection` | Reflection | 30 | 3.1% |
| `id:thunderDefence` | Thunder Defence | 30 | 3.1% |
| `id:healingEfficiency` | Healing Efficiency | 28 | 2.9% |
| `id:exploding` | Exploding | 20 | 2.1% |
| `id:sprint` | Sprint | 19 | 2.0% |
| `id:sprintRegen` | Sprint Regen | 15 | 1.5% |
| `id:gatherSpeed` | Gather Speed | 13 | 1.3% |
| `id:stealing` | Stealing | 13 | 1.3% |
| `id:rawAttackSpeed` | Raw Attack Speed | 10 | 1.0% |
| `id:elementalDamage` | Elemental Damage | 9 | 0.9% |
| `id:rawMaxMana` | Raw Max Mana | 8 | 0.8% |
| `id:jumpHeight` | Jump Height | 7 | 0.7% |
| `id:lootQuality` | Loot Quality | 7 | 0.7% |
| `id:elementalDefence` | Elemental Defence | 6 | 0.6% |
| `id:damage` | Damage | 5 | 0.5% |
| `id:knockback` | Knockback | 5 | 0.5% |
| `id:rawEarthMainAttackDamage` | Raw Earth Main Attack Damage | 4 | 0.4% |
| `id:rawFireDamage` | Raw Fire Damage | 4 | 0.4% |
| `id:rawFireSpellDamage` | Raw Fire Spell Damage | 4 | 0.4% |
| `id:rawThunderDamage` | Raw Thunder Damage | 4 | 0.4% |
| `id:rawWaterDamage` | Raw Water Damage | 4 | 0.4% |
| `id:mainAttackRange` | Main Attack Range | 3 | 0.3% |
| `id:rawAirDamage` | Raw Air Damage | 3 | 0.3% |
| `id:rawWaterMainAttackDamage` | Raw Water Main Attack Damage | 3 | 0.3% |
| `id:rawEarthSpellDamage` | Raw Earth Spell Damage | 2 | 0.2% |
| `id:rawFireMainAttackDamage` | Raw Fire Main Attack Damage | 2 | 0.2% |
| `id:rawThunderMainAttackDamage` | Raw Thunder Main Attack Damage | 2 | 0.2% |
| `id:waterSpellDamage` | Water Spell Damage | 2 | 0.2% |
| `id:2ndSpellCost` | 2nd Spell Cost | 1 | 0.1% |
| `id:airSpellDamage` | Air Spell Damage | 1 | 0.1% |
| `id:earthMainAttackDamage` | Earth Main Attack Damage | 1 | 0.1% |
| `id:elementalSpellDamage` | Elemental Spell Damage | 1 | 0.1% |
| `id:fireSpellDamage` | Fire Spell Damage | 1 | 0.1% |
| `id:neutralDamage` | Neutral Damage | 1 | 0.1% |
| `id:rawAirMainAttackDamage` | Raw Air Main Attack Damage | 1 | 0.1% |
| `id:rawAirSpellDamage` | Raw Air Spell Damage | 1 | 0.1% |
| `id:rawEarthDamage` | Raw Earth Damage | 1 | 0.1% |
| `id:rawNeutralDamage` | Raw Neutral Damage | 1 | 0.1% |
| `id:rawNeutralMainAttackDamage` | Raw Neutral Main Attack Damage | 1 | 0.1% |
| `id:rawThunderSpellDamage` | Raw Thunder Spell Damage | 1 | 0.1% |
| `id:rawWaterSpellDamage` | Raw Water Spell Damage | 1 | 0.1% |
| `id:waterMainAttackDamage` | Water Main Attack Damage | 1 | 0.1% |

## 成品属性（item）

> 只作用于成品(装备)的属性，格式 item:属性:数值

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `item:durability:-52` | 耐久度 -52 | 23 | 2.4% |
| `item:strength:+10` | 力量需求 +10 | 23 | 2.4% |
| `item:defence:+10` | 防御需求 +10 | 20 | 2.1% |
| `item:durability:-40` | 耐久度 -40 | 20 | 2.1% |
| `item:agility:+10` | 技巧需求 +10 | 18 | 1.9% |
| `item:dexterity:+10` | 敏捷需求 +10 | 16 | 1.6% |
| `item:durability:-70` | 耐久度 -70 | 16 | 1.6% |
| `item:durability:-38` | 耐久度 -38 | 15 | 1.5% |
| `item:durability:-26` | 耐久度 -26 | 13 | 1.3% |
| `item:intelligence:+10` | 智力需求 +10 | 13 | 1.3% |
| `item:defence:+12` | 防御需求 +12 | 12 | 1.2% |
| `item:defence:+8` | 防御需求 +8 | 12 | 1.2% |
| `item:durability:-35` | 耐久度 -35 | 12 | 1.2% |
| `item:durability:-87` | 耐久度 -87 | 12 | 1.2% |
| `item:intelligence:+12` | 智力需求 +12 | 12 | 1.2% |
| `item:strength:+8` | 力量需求 +8 | 12 | 1.2% |
| `item:durability:-105` | 耐久度 -105 | 11 | 1.1% |
| `item:durability:-21` | 耐久度 -21 | 11 | 1.1% |
| `item:durability:-24` | 耐久度 -24 | 11 | 1.1% |
| `item:durability:-45` | 耐久度 -45 | 11 | 1.1% |
| `item:strength:+5` | 力量需求 +5 | 11 | 1.1% |
| `item:agility:+12` | 技巧需求 +12 | 10 | 1.0% |
| `item:defence:+15` | 防御需求 +15 | 10 | 1.0% |
| `item:durability:-31` | 耐久度 -31 | 10 | 1.0% |
| `item:durability:-47` | 耐久度 -47 | 10 | 1.0% |
| `item:durability:-59` | 耐久度 -59 | 10 | 1.0% |
| `item:durability:-79` | 耐久度 -79 | 10 | 1.0% |
| `item:strength:+12` | 力量需求 +12 | 10 | 1.0% |
| `item:agility:+15` | 技巧需求 +15 | 9 | 0.9% |
| `item:dexterity:+12` | 敏捷需求 +12 | 9 | 0.9% |
| `item:durability:-110` | 耐久度 -110 | 9 | 0.9% |
| `item:durability:-44` | 耐久度 -44 | 9 | 0.9% |
| `item:durability:-90` | 耐久度 -90 | 9 | 0.9% |
| `item:intelligence:+15` | 智力需求 +15 | 9 | 0.9% |
| `item:intelligence:+20` | 智力需求 +20 | 9 | 0.9% |
| `item:strength:+6` | 力量需求 +6 | 9 | 0.9% |
| `item:agility:+20` | 技巧需求 +20 | 8 | 0.8% |
| `item:durability:-115` | 耐久度 -115 | 8 | 0.8% |
| `item:durability:-150` | 耐久度 -150 | 8 | 0.8% |
| `item:durability:-160` | 耐久度 -160 | 8 | 0.8% |
| `item:durability:-30` | 耐久度 -30 | 8 | 0.8% |
| `item:durability:-37` | 耐久度 -37 | 8 | 0.8% |
| `item:durability:-42` | 耐久度 -42 | 8 | 0.8% |
| `item:durability:-49` | 耐久度 -49 | 8 | 0.8% |
| `item:durability:-51` | 耐久度 -51 | 8 | 0.8% |
| `item:durability:-56` | 耐久度 -56 | 8 | 0.8% |
| `item:durability:-58` | 耐久度 -58 | 8 | 0.8% |
| `item:durability:-80` | 耐久度 -80 | 8 | 0.8% |
| `item:durability:-98` | 耐久度 -98 | 8 | 0.8% |
| `item:agility:+8` | 技巧需求 +8 | 7 | 0.7% |
| `item:defence:+14` | 防御需求 +14 | 7 | 0.7% |
| `item:defence:+30` | 防御需求 +30 | 7 | 0.7% |
| `item:dexterity:+8` | 敏捷需求 +8 | 7 | 0.7% |
| `item:durability:-100` | 耐久度 -100 | 7 | 0.7% |
| `item:durability:-149` | 耐久度 -149 | 7 | 0.7% |
| `item:durability:-17` | 耐久度 -17 | 7 | 0.7% |
| `item:durability:-33` | 耐久度 -33 | 7 | 0.7% |
| `item:durability:-54` | 耐久度 -54 | 7 | 0.7% |
| `item:durability:-63` | 耐久度 -63 | 7 | 0.7% |
| `item:durability:-65` | 耐久度 -65 | 7 | 0.7% |
| `item:defence:+16` | 防御需求 +16 | 6 | 0.6% |
| `item:defence:+4` | 防御需求 +4 | 6 | 0.6% |
| `item:defence:+5` | 防御需求 +5 | 6 | 0.6% |
| `item:defence:-10` | 防御需求 -10 | 6 | 0.6% |
| `item:dexterity:+20` | 敏捷需求 +20 | 6 | 0.6% |
| `item:dexterity:+6` | 敏捷需求 +6 | 6 | 0.6% |
| `item:durability:-122` | 耐久度 -122 | 6 | 0.6% |
| `item:durability:-23` | 耐久度 -23 | 6 | 0.6% |
| `item:durability:-50` | 耐久度 -50 | 6 | 0.6% |
| `item:durability:-60` | 耐久度 -60 | 6 | 0.6% |
| `item:durability:-66` | 耐久度 -66 | 6 | 0.6% |
| `item:durability:-75` | 耐久度 -75 | 6 | 0.6% |
| `item:durability:-78` | 耐久度 -78 | 6 | 0.6% |
| `item:durability:-88` | 耐久度 -88 | 6 | 0.6% |
| `item:intelligence:+8` | 智力需求 +8 | 6 | 0.6% |
| `item:strength:+15` | 力量需求 +15 | 6 | 0.6% |
| `item:strength:+18` | 力量需求 +18 | 6 | 0.6% |
| `item:defence:+18` | 防御需求 +18 | 5 | 0.5% |
| `item:defence:+20` | 防御需求 +20 | 5 | 0.5% |
| `item:defence:+25` | 防御需求 +25 | 5 | 0.5% |
| `item:dexterity:+14` | 敏捷需求 +14 | 5 | 0.5% |
| `item:dexterity:+15` | 敏捷需求 +15 | 5 | 0.5% |
| `item:dexterity:+5` | 敏捷需求 +5 | 5 | 0.5% |
| `item:dexterity:+7` | 敏捷需求 +7 | 5 | 0.5% |
| `item:dexterity:+9` | 敏捷需求 +9 | 5 | 0.5% |
| `item:durability:-112` | 耐久度 -112 | 5 | 0.5% |
| `item:durability:-120` | 耐久度 -120 | 5 | 0.5% |
| `item:durability:-53` | 耐久度 -53 | 5 | 0.5% |
| `item:durability:-73` | 耐久度 -73 | 5 | 0.5% |
| `item:durability:-86` | 耐久度 -86 | 5 | 0.5% |
| `item:durability:-94` | 耐久度 -94 | 5 | 0.5% |
| `item:durability:-99` | 耐久度 -99 | 5 | 0.5% |
| `item:intelligence:+25` | 智力需求 +25 | 5 | 0.5% |
| `item:intelligence:+30` | 智力需求 +30 | 5 | 0.5% |
| `item:intelligence:+5` | 智力需求 +5 | 5 | 0.5% |
| `item:strength:+25` | 力量需求 +25 | 5 | 0.5% |
| `item:strength:-10` | 力量需求 -10 | 5 | 0.5% |
| `item:agility:-10` | 技巧需求 -10 | 4 | 0.4% |
| `item:dexterity:+30` | 敏捷需求 +30 | 4 | 0.4% |
| `item:durability:-124` | 耐久度 -124 | 4 | 0.4% |
| `item:durability:-125` | 耐久度 -125 | 4 | 0.4% |
| `item:durability:-131` | 耐久度 -131 | 4 | 0.4% |
| `item:durability:-135` | 耐久度 -135 | 4 | 0.4% |
| `item:durability:-140` | 耐久度 -140 | 4 | 0.4% |
| `item:durability:-145` | 耐久度 -145 | 4 | 0.4% |
| `item:durability:-175` | 耐久度 -175 | 4 | 0.4% |
| `item:durability:-61` | 耐久度 -61 | 4 | 0.4% |
| `item:durability:-71` | 耐久度 -71 | 4 | 0.4% |
| `item:durability:-74` | 耐久度 -74 | 4 | 0.4% |
| `item:durability:-77` | 耐久度 -77 | 4 | 0.4% |
| `item:durability:-85` | 耐久度 -85 | 4 | 0.4% |
| `item:strength:+13` | 力量需求 +13 | 4 | 0.4% |
| `item:agility:+4` | 技巧需求 +4 | 3 | 0.3% |
| `item:agility:+5` | 技巧需求 +5 | 3 | 0.3% |
| `item:agility:+7` | 技巧需求 +7 | 3 | 0.3% |
| `item:defence:+35` | 防御需求 +35 | 3 | 0.3% |
| `item:defence:-25` | 防御需求 -25 | 3 | 0.3% |
| `item:defence:-5` | 防御需求 -5 | 3 | 0.3% |
| `item:dexterity:+16` | 敏捷需求 +16 | 3 | 0.3% |
| `item:dexterity:-10` | 敏捷需求 -10 | 3 | 0.3% |
| `item:durability:+56` | 耐久度 +56 | 3 | 0.3% |
| `item:durability:-101` | 耐久度 -101 | 3 | 0.3% |
| `item:durability:-107` | 耐久度 -107 | 3 | 0.3% |
| `item:durability:-108` | 耐久度 -108 | 3 | 0.3% |
| `item:durability:-109` | 耐久度 -109 | 3 | 0.3% |
| `item:durability:-119` | 耐久度 -119 | 3 | 0.3% |
| `item:durability:-126` | 耐久度 -126 | 3 | 0.3% |
| `item:durability:-154` | 耐久度 -154 | 3 | 0.3% |
| `item:durability:-157` | 耐久度 -157 | 3 | 0.3% |
| `item:durability:-165` | 耐久度 -165 | 3 | 0.3% |
| `item:durability:-172` | 耐久度 -172 | 3 | 0.3% |
| `item:durability:-19` | 耐久度 -19 | 3 | 0.3% |
| `item:durability:-28` | 耐久度 -28 | 3 | 0.3% |
| `item:durability:-34` | 耐久度 -34 | 3 | 0.3% |
| `item:durability:-39` | 耐久度 -39 | 3 | 0.3% |
| `item:durability:-62` | 耐久度 -62 | 3 | 0.3% |
| `item:durability:-68` | 耐久度 -68 | 3 | 0.3% |
| `item:durability:-76` | 耐久度 -76 | 3 | 0.3% |
| `item:durability:-89` | 耐久度 -89 | 3 | 0.3% |
| `item:durability:-92` | 耐久度 -92 | 3 | 0.3% |
| `item:durability:-96` | 耐久度 -96 | 3 | 0.3% |
| `item:durability:-97` | 耐久度 -97 | 3 | 0.3% |
| `item:intelligence:+18` | 智力需求 +18 | 3 | 0.3% |
| `item:intelligence:-10` | 智力需求 -10 | 3 | 0.3% |
| `item:strength:+14` | 力量需求 +14 | 3 | 0.3% |
| `item:strength:+16` | 力量需求 +16 | 3 | 0.3% |
| `item:strength:+20` | 力量需求 +20 | 3 | 0.3% |
| `item:strength:+30` | 力量需求 +30 | 3 | 0.3% |
| `item:strength:+9` | 力量需求 +9 | 3 | 0.3% |
| `item:strength:-15` | 力量需求 -15 | 3 | 0.3% |
| `item:agility:+14` | 技巧需求 +14 | 2 | 0.2% |
| `item:agility:+16` | 技巧需求 +16 | 2 | 0.2% |
| `item:agility:+22` | 技巧需求 +22 | 2 | 0.2% |
| `item:agility:+25` | 技巧需求 +25 | 2 | 0.2% |
| `item:agility:+30` | 技巧需求 +30 | 2 | 0.2% |
| `item:agility:-17` | 技巧需求 -17 | 2 | 0.2% |
| `item:agility:-5` | 技巧需求 -5 | 2 | 0.2% |
| `item:defence:+6` | 防御需求 +6 | 2 | 0.2% |
| `item:defence:+7` | 防御需求 +7 | 2 | 0.2% |
| `item:dexterity:+25` | 敏捷需求 +25 | 2 | 0.2% |
| `item:dexterity:+4` | 敏捷需求 +4 | 2 | 0.2% |
| `item:dexterity:-5` | 敏捷需求 -5 | 2 | 0.2% |
| `item:durability:+18` | 耐久度 +18 | 2 | 0.2% |
| `item:durability:+21` | 耐久度 +21 | 2 | 0.2% |
| `item:durability:+42` | 耐久度 +42 | 2 | 0.2% |
| `item:durability:+5` | 耐久度 +5 | 2 | 0.2% |
| `item:durability:-104` | 耐久度 -104 | 2 | 0.2% |
| `item:durability:-106` | 耐久度 -106 | 2 | 0.2% |
| `item:durability:-117` | 耐久度 -117 | 2 | 0.2% |
| `item:durability:-130` | 耐久度 -130 | 2 | 0.2% |
| `item:durability:-144` | 耐久度 -144 | 2 | 0.2% |
| `item:durability:-155` | 耐久度 -155 | 2 | 0.2% |
| `item:durability:-156` | 耐久度 -156 | 2 | 0.2% |
| `item:durability:-159` | 耐久度 -159 | 2 | 0.2% |
| `item:durability:-162` | 耐久度 -162 | 2 | 0.2% |
| `item:durability:-163` | 耐久度 -163 | 2 | 0.2% |
| `item:durability:-183` | 耐久度 -183 | 2 | 0.2% |
| `item:durability:-184` | 耐久度 -184 | 2 | 0.2% |
| `item:durability:-55` | 耐久度 -55 | 2 | 0.2% |
| `item:durability:-57` | 耐久度 -57 | 2 | 0.2% |
| `item:durability:-84` | 耐久度 -84 | 2 | 0.2% |
| `item:durability:-91` | 耐久度 -91 | 2 | 0.2% |
| `item:durability:-93` | 耐久度 -93 | 2 | 0.2% |
| `item:durability:-95` | 耐久度 -95 | 2 | 0.2% |
| `item:intelligence:+23` | 智力需求 +23 | 2 | 0.2% |
| `item:intelligence:+4` | 智力需求 +4 | 2 | 0.2% |
| `item:intelligence:+7` | 智力需求 +7 | 2 | 0.2% |
| `item:intelligence:-15` | 智力需求 -15 | 2 | 0.2% |
| `item:intelligence:-25` | 智力需求 -25 | 2 | 0.2% |
| `item:strength:+22` | 力量需求 +22 | 2 | 0.2% |
| `item:strength:+24` | 力量需求 +24 | 2 | 0.2% |
| `item:strength:+4` | 力量需求 +4 | 2 | 0.2% |
| `item:strength:-5` | 力量需求 -5 | 2 | 0.2% |
| `item:agility:+11` | 技巧需求 +11 | 1 | 0.1% |
| `item:agility:+13` | 技巧需求 +13 | 1 | 0.1% |
| `item:agility:+18` | 技巧需求 +18 | 1 | 0.1% |
| `item:agility:+23` | 技巧需求 +23 | 1 | 0.1% |
| `item:agility:+24` | 技巧需求 +24 | 1 | 0.1% |
| `item:agility:+3` | 技巧需求 +3 | 1 | 0.1% |
| `item:agility:+35` | 技巧需求 +35 | 1 | 0.1% |
| `item:agility:+6` | 技巧需求 +6 | 1 | 0.1% |
| `item:agility:-15` | 技巧需求 -15 | 1 | 0.1% |
| `item:agility:-20` | 技巧需求 -20 | 1 | 0.1% |
| `item:agility:-25` | 技巧需求 -25 | 1 | 0.1% |
| `item:agility:-35` | 技巧需求 -35 | 1 | 0.1% |
| `item:agility:-8` | 技巧需求 -8 | 1 | 0.1% |
| `item:defence:+13` | 防御需求 +13 | 1 | 0.1% |
| `item:defence:+17` | 防御需求 +17 | 1 | 0.1% |
| `item:defence:+19` | 防御需求 +19 | 1 | 0.1% |
| `item:defence:+24` | 防御需求 +24 | 1 | 0.1% |
| `item:defence:+29` | 防御需求 +29 | 1 | 0.1% |
| `item:defence:+3` | 防御需求 +3 | 1 | 0.1% |
| `item:defence:+34` | 防御需求 +34 | 1 | 0.1% |
| `item:defence:+9` | 防御需求 +9 | 1 | 0.1% |
| `item:defence:-17` | 防御需求 -17 | 1 | 0.1% |
| `item:defence:-20` | 防御需求 -20 | 1 | 0.1% |
| `item:defence:-40` | 防御需求 -40 | 1 | 0.1% |
| `item:dexterity:+11` | 敏捷需求 +11 | 1 | 0.1% |
| `item:dexterity:+13` | 敏捷需求 +13 | 1 | 0.1% |
| `item:dexterity:+19` | 敏捷需求 +19 | 1 | 0.1% |
| `item:dexterity:+21` | 敏捷需求 +21 | 1 | 0.1% |
| `item:dexterity:+27` | 敏捷需求 +27 | 1 | 0.1% |
| `item:dexterity:+65` | 敏捷需求 +65 | 1 | 0.1% |
| `item:dexterity:-15` | 敏捷需求 -15 | 1 | 0.1% |
| `item:dexterity:-17` | 敏捷需求 -17 | 1 | 0.1% |
| `item:dexterity:-20` | 敏捷需求 -20 | 1 | 0.1% |
| `item:dexterity:-25` | 敏捷需求 -25 | 1 | 0.1% |
| `item:dexterity:-6` | 敏捷需求 -6 | 1 | 0.1% |
| `item:durability:+22` | 耐久度 +22 | 1 | 0.1% |
| `item:durability:+35` | 耐久度 +35 | 1 | 0.1% |
| `item:durability:+37` | 耐久度 +37 | 1 | 0.1% |
| `item:durability:+39` | 耐久度 +39 | 1 | 0.1% |
| `item:durability:+4` | 耐久度 +4 | 1 | 0.1% |
| `item:durability:+41` | 耐久度 +41 | 1 | 0.1% |
| `item:durability:+45` | 耐久度 +45 | 1 | 0.1% |
| `item:durability:+47` | 耐久度 +47 | 1 | 0.1% |
| `item:durability:+60` | 耐久度 +60 | 1 | 0.1% |
| `item:durability:+63` | 耐久度 +63 | 1 | 0.1% |
| `item:durability:+70` | 耐久度 +70 | 1 | 0.1% |
| `item:durability:+80` | 耐久度 +80 | 1 | 0.1% |
| `item:durability:-102` | 耐久度 -102 | 1 | 0.1% |
| `item:durability:-103` | 耐久度 -103 | 1 | 0.1% |
| `item:durability:-111` | 耐久度 -111 | 1 | 0.1% |
| `item:durability:-114` | 耐久度 -114 | 1 | 0.1% |
| `item:durability:-116` | 耐久度 -116 | 1 | 0.1% |
| `item:durability:-118` | 耐久度 -118 | 1 | 0.1% |
| `item:durability:-121` | 耐久度 -121 | 1 | 0.1% |
| `item:durability:-127` | 耐久度 -127 | 1 | 0.1% |
| `item:durability:-129` | 耐久度 -129 | 1 | 0.1% |
| `item:durability:-133` | 耐久度 -133 | 1 | 0.1% |
| `item:durability:-136` | 耐久度 -136 | 1 | 0.1% |
| `item:durability:-138` | 耐久度 -138 | 1 | 0.1% |
| `item:durability:-139` | 耐久度 -139 | 1 | 0.1% |
| `item:durability:-141` | 耐久度 -141 | 1 | 0.1% |
| `item:durability:-142` | 耐久度 -142 | 1 | 0.1% |
| `item:durability:-148` | 耐久度 -148 | 1 | 0.1% |
| `item:durability:-151` | 耐久度 -151 | 1 | 0.1% |
| `item:durability:-153` | 耐久度 -153 | 1 | 0.1% |
| `item:durability:-158` | 耐久度 -158 | 1 | 0.1% |
| `item:durability:-164` | 耐久度 -164 | 1 | 0.1% |
| `item:durability:-166` | 耐久度 -166 | 1 | 0.1% |
| `item:durability:-169` | 耐久度 -169 | 1 | 0.1% |
| `item:durability:-170` | 耐久度 -170 | 1 | 0.1% |
| `item:durability:-177` | 耐久度 -177 | 1 | 0.1% |
| `item:durability:-179` | 耐久度 -179 | 1 | 0.1% |
| `item:durability:-181` | 耐久度 -181 | 1 | 0.1% |
| `item:durability:-185` | 耐久度 -185 | 1 | 0.1% |
| `item:durability:-187` | 耐久度 -187 | 1 | 0.1% |
| `item:durability:-192` | 耐久度 -192 | 1 | 0.1% |
| `item:durability:-20` | 耐久度 -20 | 1 | 0.1% |
| `item:durability:-22` | 耐久度 -22 | 1 | 0.1% |
| `item:durability:-29` | 耐久度 -29 | 1 | 0.1% |
| `item:durability:-36` | 耐久度 -36 | 1 | 0.1% |
| `item:durability:-46` | 耐久度 -46 | 1 | 0.1% |
| `item:durability:-48` | 耐久度 -48 | 1 | 0.1% |
| `item:durability:-64` | 耐久度 -64 | 1 | 0.1% |
| `item:durability:-67` | 耐久度 -67 | 1 | 0.1% |
| `item:durability:-69` | 耐久度 -69 | 1 | 0.1% |
| `item:durability:-72` | 耐久度 -72 | 1 | 0.1% |
| `item:durability:-81` | 耐久度 -81 | 1 | 0.1% |
| `item:durability:-82` | 耐久度 -82 | 1 | 0.1% |
| `item:durability:-83` | 耐久度 -83 | 1 | 0.1% |
| `item:durability:-9` | 耐久度 -9 | 1 | 0.1% |
| `item:intelligence:+13` | 智力需求 +13 | 1 | 0.1% |
| `item:intelligence:+14` | 智力需求 +14 | 1 | 0.1% |
| `item:intelligence:+16` | 智力需求 +16 | 1 | 0.1% |
| `item:intelligence:+28` | 智力需求 +28 | 1 | 0.1% |
| `item:intelligence:+3` | 智力需求 +3 | 1 | 0.1% |
| `item:intelligence:+35` | 智力需求 +35 | 1 | 0.1% |
| `item:intelligence:+37` | 智力需求 +37 | 1 | 0.1% |
| `item:intelligence:+40` | 智力需求 +40 | 1 | 0.1% |
| `item:intelligence:+6` | 智力需求 +6 | 1 | 0.1% |
| `item:intelligence:+9` | 智力需求 +9 | 1 | 0.1% |
| `item:intelligence:-11` | 智力需求 -11 | 1 | 0.1% |
| `item:intelligence:-12` | 智力需求 -12 | 1 | 0.1% |
| `item:intelligence:-20` | 智力需求 -20 | 1 | 0.1% |
| `item:strength:+11` | 力量需求 +11 | 1 | 0.1% |
| `item:strength:+17` | 力量需求 +17 | 1 | 0.1% |
| `item:strength:+21` | 力量需求 +21 | 1 | 0.1% |
| `item:strength:+28` | 力量需求 +28 | 1 | 0.1% |
| `item:strength:+3` | 力量需求 +3 | 1 | 0.1% |
| `item:strength:+35` | 力量需求 +35 | 1 | 0.1% |
| `item:strength:+38` | 力量需求 +38 | 1 | 0.1% |
| `item:strength:+7` | 力量需求 +7 | 1 | 0.1% |
| `item:strength:-13` | 力量需求 -13 | 1 | 0.1% |
| `item:strength:-25` | 力量需求 -25 | 1 | 0.1% |

## 消耗品属性（consumable）

> 只作用于消耗品(卷轴/药水)的属性，格式 consumable:属性:数值

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `consumable:duration:-120` | 持续时间 -120 | 20 | 2.1% |
| `consumable:duration:-100` | 持续时间 -100 | 12 | 1.2% |
| `consumable:duration:-140` | 持续时间 -140 | 12 | 1.2% |
| `consumable:duration:-160` | 持续时间 -160 | 11 | 1.1% |
| `consumable:duration:-190` | 持续时间 -190 | 11 | 1.1% |
| `consumable:duration:-110` | 持续时间 -110 | 10 | 1.0% |
| `consumable:duration:-210` | 持续时间 -210 | 10 | 1.0% |
| `consumable:duration:-300` | 持续时间 -300 | 10 | 1.0% |
| `consumable:duration:-180` | 持续时间 -180 | 9 | 0.9% |
| `consumable:charges:+1` | 使用次数 +1 | 8 | 0.8% |
| `consumable:duration:-130` | 持续时间 -130 | 8 | 0.8% |
| `consumable:duration:-150` | 持续时间 -150 | 8 | 0.8% |
| `consumable:duration:-170` | 持续时间 -170 | 8 | 0.8% |
| `consumable:duration:-200` | 持续时间 -200 | 8 | 0.8% |
| `consumable:duration:-220` | 持续时间 -220 | 8 | 0.8% |
| `consumable:duration:-400` | 持续时间 -400 | 8 | 0.8% |
| `consumable:duration:-60` | 持续时间 -60 | 7 | 0.7% |
| `consumable:duration:-90` | 持续时间 -90 | 7 | 0.7% |
| `consumable:duration:-270` | 持续时间 -270 | 6 | 0.6% |
| `consumable:duration:-350` | 持续时间 -350 | 6 | 0.6% |
| `consumable:duration:-70` | 持续时间 -70 | 6 | 0.6% |
| `consumable:duration:-48` | 持续时间 -48 | 5 | 0.5% |
| `consumable:duration:-78` | 持续时间 -78 | 5 | 0.5% |
| `consumable:charges:+2` | 使用次数 +2 | 4 | 0.4% |
| `consumable:charges:-1` | 使用次数 -1 | 4 | 0.4% |
| `consumable:duration:+90` | 持续时间 +90 | 4 | 0.4% |
| `consumable:duration:-115` | 持续时间 -115 | 4 | 0.4% |
| `consumable:duration:-230` | 持续时间 -230 | 4 | 0.4% |
| `consumable:duration:-240` | 持续时间 -240 | 4 | 0.4% |
| `consumable:duration:-250` | 持续时间 -250 | 4 | 0.4% |
| `consumable:duration:-280` | 持续时间 -280 | 4 | 0.4% |
| `consumable:duration:-360` | 持续时间 -360 | 4 | 0.4% |
| `consumable:duration:-54` | 持续时间 -54 | 4 | 0.4% |
| `consumable:duration:-84` | 持续时间 -84 | 4 | 0.4% |
| `consumable:duration:-99` | 持续时间 -99 | 4 | 0.4% |
| `consumable:duration:+120` | 持续时间 +120 | 3 | 0.3% |
| `consumable:duration:-165` | 持续时间 -165 | 3 | 0.3% |
| `consumable:duration:-225` | 持续时间 -225 | 3 | 0.3% |
| `consumable:duration:-260` | 持续时间 -260 | 3 | 0.3% |
| `consumable:duration:-310` | 持续时间 -310 | 3 | 0.3% |
| `consumable:duration:-315` | 持续时间 -315 | 3 | 0.3% |
| `consumable:duration:-36` | 持续时间 -36 | 3 | 0.3% |
| `consumable:duration:-38` | 持续时间 -38 | 3 | 0.3% |
| `consumable:duration:-380` | 持续时间 -380 | 3 | 0.3% |
| `consumable:duration:-410` | 持续时间 -410 | 3 | 0.3% |
| `consumable:duration:-45` | 持续时间 -45 | 3 | 0.3% |
| `consumable:duration:-550` | 持续时间 -550 | 3 | 0.3% |
| `consumable:duration:-620` | 持续时间 -620 | 3 | 0.3% |
| `consumable:duration:-80` | 持续时间 -80 | 3 | 0.3% |
| `consumable:duration:-93` | 持续时间 -93 | 3 | 0.3% |
| `consumable:duration:+200` | 持续时间 +200 | 2 | 0.2% |
| `consumable:duration:+30` | 持续时间 +30 | 2 | 0.2% |
| `consumable:duration:+40` | 持续时间 +40 | 2 | 0.2% |
| `consumable:duration:+60` | 持续时间 +60 | 2 | 0.2% |
| `consumable:duration:-101` | 持续时间 -101 | 2 | 0.2% |
| `consumable:duration:-290` | 持续时间 -290 | 2 | 0.2% |
| `consumable:duration:-320` | 持续时间 -320 | 2 | 0.2% |
| `consumable:duration:-325` | 持续时间 -325 | 2 | 0.2% |
| `consumable:duration:-330` | 持续时间 -330 | 2 | 0.2% |
| `consumable:duration:-370` | 持续时间 -370 | 2 | 0.2% |
| `consumable:duration:-40` | 持续时间 -40 | 2 | 0.2% |
| `consumable:duration:-460` | 持续时间 -460 | 2 | 0.2% |
| `consumable:duration:-490` | 持续时间 -490 | 2 | 0.2% |
| `consumable:duration:-560` | 持续时间 -560 | 2 | 0.2% |
| `consumable:duration:-600` | 持续时间 -600 | 2 | 0.2% |
| `consumable:duration:-66` | 持续时间 -66 | 2 | 0.2% |
| `consumable:duration:-69` | 持续时间 -69 | 2 | 0.2% |
| `consumable:duration:-720` | 持续时间 -720 | 2 | 0.2% |
| `consumable:duration:-75` | 持续时间 -75 | 2 | 0.2% |
| `consumable:duration:-95` | 持续时间 -95 | 2 | 0.2% |
| `consumable:duration:-97` | 持续时间 -97 | 2 | 0.2% |
| `consumable:duration:+100` | 持续时间 +100 | 1 | 0.1% |
| `consumable:duration:+110` | 持续时间 +110 | 1 | 0.1% |
| `consumable:duration:+125` | 持续时间 +125 | 1 | 0.1% |
| `consumable:duration:+15` | 持续时间 +15 | 1 | 0.1% |
| `consumable:duration:+160` | 持续时间 +160 | 1 | 0.1% |
| `consumable:duration:+24` | 持续时间 +24 | 1 | 0.1% |
| `consumable:duration:+280` | 持续时间 +280 | 1 | 0.1% |
| `consumable:duration:+360` | 持续时间 +360 | 1 | 0.1% |
| `consumable:duration:+370` | 持续时间 +370 | 1 | 0.1% |
| `consumable:duration:+380` | 持续时间 +380 | 1 | 0.1% |
| `consumable:duration:+400` | 持续时间 +400 | 1 | 0.1% |
| `consumable:duration:+45` | 持续时间 +45 | 1 | 0.1% |
| `consumable:duration:+48` | 持续时间 +48 | 1 | 0.1% |
| `consumable:duration:+75` | 持续时间 +75 | 1 | 0.1% |
| `consumable:duration:+96` | 持续时间 +96 | 1 | 0.1% |
| `consumable:duration:-10` | 持续时间 -10 | 1 | 0.1% |
| `consumable:duration:-103` | 持续时间 -103 | 1 | 0.1% |
| `consumable:duration:-105` | 持续时间 -105 | 1 | 0.1% |
| `consumable:duration:-1100` | 持续时间 -1100 | 1 | 0.1% |
| `consumable:duration:-125` | 持续时间 -125 | 1 | 0.1% |
| `consumable:duration:-135` | 持续时间 -135 | 1 | 0.1% |
| `consumable:duration:-141` | 持续时间 -141 | 1 | 0.1% |
| `consumable:duration:-144` | 持续时间 -144 | 1 | 0.1% |
| `consumable:duration:-145` | 持续时间 -145 | 1 | 0.1% |
| `consumable:duration:-155` | 持续时间 -155 | 1 | 0.1% |
| `consumable:duration:-181` | 持续时间 -181 | 1 | 0.1% |
| `consumable:duration:-185` | 持续时间 -185 | 1 | 0.1% |
| `consumable:duration:-195` | 持续时间 -195 | 1 | 0.1% |
| `consumable:duration:-235` | 持续时间 -235 | 1 | 0.1% |
| `consumable:duration:-252` | 持续时间 -252 | 1 | 0.1% |
| `consumable:duration:-275` | 持续时间 -275 | 1 | 0.1% |
| `consumable:duration:-305` | 持续时间 -305 | 1 | 0.1% |
| `consumable:duration:-340` | 持续时间 -340 | 1 | 0.1% |
| `consumable:duration:-365` | 持续时间 -365 | 1 | 0.1% |
| `consumable:duration:-39` | 持续时间 -39 | 1 | 0.1% |
| `consumable:duration:-390` | 持续时间 -390 | 1 | 0.1% |
| `consumable:duration:-425` | 持续时间 -425 | 1 | 0.1% |
| `consumable:duration:-440` | 持续时间 -440 | 1 | 0.1% |
| `consumable:duration:-450` | 持续时间 -450 | 1 | 0.1% |
| `consumable:duration:-50` | 持续时间 -50 | 1 | 0.1% |
| `consumable:duration:-51` | 持续时间 -51 | 1 | 0.1% |
| `consumable:duration:-520` | 持续时间 -520 | 1 | 0.1% |
| `consumable:duration:-540` | 持续时间 -540 | 1 | 0.1% |
| `consumable:duration:-57` | 持续时间 -57 | 1 | 0.1% |
| `consumable:duration:-580` | 持续时间 -580 | 1 | 0.1% |
| `consumable:duration:-590` | 持续时间 -590 | 1 | 0.1% |
| `consumable:duration:-63` | 持续时间 -63 | 1 | 0.1% |
| `consumable:duration:-660` | 持续时间 -660 | 1 | 0.1% |
| `consumable:duration:-666` | 持续时间 -666 | 1 | 0.1% |
| `consumable:duration:-67` | 持续时间 -67 | 1 | 0.1% |
| `consumable:duration:-670` | 持续时间 -670 | 1 | 0.1% |
| `consumable:duration:-690` | 持续时间 -690 | 1 | 0.1% |
| `consumable:duration:-700` | 持续时间 -700 | 1 | 0.1% |
| `consumable:duration:-740` | 持续时间 -740 | 1 | 0.1% |
| `consumable:duration:-750` | 持续时间 -750 | 1 | 0.1% |
| `consumable:duration:-77` | 持续时间 -77 | 1 | 0.1% |
| `consumable:duration:-770` | 持续时间 -770 | 1 | 0.1% |
| `consumable:duration:-800` | 持续时间 -800 | 1 | 0.1% |
| `consumable:duration:-81` | 持续时间 -81 | 1 | 0.1% |
| `consumable:duration:-820` | 持续时间 -820 | 1 | 0.1% |
| `consumable:duration:-85` | 持续时间 -85 | 1 | 0.1% |
| `consumable:duration:-87` | 持续时间 -87 | 1 | 0.1% |
| `consumable:duration:-900` | 持续时间 -900 | 1 | 0.1% |
| `consumable:duration:-94` | 持续时间 -94 | 1 | 0.1% |
| `consumable:duration:-945` | 持续时间 -945 | 1 | 0.1% |
| `consumable:duration:-96` | 持续时间 -96 | 1 | 0.1% |
| `consumable:duration:-98` | 持续时间 -98 | 1 | 0.1% |

## 相邻加成（position）

> 配方格相对位置的效果加成(%)，格式 position:位置:数值

| 标签 | 含义 | 物品数 | 占比 |
| --- | --- | ---: | ---: |
| `position:touching:+25` | 相邻 位置加成 +25% | 5 | 0.5% |
| `position:touching:+15` | 相邻 位置加成 +15% | 4 | 0.4% |
| `position:left:-160` | 左侧 位置加成 -160% | 3 | 0.3% |
| `position:not_touching:+15` | 不相邻 位置加成 +15% | 3 | 0.3% |
| `position:above:-160` | 上方 位置加成 -160% | 2 | 0.2% |
| `position:not_touching:-15` | 不相邻 位置加成 -15% | 2 | 0.2% |
| `position:not_touching:-40` | 不相邻 位置加成 -40% | 2 | 0.2% |
| `position:right:-160` | 右侧 位置加成 -160% | 2 | 0.2% |
| `position:touching:+120` | 相邻 位置加成 +120% | 2 | 0.2% |
| `position:touching:+20` | 相邻 位置加成 +20% | 2 | 0.2% |
| `position:touching:+50` | 相邻 位置加成 +50% | 2 | 0.2% |
| `position:touching:-110` | 相邻 位置加成 -110% | 2 | 0.2% |
| `position:touching:-40` | 相邻 位置加成 -40% | 2 | 0.2% |
| `position:touching:-50` | 相邻 位置加成 -50% | 2 | 0.2% |
| `position:above:+110` | 上方 位置加成 +110% | 1 | 0.1% |
| `position:above:+115` | 上方 位置加成 +115% | 1 | 0.1% |
| `position:above:+25` | 上方 位置加成 +25% | 1 | 0.1% |
| `position:above:+55` | 上方 位置加成 +55% | 1 | 0.1% |
| `position:above:+60` | 上方 位置加成 +60% | 1 | 0.1% |
| `position:above:+80` | 上方 位置加成 +80% | 1 | 0.1% |
| `position:above:-100` | 上方 位置加成 -100% | 1 | 0.1% |
| `position:above:-110` | 上方 位置加成 -110% | 1 | 0.1% |
| `position:above:-120` | 上方 位置加成 -120% | 1 | 0.1% |
| `position:above:-25` | 上方 位置加成 -25% | 1 | 0.1% |
| `position:above:-40` | 上方 位置加成 -40% | 1 | 0.1% |
| `position:above:-47` | 上方 位置加成 -47% | 1 | 0.1% |
| `position:above:-75` | 上方 位置加成 -75% | 1 | 0.1% |
| `position:left:+110` | 左侧 位置加成 +110% | 1 | 0.1% |
| `position:left:+130` | 左侧 位置加成 +130% | 1 | 0.1% |
| `position:left:+30` | 左侧 位置加成 +30% | 1 | 0.1% |
| `position:left:+85` | 左侧 位置加成 +85% | 1 | 0.1% |
| `position:left:-100` | 左侧 位置加成 -100% | 1 | 0.1% |
| `position:left:-120` | 左侧 位置加成 -120% | 1 | 0.1% |
| `position:left:-122` | 左侧 位置加成 -122% | 1 | 0.1% |
| `position:left:-15` | 左侧 位置加成 -15% | 1 | 0.1% |
| `position:left:-150` | 左侧 位置加成 -150% | 1 | 0.1% |
| `position:left:-200` | 左侧 位置加成 -200% | 1 | 0.1% |
| `position:left:-30` | 左侧 位置加成 -30% | 1 | 0.1% |
| `position:left:-40` | 左侧 位置加成 -40% | 1 | 0.1% |
| `position:left:-47` | 左侧 位置加成 -47% | 1 | 0.1% |
| `position:left:-50` | 左侧 位置加成 -50% | 1 | 0.1% |
| `position:left:-53` | 左侧 位置加成 -53% | 1 | 0.1% |
| `position:left:-60` | 左侧 位置加成 -60% | 1 | 0.1% |
| `position:not_touching:+10` | 不相邻 位置加成 +10% | 1 | 0.1% |
| `position:not_touching:+115` | 不相邻 位置加成 +115% | 1 | 0.1% |
| `position:not_touching:+25` | 不相邻 位置加成 +25% | 1 | 0.1% |
| `position:not_touching:+30` | 不相邻 位置加成 +30% | 1 | 0.1% |
| `position:not_touching:+50` | 不相邻 位置加成 +50% | 1 | 0.1% |
| `position:not_touching:+55` | 不相邻 位置加成 +55% | 1 | 0.1% |
| `position:not_touching:+60` | 不相邻 位置加成 +60% | 1 | 0.1% |
| `position:not_touching:-100` | 不相邻 位置加成 -100% | 1 | 0.1% |
| `position:not_touching:-25` | 不相邻 位置加成 -25% | 1 | 0.1% |
| `position:not_touching:-30` | 不相邻 位置加成 -30% | 1 | 0.1% |
| `position:not_touching:-35` | 不相邻 位置加成 -35% | 1 | 0.1% |
| `position:not_touching:-65` | 不相邻 位置加成 -65% | 1 | 0.1% |
| `position:not_touching:-80` | 不相邻 位置加成 -80% | 1 | 0.1% |
| `position:right:+110` | 右侧 位置加成 +110% | 1 | 0.1% |
| `position:right:+140` | 右侧 位置加成 +140% | 1 | 0.1% |
| `position:right:+30` | 右侧 位置加成 +30% | 1 | 0.1% |
| `position:right:+85` | 右侧 位置加成 +85% | 1 | 0.1% |
| `position:right:-100` | 右侧 位置加成 -100% | 1 | 0.1% |
| `position:right:-122` | 右侧 位置加成 -122% | 1 | 0.1% |
| `position:right:-150` | 右侧 位置加成 -150% | 1 | 0.1% |
| `position:right:-180` | 右侧 位置加成 -180% | 1 | 0.1% |
| `position:right:-30` | 右侧 位置加成 -30% | 1 | 0.1% |
| `position:right:-40` | 右侧 位置加成 -40% | 1 | 0.1% |
| `position:right:-47` | 右侧 位置加成 -47% | 1 | 0.1% |
| `position:right:-50` | 右侧 位置加成 -50% | 1 | 0.1% |
| `position:right:-53` | 右侧 位置加成 -53% | 1 | 0.1% |
| `position:right:-60` | 右侧 位置加成 -60% | 1 | 0.1% |
| `position:touching:+115` | 相邻 位置加成 +115% | 1 | 0.1% |
| `position:touching:+30` | 相邻 位置加成 +30% | 1 | 0.1% |
| `position:touching:+35` | 相邻 位置加成 +35% | 1 | 0.1% |
| `position:touching:+47` | 相邻 位置加成 +47% | 1 | 0.1% |
| `position:touching:+53` | 相邻 位置加成 +53% | 1 | 0.1% |
| `position:touching:-1` | 相邻 位置加成 -1% | 1 | 0.1% |
| `position:touching:-10` | 相邻 位置加成 -10% | 1 | 0.1% |
| `position:touching:-100` | 相邻 位置加成 -100% | 1 | 0.1% |
| `position:touching:-115` | 相邻 位置加成 -115% | 1 | 0.1% |
| `position:touching:-15` | 相邻 位置加成 -15% | 1 | 0.1% |
| `position:touching:-25` | 相邻 位置加成 -25% | 1 | 0.1% |
| `position:touching:-80` | 相邻 位置加成 -80% | 1 | 0.1% |
| `position:under:+110` | 下方 位置加成 +110% | 1 | 0.1% |
| `position:under:+115` | 下方 位置加成 +115% | 1 | 0.1% |
| `position:under:+25` | 下方 位置加成 +25% | 1 | 0.1% |
| `position:under:+55` | 下方 位置加成 +55% | 1 | 0.1% |
| `position:under:+60` | 下方 位置加成 +60% | 1 | 0.1% |
| `position:under:+80` | 下方 位置加成 +80% | 1 | 0.1% |
| `position:under:-100` | 下方 位置加成 -100% | 1 | 0.1% |
| `position:under:-120` | 下方 位置加成 -120% | 1 | 0.1% |
| `position:under:-160` | 下方 位置加成 -160% | 1 | 0.1% |
| `position:under:-20` | 下方 位置加成 -20% | 1 | 0.1% |
| `position:under:-25` | 下方 位置加成 -25% | 1 | 0.1% |
| `position:under:-40` | 下方 位置加成 -40% | 1 | 0.1% |
| `position:under:-53` | 下方 位置加成 -53% | 1 | 0.1% |
| `position:under:-75` | 下方 位置加成 -75% | 1 | 0.1% |
