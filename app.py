import random
import os
import gradio as gr

# 元ファイル「単語.py」の全Chapterの問題データを利用しています。
# Chapter選択はなく、全Chapterからランダムに出題します。

chapter_questions = {'Chapter 1': [{'question': 'He ___ to the store yesterday.', 'options': ['go', 'goes', 'went', 'gone'], 'answer': 'went', 'explanation': "過去の出来事なので、動詞 'go' の過去形 'went' を使います。", 'derived_word': '時制: 過去形'}, {'question': 'She ___ learning English since last year.', 'options': ['is', 'was', 'has been', 'had been'], 'answer': 'has been', 'explanation': "「昨年からずっと」と継続を表すので、現在完了進行形 'has been learning' を使います。", 'derived_word': '時制: 現在完了進行形'}, {'question': 'By the time he arrived, the movie ___ already finished.', 'options': ['is', 'was', 'has', 'had'], 'answer': 'had', 'explanation': "彼が到着した時点よりも前に映画が終わっていたので、過去完了形 'had finished' を使います。", 'derived_word': '時制: 過去完了形'}, {'question': 'I ___ a book when she called me.', 'options': ['read', 'am reading', 'was reading', 'have read'], 'answer': 'was reading', 'explanation': "彼女が電話をかけてきた時に、私が本を読んでいる最中だった状況を表すので、過去進行形 'was reading' を使います。", 'derived_word': '時制: 過去進行形'}, {'question': 'The sun ___ in the east.', 'options': ['rise', 'rose', 'rises', 'will rise'], 'answer': 'rises', 'explanation': "普遍的な事実なので、現在形 'rises' を使います。", 'derived_word': '時制: 現在形'}], 'Chapter 2': [{'question': 'This is the book ___ I bought yesterday.', 'options': ['who', 'whose', 'which', 'where'], 'answer': 'which', 'explanation': "先行詞が物（the book）なので、関係代名詞 'which' を使います。目的格の関係代名詞なので省略も可能です。", 'derived_word': '関係詞: 目的格の関係代名詞'}, {'question': 'I know a man ___ can speak five languages.', 'options': ['which', 'whose', 'who', 'whom'], 'answer': 'who', 'explanation': "先行詞が人（a man）で、動詞 'can speak' の主語になるので、関係代名詞 'who' を使います。", 'derived_word': '関係詞: 主格の関係代名詞'}, {'question': 'He showed me the house ___ he was born.', 'options': ['which', 'who', 'where', 'when'], 'answer': 'where', 'explanation': "先行詞が場所（the house）で、完全な文が続くので、関係副詞 'where' を使います。", 'derived_word': '関係詞: 関係副詞 (場所)'}, {'question': 'She has a dog ___ name is Pochi.', 'options': ['who', 'which', 'that', 'whose'], 'answer': 'whose', 'explanation': "先行詞（a dog）の所有を表すので、関係代名詞 'whose' を使います。", 'derived_word': '関係詞: 所有格の関係代名詞'}, {'question': 'Tell me ___ you want.', 'options': ['that', 'what', 'which', 'where'], 'answer': 'what', 'explanation': "「～なこと/もの」という意味で、先行詞を含んで名詞節を作るので、関係代名詞 'what' を使います。", 'derived_word': '関係詞: 複合関係代名詞'}], 'Chapter 3': [{'question': 'If I ___ a bird, I would fly to you.', 'options': ['am', 'was', 'were', 'had been'], 'answer': 'were', 'explanation': "現在の事実とは異なる仮定を表す仮定法過去なので、'If I were' を使います。", 'derived_word': '仮定法: 仮定法過去'}, {'question': 'If I had known, I ___ you.', 'options': ['would tell', 'would have told', 'will tell', 'told'], 'answer': 'would have told', 'explanation': "過去の事実とは異なる仮定を表す仮定法過去完了なので、'would have told' を使います。", 'derived_word': '仮定法: 仮定法過去完了'}, {'question': 'I wish I ___ taller.', 'options': ['am', 'was', 'were', 'had been'], 'answer': 'were', 'explanation': "現在の願望を表す 'I wish + 仮定法過去' の形なので、'were' を使います。", 'derived_word': '仮定法: I wish + 仮定法'}, {'question': 'It is important that he ___ well.', 'options': ['studies', 'study', 'studied', 'to study'], 'answer': 'study', 'explanation': "'It is important that S + (should) 原形動詞' の構文なので、動詞の原形 'study' を使います。", 'derived_word': '仮定法: 提案・要求などのthat節内'}, {'question': 'If it ___ for your help, I would have failed.', 'options': ['was not', 'were not', 'had not been', 'is not'], 'answer': 'had not been', 'explanation': "「もし～がなければ」という意味で、過去の仮定を表すので 'If it had not been for' を使います。", 'derived_word': '仮定法: If it were not for/had not been for'}], 'Chapter 4': [{'question': 'The letter ___ by him yesterday.', 'options': ['write', 'wrote', 'was written', 'is written'], 'answer': 'was written', 'explanation': "「手紙が彼によって書かれた」という過去の受動態なので、'was written' を使います。", 'derived_word': '受動態: 過去の受動態'}, {'question': 'English ___ all over the world.', 'options': ['speak', 'spoke', 'is spoken', 'has spoken'], 'answer': 'is spoken', 'explanation': "「英語が世界中で話されている」という現在の事実を表す受動態なので、'is spoken' を使います。", 'derived_word': '受動態: 現在の受動態'}, {'question': 'A new bridge ___ next year.', 'options': ['build', 'is built', 'will be built', 'was built'], 'answer': 'will be built', 'explanation': "「新しい橋が来年建設されるだろう」という未来の受動態なので、'will be built' を使います。", 'derived_word': '受動態: 未来の受動態'}, {'question': 'He ___ to be a genius.', 'options': ['says', 'is said', 'said', 'was saying'], 'answer': 'is said', 'explanation': "「彼は天才だと言われている」という受動態の慣用表現 'be said to do' を使います。", 'derived_word': '受動態: 慣用表現 (S is said to do)'}, {'question': 'The window ___ by the children.', 'options': ['break', 'broke', 'was broken', 'has broken'], 'answer': 'was broken', 'explanation': "「窓が子供たちによって割られた」という過去の受動態なので、'was broken' を使います。", 'derived_word': '受動態: 過去の受動態'}], 'Chapter 5': [{'question': '___ nothing to do, I went to bed early.', 'options': ['Having', 'To have', 'Had', 'To have had'], 'answer': 'Having', 'explanation': "「することが何もなかったので」という理由を表す分詞構文なので、'Having nothing to do' を使います。", 'derived_word': '分詞構文: 理由'}, {'question': '___ on the bench, he read a newspaper.', 'options': ['Sitting', 'Sat', 'To sit', 'To be sitting'], 'answer': 'Sitting', 'explanation': "「ベンチに座りながら」という付帯状況を表す分詞構文なので、'Sitting on the bench' を使います。", 'derived_word': '分詞構文: 付帯状況'}, {'question': '___ from a distance, the stone looks like a face.', 'options': ['See', 'Seen', 'Seeing', 'To see'], 'answer': 'Seen', 'explanation': "「遠くから見ると」という受動の意味を表す分詞構文なので、過去分詞 'Seen' を使います。", 'derived_word': '分詞構文: 受動の意味'}, {'question': '___ in Hokkaido, she knows a lot about snow.', 'options': ['Born', 'Being born', 'To be born', 'Having been born'], 'answer': 'Born', 'explanation': "「北海道で生まれたので」という理由を表す分詞構文で、受動の意味なので過去分詞 'Born' を使います。", 'derived_word': '分詞構文: 受動の理由'}, {'question': '___ carefully, the problem is easy to solve.', 'options': ['Consider', 'Considering', 'Considered', 'To consider'], 'answer': 'Considered', 'explanation': "「注意深く考えれば」という条件を表す分詞構文で、主語が「問題」であり、問題が考えられる側なので受動の意味で過去分詞 'Considered' を使います。", 'derived_word': '分詞構文: 条件'}], 'Chapter 6': [{'question': "'accomplish'", 'options': ['達成する', '避ける', '比較する', '忘れる'], 'answer': '達成する', 'explanation': "'accomplish' は「達成する、成し遂げる」という意味です。", 'derived_word': 'achievement (達成)'}, {'question': "'approximate'", 'options': ['正確な', 'おおよその', '詳細な', '不明確な'], 'answer': 'おおよその', 'explanation': "'approximate' は「おおよその、およそ～」という意味です。", 'derived_word': 'estimation (概算)'}, {'question': "'cooperate'", 'options': ['競争する', '協力する', '無視する', '反対する'], 'answer': '協力する', 'explanation': "'cooperate' は「協力する、共同する」という意味です。", 'derived_word': 'collaboration (共同)'}, {'question': "'distinguish'", 'options': ['混同する', '区別する', '結合する', '統一する'], 'answer': '区別する', 'explanation': "'distinguish' は「区別する、見分ける」という意味です。", 'derived_word': 'discern (見分ける)'}, {'question': "'hesitate'", 'options': ['決断する', '躊躇する', '進む', '同意する'], 'answer': '躊躇する', 'explanation': "'hesitate' は「躊躇する、ためらう」という意味です。", 'derived_word': 'reluctance (ためらい)'}, {'question': "'identify'", 'options': ['区別できない', '特定する', '無視する', '混同する'], 'answer': '特定する', 'explanation': "'identify' は「特定する、識別する」という意味です。", 'derived_word': 'recognize (認識する)'}, {'question': "'interpret'", 'options': ['無視する', '誤解する', '解釈する', '否定する'], 'answer': '解釈する', 'explanation': "'interpret' は「解釈する、通訳する」という意味です。", 'derived_word': 'explain (説明する)'}, {'question': "'maintain'", 'options': ['放棄する', '維持する', '破壊する', '変更する'], 'answer': '維持する', 'explanation': "'maintain' は「維持する、主張する」という意味です。", 'derived_word': 'preserve (保存する)'}, {'question': "'obtain'", 'options': ['失う', '手に入れる', '与える', '拒否する'], 'answer': '手に入れる', 'explanation': "'obtain' は「手に入れる、獲得する」という意味です。", 'derived_word': 'acquire (獲得する)'}, {'question': "'propose'", 'options': ['反対する', '提案する', '撤回する', '強制する'], 'answer': '提案する', 'explanation': "'propose' は「提案する、もくろむ」という意味です。", 'derived_word': 'suggest (提案する)'}], 'Chapter 7': [{'question': "'illustrate'", 'options': ['隠す', '説明する', '否定する', '混乱させる'], 'answer': '説明する', 'explanation': "'illustrate' は「（例などを用いて）説明する、挿絵を入れる」という意味です。", 'derived_word': 'demonstrate (実演する)'}, {'question': "'inquire'", 'options': ['答える', '尋ねる', '教える', '命令する'], 'answer': '尋ねる', 'explanation': "'inquire' は「尋ねる、問い合わせる」という意味です。", 'derived_word': 'query (質問)'}, {'question': "'modify'", 'options': ['維持する', '変更する', '破壊する', '開始する'], 'answer': '変更する', 'explanation': "'modify' は「修正する、変更する」という意味です。", 'derived_word': 'alteration (変更)'}, {'question': "'persuade'", 'options': ['諦めさせる', '説得する', '禁止する', '強制する'], 'answer': '説得する', 'explanation': "'persuade' は「説得する」という意味です。", 'derived_word': 'convince (納得させる)'}, {'question': "'recognize'", 'options': ['見過ごす', '認識する', '忘れる', '軽視する'], 'answer': '認識する', 'explanation': "'recognize' は「認識する、見覚えがある」という意味です。", 'derived_word': 'identify (特定する)'}, {'question': "'accommodate'", 'options': ['拒否する', '収容する', '邪魔する', '破壊する'], 'answer': '収容する', 'explanation': "'accommodate' は「収容する、適応させる」という意味です。", 'derived_word': 'lodge (宿泊させる)'}, {'question': "'anticipate'", 'options': ['予期しない', '予期する', '無視する', '遅らせる'], 'answer': '予期する', 'explanation': "'anticipate' は「予期する、期待する」という意味です。", 'derived_word': 'expect (期待する)'}, {'question': "'compile'", 'options': ['分解する', '編集する', '捨てる', '隠す'], 'answer': '編集する', 'explanation': "'compile' は「編集する、集める」という意味です。", 'derived_word': 'gather (集める)'}, {'question': "'contemplate'", 'options': ['無視する', '熟考する', '軽視する', '行動する'], 'answer': '熟考する', 'explanation': "'contemplate' は「熟考する、じっくり考える」という意味です。", 'derived_word': 'ponder (熟考する)'}, {'question': "'deduce'", 'options': ['推論できない', '推論する', '無視する', '否定する'], 'answer': '推論する', 'explanation': "'deduce' は「推論する、導き出す」という意味です。", 'derived_word': 'infer (推論する)'}], 'Chapter 8': [{'question': "'release'", 'options': ['拘束する', '解放する', '保持する', '捕らえる'], 'answer': '解放する', 'explanation': "'release' は「解放する、発表する」という意味です。", 'derived_word': 'liberate (解放する)'}, {'question': "'resolve'", 'options': ['複雑にする', '解決する', '諦める', '避ける'], 'answer': '解決する', 'explanation': "'resolve' は「解決する、決心する」という意味です。", 'derived_word': 'resolution (解決)'}, {'question': "'simulate'", 'options': ['破壊する', '模倣する', '創造する', '無視する'], 'answer': '模倣する', 'explanation': "'simulate' は「模倣する、～のふりをする」という意味です。", 'derived_word': 'imitate (模倣する)'}, {'question': "'suspect'", 'options': ['信頼する', '疑う', '確信する', '証明する'], 'answer': '疑う', 'explanation': "'suspect' は「疑う、～ではないかと感じる」という意味です。", 'derived_word': 'doubt (疑い)'}, {'question': "'transform'", 'options': ['維持する', '変形させる', '元に戻す', '抑制する'], 'answer': '変形させる', 'explanation': "'transform' は「変形させる、変化させる」という意味です。", 'derived_word': 'metamorphosis (変形)'}, {'question': "'diminish'", 'options': ['増加させる', '減少させる', '維持する', '拡大する'], 'answer': '減少させる', 'explanation': "'diminish' は「減少させる、小さくする」という意味です。", 'derived_word': 'decrease (減少)'}, {'question': "'endeavor'", 'options': ['諦める', '努力する', '怠ける', '避ける'], 'answer': '努力する', 'explanation': "'endeavor' は「努力する、試みる」という意味です。", 'derived_word': 'strive (努力する)'}, {'question': "'eradicate'", 'options': ['育てる', '根絶する', '広める', '維持する'], 'answer': '根絶する', 'explanation': "'eradicate' は「根絶する、撲滅する」という意味です。", 'derived_word': 'eliminate (排除する)'}, {'question': "'excel'", 'options': ['劣る', '優れる', '失敗する', '平均的である'], 'answer': '優れる', 'explanation': "'excel' は「優れる、秀でる」という意味です。", 'derived_word': 'surpass (超越する)'}, {'question': "'flourish'", 'options': ['衰退する', '繁栄する', '枯れる', '停滞する'], 'answer': '繁栄する', 'explanation': "'flourish' は「繁栄する、栄える」という意味です。", 'derived_word': 'thrive (繁盛する)'}], 'Chapter 9': [{'question': "'ultimate'", 'options': ['最初の', '究極の', '中間の', '普通の'], 'answer': '究極の', 'explanation': "'ultimate' は「究極の、最終的な」という意味です。", 'derived_word': 'final (最終の)'}, {'question': "'unique'", 'options': ['一般的な', '独特の', '似ている', '平凡な'], 'answer': '独特の', 'explanation': "'unique' は「独特の、唯一の」という意味です。", 'derived_word': 'distinctive (独特の)'}, {'question': "'valid'", 'options': ['無効な', '有効な', '不正確な', '曖昧な'], 'answer': '有効な', 'explanation': "'valid' は「有効な、妥当な」という意味です。", 'derived_word': 'legitimate (合法的な)'}, {'question': "'vast'", 'options': ['狭い', '広大な', '小さい', '限られた'], 'answer': '広大な', 'explanation': "'vast' は「広大な、莫大な」という意味です。", 'derived_word': 'enormous (莫大な)'}, {'question': "'fragile'", 'options': ['丈夫な', '壊れやすい', '硬い', '柔軟な'], 'answer': '壊れやすい', 'explanation': "'fragile' は「壊れやすい、もろい」という意味です。", 'derived_word': 'brittle (脆い)'}], 'Chapter 10': [{'question': "'genuine'", 'options': ['偽物の', '本物の', '疑わしい', '模倣の'], 'answer': '本物の', 'explanation': "'genuine' は「本物の、誠実な」という意味です。", 'derived_word': 'authentic (本物の)'}, {'question': "'humble'", 'options': ['傲慢な', '謙虚な', '派手な', '自信のある'], 'answer': '謙虚な', 'explanation': "'humble' は「謙虚な、質素な」という意味です。", 'derived_word': 'modest (控えめな)'}, {'question': "'immense'", 'options': ['微小な', '巨大な', '普通の', '限定された'], 'answer': '巨大な', 'explanation': "'immense' は「巨大な、計り知れない」という意味です。", 'derived_word': 'colossal (巨大な)'}, {'question': "'intense'", 'options': ['穏やかな', '激しい', '薄い', '弱い'], 'answer': '激しい', 'explanation': "'intense' は「激しい、強烈な」という意味です。", 'derived_word': 'fierce (猛烈な)'}, {'question': "'modest'", 'options': ['派手な', '控えめな', '大胆な', '過度な'], 'answer': '控えめな', 'explanation': "'modest' は「控えめな、謙虚な」という意味です。", 'derived_word': 'unassuming (控えめな)'}], 'Chapter 11': [{'question': "'notable'", 'options': ['目立たない', '注目すべき', '普通の', '取るに足らない'], 'answer': '注目すべき', 'explanation': "'notable' は「注目すべき、著名な」という意味です。", 'derived_word': 'remarkable (注目すべき)'}, {'question': "'obscure'", 'options': ['明確な', '曖昧な', '知られている', '輝かしい'], 'answer': '曖昧な', 'explanation': "'obscure' は「不明瞭な、曖昧な」という意味です。", 'derived_word': 'unclear (不明瞭な)'}, {'question': "'peculiar'", 'options': ['一般的な', '特有の', '普通の', '共有された'], 'answer': '特有の', 'explanation': "'peculiar' は「独特の、変な」という意味です。", 'derived_word': 'odd (奇妙な)'}, {'question': "'rigid'", 'options': ['柔軟な', '厳格な', '緩い', '柔らかい'], 'answer': '厳格な', 'explanation': "'rigid' は「厳格な、硬直した」という意味です。", 'derived_word': 'inflexible (融通の利かない)'}, {'question': "'sparse'", 'options': ['密な', 'まばらな', '豊富な', 'ぎっしり詰まった'], 'answer': 'まばらな', 'explanation': "'sparse' は「まばらな、希薄な」という意味です。", 'derived_word': 'scattered (散らばった)'}], 'Chapter 12': [{'question': "'subtle'", 'options': ['明白な', '微妙な', '粗雑な', '直接的な'], 'answer': '微妙な', 'explanation': "'subtle' は「微妙な、巧妙な」という意味です。", 'derived_word': 'delicate (繊細な)'}, {'question': "'trivial'", 'options': ['重要な', '些細な', '深刻な', '主要な'], 'answer': '些細な', 'explanation': "'trivial' は「些細な、取るに足らない」という意味です。", 'derived_word': 'insignificant (取るに足らない)'}, {'question': "'unanimous'", 'options': ['意見が分かれる', '満場一致の', '反対の', '多様な'], 'answer': '満場一致の', 'explanation': "'unanimous' は「満場一致の、異議のない」という意味です。", 'derived_word': 'agreed (合意した)'}, {'question': "'vague'", 'options': ['明確な', '漠然とした', '正確な', '具体的な'], 'answer': '漠然とした', 'explanation': "'vague' は「漠然とした、不明瞭な」という意味です。", 'derived_word': 'ambiguous (曖昧な)'}, {'question': "'witty'", 'options': ['愚かな', '気の利いた', '退屈な', '真面目な'], 'answer': '気の利いた', 'explanation': "'witty' は「気の利いた、機知に富んだ」という意味です。", 'derived_word': 'clever (気の利いた)'}], 'Chapter 13': [{'question': "'abolish'", 'options': ['設立する', '廃止する', '強化する', '支持する'], 'answer': '廃止する', 'explanation': "'abolish' は「廃止する、撤廃する」という意味です。", 'derived_word': 'eliminate (排除する)'}, {'question': "'acknowledge'", 'options': ['否定する', '認める', '無視する', '拒否する'], 'answer': '認める', 'explanation': "'acknowledge' は「認める、承認する」という意味です。", 'derived_word': 'recognize (認める)'}, {'question': "'compromise'", 'options': ['対立する', '妥協する', '主張する', '勝つ'], 'answer': '妥協する', 'explanation': "'compromise' は「妥協する、和解する」という意味です。", 'derived_word': 'settlement (和解)'}, {'question': "'confront'", 'options': ['避ける', '直面する', '隠れる', '逃げる'], 'answer': '直面する', 'explanation': "'confront' は「直面する、対決する」という意味です。", 'derived_word': 'face (直面する)'}, {'question': "'decline'", 'options': ['増加する', '減少する', '安定する', '発展する'], 'answer': '減少する', 'explanation': "'decline' は「減少する、衰退する、辞退する」という意味です。", 'derived_word': 'decrease (減少する)'}], 'Chapter 14': [{'question': "'endorse'", 'options': ['反対する', '支持する', '批判する', '無視する'], 'answer': '支持する', 'explanation': "'endorse' は「支持する、是認する」という意味です。", 'derived_word': 'approve (承認する)'}, {'question': "'eradicate'", 'options': ['繁殖させる', '根絶する', '広める', '維持する'], 'answer': '根絶する', 'explanation': "'eradicate' は「根絶する、撲滅する」という意味です。", 'derived_word': 'destroy (根絶する)'}, {'question': "'fluctuate'", 'options': ['安定する', '変動する', '固定する', '減少する'], 'answer': '変動する', 'explanation': "'fluctuate' は「変動する、上下する」という意味です。", 'derived_word': 'vary (変動する)'}, {'question': "'intensify'", 'options': ['弱める', '強める', '減らす', '緩和する'], 'answer': '強める', 'explanation': "'intensify' は「強める、激しくする」という意味です。", 'derived_word': 'strengthen (強化する)'}, {'question': "'omit'", 'options': ['含める', '省略する', '強調する', '追加する'], 'answer': '省略する', 'explanation': "'omit' は「省略する、削除する」という意味です。", 'derived_word': 'exclude (除外する)'}], 'Chapter 15': [{'question': "'precede'", 'options': ['後続する', '先行する', '同時に起こる', '中断する'], 'answer': '先行する', 'explanation': "'precede' は「先行する、～より前に起こる」という意味です。", 'derived_word': 'forego (先行する)'}, {'question': "'reiterate'", 'options': ['一度だけ言う', '繰り返す', '沈黙する', '修正する'], 'answer': '繰り返す', 'explanation': "'reiterate' は「繰り返して言う、反復する」という意味です。", 'derived_word': 'repeat (繰り返す)'}, {'question': "'suppress'", 'options': ['解放する', '抑圧する', '奨励する', '支持する'], 'answer': '抑圧する', 'explanation': "'suppress' は「抑圧する、鎮圧する」という意味です。", 'derived_word': 'repress (抑える)'}, {'question': "'undergo'", 'options': ['避ける', '経験する', '始める', '拒否する'], 'answer': '経験する', 'explanation': "'undergo' は「経験する、耐え忍ぶ」という意味です。", 'derived_word': 'experience (経験する)'}, {'question': "'validate'", 'options': ['無効にする', '検証する', '否定する', '無視する'], 'answer': '検証する', 'explanation': "'validate' は「検証する、有効にする」という意味です。", 'derived_word': 'confirm (確認する)'}], 'Chapter 16': [{'question': 'It is important for us to protect the environment.', 'options': ['私たちが環境を保護することは重要ではない。', '私たちが環境を破壊することは重要である。', '私たちが環境を保護することは重要である。', '環境を保護することは私たちにとって不可能である。'], 'answer': '私たちが環境を保護することは重要である。', 'explanation': "'It is important for us to protect the environment.' は「私たちが環境を保護することは重要である」という意味です。", 'derived_word': '和訳問題'}, {'question': 'He tried to explain the difficult problem to me.', 'options': ['彼は私に難しい問題を説明しようとしなかった。', '彼は私に難しい問題を説明してくれた。', '彼は私に難しい問題を説明しようとした。', '彼はその問題が難しすぎると言った。'], 'answer': '彼は私に難しい問題を説明しようとした。', 'explanation': "'tried to explain' は「説明しようとした」という意味です。", 'derived_word': '和訳問題'}, {'question': 'She has been studying English for five years.', 'options': ['彼女は5年間英語を勉強していた。', '彼女は5年間英語を勉強し始めた。', '彼女は5年間英語を勉強している。', '彼女は5年間英語を勉強するだろう。'], 'answer': '彼女は5年間英語を勉強している。', 'explanation': "'has been studying' は現在完了進行形で、「ずっと～し続けている」という意味です。", 'derived_word': '和訳問題'}, {'question': 'The book which I read yesterday was very interesting.', 'options': ['私が昨日読んだ本は全く面白くなかった。', '私が昨日読んだ本はとても面白かった。', '私は昨日とても面白い本を読んだ。', '昨日、本を読んで、それがとても面白かった。'], 'answer': '私が昨日読んだ本はとても面白かった。', 'explanation': "'which I read yesterday' は関係代名詞節で、'the book' を修飾しています。", 'derived_word': '和訳問題'}, {'question': 'If I were you, I would accept the offer.', 'options': ['もし私があなたなら、その申し出を受け入れないだろう。', 'もし私があなたなら、その申し出を受け入れるだろう。', '私はあなただったので、その申し出を受け入れた。', 'あなたはその申し出を受け入れるべきだ。'], 'answer': 'もし私があなたなら、その申し出を受け入れるだろう。', 'explanation': "'If I were you, I would accept...' は仮定法過去で、「もし私があなたなら～だろう」という意味です。", 'derived_word': '和訳問題'}], 'Chapter 17': [{'question': 'He succeeded in solving the difficult problem.', 'options': ['彼は難しい問題を解決できなかった。', '彼は難しい問題を解決しようとした。', '彼は難しい問題を解決することに成功した。', '彼は難しい問題を解決するのを諦めた。'], 'answer': '彼は難しい問題を解決することに成功した。', 'explanation': "'succeeded in doing' は「～することに成功した」という意味です。", 'derived_word': '和訳問題'}, {'question': 'She devoted herself to helping the poor.', 'options': ['彼女は貧しい人々を助けることに反対した。', '彼女は貧しい人々を助けることに身を捧げた。', '彼女は貧しい人々を助けるのをやめた。', '彼女は貧しい人々を助けたくなかった。'], 'answer': '彼女は貧しい人々を助けることに身を捧げた。', 'explanation': "'devoted herself to doing' は「～することに専念する/身を捧げる」という意味です。", 'derived_word': '和訳問題'}, {'question': "I'm looking forward to hearing from you soon.", 'options': ['私はすぐにあなたから便りを聞きたくない。', '私はすぐにあなたから便りを聞くことを期待していない。', '私はすぐにあなたから便りを聞くのを楽しみにしている。', '私はすぐにあなたに手紙を書くつもりだ。'], 'answer': '私はすぐにあなたから便りを聞くのを楽しみにしている。', 'explanation': "'look forward to doing' は「～するのを楽しみにする」という意味です。'to' の後は動名詞になります。", 'derived_word': '和訳問題'}, {'question': 'The news made her very sad.', 'options': ['そのニュースは彼女を喜ばせた。', 'そのニュースは彼女を全く悲しませなかった。', 'そのニュースは彼女をとても悲しませた。', '彼女はニュースを聞いて悲しかった。'], 'answer': 'そのニュースは彼女をとても悲しませた。', 'explanation': "'make + 目的語 + 形容詞' は「目的語を～の状態にする」という意味です。", 'derived_word': '和訳問題'}, {'question': 'It is no use crying over spilled milk.', 'options': ['こぼれた牛乳について泣くことは意味がある。', 'こぼれた牛乳を嘆いても仕方がない。', 'こぼれた牛乳を拾い上げるべきだ。', '牛乳がこぼれても心配する必要はない。'], 'answer': 'こぼれた牛乳を嘆いても仕方がない。', 'explanation': "'It is no use doing' は「～しても無駄である/仕方がない」という慣用表現です。", 'derived_word': '和訳問題'}], 'Chapter 18': [{'question': 'What do you think of his new plan?', 'options': ['彼の新しい計画についてどう思いますか？', '彼は新しい計画を考えている。', '彼の新しい計画はうまくいきますか？', 'あなたは彼の新しい計画が好きですか？'], 'answer': '彼の新しい計画についてどう思いますか？', 'explanation': "'What do you think of ～?' は「～についてどう思いますか？」という意味です。", 'derived_word': '和訳問題'}, {'question': 'He was surprised at the sudden news.', 'options': ['彼はその突然のニュースに驚かなかった。', '彼はその突然のニュースを期待していた。', '彼はその突然のニュースに驚いた。', '彼はその突然のニュースを無視した。'], 'answer': '彼はその突然のニュースに驚いた。', 'explanation': "'be surprised at ～' は「～に驚く」という意味です。", 'derived_word': '和訳問題'}, {'question': 'The picture was painted by a famous artist.', 'options': ['その絵は有名な芸術家によって描かれなかった。', 'その絵は有名な芸術家が描いた。', 'その絵は有名な芸術家によって描かれた。', '有名な芸術家はその絵を展示した。'], 'answer': 'その絵は有名な芸術家によって描かれた。', 'explanation': "'was painted by ～' は受動態で、「～によって描かれた」という意味です。", 'derived_word': '和訳問題'}, {'question': 'Despite the heavy rain, they went out.', 'options': ['大雨にもかかわらず、彼らは出かけた。', '大雨だったので、彼らは出かけなかった。', '大雨のために、彼らは出かけた。', '大雨が止んでから、彼らは出かけた。'], 'answer': '大雨にもかかわらず、彼らは出かけた。', 'explanation': "'Despite ～' は「～にもかかわらず」という意味です。", 'derived_word': '和訳問題'}, {'question': 'The more you practice, the better you will become.', 'options': ['練習すればするほど、悪くなるだろう。', '練習すればするほど、上手になるだろう。', '練習はあまり重要ではない。', 'あなたはもっと練習するべきだ。'], 'answer': '練習すればするほど、上手になるだろう。', 'explanation': "'The more ..., the better ...' は「～すればするほど、ますます～になる」という比較構文です。", 'derived_word': '和訳問題'}], 'Chapter 19': [{'question': 'He seems to have forgotten his wallet.', 'options': ['彼は財布を忘れたようだ。', '彼は財布を忘れていないようだ。', '彼は財布を忘れたことを否定した。', '彼は財布を忘れるべきではない。'], 'answer': '彼は財布を忘れたようだ。', 'explanation': "'seems to have done' は「～したようだ」という完了不定詞の表現です。", 'derived_word': '和訳問題'}, {'question': 'It is believed that he is a genius.', 'options': ['彼は天才だと信じられていない。', '彼が天才であることは事実だ。', '彼は天才だと信じられている。', '彼が天才であると彼は信じている。'], 'answer': '彼は天才だと信じられている。', 'explanation': "'It is believed that ～' は「～だと信じられている」という受動態の構文です。", 'derived_word': '和訳問題'}, {'question': 'He was made to work all day long.', 'options': ['彼は一日中働くことを望んだ。', '彼は一日中働くように強制された。', '彼は一日中働いた。', '彼は一日中働かされることを避けた。'], 'answer': '彼は一日中働くように強制された。', 'explanation': "'be made to do' は「～させられる」という使役動詞の受動態です。", 'derived_word': '和訳問題'}, {'question': 'The teacher told us not to be late for school.', 'options': ['先生は私たちに学校に遅刻するように言った。', '先生は私たちに学校に遅刻しないように言った。', '先生は私たちが学校に遅刻しても気にしなかった。', '先生は私たちが学校に遅刻するのを許可した。'], 'answer': '先生は私たちに学校に遅刻しないように言った。', 'explanation': "'tell + 目的語 + not to do' は「目的語に～しないように言う」という意味です。", 'derived_word': '和訳問題'}, {'question': 'I wonder if he will come to the party.', 'options': ['彼がパーティーに来るかどうか知っている。', '彼がパーティーに来るかどうか疑問に思う。', '彼がパーティーに来ることは確実だ。', '私は彼がパーティーに来ることを願っている。'], 'answer': '彼がパーティーに来るかどうか疑問に思う。', 'explanation': "'wonder if ～' は「～かどうかと思う/疑問に思う」という意味です。", 'derived_word': '和訳問題'}], 'Chapter 20': [{'question': 'It took me two hours to finish my homework.', 'options': ['宿題を終えるのに2時間かからなかった。', '宿題を終えるのに2時間かかった。', '私は2時間で宿題を終えられなかった。', '宿題を終えるのに2時間はかからないだろう。'], 'answer': '宿題を終えるのに2時間かかった。', 'explanation': "'It takes + 人 + 時間 + to do' は「人が～するのに時間がかかる」という意味です。", 'derived_word': '和訳問題'}, {'question': 'I had my car repaired yesterday.', 'options': ['私は昨日車を修理しなかった。', '私は昨日車を修理させた。', '私は昨日車を自分で修理した。', '私の車は昨日修理された。'], 'answer': '私は昨日車を修理させた。', 'explanation': "'have + 目的語 + 過去分詞' は「目的語を～してもらう」という使役の意味です。", 'derived_word': '和訳問題'}, {'question': 'He is used to getting up early.', 'options': ['彼は早起きに慣れていない。', '彼は早起きするだろう。', '彼は早起きするのに慣れている。', '彼は以前は早起きしていた。'], 'answer': '彼は早起きするのに慣れている。', 'explanation': "'be used to doing' は「～するのに慣れている」という意味です。'used to do' は「以前は～していた」という意味です。", 'derived_word': '和訳問題'}, {'question': 'There is no knowing what will happen next.', 'options': ['次に何が起こるか知っている。', '次に何が起こるか知ることはできない。', '次に何が起こるか予測できる。', '次に何が起こるか心配する必要はない。'], 'answer': '次に何が起こるか知ることはできない。', 'explanation': "'There is no doing' は「～することはできない」という意味です。", 'derived_word': '和訳問題'}, {'question': 'This is the place where I first met her.', 'options': ['ここは私が初めて彼女に会わなかった場所だ。', 'ここは私が初めて彼女に会った場所だ。', '彼女は初めてここで私に会った。', '私はここで彼女と初めて会ったことを覚えていない。'], 'answer': 'ここは私が初めて彼女に会った場所だ。', 'explanation': "'where I first met her' は関係副詞節で、'the place' を修飾しています。", 'derived_word': '和訳問題'}]}

