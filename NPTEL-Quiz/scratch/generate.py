import json
  
def generate_html():
    with open('data.json', 'r', encoding='utf-8') as f:
        questions_json_str = f.read()
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NPTEL Sustainable Development Quiz</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #6366F1;
            --primary-hover: #4F46E5;
            --primary-light: #EEF2FF;
            --secondary: #EC4899;
            --success: #10B981;
            --danger: #EF4444;
            --background: #0F172A;
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --border: #334155;
            
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.05);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
        }}

        body {{
            background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
            color: var(--text-main);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }}

        /* Dynamic background elements */
        .bg-orb-1 {{
            position: fixed;
            top: -100px;
            left: -100px;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, rgba(0,0,0,0) 70%);
            z-index: -1;
            filter: blur(40px);
            animation: float 10s ease-in-out infinite alternate;
        }}

        .bg-orb-2 {{
            position: fixed;
            bottom: -100px;
            right: -100px;
            width: 500px;
            height: 500px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(236,72,153,0.15) 0%, rgba(0,0,0,0) 70%);
            z-index: -1;
            filter: blur(40px);
            animation: float 12s ease-in-out infinite alternate-reverse;
        }}

        @keyframes float {{
            0% {{ transform: translate(0, 0) scale(1); }}
            100% {{ transform: translate(30px, 30px) scale(1.1); }}
        }}

        .container {{
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            max-width: 800px;
            width: 100%;
            border-radius: 24px;
            box-shadow: var(--glass-shadow);
            padding: 40px;
            position: relative;
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(40px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        h1 {{
            text-align: center;
            font-size: 36px;
            font-weight: 800;
            background: linear-gradient(to right, #818CF8, #F472B6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            letter-spacing: -0.02em;
        }}
        
        .subtitle {{
            text-align: center;
            color: var(--text-muted);
            margin-bottom: 40px;
            font-size: 18px;
            font-weight: 400;
        }}

        /* --- Setup Section --- */
        .setup-section {{
            display: flex;
            flex-direction: column;
            gap: 30px;
        }}

        .mode-selection h3, .week-selection h3 {{
            font-size: 18px;
            color: var(--text-main);
            margin-bottom: 16px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .mode-selection h3::before, .week-selection h3::before {{
            content: '';
            display: inline-block;
            width: 8px;
            height: 24px;
            background: var(--primary);
            border-radius: 4px;
        }}

        .mode-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }}

        .mode-card {{
            background: rgba(30, 41, 59, 0.4);
            border: 2px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .mode-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.05), transparent);
            transform: translateX(-100%);
            transition: transform 0.5s;
        }}

        .mode-card:hover::before {{
            transform: translateX(100%);
        }}

        .mode-card:hover {{
            border-color: rgba(99, 102, 241, 0.5);
            transform: translateY(-4px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            background: rgba(49, 46, 129, 0.2);
        }}

        .mode-card.selected {{
            border-color: var(--primary);
            background: rgba(79, 70, 229, 0.15);
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) inset;
        }}

        .mode-icon {{
            font-size: 32px;
            margin-bottom: 12px;
            display: block;
        }}

        .mode-title {{
            font-size: 18px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 4px;
        }}

        .mode-desc {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        .week-selection {{
            display: none;
            animation: fadeIn 0.4s ease;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .week-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 12px;
        }}

        .week-btn {{
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 0;
            color: var(--text-main);
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .week-btn:hover {{
            background: rgba(79, 70, 229, 0.2);
            border-color: var(--primary);
            transform: scale(1.05);
        }}

        .week-btn.selected {{
            background: var(--primary);
            border-color: var(--primary);
            color: white;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }}

        .btn-start-wrapper {{
            text-align: center;
            margin-top: 20px;
        }}

        .btn-start {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            padding: 16px 48px;
            font-size: 20px;
            font-weight: 700;
            border-radius: 100px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(236, 72, 153, 0.3);
            opacity: 0.5;
            pointer-events: none;
        }}

        .btn-start.active {{
            opacity: 1;
            pointer-events: auto;
        }}

        .btn-start.active:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 12px 24px rgba(236, 72, 153, 0.4);
        }}

        /* --- Quiz Section --- */
        .quiz-section {{
            display: none;
        }}

        .progress-container {{
            margin-bottom: 30px;
        }}

        .progress-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .week-badge {{
            background: rgba(99, 102, 241, 0.15);
            color: #A5B4FC;
            padding: 6px 14px;
            border-radius: 100px;
            font-size: 14px;
            font-weight: 600;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }}

        .progress-text {{
            font-size: 15px;
            font-weight: 600;
            color: var(--text-muted);
        }}

        .progress-bar-bg {{
            background-color: var(--border);
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
        }}

        .progress-bar-fill {{
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            height: 100%;
            width: 0%;
            transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 5px;
        }}

        .question-box {{
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid var(--glass-border);
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 24px;
        }}

        .question-text {{
            font-size: 22px;
            font-weight: 500;
            line-height: 1.5;
            color: var(--text-main);
        }}

        .options-grid {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-bottom: 24px;
        }}

        .option-btn {{
            background: rgba(30, 41, 59, 0.6);
            border: 2px solid var(--border);
            padding: 18px 24px;
            border-radius: 16px;
            text-align: left;
            font-size: 17px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            color: var(--text-main);
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
        }}

        .option-btn::before {{
            content: '';
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 4px;
            background: transparent;
            transition: background 0.2s;
        }}

        .option-btn:hover:not(:disabled) {{
            border-color: rgba(99, 102, 241, 0.5);
            background: rgba(30, 41, 59, 0.9);
            transform: translateX(4px);
        }}

        .option-btn:hover:not(:disabled)::before {{
            background: var(--primary);
        }}

        .option-btn.correct {{
            background: rgba(16, 185, 129, 0.1);
            border-color: var(--success);
            color: #34D399;
        }}

        .option-btn.correct::before {{
            background: var(--success);
        }}

        .option-btn.wrong {{
            background: rgba(239, 68, 68, 0.1);
            border-color: var(--danger);
            color: #F87171;
        }}
        
        .option-btn.wrong::before {{
            background: var(--danger);
        }}

        .option-btn:disabled {{
            cursor: not-allowed;
        }}

        .feedback-area {{
            min-height: 28px;
            margin-bottom: 24px;
            font-weight: 600;
            font-size: 18px;
            text-align: center;
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.3s ease;
        }}

        .feedback-area.show {{
            opacity: 1;
            transform: translateY(0);
        }}

        .feedback-area.correct {{
            color: var(--success);
            text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
        }}

        .feedback-area.wrong {{
            color: var(--danger);
            text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
        }}

        .action-buttons {{
            display: flex;
            justify-content: flex-end;
        }}

        .btn-next {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 14px 32px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 100px;
            cursor: pointer;
            display: none;
            transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            animation: fadeIn 0.3s ease;
        }}

        .btn-next:hover {{
            background: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
        }}

        /* --- Results Section --- */
        .result-section {{
            display: none;
            text-align: center;
        }}

        .score-circle {{
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: conic-gradient(var(--primary) 0%, rgba(255,255,255,0.05) 0%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 40px;
            position: relative;
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.2);
            transition: background 1s ease-out;
        }}

        .score-circle::before {{
            content: '';
            position: absolute;
            inset: -10px;
            border-radius: 50%;
            background: conic-gradient(from 0deg, transparent, var(--secondary), transparent);
            z-index: -1;
            animation: spin 4s linear infinite;
            opacity: 0.3;
        }}

        @keyframes spin {{
            100% {{ transform: rotate(360deg); }}
        }}

        .score-circle-inner {{
            width: 150px;
            height: 150px;
            background: var(--background);
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 4px 10px rgba(0,0,0,0.5);
        }}

        .score-percent {{
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(to right, #818CF8, #F472B6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
        }}

        .score-label {{
            font-size: 14px;
            color: var(--text-muted);
            margin-top: 4px;
            font-weight: 500;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            padding: 24px;
            border-radius: 16px;
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid var(--border);
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-4px);
        }}

        .stat-card h3 {{
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .stat-val {{
            font-size: 32px;
            font-weight: 800;
        }}

        .stat-correct .stat-val {{ color: #34D399; text-shadow: 0 0 10px rgba(52, 211, 153, 0.3); }}
        .stat-wrong .stat-val {{ color: #F87171; text-shadow: 0 0 10px rgba(248, 113, 113, 0.3); }}

        .btn-restart {{
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 16px 40px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 100px;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .btn-restart:hover {{
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }}

        /* Responsive */
        @media (max-width: 600px) {{
            .container {{ padding: 24px; border-radius: 16px; }}
            h1 {{ font-size: 28px; }}
            .mode-grid {{ grid-template-columns: 1fr; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

    <div class="bg-orb-1"></div>
    <div class="bg-orb-2"></div>

    <div class="container">
        <!-- Setup Section -->
        <div class="setup-section" id="setupSection">
            <div>
                <h1>Sustainable Dev Quiz</h1>
                <p class="subtitle">Test your knowledge across 12 weeks of NPTEL content.</p>
            </div>
            
            <div class="mode-selection">
                <h3>Select Quiz Mode</h3>
                <div class="mode-grid">
                    <div class="mode-card" data-mode="full">
                        <span class="mode-icon">🌟</span>
                        <div class="mode-title">Full Quiz</div>
                        <div class="mode-desc">All 12 weeks combined</div>
                    </div>
                    <div class="mode-card" data-mode="first_half">
                        <span class="mode-icon">📖</span>
                        <div class="mode-title">First Half</div>
                        <div class="mode-desc">Weeks 1 to 6</div>
                    </div>
                    <div class="mode-card" data-mode="second_half">
                        <span class="mode-icon">🚀</span>
                        <div class="mode-title">Second Half</div>
                        <div class="mode-desc">Weeks 7 to 12</div>
                    </div>
                    <div class="mode-card" data-mode="single">
                        <span class="mode-icon">🎯</span>
                        <div class="mode-title">Single Week</div>
                        <div class="mode-desc">Focus on one week</div>
                    </div>
                </div>
            </div>

            <div class="week-selection" id="weekSelection">
                <h3>Select Week</h3>
                <div class="week-grid">
                    <button class="week-btn" data-week="1">W1</button>
                    <button class="week-btn" data-week="2">W2</button>
                    <button class="week-btn" data-week="3">W3</button>
                    <button class="week-btn" data-week="4">W4</button>
                    <button class="week-btn" data-week="5">W5</button>
                    <button class="week-btn" data-week="6">W6</button>
                    <button class="week-btn" data-week="7">W7</button>
                    <button class="week-btn" data-week="8">W8</button>
                    <button class="week-btn" data-week="9">W9</button>
                    <button class="week-btn" data-week="10">W10</button>
                    <button class="week-btn" data-week="11">W11</button>
                    <button class="week-btn" data-week="12">W12</button>
                </div>
            </div>

            <div class="btn-start-wrapper">
                <button class="btn-start" id="startBtn">Start Adventure</button>
            </div>
        </div>

        <!-- Quiz Section -->
        <div class="quiz-section" id="quizSection">
            <div class="progress-container">
                <div class="progress-header">
                    <div class="week-badge" id="weekBadge">Week 1</div>
                    <div class="progress-text" id="progressText">Question 1 / 10</div>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" id="progressBar"></div>
                </div>
            </div>

            <div class="question-box">
                <div class="question-text" id="questionText">
                    Question goes here?
                </div>
            </div>

            <div class="options-grid" id="optionsGrid">
                <!-- Options injected here -->
            </div>

            <div class="feedback-area" id="feedbackArea"></div>

            <div class="action-buttons">
                <button class="btn-next" id="nextBtn">Next Question →</button>
            </div>
        </div>

        <!-- Result Section -->
        <div class="result-section" id="resultSection">
            <h1>Quiz Completed!</h1>
            <p class="subtitle" id="resultMessage">Great effort! Here is your performance.</p>

            <div class="score-circle" id="scoreCircle">
                <div class="score-circle-inner">
                    <div class="score-percent" id="scorePercent">0%</div>
                    <div class="score-label">SCORE</div>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card stat-correct">
                    <h3>Correct Answers</h3>
                    <div class="stat-val" id="correctCount">0</div>
                </div>
                <div class="stat-card stat-wrong">
                    <h3>Wrong Answers</h3>
                    <div class="stat-val" id="wrongCount">0</div>
                </div>
            </div>

            <button class="btn-restart" id="restartBtn">Take Another Quiz</button>
        </div>
    </div>

    <script>
        const allQuestions = {questions_json_str};

        // DOM Elements
        const setupSection = document.getElementById('setupSection');
        const quizSection = document.getElementById('quizSection');
        const resultSection = document.getElementById('resultSection');
        
        const modeCards = document.querySelectorAll('.mode-card');
        const weekSelection = document.getElementById('weekSelection');
        const weekBtns = document.querySelectorAll('.week-btn');
        const startBtn = document.getElementById('startBtn');

        const weekBadge = document.getElementById('weekBadge');
        const progressText = document.getElementById('progressText');
        const progressBar = document.getElementById('progressBar');
        const questionText = document.getElementById('questionText');
        const optionsGrid = document.getElementById('optionsGrid');
        const feedbackArea = document.getElementById('feedbackArea');
        const nextBtn = document.getElementById('nextBtn');

        const scoreCircle = document.getElementById('scoreCircle');
        const scorePercent = document.getElementById('scorePercent');
        const correctCountEl = document.getElementById('correctCount');
        const wrongCountEl = document.getElementById('wrongCount');
        const resultMessage = document.getElementById('resultMessage');
        const restartBtn = document.getElementById('restartBtn');

        // State
        let selectedMode = null;
        let selectedWeek = null;
        let currentQuestions = [];
        let currentQuestionIndex = 0;
        let score = 0;
        let wrongCount = 0;
        let hasAnswered = false;

        // Utility: Shuffle Array
        function shuffle(array) {{
            let currentIndex = array.length, randomIndex;
            while (currentIndex != 0) {{
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex--;
                [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
            }}
            return array;
        }}

        // Setup Listeners
        modeCards.forEach(card => {{
            card.addEventListener('click', () => {{
                // Remove selected from all
                modeCards.forEach(c => c.classList.remove('selected'));
                // Add to clicked
                card.classList.add('selected');
                selectedMode = card.getAttribute('data-mode');

                if (selectedMode === 'single') {{
                    weekSelection.style.display = 'block';
                    validateStart();
                }} else {{
                    weekSelection.style.display = 'none';
                    selectedWeek = null; // Reset week if not single
                    weekBtns.forEach(b => b.classList.remove('selected'));
                    startBtn.classList.add('active');
                }}
            }});
        }});

        weekBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                weekBtns.forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                selectedWeek = parseInt(btn.getAttribute('data-week'));
                validateStart();
            }});
        }});

        function validateStart() {{
            if (selectedMode === 'single' && !selectedWeek) {{
                startBtn.classList.remove('active');
            }} else {{
                startBtn.classList.add('active');
            }}
        }}

        startBtn.addEventListener('click', () => {{
            if(!startBtn.classList.contains('active')) return;
            startQuiz();
        }});

        nextBtn.addEventListener('click', handleNext);
        restartBtn.addEventListener('click', () => {{
            resultSection.style.display = 'none';
            setupSection.style.display = 'flex';
            // Reset setup state
            selectedMode = null;
            selectedWeek = null;
            modeCards.forEach(c => c.classList.remove('selected'));
            weekBtns.forEach(b => b.classList.remove('selected'));
            weekSelection.style.display = 'none';
            startBtn.classList.remove('active');
        }});

        function startQuiz() {{
            let filtered = [];

            if (selectedMode === 'full') {{
                filtered = [...allQuestions];
            }} else if (selectedMode === 'first_half') {{
                filtered = allQuestions.filter(q => q.week >= 1 && q.week <= 6);
            }} else if (selectedMode === 'second_half') {{
                filtered = allQuestions.filter(q => q.week >= 7 && q.week <= 12);
            }} else if (selectedMode === 'single') {{
                filtered = allQuestions.filter(q => q.week === selectedWeek);
            }}

            if(filtered.length === 0) return;

            currentQuestions = shuffle(filtered);
            currentQuestionIndex = 0;
            score = 0;
            wrongCount = 0;

            setupSection.style.display = 'none';
            quizSection.style.display = 'block';
            
            loadQuestion();
        }}

        function loadQuestion() {{
            hasAnswered = false;
            nextBtn.style.display = 'none';
            feedbackArea.className = 'feedback-area';
            feedbackArea.textContent = '';

            const q = currentQuestions[currentQuestionIndex];
            
            weekBadge.textContent = `Week ${{q.week}}`;
            progressText.textContent = `Question ${{currentQuestionIndex + 1}} / ${{currentQuestions.length}}`;
            
            // Wait a tick for CSS transition
            setTimeout(() => {{
                progressBar.style.width = `${{((currentQuestionIndex) / currentQuestions.length) * 100}}%`;
            }}, 50);

            questionText.textContent = q.question;
            optionsGrid.innerHTML = '';

            q.options.forEach(opt => {{
                const btn = document.createElement('button');
                btn.className = 'option-btn';
                btn.textContent = opt;
                btn.onclick = () => selectOption(btn, opt, q.answer);
                optionsGrid.appendChild(btn);
            }});
        }}

        function selectOption(selectedBtn, selectedOpt, correctOpt) {{
            if (hasAnswered) return;
            hasAnswered = true;

            const isCorrect = (selectedOpt === correctOpt);
            
            const allBtns = optionsGrid.querySelectorAll('.option-btn');
            allBtns.forEach(btn => {{
                btn.disabled = true;
                if (btn.textContent === correctOpt) {{
                    btn.classList.add('correct');
                }}
            }});

            if (isCorrect) {{
                selectedBtn.classList.add('correct');
                feedbackArea.textContent = '✅ Excellent! That is correct.';
                feedbackArea.classList.add('show', 'correct');
                score++;
            }} else {{
                selectedBtn.classList.add('wrong');
                feedbackArea.textContent = `❌ Incorrect. The correct answer is: ${{correctOpt}}`;
                feedbackArea.classList.add('show', 'wrong');
                wrongCount++;
            }}

            nextBtn.style.display = 'inline-block';
            if (currentQuestionIndex === currentQuestions.length - 1) {{
                nextBtn.textContent = 'View Results →';
            }} else {{
                nextBtn.textContent = 'Next Question →';
            }}
        }}

        function handleNext() {{
            if (currentQuestionIndex < currentQuestions.length - 1) {{
                currentQuestionIndex++;
                loadQuestion();
            }} else {{
                showResults();
            }}
        }}

        function showResults() {{
            quizSection.style.display = 'none';
            resultSection.style.display = 'block';

            const total = currentQuestions.length;
            const percentage = Math.round((score / total) * 100);

            correctCountEl.textContent = score;
            wrongCountEl.textContent = wrongCount;
            
            // Animate percentage text
            let currentPercent = 0;
            const interval = setInterval(() => {{
                currentPercent += 2;
                if(currentPercent >= percentage) {{
                    currentPercent = percentage;
                    clearInterval(interval);
                }}
                scorePercent.textContent = `${{currentPercent}}%`;
            }}, 20);

            // Animate circle
            setTimeout(() => {{
                scoreCircle.style.background = `conic-gradient(var(--primary) ${{percentage}}%, rgba(255,255,255,0.05) 0%)`;
            }}, 100);

            if(percentage >= 80) {{
                resultMessage.textContent = 'Outstanding performance! You mastered this!';
            }} else if (percentage >= 50) {{
                resultMessage.textContent = 'Good effort! A little more review and you will be perfect.';
            }} else {{
                resultMessage.textContent = 'Keep practicing! Review the materials and try again.';
            }}
        }}
    </script>
</body>
</html>"""
    
    with open('main.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    generate_html()
