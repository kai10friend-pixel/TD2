import random
import os
import gradio as gr

# 元ファイル「単語.py」の全Chapterの問題データを利用しています。
# Chapter選択はなく、全Chapterからランダムに出題します。

# 写真に写っている単語帳（Unit 71〜80）の語句を出題します。
# 問題は英語の単語・熟語、選択肢は日本語訳です。
_vocabulary = [('take off', '離陸する'), ('see A off', '見送る'), ('keep off A', '近づけない・避ける'), ('go with A', '～に合う・調和する'), ('deal with A', '～を扱う・対処する'), ('cope with A', '～にうまく対処する'), ('be filled with A', '～で満たされている'), ('be worried about A', '～を心配している'), ('be struck by A', '～に心を打たれる'), ('be crowded with A', '～で混雑している'), ('be caught in A', '～にあう・巻き込まれる'), ('be based on A', '～に基づく'), ('think over A', '～を熟考する'), ('run over A', '～をひく'), ('turn over A', '～をひっくり返す・めくる'), ('ask for A', '～を求める'), ('feel for A', '～に同情する'), ('apart from A', '～を除いて・～のほかに'), ('other than A', '～以外に'), ('in spite of A', '～にもかかわらず'), ('regardless of A', '～に関係なく'), ('for all A', '～にもかかわらず'), ('after all', '結局'), ('above all', 'とりわけ'), ('belong to A', '～に所属する'), ('occur to A', '（考えなどが）～の頭に浮かぶ'), ('stick to A', '～を守る・～にくっつく'), ('graduate from A', '～を卒業する'), ('suffer from A', '～に苦しむ'), ('result from A', '～の結果として起こる'), ('result in A', '～という結果に終わる'), ('fill in A', '～を書き込む'), ('put on weight', '太る'), ('lose weight', 'やせる'), ('up to date', '最新の'), ('out of date', '時代遅れの'), ('check out', 'チェックアウトする'), ('make out A', '～を判読する・見分ける'), ('figure out A', '～を理解する・解決する'), ('give out A', '～を配る'), ('wear out A', '～を使い果たす・疲れさせる'), ('point out A', '～を指摘する'), ('believe in A', '～の存在・価値を信じる'), ('hand in A', '～を提出する'), ('in place of A', '～の代わりに'), ('in case of A', '～の場合には'), ('in addition to A', '～に加えて'), ('in connection with A', '～に関連して'), ('clear up', '晴れ上がる'), ('cheer up', '～を元気づける'), ('depend on A', '～に頼る・次第である'), ('rely on A', '～を当てにする'), ('count on A', '～を頼りにする'), ('focus on A', '～に焦点を合わせる・集中する'), ('more or less', '多かれ少なかれ・大体'), ('sooner or later', '遅かれ早かれ'), ('no longer', 'もはや～ない'), ('at least', '少なくとも'), ('at (the) most', '多くとも・せいぜい'), ('cooperate', '協力する'), ('compete', '競う'), ('capture', '捕らえる'), ('release', '解放する・発表する'), ('increase', '増える・増やす'), ('decrease', '減る・減らす'), ('concentrate', '集中する'), ('distract', '注意をそらす'), ('company', '仲間・会社'), ('respect', '点・尊敬する'), ('object', '物体・対象・反対する'), ('count', '重要である・数える'), ('encourage', '励ます'), ('ensure', '確実にする'), ('enable', '可能にする'), ('enrich', '豊かにする'), ('entitle', '資格を与える'), ('worsen', 'さらに悪くなる'), ('frighten', '怖がらせる'), ('escape', '逃れる'), ('search', '捜索する・探す'), ('reflect', '反射する・熟考する'), ('preserve', '保存する'), ('conserve', '保全する'), ('observe', '観察する'), ('deserve', '～に値する'), ('admit', '認める'), ('acknowledge', '認める'), ('differ', '異なる'), ('vary', 'さまざまに異なる'), ('sense', '感覚'), ('direction', '方向'), ('attract', '引きつける'), ('attention', '注意・関心'), ('yell', '大声で叫ぶ'), ('scream', '悲鳴を上げる'), ('solve', '解決する'), ('resolve', '解決する・決心する'), ('extend', '延長する・拡大する'), ('expand', '拡大する'), ('destroy', '破壊する'), ('collapse', '崩れ落ちる'), ('gain', '手に入れる・増す'), ('obtain', '手に入れる・獲得する'), ('encounter', '直面する・出会う'), ('confront', '直面する'), ('offer', '申し出る・提供する'), ('owe', '借りている・～のおかげである'), ('spare', '（時間などを）割く'), ('especially', '特に'), ('particularly', '特に'), ('definitely', '間違いなく・確実に'), ('precisely', '正確に・まさしく'), ('absolutely', '完全に・まったく'), ('entirely', '完全に'), ('probably', 'おそらく'), ('hopefully', '願わくは'), ('unfortunately', '不運にも')]
_meanings = [meaning for _, meaning in _vocabulary]