QUESTIONS_PER_STAGE = 10


QUESTIONS_PER_STAGE = 10
TICK_SECONDS = 0.5
ROUTE = [(35, 55), (150, 55), (190, 75), (205, 115), (280, 130), (355, 130), (390, 165), (410, 205), (500, 205), (560, 185), (590, 145), (620, 115), (720, 115)]
TOWER_SPOTS = [(250, 82), (350, 185), (515, 135)]


def new_enemy(enemy_id):
    return {"id": enemy_id, "p": 0.0, "hp": 2, "max_hp": 2, "x": ROUTE[0][0], "y": ROUTE[0][1]}


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
        "tower_cooldowns": [0, 0, 0], "kills": 0, "message": "ゲーム開始！敵が道を進みます。タワーは射程内の敵を自動攻撃します。"
    }
    state["enemies"].append(new_enemy(state["next_enemy_id"]))
    state["next_enemy_id"] += 1
    return render_question(state, "🏰 ゲーム開始！初期コイン50枚でタワーを強化できます。")


def hud(state):
    idx = state["index"]
    total = len(state["questions"])
    stage = idx // QUESTIONS_PER_STAGE + 1
    return (
        f"## 🏰 FlashVocab Defense\n"
        f"**ステージ：** {stage}　**問題：** {min(idx + 1, total)} / {total}\n\n"
        f"❤️ **城HP：** {state['hp']} / 100　　🪙 **コイン：** {state['coins']}　　"
        f"🎯 **正解：** {state['score']}　　🏹 **タワーLv：** {state['tower_level']}　　"
        f"👾 **撃破：** {state['kills']}"
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
        x, y = e["x"], e["y"]
        bits.append(f'<g transform="translate({x:.1f} {y:.1f})"><path d="M-8 -8l-7 -13 13 5M8 -8l7 -13 -13 5" fill="#a8e56a" stroke="#315c28" stroke-width="2"/><circle r="12" fill="#a8e56a" stroke="#315c28" stroke-width="2"/><circle cx="-4" cy="-2" r="2" fill="#142318"/><circle cx="4" cy="-2" r="2" fill="#142318"/><path d="M-4 4q4 4 8 0" fill="none" stroke="#142318" stroke-width="2"/><rect x="-13" y="-21" width="26" height="4" rx="2" fill="#3b2020"/><rect x="-13" y="-21" width="{26*max(0,e["hp"])/e["max_hp"]:.1f}" height="4" rx="2" fill="#ff6b6b"/></g>')
    bits.append('</svg><div class="battle-foot"><span>👾 敵：HPバーが0で撃破</span><span>🏹 タワー：射程内を自動攻撃</span><span>💥 ゴール到達で城HP減少</span></div></div>')
    bits.append('''<style>.battle-wrap{border:1px solid #3c7658;border-radius:14px;overflow:hidden;background:#102d21;color:#eef9f0;margin:8px 0 14px}.battle-head,.battle-foot{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;padding:10px 14px;background:#183d2b;font-size:13px}.battle-wrap svg{display:block;width:100%;height:auto}.battle-foot{color:#d7f3df}</style>''')
    return "".join(bits)


def simulate_battle(state):
    if state.get("finished"):
        return
    state["ticks"] += 1
    # Spawn an enemy every 6 ticks (about 3 seconds), while the castle stands.
    if state["ticks"] % 6 == 0 and len(state["enemies"]) < 8 and state["hp"] > 0:
        state["enemies"].append(new_enemy(state["next_enemy_id"]))
        state["next_enemy_id"] += 1
    # Move enemies along the route; a reached goal damages the castle.
    for e in state["enemies"]:
        e["p"] += 0.009
        e["x"], e["y"] = route_position(e["p"])
    survivors = []
    for e in state["enemies"]:
        if e["p"] >= 1:
            state["hp"] = max(0, state["hp"] - 15)
            state["message"] = "🚨 敵がゴールに到達！城HPが15減少しました。"
        else:
            survivors.append(e)
    state["enemies"] = survivors
    # Towers fire automatically at the nearest enemy in range. Each shot deals 1 damage.
    state["shots"] = []
    for i, (tx, ty) in enumerate(TOWER_SPOTS):
        state["tower_cooldowns"][i] = max(0, state["tower_cooldowns"][i] - 1)
        radius = 90 + (state["tower_level"] - 1) * 8
        targets = [e for e in state["enemies"] if ((e["x"]-tx)**2 + (e["y"]-ty)**2)**0.5 <= radius]
        if targets and state["tower_cooldowns"][i] <= 0:
            target = min(targets, key=lambda e: ((e["x"]-tx)**2 + (e["y"]-ty)**2))
            target["hp"] -= 1 + (state["tower_level"] - 1) // 2
            state["shots"].append({"x1": tx, "y1": ty, "x2": target["x"], "y2": target["y"]})
            state["tower_cooldowns"][i] = max(1, 4 - (state["tower_level"] - 1) // 2)
            if target["hp"] <= 0:
                state["coins"] += 5
                state["kills"] += 1
                state["message"] = "💥 敵を撃破！ボーナス+5コイン！"
    state["enemies"] = [e for e in state["enemies"] if e["hp"] > 0]
    if state["hp"] <= 0:
        state["finished"] = True
        state["message"] = "💥 城が陥落しました。ゲーム開始ボタンで再挑戦できます。"


def render_question(state, message=""):
    if state["index"] >= len(state["questions"]) or state["hp"] <= 0:
        state["finished"] = True
        total = len(state["questions"])
        accuracy = state["score"] / total * 100 if total else 0
        title = "## 💥 城が陥落しました！" if state["hp"] <= 0 else "## 🏆 全問題クリア！"
        summary = f"{title}\n\n正解数：**{state['score']} / {total}**　正答率：**{accuracy:.1f}%**　獲得コイン：**{state['coins']}**　撃破数：**{state['kills']}**"
        if state["wrong"]:
            summary += "\n\n### 📘 復習する問題\n"
            for i, q in enumerate(state["wrong"], 1):
                summary += f"\n**{i}. {q['question']}**\n- 正解：{q['answer']}\n- 解説：{q.get('explanation', '解説はありません。')}\n"
        return hud(state), summary, gr.update(choices=[], value=None), gr.update(visible=False), battle_html(state), gr.update(interactive=False), state
    q = state["questions"][state["index"]]
    remaining = max(0, len(state["questions"]) - state["index"] - 1)
    question_text = f"### ⚔️ 英語クイズ\n\n**{q['question']}**\n\n{message}\n\n敵が城に到達すると城HPが15減ります。不正解でも城HPが10減ります。"
    return hud(state), question_text, gr.update(choices=q.get("options", []), value=None), gr.update(visible=True), battle_html(state), gr.update(interactive=not state["finished"]), state


def answer_question(choice, state):
    if not state:
        return start_game()
    if state.get("finished"):
        return render_question(state, "ゲームは終了しています。ゲーム開始ボタンを押してください。")
    if not choice:
        return hud(state), "選択肢を選んでから回答してください。", gr.update(), gr.update(visible=True), battle_html(state), gr.update(), state
    q = state["questions"][state["index"]]
    if choice == q["answer"]:
        state["score"] += 1
        state["coins"] += 10
        state["tower_level"] = 1 + state["score"] // 5
        message = f"✅ **正解！** +10コイン。\n\n📖 {q.get('explanation', '')}"
    else:
        state["wrong"].append(q)
        state["hp"] = max(0, state["hp"] - 10)
        message = f"❌ **不正解！** 城HPが10減少。\n\n**正解：** {q['answer']}\n\n📖 {q.get('explanation', '')}"
    state["index"] += 1
    if state["index"] % QUESTIONS_PER_STAGE == 0 and state["hp"] > 0 and state["index"] < len(state["questions"]):
        state["coins"] += 20
        message += "\n\n🌟 **ステージ突破ボーナス：+20コイン！**"
    state["message"] = message
    return render_question(state, message)


def upgrade_tower(state):
    if not state:
        return start_game()
    if state.get("finished"):
        return hud(state), battle_html(state), state, "ゲーム終了後は強化できません。"
    cost = 30 * state["tower_level"]
    if state["coins"] < cost:
        return hud(state), battle_html(state), state, f"コイン不足！強化には🪙 {cost}枚必要です。"
    state["coins"] -= cost
    state["tower_level"] += 1
    state["message"] = f"⬆️ タワーをLv.{state['tower_level']}に強化！攻撃力・射程・攻撃速度が上がりました。"
    return hud(state), battle_html(state), state, state["message"]


def timer_tick(state):
    if not state:
        return "## 🏰 FlashVocab Defense", "", state, gr.update(interactive=False)
    if not state.get("finished"):
        simulate_battle(state)
        if state.get("hp", 0) <= 0:
            state["finished"] = True
    return hud(state), battle_html(state), state, gr.update(interactive=not state.get("finished", False))


with gr.Blocks(title="FlashVocab Defense", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏰 FlashVocab Defense\n英単語を解いて城を守り、コインでタワーを強化しよう！")
    status = gr.Markdown()
    battle_view = gr.HTML()
    with gr.Row():
        upgrade_btn = gr.Button("⬆️ タワー強化（コイン消費）", variant="secondary")
        upgrade_message = gr.Markdown("強化費用：Lv.1なら30コイン")
    question = gr.Markdown("「ゲーム開始」を押してスタート！")
    choice = gr.Radio(choices=[], label="正しい答えを選んでね")
    with gr.Row():
        answer_btn = gr.Button("⚔️ 回答する", variant="primary")
        start_btn = gr.Button("🔄 ゲーム開始 / もう一度遊ぶ")
    state = gr.State({})
    timer = gr.Timer(TICK_SECONDS)

    start_btn.click(start_game, outputs=[status, question, choice, answer_btn, battle_view, upgrade_btn, state])
    answer_btn.click(answer_question, inputs=[choice, state], outputs=[status, question, choice, answer_btn, battle_view, upgrade_btn, state])
    upgrade_btn.click(upgrade_tower, inputs=[state], outputs=[status, battle_view, state, upgrade_message])
    timer.tick(timer_tick, inputs=[state], outputs=[status, battle_view, state, answer_btn])

    gr.Markdown("---\n**戦闘ルール：** 敵は約3秒ごとに出現し、ゴールに到達すると城HPが15減ります。不正解でも城HPが10減少。タワーは射程内の敵を自動攻撃し、撃破すると+5コイン。正解で+10コイン、10問ごとに+20コイン。タワー強化はレベルに応じたコインを消費し、攻撃力・射程・攻撃速度が上がります。")

if __name__ == "__main__":
    # RenderのPORT環境変数を使い、外部からアクセスできるアドレスで起動する
    port = int(os.environ.get("PORT", "10000"))
    demo.launch(server_name="0.0.0.0", server_port=port)
