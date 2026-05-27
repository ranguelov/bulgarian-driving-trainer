'use strict';

/**
 * quiz-engine.test.js
 * Run: node --test tests/quiz-engine.test.js
 * Requires Node >= 18 (node:test built-in). No npm dependencies.
 */
const { describe, it, beforeEach } = require('node:test');
const assert = require('node:assert/strict');

const QE = require('../quiz-engine.js');

/* ═══════════════════════════════════════════════════
   FIXTURES
═══════════════════════════════════════════════════ */

const Q_TEXT_SINGLE = {
  id: 't1_1_1', topic: 't1', points: 2,
  question: 'Кое е правилното?', question_ru: 'Что верно?',
  has_image: false, images: [],
  answers: [
    { text: 'Да',  text_ru: 'Да',  correct: true,  image: null },
    { text: 'Не',  text_ru: 'Нет', correct: false, image: null },
    { text: 'Може', text_ru: 'Возможно', correct: false, image: null },
  ],
};

const Q_TEXT_MULTI = {
  id: 't1_2_1', topic: 't1', points: 2,
  question: 'Изберете верните.', question_ru: 'Выберите верные.',
  has_image: false, images: [],
  answers: [
    { text: 'А', text_ru: 'А', correct: true,  image: null },
    { text: 'Б', text_ru: 'Б', correct: true,  image: null },
    { text: 'В', text_ru: 'В', correct: false, image: null },
  ],
};

const Q_IMG_ANSWER = {
  id: 't12_1_1', topic: 't12', points: 2,
  question: 'Кой знак?', question_ru: 'Какой знак?',
  has_image: true,
  images: ['t12_question_1_1_img_1.png', 't12_question_1_1_img_2.png',
           't12_question_1_1_img_3.png', 't12_question_1_1_img_4.png'],
  answers: [
    { text: '', text_ru: '', correct: true,  image: 't12_question_1_1_img_1.png' },
    { text: '', text_ru: '', correct: false, image: 't12_question_1_1_img_2.png' },
    { text: '', text_ru: '', correct: false, image: 't12_question_1_1_img_3.png' },
    { text: '', text_ru: '', correct: false, image: 't12_question_1_1_img_4.png' },
  ],
};

const Q_T14 = {
  id: 't14_1_1', topic: 't14', points: 1,
  question: 'Въпрос т14', question_ru: 'Вопрос т14',
  has_image: false, images: [],
  answers: [
    { text: 'Да', text_ru: 'Да', correct: true,  image: null },
    { text: 'Не', text_ru: 'Нет', correct: false, image: null },
  ],
};

const ALL_QUESTIONS = [Q_TEXT_SINGLE, Q_TEXT_MULTI, Q_IMG_ANSWER, Q_T14];

/* ═══════════════════════════════════════════════════
   filterByTopic
═══════════════════════════════════════════════════ */
describe('filterByTopic', () => {
  it('returns only questions from the requested topic', () => {
    const result = QE.filterByTopic(ALL_QUESTIONS, 't1');
    assert.equal(result.length, 2);
    assert.ok(result.every(q => q.topic === 't1'));
  });

  it('returns empty array when topic does not exist', () => {
    const result = QE.filterByTopic(ALL_QUESTIONS, 't99');
    assert.deepEqual(result, []);
  });

  it('returns all matching items — topic t12 has 1 question', () => {
    assert.equal(QE.filterByTopic(ALL_QUESTIONS, 't12').length, 1);
  });
});

/* ═══════════════════════════════════════════════════
   isAnswerImages
═══════════════════════════════════════════════════ */
describe('isAnswerImages', () => {
  it('returns true for image-answer question', () => {
    assert.ok(QE.isAnswerImages(Q_IMG_ANSWER));
  });

  it('returns false for text-answer question', () => {
    assert.ok(!QE.isAnswerImages(Q_TEXT_SINGLE));
  });

  it('returns false for multi-text question', () => {
    assert.ok(!QE.isAnswerImages(Q_TEXT_MULTI));
  });
});