def make_vocabulary_questions():
    questions = []
    for i, (word, meaning) in enumerate(_vocabulary):
        distractors = []
        for offset in (7, 19, 31):
            candidate = _meanings[(i + offset) % len(_meanings)]
            if candidate != meaning and candidate not in distractors:
                distractors.append(candidate)
        j = 1
        while len(distractors) < 3:
            candidate = _meanings[(i + j) % len(_meanings)]
            j += 1
            if candidate != meaning and candidate not in distractors:
                distractors.append(candidate)
        options = distractors + [meaning]
        random.shuffle(options)
        questions.append({
            "question": word,
            "options": options,
            "answer": meaning,
            "explanation": f"'{word}' は「{meaning}」という意味です。写真の単語帳 Unit 71〜80の左ページにある見出し語です。",
            "derived_word": "単語帳 Unit 71〜80"
        })
    return questions

chapter_questions = {"単語・熟語 Unit 71〜80": make_vocabulary_questions()}


QUESTIONS_PER_STAGE = 10


QUESTIONS_PER_STAGE = 10
TICK_SECONDS = 0.5
TICKS_PER_20_SECONDS = int(20 / TICK_SECONDS)
ROUTE = [(35, 55), (150, 55), (190, 75), (205, 115), (280, 130), (355, 130), (390, 165), (410, 205), (500, 205), (560, 185), (590, 145), (620, 115), (720, 115)]
TOWER_SPOTS = [(250, 82), (350, 185), (515, 135)]


def new_enemy(enemy_id, tier=1, boss=False):
    # 通常敵はランク1がHP2で、ランクごとにHPが8増加。ボスはHP400。
    max_hp = 400 if boss else 2 + (tier - 1) * 8
    return {"id": enemy_id, "p": 0.0, "tier": 6 if boss else tier,
            "boss": boss, "hp": max_hp, "max_hp": max_hp,
            "x": ROUTE[0][0], "y": ROUTE[0][1]}


