#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财报排雷大师
扫雷类游戏，但扫的是财报里的地雷。
找出的雷越多，赚钱的概率越大。
一款游戏让你学会识别A股财报里的经典造假套路。
"""

import random
import os

C_RED    = "\033[91m"
C_GREEN  = "\033[92m"
C_YELLOW = "\033[93m"
C_CYAN   = "\033[96m"
C_WHITE  = "\033[97m"
C_BOLD   = "\033[1m"
C_RESET  = "\033[0m"
C_DIM    = "\033[2m"
C_MAGENTA= "\033[95m"

GRID_W = 16
GRID_H = 10

# 财报项目（格子的内容）
ITEMS = [
    ("应收账款", "大幅增长，应收账款远超营收增速"),
    ("存货周转", "明显下降，存货积压严重"),
    ("经营现金流", "多年为负，靠借钱维持"),
    ("商誉", "商誉占净资产超50%"),
    ("毛利率", "远高于同行，可能造假"),
    ("关联交易", "频繁与关联方交易，利益输送"),
    ("研发费用", "研发支出大幅资本化，虚增利润"),
    ("销售收入", "集中在少数客户，回款困难"),
    ("固定资产", "在建工程迟迟不转固，折旧虚减"),
    ("银行借款", "账面有大量现金，却借更多债"),
    ("审计意见", "非标审计意见，风险提示"),
    ("更换会计所", "频繁更换会计师事务所"),
    ("股权质押", "大股东高比例质押，动机存疑"),
    ("存货", "存货增长远超营收，积压严重"),
    ("预付款项", "大额预付给关联方，输送嫌疑"),
    ("政府补助", "利润严重依赖政府补助"),
    ("应收账款周转", "周转天数明显延长"),
    ("毛利率波动", "毛利率异常稳定，疑似调节"),
]

MINES = [
    ("🔴 应收账款地雷", "公司通过虚构销售合同、提前确认收入等方式虚增应收账款，最终形成坏账"),
    ("🔴 存货地雷", "实际已滞销的产品仍按成本计价，计提跌价准备严重不足"),
    ("🔴 现金流地雷", "经营现金流持续为负，靠非经常性损益和融资维持账面盈利"),
    ("🔴 商誉地雷", "高溢价收购形成的商誉，一旦标的业绩不达标直接计提减值，当年巨亏"),
    ("🔴 毛利率地雷", "远高于同行的毛利率，背后可能是虚构业务、关联交易定价"),
    ("🔴 关联交易地雷", "向关联方高价采购低价销售，向大股东输送利益"),
    ("🔴 研发资本化地雷", "研发支出大量资本化而非费用化，虚增当期利润"),
    ("🔴 客户集中地雷", "销售收入依赖少数客户，客户出问题直接导致业绩崩塌"),
    ("🔴 在建工程地雷", "在建工程迟迟不转固，减少折旧，虚增利润"),
    ("🔴 货币资金地雷", "账面大量现金却还要大量借款，可能资金已被冻结或虚构"),
    ("🔴 审计非标地雷", "被出具非标审计意见，说明财报可信度存在重大问题"),
    ("🔴 换会计所地雷", "频繁更换审计机构，往往是为了绕过审计监督"),
    ("🔴 大股东质押地雷", "大股东高比例质押，股价下跌存在控制权变更风险"),
    ("🔴 存货积压地雷", "存货增长远超营收增长，产品已无市场竞争力"),
    ("🔴 预付地雷", "大额预付款项流向关联方，本质是资金占用"),
    ("🔴 政府补助地雷", "利润几乎全靠政府补助，主营业务已无造血能力"),
]

SAFE_ITEMS = [
    ("✓ 营收增长", "与行业增速匹配，实打实的增长"),
    ("✓ 现金流", "经营现金流持续为正，造血能力健康"),
    ("✓ 应收账款", "增速与营收匹配，周转率稳定"),
    ("✓ 毛利率", "与行业水平一致，波动合理"),
    ("✓ 存货周转", "周转正常，不存在积压"),
    ("✓ 资产负债率", "杠杆水平合理，风险可控"),
    ("✓ 研发投入", "费用化比例合理，不存在调节"),
    ("✓ 分红", "持续分红，回报股东"),
    ("✓ 合同负债", "预收款项充足，说明产品竞争力强"),
    ("✓ 审计意见", "标准无保留意见，财报可信"),
]

def clear():
    os.system("clear")

def header():
    print(f"{C_BOLD}{C_CYAN}{'='*(GRID_W*4+5)}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  财报排雷大师  |  踩到地雷=踩雷  |  查看全部=揭开{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'='*(GRID_W*4+5)}{C_RESET}")

def place_mines_and_safe(grid, mine_count):
    """放置地雷和安全项"""
    mines = []
    total_cells = GRID_W * GRID_H
    mine_positions = set()
    safe_positions = set()

    # 先放地雷
    while len(mine_positions) < mine_count:
        pos = random.randint(0, total_cells - 1)
        if pos not in mine_positions:
            mine_positions.add(pos)

    # 放安全项
    while len(safe_positions) < min(10, total_cells - mine_count):
        pos = random.randint(0, total_cells - 1)
        if pos not in mine_positions and pos not in safe_positions:
            safe_positions.add(pos)

    # 放提示项（既不是雷也不是安全的，只是财报项目）
    hints = list(range(total_cells))
    random.shuffle(hints)
    hint_count = total_cells - mine_count - len(safe_positions)

    for i, pos in enumerate(hints[:hint_count]):
        row, col = pos // GRID_W, pos % GRID_W
        item_name, item_desc = random.choice(ITEMS)
        grid[row][col] = {
            'type': 'hint',
            'name': item_name,
            'desc': item_desc,
            'revealed': False,
        }

    for pos in mine_positions:
        row, col = pos // GRID_W, pos % GRID_W
        mine_name, mine_desc = random.choice(MINES)
        grid[row][col] = {
            'type': 'mine',
            'name': mine_name,
            'desc': mine_desc,
            'revealed': False,
        }

    for pos in safe_positions:
        row, col = pos // GRID_W, pos % GRID_W
        safe_name, safe_desc = random.choice(SAFE_ITEMS)
        grid[row][col] = {
            'type': 'safe',
            'name': safe_name,
            'desc': safe_desc,
            'revealed': False,
        }

    return len(mine_positions), len(safe_positions)

def draw_grid(grid, found_mines, flag_grid):
    print()
    # 列号
    print(f"  {C_DIM}    {C_RESET}", end="")
    for c in range(GRID_W):
        print(f"{C_DIM}{c:2d} {C_RESET}", end="")
    print()
    print(f"  {C_BOLD}{C_DIM}{'─'*(GRID_W*4+5)}{C_RESET}")

    for r in range(GRID_H):
        print(f"  {C_DIM}{r:2d}{C_RESET} ", end="")
        for c in range(GRID_W):
            cell = grid[r][c]
            if flag_grid[r][c]:
                print(f"{C_YELLOW}[?]{C_RESET} ", end="")
            elif cell['revealed']:
                if cell['type'] == 'mine':
                    print(f"{C_RED}{C_BOLD}[💥]{C_RESET} ", end="")
                elif cell['type'] == 'safe':
                    print(f"{C_GREEN}{C_BOLD}[✓]{C_RESET} ", end="")
                else:
                    count = count_adjacent_mines(grid, r, c)
                    if count == 0:
                        print(f"{C_WHITE} .  {C_RESET}", end="")
                    else:
                        print(f"{C_YELLOW}[{count}]{C_RESET} ", end="")
            else:
                print(f"{C_CYAN}[▓]{C_RESET} ", end="")
        print(f" {C_DIM}{r:2d}{C_RESET}")
    print()

def count_adjacent_mines(grid, row, col):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_H and 0 <= nc < GRID_W:
                if grid[nr][nc]['type'] == 'mine':
                    count += 1
    return count

def reveal_cell(grid, r, c):
    """揭开格子"""
    if grid[r][c]['revealed']:
        return None, False

    grid[r][c]['revealed'] = True

    if grid[r][c]['type'] == 'mine':
        return grid[r][c], True  # 踩雷了

    if grid[r][c]['type'] == 'safe':
        return grid[r][c], False  # 安全项

    # hint类型：显示提示但不自动展开
    return grid[r][c], False

def reveal_all(grid):
    for r in range(GRID_H):
        for c in range(GRID_W):
            grid[r][c]['revealed'] = True

def auto_detect(grid):
    """智能检测：找出高确信度的地雷"""
    detected = []
    for r in range(GRID_H):
        for c in range(GRID_W):
            cell = grid[r][c]
            if cell['type'] == 'mine' and not cell['revealed']:
                # 检查周围8格是否全是已揭示的非雷格
                adj_revealed = 0
                adj_unknown = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < GRID_H and 0 <= nc < GRID_W:
                            if grid[nr][nc]['revealed'] and grid[nr][nc]['type'] != 'mine':
                                adj_revealed += 1
                            elif not grid[nr][nc]['revealed']:
                                adj_unknown += 1
                if adj_unknown <= 1:
                    detected.append((r, c))
    return detected

def main():
    clear()
    print(f"{C_BOLD}{C_CYAN}{'='*(GRID_W*4+5)}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  财报排雷大师  |  在财报里找出地雷{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'='*(GRID_W*4+5)}{C_RESET}")
    print(f"""
  {C_WHITE}游戏说明：{C_RESET}
  {C_CYAN}[▓]{C_RESET} = 未查看的财报项目（点击查看详情）
  {C_RED}[💥]{C_RESET} = 地雷（财报造假/风险项目，踩到即爆）
  {C_GREEN}[✓]{C_RESET} = 安全项（财务健康信号）
  {C_YELLOW}[数字]{C_RESET} = 周围地雷数量提示
  {C_YELLOW}[?]{C_RESET} = 标记可疑项目

  {C_BOLD}操作：{C_RESET}
  揭开：输入坐标，如 3,5
  标记：输入 f 3,5（如 f 3,5）
  全部揭开：输入 reveal
  智能检测：输入 auto