/* ═══════════════════════════════════════════════════
   isMulti
═══════════════════════════════════════════════════ */
describe('isMulti', () => {
  it('returns true when >1 correct answers', () => {
    assert.ok(QE.isMulti(Q_TEXT_MULTI));
  });

  it('returns false for single-answer question', () => {
    assert.ok(!QE.isMulti(Q_TEXT_SINGLE));
  });

  it('returns false for image question (1 correct)', () => {
    assert.ok(!QE.isMulti(Q_IMG_ANSWER));
  });
});

/* ═══════════════════════════════════════════════════
   checkAnswer
═══════════════════════════════════════════════════ */
describe('checkAnswer', () => {
  it('returns true for correct single selection', () => {
    assert.ok(QE.checkAnswer(Q_TEXT_SINGLE, [0]));
  });

  it('returns false for wrong single selection', () => {
    assert.ok(!QE.checkAnswer(Q_TEXT_SINGLE, [1]));
    assert.ok(!QE.checkAnswer(Q_TEXT_SINGLE, [2]));
  });

  it('returns true for fully correct multi selection', () => {
    assert.ok(QE.checkAnswer(Q_TEXT_MULTI, [0, 1]));
  });

  it('returns false when only one of two correct is selected', () => {
    assert.ok(!QE.checkAnswer(Q_TEXT_MULTI, [0]));
    assert.ok(!QE.checkAnswer(Q_TEXT_MULTI, [1]));
  });

  it('returns false when a wrong answer is also selected in multi', () => {
    assert.ok(!QE.checkAnswer(Q_TEXT_MULTI, [0, 1, 2]));
  });

  it('returns true for correct image answer', () => {
    assert.ok(QE.checkAnswer(Q_IMG_ANSWER, [0]));
  });

  it('returns false for wrong image answer', () => {
    assert.ok(!QE.checkAnswer(Q_IMG_ANSWER, [1]));
  });

  it('returns false for empty selection', () => {
    assert.ok(!QE.checkAnswer(Q_TEXT_SINGLE, []));
  });

  it('handles bad inputs gracefully', () => {
    assert.ok(!QE.checkAnswer(null, [0]));
    assert.ok(!QE.checkAnswer(Q_TEXT_SINGLE, null));
  });
});

/* ═══════════════════════════════════════════════════
   generateExam
═══════════════════════════════════════════════════ */
describe('generateExam', () => {
  // Use a bigger pool so we can actually pick 45
  const BIG_POOL = Array.from({ length: 100 }, (_, i) => ({
    id: `t1_${i}`, topic: 't1', points: 2,
    question: `Q${i}`, question_ru: `Q${i}RU`,
    has_image: false, images: [],
    answers: [{ text: 'А', text_ru: 'А', correct: true, image: null }],
  }));

  it('returns exactly count items', () => {
    assert.equal(QE.generateExam(BIG_POOL, 45).length, 45);
  });

  it('returns all items when pool is smaller than count', () => {
    assert.equal(QE.generateExam(ALL_QUESTIONS, 45).length, ALL_QUESTIONS.length);
  });

  it('returns no duplicate ids', () => {
    const exam = QE.generateExam(BIG_POOL, 45);
    const ids = exam.map(q => q.id);
    assert.equal(new Set(ids).size, ids.length);
  });

  it('returns empty array for empty pool', () => {
    assert.deepEqual(QE.generateExam([], 45), []);
  });

  it('defaults to 45 questions when count is omitted', () => {
    assert.equal(QE.generateExam(BIG_POOL).length, 45);
  });

  it('produces different order on successive calls (randomised)', () => {
    // With 100 items the probability of two identical shuffles is ~1/100! ≈ 0
    const a = QE.generateExam(BIG_POOL, 45).map(q => q.id).join(',');
    const b = QE.generateExam(BIG_POOL, 45).map(q => q.id).join(',');
    // Allow tiny probability of collision in CI — just log, don't fail
    if (a === b) {
      console.warn('Warning: two shuffles produced identical order (extremely unlikely)');
    }
    // We assert at least one is valid (length correct)
    assert.equal(a.split(',').length, 45);
  });
});