def enemy_svg(e):
    """通常敵はランク別、ボスは黒い体と赤い目で描く。"""
    if e.get("boss"):
        radius = 25
        bar_width = 58
        hp_width = bar_width * max(0, e["hp"]) / max(1, e["max_hp"])
        return (f'<g transform="translate({e["x"]:.1f} {e["y"]:.1f})">'
                f'<path d="M-20 -14L-31 -30L-10 -23L0 -34L10 -23L31 -30L20 -14Z" fill="#090909" stroke="#444" stroke-width="3"/>'
                f'<circle r="{radius}" fill="#050505" stroke="#555" stroke-width="4"/>'
                f'<circle cx="-9" cy="-4" r="5" fill="#ff1717" stroke="#ff7777" stroke-width="1.5"/>'
                f'<circle cx="9" cy="-4" r="5" fill="#ff1717" stroke="#ff7777" stroke-width="1.5"/>'
                f'<path d="M-10 10L-5 15L0 10L5 15L10 10" fill="none" stroke="#a00" stroke-width="3"/>'
                f'<rect x="{-bar_width/2}" y="-42" width="{bar_width}" height="6" rx="3" fill="#3b2020"/>'
                f'<rect x="{-bar_width/2}" y="-42" width="{hp_width:.1f}" height="6" rx="3" fill="#ff3030"/>'
                f'<text x="0" y="42" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffdddd">BOSS {e["hp"]}/{e["max_hp"]}</text></g>')
    tier = e.get("tier", 1)
    styles = {
        1: ("#a8e56a", "#315c28", 12, ""),
        2: ("#67d7ed", "#176178", 13, '<path d="M-11 -7L-8 -15L0 -11L8 -15L11 -7L8 8H-8Z" fill="#b7eaf4" stroke="#176178" stroke-width="2"/>'),
        3: ("#b98aff", "#552b83", 14, '<path d="M-9 -8L-18 -20L-5 -16L0 -22L5 -16L18 -20L9 -8Z" fill="#e2c8ff" stroke="#552b83" stroke-width="2"/>'),
        4: ("#ff795f", "#8a261c", 16, '<path d="M-10 -8L-20 -22L-6 -17L0 -24L6 -17L20 -22L10 -8Z" fill="#ffbd8f" stroke="#8a261c" stroke-width="2"/><path d="M-12 2H12V12H-12Z" fill="#a72d24" stroke="#641a16" stroke-width="2"/>'),
        5: ("#ffd34e", "#8c5b08", 19, '<path d="M-13 -9L-25 -25L-7 -19L0 -29L7 -19L25 -25L13 -9Z" fill="#fff0a3" stroke="#8c5b08" stroke-width="3"/><path d="M-15 2H15V15H-15Z" fill="#d99116" stroke="#8c5b08" stroke-width="2"/>'),
    }
    color, outline, radius, armor = styles[min(tier, 5)]
    eye = max(2, radius * 0.17)
    bar_width = 2 * radius + 2
    hp_width = bar_width * max(0, e["hp"]) / max(1, e["max_hp"])
    return (f'<g transform="translate({e["x"]:.1f} {e["y"]:.1f})">'
            f'{armor}<circle r="{radius}" fill="{color}" stroke="{outline}" stroke-width="2.5"/>'
            f'<circle cx="{-radius*0.32:.1f}" cy="{-radius*0.12:.1f}" r="{eye:.1f}" fill="#142318"/>'
            f'<circle cx="{radius*0.32:.1f}" cy="{-radius*0.12:.1f}" r="{eye:.1f}" fill="#142318"/>'
            f'<path d="M{-radius*0.3:.1f} {radius*0.35:.1f}q{radius*0.3:.1f} {radius*0.3:.1f} {radius*0.6:.1f} 0" fill="none" stroke="{outline}" stroke-width="2"/>'
            f'<rect x="{-bar_width/2:.1f}" y="{-radius-11}" width="{bar_width}" height="4" rx="2" fill="#3b2020"/>'
            f'<rect x="{-bar_width/2:.1f}" y="{-radius-11}" width="{hp_width:.1f}" height="4" rx="2" fill="#ff6b6b"/>'
            f'<text x="0" y="{radius+12}" text-anchor="middle" font-size="9" font-weight="bold" fill="white">T{tier}</text></g>')


def route_position(p):
    lengths = []
    total = 0.0
    for a, b in zip(ROUTE, ROUTE[1:]):
        length = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        lengths.append(length)
        total += length
    target = max(0.0, min(1.0, p)) * total
    for i, length in enumerate(lengths):
        if target <= length:
            a, b = ROUTE[i], ROUTE[i + 1]
            ratio = target / length if length else 0
            return a[0] + (b[0] - a[0]) * ratio, a[1] + (b[1] - a[1]) * ratio
        target -= length
    return ROUTE[-1]