""")

    input(f"  {C_CYAN}[回车开始排雷]{C_RESET}")

    difficulty = input(f"  难度 (1=简单8雷 2=中等12雷 3=困难15雷): {C_RESET}").strip()
    mine_counts = {'1': 8, '2': 12, '3': 15}
    mine_count = mine_counts.get(difficulty, 10)

    # 初始化
    grid = [[{'type': 'empty', 'revealed': False} for _ in range(GRID_W)] for _ in range(GRID_H)]
    flag_grid = [[False] * GRID_W for _ in range(GRID_H)]
    total_mines, total_safe = place_mines_and_safe(grid, mine_count)
    found_mines = 0
    steps = 0
    game_over = False

    while not game_over:
        clear()
        header()
        print(f"  回合：{steps}  已标雷：{found_mines}/{total_mines}  "
              f"安全项：{sum(1 for r in range(GRID_H) for c in range(GRID_W) if grid[r][c]['type']=='safe' and grid[r][c]['revealed'])}/{total_safe}")
        print()
        draw_grid(grid, found_mines, flag_grid)
        print(f"  {C_DIM}操作：坐标(如3,5) | f+坐标标记(如f 3,5) | reveal全揭 | auto智能检测{C_RESET}")

        if game_over:
            break

        cmd = input(f"  {C_CYAN}> {C_RESET}").strip()

        if cmd == 'reveal':
            reveal_all(grid)
            game_over = True
            break

        if cmd == 'auto':
            detected = auto_detect(grid)
            if detected:
                msg = f"智能检测到 {len(detected)} 个可疑雷区，已标记"
                for r, c in detected:
                    flag_grid[r][c] = True
            else:
                msg = "未检测到确信度足够高的雷区"
            clear()
            header()
            print(f"\n  {C_YELLOW}{msg}{C_RESET}")
            print()
            draw_grid(grid, found_mines, flag_grid)
            input(f"\n  {C_CYAN}[回车继续]{C_RESET}")
            continue

        if cmd.startswith('f '):
            try:
                _, coord = cmd.split()
                r, c = map(int, coord.split(','))
                if 0 <= r < GRID_H and 0 <= c < GRID_W:
                    flag_grid[r][c] = not flag_grid[r][c]
                    found_mines = sum(flag_grid[r][c] for r in range(GRID_H) for c in range(GRID_W))
                    steps += 1
            except:
                pass
            continue

        try:
            r, c = map(int, cmd.split(','))
            if not (0 <= r < GRID_H and 0 <= c < GRID_W):
                continue
            if flag_grid[r][c]:
                continue

            cell, exploded = reveal_cell(grid, r, c)
            steps += 1

            if exploded:
                clear()
                header()
                draw_grid(grid, found_mines, flag_grid)
                print(f"\n  {C_RED}{C_BOLD}💥 踩雷了！！！{C_RESET}")
                print(f"  {C_RED}{cell['name']}{C_RESET}")
                print(f"  {C_WHITE}{cell['desc']}{C_RESET}")
                print(f"\n  {C_DIM}这是A股常见的财报造假/风险手法之一{C_RESET}")
                game_over = True
                input(f"\n  {C_CYAN}[回车结束]{C_RESET}")

            elif cell and cell['type'] == 'safe':
                clear()
                header()
                draw_grid(grid, found_mines, flag_grid)
                print(f"\n  {C_GREEN}✓ 发现安全项：{cell['name']}{C_RESET}")
                print(f"  {C_WHITE}{cell['desc']}{C_RESET}")
                input(f"\n  {C_CYAN}[回车继续]{C_RESET}")

            elif cell and cell['type'] == 'hint':
                clear()
                header()
                draw_grid(grid, found_mines, flag_grid)
                print(f"\n  {C_YELLOW}📋 项目：{cell['name']}{C_RESET}")
                print(f"  {C_WHITE}{cell['desc']}{C_RESET}")
                # 提示周围雷数
                count = count_adjacent_mines(grid, r, c)
                if count > 0:
                    print(f"  {C_YELLOW}周围可能有约 {count} 个雷地雷{C_RESET}")
                else:
                    print(f"  {C_GREEN}周围暂无雷，可以继续探索{C_RESET}")
                input(f"\n  {C_CYAN}[回车继续]{C_RESET}")

            # 检测是否所有雷都找到了
            all_mines_found = all(
                grid[r][c]['revealed'] or grid[r][c]['type'] != 'mine'
                for r in range(GRID_H) for c in range(GRID_W)
            ) and all(
                grid[r][c]['type'] != 'mine' or grid[r][c]['revealed'] or flag_grid[r][c]
                for r in range(GRID_H) for c in range(GRID_W)
            )

            safe_found = sum(1 for r in range(GRID_H) for c in range(GRID_W)
                           if grid[r][c]['type'] == 'safe' and grid[r][c]['revealed'])
            if safe_found == total_safe:
                clear()
                header()
                print(f"\n  {C_GREEN}{C_BOLD}🎉 全部安全项已找到！排雷成功！{C_RESET}")
                print(f"  用了 {steps} 步完成排雷")
                game_over = True
                input(f"\n  {C_CYAN}[回车结束]{C_RESET}")

        except:
            pass

    # 最终结果
    clear()
    header()
    reveal_all(grid)
    draw_grid(grid, found_mines, flag_grid)

    safe_found = sum(1 for r in range(GRID_H) for c in range(GRID_W)
                    if grid[r][c]['type'] == 'safe' and grid[r][c]['revealed'])
    mines_found = sum(1 for r in range(GRID_H) for c in range(GRID_W)
                     if grid[r][c]['type'] == 'mine' and grid[r][c]['revealed'])
    mines_exploded = sum(1 for r in range(GRID_H) for c in range(GRID_W)
                        if grid[r][c]['type'] == 'mine' and grid[r][c]['revealed'] and grid[r][c].get('exploded', False))

    print(f"\n  {C_BOLD}【排雷报告】{C_RESET}")
    print(f"  总雷数：{total_mines}  踩爆：{mines_exploded}  安全项：{safe_found}/{total_safe}")
    print(f"  步数：{steps}")

    if mines_exploded == 0:
        print(f"\n  {C_GREEN}评价：完美的财报审计能力！你能识别A股大部分财报造假手法！{C_RESET}")
    elif mines_exploded <= 2:
        print(f"\n  {C_YELLOW}评价：不错的财报排雷能力，继续磨练！{C_RESET}")
    else:
        print(f"\n  {C_RED}评价：踩了太多雷，在A股容易被割韭菜...{C_RESET}")

    print(f"\n  {C_MAGENTA}记住这些雷的样子：{C_RESET}")
    for r in range(GRID_H):
        for c in range(GRID_W):
            if grid[r][c]['type'] == 'mine' and grid[r][c].get('exploded', False):
                print(f"  {C_RED}· {grid[r][c]['name']}{C_RESET}")
    print(f"\n  {C_CYAN}[回车退出]{C_RESET}")
    input()

if __name__ == "__main__":
    main()