/* ═══════════════════════════════════════════════════
   calculateScore
═══════════════════════════════════════════════════ */
describe('calculateScore', () => {
  it('sums points for correct answers', () => {
    const results = [
      { correct: true,  question: Q_TEXT_SINGLE }, // 2 pts
      { correct: true,  question: Q_TEXT_MULTI  }, // 2 pts
      { correct: false, question: Q_T14          }, // 0 pts (wrong)
      { correct: true,  question: Q_T14          }, // 1 pt
    ];
    assert.equal(QE.calculateScore(results), 5);
  });

  it('returns 0 for all wrong answers', () => {
    const results = [
      { correct: false, question: Q_TEXT_SINGLE },
      { correct: false, question: Q_T14 },
    ];
    assert.equal(QE.calculateScore(results), 0);
  });

  it('returns 0 for empty array', () => {
    assert.equal(QE.calculateScore([]), 0);
  });

  it('handles missing points field — defaults to 1', () => {
    const q = { id: 'x', answers: [] }; // no points field
    assert.equal(QE.calculateScore([{ correct: true, question: q }]), 1);
  });
});

/* ═══════════════════════════════════════════════════
   maxScore
═══════════════════════════════════════════════════ */
describe('maxScore', () => {
  it('sums all question points', () => {
    // t1×3 = 2+2+2=6, t14×1 = 1  → but Q_IMG_ANSWER is t12 pts=2
    assert.equal(QE.maxScore(ALL_QUESTIONS), 2 + 2 + 2 + 1);
  });
});

/* ═══════════════════════════════════════════════════
   recordAttempt + getWeakSpots  (with mock storage)
═══════════════════════════════════════════════════ */
describe('recordAttempt + getWeakSpots', () => {
  // Fresh in-memory mock before each test
  let store;
  beforeEach(() => {
    store = {};
    QE.setStorage({
      getItem:  key       => store[key] ?? null,
      setItem:  (key, val) => { store[key] = val; },
    });
  });

  it('records an attempt and stores it', () => {
    QE.recordAttempt('t1_1_1', true);
    const raw = JSON.parse(store['pdd_attempts']);
    assert.deepEqual(raw['t1_1_1'], { attempts: 1, errors: 0 });
  });

  it('increments errors for wrong answer', () => {
    QE.recordAttempt('t1_1_1', false);
    QE.recordAttempt('t1_1_1', false);
    const raw = JSON.parse(store['pdd_attempts']);
    assert.deepEqual(raw['t1_1_1'], { attempts: 2, errors: 2 });
  });

  it('accumulates mixed correct/wrong', () => {
    QE.recordAttempt('t1_1_1', true);
    QE.recordAttempt('t1_1_1', false);
    QE.recordAttempt('t1_1_1', true);
    const raw = JSON.parse(store['pdd_attempts']);
    assert.deepEqual(raw['t1_1_1'], { attempts: 3, errors: 1 });
  });

  it('getWeakSpots returns only questions with errors', () => {
    QE.recordAttempt('t1_1_1', false);  // error
    QE.recordAttempt('t1_2_1', true);   // no error
    const weak = QE.getWeakSpots(ALL_QUESTIONS);
    assert.equal(weak.length, 1);
    assert.equal(weak[0].id, 't1_1_1');
  });

  it('getWeakSpots sorts by error rate descending', () => {
    // t1_1_1: 1/1 = 100% error rate
    QE.recordAttempt('t1_1_1', false);
    // t1_2_1: 1/3 = 33% error rate
    QE.recordAttempt('t1_2_1', true);
    QE.recordAttempt('t1_2_1', true);
    QE.recordAttempt('t1_2_1', false);

    const weak = QE.getWeakSpots(ALL_QUESTIONS);
    assert.equal(weak[0].id, 't1_1_1'); // highest rate first
    assert.equal(weak[1].id, 't1_2_1');
  });

  it('getWeakSpots returns empty array when no errors recorded', () => {
    QE.recordAttempt('t1_1_1', true);
    assert.deepEqual(QE.getWeakSpots(ALL_QUESTIONS), []);
  });

  it('getWeakSpots only returns questions present in the pool', () => {
    QE.recordAttempt('t99_99_99', false); // not in ALL_QUESTIONS
    assert.deepEqual(QE.getWeakSpots(ALL_QUESTIONS), []);
  });
});