def start_game():
    all_questions = []
    for chapter_list in chapter_questions.values():
        all_questions.extend(chapter_list)
    random.shuffle(all_questions)
    state = {
        "questions": all_questions, "index": 0, "coins": 50, "score": 0,
        "hp": 100, "tower_level": 1, "wrong": [], "finished": False,
        "enemies": [], "shots": [], "next_enemy_id": 1, "ticks": 0,
        "tower_cooldowns": [0, 0, 0], "kills": 0, "elapsed_ticks": 0, "enemy_tier": 1,
        "boss_spawned": False, "sound_event": None,
        "message": "ゲーム開始！20秒ごとに敵が強くなります。150秒後にはHP400のボスが出現！"
    }
    state["enemies"].append(new_enemy(state["next_enemy_id"], state["enemy_tier"]))
    state["next_enemy_id"] += 1
    return render_question(state, "🏰 ゲーム開始！初期コイン50枚でタワーを強化できます。")


def hud(state):
    idx = state["index"]
    total = len(state["questions"])
    stage = idx // QUESTIONS_PER_STAGE + 1
    boss_status = "　👑 **BOSS出現中！**" if any(e.get("boss") for e in state.get("enemies", [])) else ("　👑 **BOSS撃破済み！**" if state.get("boss_spawned") and state.get("boss_defeated") else "")
    if state.get("boss_defeated"):
        return (
            "# 🎉 congratulation!\n\n**ボスを撃破しました！ゲームクリア！**\n\n"
            f"❤️ 城HP：**{state['hp']} / 100**　🪙 コイン：**{state['coins']}**　"
            f"🎯 正解：**{state['score']}**　🏹 タワーLv：**{state['tower_level']}**　"
            f"👾 撃破：**{state['kills']}**"
        )
    return (
        f"## 🏰 ENGLISH DEFENSE\n"
        f"**ステージ：** {stage}　**問題：** {min(idx + 1, total)} / {total}\n\n"
        f"❤️ **城HP：** {state['hp']} / 100　　🪙 **コイン：** {state['coins']}　　"
        f"🎯 **正解：** {state['score']}　　🏹 **タワーLv：** {state['tower_level']}　　"
        f"👾 **撃破：** {state['kills']}　　🧟 **敵ランク：** {state.get('enemy_tier', 1)}　"
        f"⏱️ **経過：** {state.get('elapsed_ticks', 0) * TICK_SECONDS:.0f}秒{boss_status}"
    )


def battle_html(state):
    # Render the current server-side battle state as SVG. The Gradio timer advances the simulation.
    route_d = "M " + " L ".join(f"{x},{y}" for x, y in ROUTE)
    bits = [f'''<div class="battle-wrap"><div class="battle-head"><b>🛡️ 防衛フィールド</b><span>敵は自動移動・タワーは自動攻撃</span></div>
    <svg viewBox="0 0 760 280" role="img" aria-label="タワーディフェンスの戦闘画面">
    <defs><linearGradient id="grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#246545"/><stop offset="1" stop-color="#123d2a"/></linearGradient><linearGradient id="road" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e0c99b"/><stop offset="1" stop-color="#a68a5e"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
    <rect width="760" height="280" rx="12" fill="url(#grass)"/><path d="{route_d}" fill="none" stroke="#604b36" stroke-width="48" stroke-linecap="round" stroke-linejoin="round"/><path d="{route_d}" fill="none" stroke="url(#road)" stroke-width="38" stroke-linecap="round" stroke-linejoin="round"/><path d="{route_d}" fill="none" stroke="#f7e7c4" stroke-width="2" stroke-dasharray="7 10" opacity=".8"/>''']
    # tower range rings and towers
    for i, (tx, ty) in enumerate(TOWER_SPOTS):
        radius = 90 + (state["tower_level"] - 1) * 8
        bits.append(f'<circle cx="{tx}" cy="{ty}" r="{radius}" fill="#a8e8ff" fill-opacity=".06" stroke="#8bdcff" stroke-opacity=".25" stroke-dasharray="5 6"/>')
        bits.append(f'<g transform="translate({tx} {ty})"><ellipse cy="18" rx="22" ry="7" fill="#10291d"/><path d="M-18 12L-14 -13H14L18 12Z" fill="#a9c5d2" stroke="#effaff" stroke-width="2"/><path d="M-20 -13L-15 -25H15L20 -13Z" fill="#e4f3f8" stroke="#fff" stroke-width="2"/><circle cy="-5" r="6" fill="#7de6ff" filter="url(#glow)"/><text x="0" y="34" text-anchor="middle" font-size="11" font-weight="bold" fill="white">Lv.{state['tower_level']}</text></g>')
    # castle at goal
    bits.append('<g transform="translate(682 55)"><rect y="18" width="48" height="43" rx="3" fill="#9aa8b5" stroke="#e7f2f8" stroke-width="2"/><path d="M-4 20V4H7V13H17V0H29V13H39V4H52V20Z" fill="#dce7ed"/><rect x="18" y="39" width="12" height="22" rx="6" fill="#34475a"/></g><text x="680" y="135" fill="white" font-size="12" font-weight="bold">GOAL</text><text x="20" y="25" fill="white" font-size="12" font-weight="bold">START</text>')
    for shot in state["shots"]:
        bits.append(f'<line x1="{shot["x1"]:.1f}" y1="{shot["y1"]:.1f}" x2="{shot["x2"]:.1f}" y2="{shot["y2"]:.1f}" stroke="#ffe36b" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>')
    for e in state["enemies"]:
        bits.append(enemy_svg(e))
    # ゲーム終了時は戦闘画面そのものに結果を大きく表示
    if state.get("boss_defeated"):
        bits.append('<rect x="65" y="88" width="630" height="104" rx="18" fill="#071f16" fill-opacity=".94" stroke="#ffe36b" stroke-width="4"/><text x="380" y="132" text-anchor="middle" font-size="34" font-weight="900" fill="#ffe36b">CONGRATULATIONS!</text><text x="380" y="164" text-anchor="middle" font-size="17" font-weight="bold" fill="white">BOSS DEFEATED</text>')
    elif state.get("boss_reached") or (state.get("finished") and state.get("hp", 100) <= 0):
        bits.append('<rect x="65" y="88" width="630" height="104" rx="18" fill="#210707" fill-opacity=".95" stroke="#ff3535" stroke-width="4"/><text x="380" y="132" text-anchor="middle" font-size="42" font-weight="900" fill="#ff4545">GAMEOVER</text><text x="380" y="164" text-anchor="middle" font-size="17" font-weight="bold" fill="white">THE CASTLE HAS FALLEN</text>')
    bits.append('</svg><div class="battle-foot"><span>👾 敵：HPバーが0で撃破</span><span>🏹 タワー：射程内を自動攻撃</span><span>💥 ゴール到達で城HP減少</span></div></div>')
    bits.append('''<style>.battle-wrap{border:1px solid #3c7658;border-radius:14px;overflow:hidden;background:#102d21;color:#eef9f0;margin:8px 0 14px}.battle-head,.battle-foot{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;padding:10px 14px;background:#183d2b;font-size:13px}.battle-wrap svg{display:block;width:100%;height:auto}.battle-foot{color:#d7f3df}</style>''')
    return "".join(bits)