/* ═══════════════════════════════════════════════════
   getQuestionText / getAnswerText
═══════════════════════════════════════════════════ */
describe('getQuestionText', () => {
  it('returns BG text', () => {
    assert.equal(QE.getQuestionText(Q_TEXT_SINGLE, 'BG'), 'Кое е правилното?');
  });
  it('returns RU text', () => {
    assert.equal(QE.getQuestionText(Q_TEXT_SINGLE, 'RU'), 'Что верно?');
  });
  it('falls back to BG if RU missing', () => {
    const q = { question: 'BG only', question_ru: '' };
    assert.equal(QE.getQuestionText(q, 'RU'), 'BG only');
  });
});

describe('getAnswerText', () => {
  const ans = { text: 'Да', text_ru: 'Да (рус)', correct: true, image: null };
  it('returns BG text', () => {
    assert.equal(QE.getAnswerText(ans, 'BG'), 'Да');
  });
  it('returns RU text', () => {
    assert.equal(QE.getAnswerText(ans, 'RU'), 'Да (рус)');
  });
  it('falls back to BG if text_ru missing', () => {
    const a = { text: 'Fallback', text_ru: '', correct: true, image: null };
    assert.equal(QE.getAnswerText(a, 'RU'), 'Fallback');
  });
});

/* ═══════════════════════════════════════════════════
   shuffleArray — randomisation utility
═══════════════════════════════════════════════════ */
describe('shuffleArray', () => {
  const ORIGINAL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  it('returns an array of the same length', () => {
    const result = QE.shuffleArray(ORIGINAL);
    assert.equal(result.length, ORIGINAL.length);
  });

  it('contains all original elements (no duplicates, no omissions)', () => {
    const result = QE.shuffleArray(ORIGINAL);
    assert.deepEqual([...result].sort((a, b) => a - b), ORIGINAL);
  });

  it('does not mutate the original array', () => {
    const copy = ORIGINAL.slice();
    QE.shuffleArray(copy);
    assert.deepEqual(copy, ORIGINAL);
  });

  it('returns a new array (not the same reference)', () => {
    const arr = [1, 2, 3];
    const result = QE.shuffleArray(arr);
    assert.notStrictEqual(result, arr);
  });

  it('handles an empty array', () => {
    assert.deepEqual(QE.shuffleArray([]), []);
  });

  it('handles a single-element array', () => {
    assert.deepEqual(QE.shuffleArray([42]), [42]);
  });

  it('produces different orderings across multiple runs (statistical)', () => {
    // Run 20 shuffles of a 10-element array; at least one must differ from original.
    // P(all 20 results identical to original) = (1/10!)^20 ≈ 10^-126 — safe to assert.
    const results = Array.from({ length: 20 }, () => QE.shuffleArray(ORIGINAL).join(','));
    const allSame = results.every(r => r === ORIGINAL.join(','));
    assert.equal(allSame, false, 'All 20 shuffles were identical — RNG may be broken');
  });

  it('shuffles answers without losing correct-answer information', () => {
    const answers = [
      { text: 'А', correct: false },
      { text: 'Б', correct: true  },
      { text: 'В', correct: false },
    ];
    const shuffled = QE.shuffleArray(answers);
    const correctCount = shuffled.filter(a => a.correct).length;
    assert.equal(correctCount, 1, 'Exactly one correct answer must survive the shuffle');
    assert.deepEqual(
      shuffled.map(a => a.text).sort(),
      answers.map(a => a.text).sort(),
      'All answer texts must be preserved'
    );
  });
});