def simulate_battle(state):
    if state.get("finished"):
        return
    state["sound_event"] = None
    previous_castle_hp = state.get("hp", 100)
    state["ticks"] += 1
    state["elapsed_ticks"] = state.get("elapsed_ticks", 0) + 1
    # 20秒ごとに新しく出現する敵のランクを上げる（ランクごとにHP +8）。
    if state["elapsed_ticks"] % TICKS_PER_20_SECONDS == 0:
        state["enemy_tier"] = min(5, state.get("enemy_tier", 1) + 1)
        state["message"] = f"⚠️ {state['elapsed_ticks'] * TICK_SECONDS:.0f}秒経過！敵がランク{state['enemy_tier']}に進化しました。HPが8増え、見た目も変化！"
    # 150秒経過した瞬間に、HP400のボスを1体だけ出現させる。
    boss_tick = int(150 / TICK_SECONDS)
    if (state["elapsed_ticks"] >= boss_tick and not state.get("boss_spawned", False)
            and state["hp"] > 0):
        # ボス出現時に通常敵を退場させ、以後はボスだけと戦う。
        state["enemies"] = []
        state["enemies"].append(new_enemy(state["next_enemy_id"], tier=6, boss=True))
        state["next_enemy_id"] += 1
        state["boss_spawned"] = True
        state["message"] = "🚨 BOSS出現！黒いボスの赤い目に注意！HP400を削り切れ！"
    # ボス出現後は通常敵を一切スポーンさせない。
    if not state.get("boss_spawned", False) and state["ticks"] % 2 == 0 and len(state["enemies"]) < 32 and state["hp"] > 0:
        state["enemies"].append(new_enemy(state["next_enemy_id"], state.get("enemy_tier", 1)))
        state["next_enemy_id"] += 1
    # Move enemies 1.5x faster along the route; a reached goal damages the castle.
    for e in state["enemies"]:
        e["p"] += 0.0135
        e["x"], e["y"] = route_position(e["p"])
    survivors = []
    for e in state["enemies"]:
        if e["p"] >= 1:
            if e.get("boss"):
                state["hp"] = 0
                state["boss_reached"] = True
                state["finished"] = True
                state["message"] = "💥 ボスが城に到達！GAMEOVER"
                state["enemies"] = []
                break
            state["hp"] = max(0, state["hp"] - 15)
            state["message"] = "🚨 敵がゴールに到達！城HPが15減少しました。"
        else:
            survivors.append(e)
    state["enemies"] = survivors
    if state.get("hp", 100) < previous_castle_hp:
        state["sound_event"] = "damage"
    # Towers fire 1.5x more frequently at the nearest enemy in range. Each shot deals 1 damage.
    state["shots"] = []
    for i, (tx, ty) in enumerate(TOWER_SPOTS):
        state["tower_cooldowns"][i] = max(0, state["tower_cooldowns"][i] - 1)
        radius = 90 + (state["tower_level"] - 1) * 8
        targets = [e for e in state["enemies"] if e["hp"] > 0 and ((e["x"]-tx)**2 + (e["y"]-ty)**2)**0.5 <= radius]
        if targets and state["tower_cooldowns"][i] <= 0:
            target = min(targets, key=lambda e: ((e["x"]-tx)**2 + (e["y"]-ty)**2))
            target["hp"] -= 1 + (state["tower_level"] - 1) // 2
            state["shots"].append({"x1": tx, "y1": ty, "x2": target["x"], "y2": target["y"]})
            if state.get("sound_event") is None:
                state["sound_event"] = "attack"
            state["tower_cooldowns"][i] = max(1, round((4 - (state["tower_level"] - 1) // 2) / 1.5))
            if target["hp"] <= 0:
                state["coins"] += 5
                state["kills"] += 1
                if target.get("boss"):
                    state["boss_defeated"] = True
                    state["finished"] = True
                    state["coins"] += 100
                    state["message"] = "🎉 congratulation! ボス撃破！ゲームクリア！"
                    # ボス撃破でゲーム終了。画面上の敵もすべて消す。
                    state["enemies"] = []
                    break
                else:
                    state["message"] = "💥 敵を撃破！ボーナス+5コイン！"
    state["enemies"] = [e for e in state["enemies"] if e["hp"] > 0]
    if state["hp"] <= 0:
        state["finished"] = True
        state["message"] = "💥 城が陥落しました。ゲーム開始ボタンで再挑戦できます。"


def upgrade_cost_text(state):
    if not state:
        return "強化費用：🪙 30枚（Lv.1 → Lv.2）"
    cost = 30 * state.get("tower_level", 1)
    return f"**次の強化費用：🪙 {cost}枚**（Lv.{state.get('tower_level', 1)} → Lv.{state.get('tower_level', 1) + 1}）"


def render_question(state, message=""):
    if state.get("finished") or state.get("boss_defeated") or state.get("boss_reached") or state["index"] >= len(state["questions"]) or state["hp"] <= 0:
        state["finished"] = True
        total = len(state["questions"])
        answered = state["index"]
        accuracy = state["score"] / answered * 100 if answered else 0
        if state.get("boss_defeated"):
            title = "# 🎉 CONGRATULATIONS!\n\n## ボスを撃破しました！ゲームクリア！"
        elif state.get("boss_reached") or state["hp"] <= 0:
            title = "# 💥 GAMEOVER\n\n## ボスが城に到達しました。城は陥落しました。"
        else:
            title = "## 🏆 全問題クリア！"
        summary = f"{title}\n\n正解数：**{state['score']} / {answered}問**　正答率：**{state['score']} / {answered} × 100 = {accuracy:.1f}%**　獲得コイン：**{state['coins']}**　撃破数：**{state['kills']}**"
        if state["wrong"]:
            summary += "\n\n### 📘 復習する問題\n"
            for i, q in enumerate(state["wrong"], 1):
                summary += f"\n**{i}. {q['question']}**\n- 正解：{q['answer']}\n- 解説：{q.get('explanation', '解説はありません。')}\n"
        return hud(state), "ゲーム終了", gr.update(choices=[], value=None), summary, "", gr.update(interactive=False), battle_html(state), upgrade_cost_text(state), state
    q = state["questions"][state["index"]]
    question_text = f"### 📝 問題\n\n**{q['question']}**"
    result_text = message or "回答欄から正しい答えを選んでね。"
    explanation_text = f"📘 **解説：** {state.get('last_explanation', q.get('explanation', ''))}" if message else ""
    return hud(state), question_text, gr.update(choices=q.get("options", []), value=None), result_text, explanation_text, gr.update(interactive=not state["finished"]), battle_html(state), upgrade_cost_text(state), state


def answer_question(choice, state):
    if not state:
        return start_game()
    if state.get("finished"):
        return render_question(state, "ゲームは終了しています。ゲーム開始ボタンを押してください。")
    if not choice:
        return hud(state), f"### 📝 問題\n\n**{state['questions'][state['index']]['question']}**", gr.update(), "選択肢を選んでから回答してください。", "", gr.update(interactive=True), battle_html(state), upgrade_cost_text(state), state
    q = state["questions"][state["index"]]
    if choice == q["answer"]:
        state["score"] += 1
        state["coins"] += 10
        message = "✅ **正解！** +10コイン。"
    else:
        state["wrong"].append(q)
        state["hp"] = max(0, state["hp"] - 10)
        message = f"❌ **不正解！** 城HPが10減少。\n\n**正解：** {q['answer']}"
    state["index"] += 1
    if state["index"] % QUESTIONS_PER_STAGE == 0 and state["hp"] > 0 and state["index"] < len(state["questions"]):
        state["coins"] += 20
        message += "\n\n🌟 **ステージ突破ボーナス：+20コイン！**"
    state["message"] = message
    state["last_explanation"] = q.get("explanation", "")
    return render_question(state, message)


def upgrade_tower(state):
    if not state:
        return start_game()
    if state.get("finished"):
        return hud(state), battle_html(state), state, "ゲーム終了後は強化できません。", upgrade_cost_text(state)
    cost = 30 * state["tower_level"]
    if state["coins"] < cost:
        return hud(state), battle_html(state), state, f"コイン不足！強化には🪙 {cost}枚必要です。", upgrade_cost_text(state)
    state["coins"] -= cost
    state["tower_level"] += 1
    state["message"] = f"⬆️ タワーをLv.{state['tower_level']}に強化！攻撃力・射程・攻撃速度が上がりました。"
    return hud(state), battle_html(state), state, state["message"], upgrade_cost_text(state)


def timer_tick(state):
    if not state:
        return "## 🏰 ENGLISH DEFENSE", "", state, gr.update(interactive=False), "「ゲーム開始」を押してスタート！", "", "", gr.update(choices=[], value=None), None, None
    if not state.get("finished"):
        simulate_battle(state)
        if state.get("hp", 0) <= 0:
            state["finished"] = True
    if state.get("finished"):
        rendered = render_question(state, state.get("message", "ゲーム終了"))
        return rendered[0], rendered[6], state, rendered[5], rendered[1], rendered[3], rendered[4], rendered[2], None, None
    event = state.get("sound_event")
    sound_file = None
    if event == "damage":
        sound_file = f"damage_{(state.get('ticks', 0) % 3) + 1}.wav"
    elif event == "attack":
        sound_file = f"attack_{(state.get('ticks', 0) % 3) + 1}.wav"
    return hud(state), battle_html(state), state, gr.update(interactive=True), gr.update(), gr.update(), gr.update(), gr.update(), sound_file, gr.update()


with gr.Blocks(title="ENGLISH DEFENSE", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏰 ENGLISH DEFENSE\n問題に答えて城を守り、コインでタワーを強化しよう！")
    status = gr.Markdown()
    battle_view = gr.HTML()
    with gr.Row():
        upgrade_btn = gr.Button("⬆️ タワー強化（コイン消費）", variant="secondary")
        upgrade_message = gr.Markdown("**次の強化費用：🪙 30枚**（Lv.1 → Lv.2）")
    upgrade_notice = gr.Markdown()

    question = gr.Markdown("「ゲーム開始」を押してスタート！")
    choice = gr.Radio(choices=[], label="解答欄：正しい答えを選んでね")
    result = gr.Markdown(label="判定")
    explanation = gr.Markdown(label="解説")
    with gr.Row():
        answer_btn = gr.Button("⚔️ 回答する", variant="primary")
        start_btn = gr.Button("🔄 ゲーム開始 / もう一度遊ぶ")
    state = gr.State({})
    timer = gr.Timer(TICK_SECONDS)
    # BGMと効果音はブラウザ側で再生。ゲーム開始ボタン操作後にBGMを開始する。
    bgm_audio = gr.Audio(value=None, autoplay=True, loop=True, visible=False, label="BGM")
    sfx_audio = gr.Audio(value=None, autoplay=True, loop=False, visible=False, label="効果音")

    start_outputs = [status, question, choice, result, explanation, answer_btn, battle_view, upgrade_message, state]
    start_btn.click(start_game, outputs=start_outputs)
    start_btn.click(lambda: "bgm.wav", outputs=bgm_audio)
    answer_btn.click(answer_question, inputs=[choice, state], outputs=start_outputs)
    upgrade_btn.click(upgrade_tower, inputs=[state], outputs=[status, battle_view, state, upgrade_notice, upgrade_message])
    timer.tick(timer_tick, inputs=[state], outputs=[status, battle_view, state, answer_btn, question, result, explanation, choice, sfx_audio, bgm_audio])

    gr.Markdown("---\n**戦闘ルール：** 敵は約1秒ごとに出現し、同時に最大32体まで表示。20秒ごとに敵ランクが上がり、敵HPが8ずつ増加し、色・大きさ・装備が変化します。150秒後にはHP400の巨大ボスが出現し、撃破すると追加で100コイン獲得。敵が城に到達すると城HPが15減ります。不正解でも城HPが10減ります。タワーは射程内の敵を自動攻撃し、通常敵を撃破すると+5コイン。正解で+10コイン、10問ごとに+20コイン。タワーは自動強化されず、強化ボタンを押してコインを消費したときだけ強化されます。")

if __name__ == "__main__":
    # RenderのPORT環境変数を使い、外部からアクセスできるアドレスで起動する
    port = int(os.environ.get("PORT", "10000"))
    demo.launch(server_name="0.0.0.0", server_port=port)