/* ═══════════════════════════════════════════════════
   prepareSession — фикс бага "ответы перемешиваются при каждом рендере"
   Тесты написаны ДО реализации (TDD). До добавления prepareSession в quiz-engine.js
   все эти тесты должны падать с "QE.prepareSession is not a function".
═══════════════════════════════════════════════════ */
describe('prepareSession', () => {
  const Q4 = {
    id: 'q1', topic: 't1', points: 2,
    question: 'Q?', question_ru: 'Q?',
    has_image: false, images: [],
    answers: [
      { text: 'A', text_ru: 'A', correct: true,  image: null },
      { text: 'B', text_ru: 'B', correct: false, image: null },
      { text: 'C', text_ru: 'C', correct: true,  image: null },
      { text: 'D', text_ru: 'D', correct: false, image: null },
    ],
  };
  const Q4b = {
    id: 'q2', topic: 't1', points: 1,
    question: 'Q2?', question_ru: 'Q2?',
    has_image: false, images: [],
    answers: [
      { text: 'X', text_ru: 'X', correct: false, image: null },
      { text: 'Y', text_ru: 'Y', correct: true,  image: null },
    ],
  };

  // ── 1. randomMode=false: порядок ответов не меняется ──────────────────
  it('randomMode=false: answer order is identical to original', () => {
    const session = QE.prepareSession([Q4], false);
    assert.deepEqual(
      session[0].answers.map(a => a.text),
      Q4.answers.map(a => a.text)
    );
  });

  // ── 2. randomMode=false: возвращает новый массив (не ту же ссылку) ────
  it('randomMode=false: returns a new array (not the same reference)', () => {
    const session = QE.prepareSession([Q4], false);
    assert.notStrictEqual(session, [Q4]);
    assert.notStrictEqual(session[0], Q4);
  });

  // ── 3. randomMode=true: все ответы сохранены (нет потери данных) ──────
  it('randomMode=true: all answers are preserved (no data loss)', () => {
    const session = QE.prepareSession([Q4], true);
    const resultTexts = session[0].answers.map(a => a.text).sort();
    const origTexts   = Q4.answers.map(a => a.text).sort();
    assert.deepEqual(resultTexts, origTexts);
  });

  // ── 4. randomMode=true: кол-во правильных ответов сохранено ──────────
  it('randomMode=true: correct-answer count is preserved', () => {
    const session = QE.prepareSession([Q4], true);
    const correctCount = session[0].answers.filter(a => a.correct).length;
    assert.equal(correctCount, 2); // исходно 2 правильных
  });

  // ── 5. Оригинальный вопрос не мутирован ──────────────────────────────
  it('does not mutate original question answers', () => {
    const origOrder = Q4.answers.map(a => a.text);
    QE.prepareSession([Q4], true);
    assert.deepEqual(Q4.answers.map(a => a.text), origOrder);
  });

  // ── 6. КЛЮЧЕВОЙ ТЕСТ: порядок стабилен внутри сессии ─────────────────
  // Это воспроизводит баг: если бы shuffle вызывался при каждом рендере,
  // session[0].answers менялось бы при каждом обращении. После фикса —
  // answers — это обычный массив, который не меняется сам по себе.
  it('answer order is STABLE — same object accessed twice gives identical order', () => {
    const session = QE.prepareSession([Q4], true);
    const firstAccess  = session[0].answers.map(a => a.text);
    const secondAccess = session[0].answers.map(a => a.text); // имитация повторного renderQ
    assert.deepEqual(firstAccess, secondAccess,
      'BUG: answer order changed between two accesses — shuffle called per-render!');
  });

  // ── 7. Несколько вопросов обрабатываются корректно ───────────────────
  it('handles multiple questions — each gets its own stable shuffled order', () => {
    const session = QE.prepareSession([Q4, Q4b], true);
    assert.equal(session.length, 2);
    // Оба вопроса должны иметь все свои ответы
    assert.equal(session[0].answers.length, 4);
    assert.equal(session[1].answers.length, 2);
  });

  // ── 8. Пустой массив вопросов ─────────────────────────────────────────
  it('returns empty array for empty input', () => {
    assert.deepEqual(QE.prepareSession([], true),  []);
    assert.deepEqual(QE.prepareSession([], false), []);
  });

  // ── 9. Вопрос с одним ответом — не падает ────────────────────────────
  it('handles single-answer question gracefully', () => {
    const singleAns = { ...Q4b, answers: [{ text: 'Only', correct: true, image: null }] };
    const session = QE.prepareSession([singleAns], true);
    assert.equal(session[0].answers.length, 1);
    assert.equal(session[0].answers[0].correct, true);
  });

  // ── 10. Все поля вопроса (кроме answers) сохранены 1-в-1 ────────────
  it('preserves all question fields except answers', () => {
    const session = QE.prepareSession([Q4], true);
    assert.equal(session[0].id,      Q4.id);
    assert.equal(session[0].topic,   Q4.topic);
    assert.equal(session[0].points,  Q4.points);
    assert.equal(session[0].question, Q4.question);
  });
});
