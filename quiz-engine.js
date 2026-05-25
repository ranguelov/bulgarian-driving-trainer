/**
 * quiz-engine.js — PDD Trainer Core Logic
 * UMD: works in Node.js (for tests) AND in browser (window.QuizEngine)
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = factory();
  } else {
    root.QuizEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ─────────────────────────────────────────
     QUESTION HELPERS
  ───────────────────────────────────────── */

  /**
   * Filter questions by topic key (e.g. 't1').
   * @param {Array}  questions  Full question array
   * @param {string} topicKey  e.g. 't1'
   * @returns {Array}
   */
  function filterByTopic(questions, topicKey) {
    return questions.filter(q => q.topic === topicKey);
  }

  /**
   * True when a question uses image answers (answers[].image is not null/undefined).
   * In this case has_image=true and images[] hold the answer images, NOT a question image.
   * @param {Object} q  Question object
   * @returns {boolean}
   */
  function isAnswerImages(q) {
    return Array.isArray(q.answers) && q.answers.some(a => a.image != null);
  }

  /**
   * True when a question has more than one correct answer.
   * @param {Object} q  Question object
   * @returns {boolean}
   */
  function isMulti(q) {
    return Array.isArray(q.answers) && q.answers.filter(a => a.correct).length > 1;
  }

  /**
   * Return question text in the requested language.
   * Falls back to BG if RU translation is missing.
   * @param {Object} q    Question object
   * @param {string} lang 'BG' | 'RU'
   * @returns {string}
   */
  function getQuestionText(q, lang) {
    if (lang === 'RU') return q.question_ru || q.question;
    return q.question;
  }

  /**
   * Return answer text in the requested language.
   * Falls back to BG if RU translation is missing.
   * @param {Object} answer  Single answer object  { text, text_ru, correct, image }
   * @param {string} lang    'BG' | 'RU'
   * @returns {string}
   */
  function getAnswerText(answer, lang) {
    if (lang === 'RU') return answer.text_ru || answer.text;
    return answer.text;
  }

  /* ─────────────────────────────────────────
     ANSWER CHECKING
  ───────────────────────────────────────── */

  /**
   * Check whether the selected answer indices are fully correct.
   *
   * For single-answer questions:   selectedIndices should be [i]
   * For multi-answer questions:    selectedIndices should be [i, j, …]
   * For image-answer questions:    same as single (one image selected)
   *
   * Returns true only when:
   *   - every correct answer is selected
   *   - no incorrect answer is selected
   *
   * @param {Object}   q                Question object
   * @param {number[]} selectedIndices  Zero-based indices of selected answers
   * @returns {boolean}
   */
  function checkAnswer(q, selectedIndices) {
    if (!q || !Array.isArray(q.answers) || !Array.isArray(selectedIndices)) return false;

    const correctSet  = new Set(q.answers.map((a, i) => a.correct ? i : -1).filter(i => i !== -1));
    const selectedSet = new Set(selectedIndices);

    // All correct answers must be selected
    for (const ci of correctSet) {
      if (!selectedSet.has(ci)) return false;
    }
    // No wrong answer may be selected
    for (const si of selectedSet) {
      if (!correctSet.has(si)) return false;
    }
    return true;
  }

  /* ─────────────────────────────────────────
     EXAM GENERATION
  ───────────────────────────────────────── */

  /**
   * Generate a randomised exam of exactly `count` questions drawn from `questions`.
   * The Bulgarian exam has 45 questions spread across topics proportionally — here
   * we simply shuffle and take the first `count` items (same distribution as real exam).
   *
   * @param {Array}  questions  Full question pool (all topics)
   * @param {number} count      Desired number of questions (default 45)
   * @returns {Array}           Shuffled slice, no duplicates
   */
  function generateExam(questions, count) {
    if (!Array.isArray(questions) || questions.length === 0) return [];
    const n = count != null ? count : 45;
    if (questions.length <= n) return shuffle(questions.slice());
    return shuffle(questions.slice()).slice(0, n);
  }

  /** Fisher-Yates in-place shuffle; returns the same array. */
  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }
    return arr;
  }

  /**
   * Return a new shuffled copy of arr without mutating the original.
   * Uses Fisher-Yates algorithm.
   * @param {Array} arr
   * @returns {Array}
   */
  function shuffleArray(arr) {
    return shuffle(arr.slice());
  }

  /* ─────────────────────────────────────────
     SCORING
  ───────────────────────────────────────── */

  /**
   * Calculate total score from an array of attempt results.
   * Bulgarian scoring: topics 1-13 → 2 pts/correct, topics 14-19 → 1 pt/correct.
   * The question's own `points` field is used if present; otherwise defaults to 1.
   *
   * @param {Array} results  Array of { correct: boolean, question: Object }
   *                         `question` must have a `points` property.
   * @returns {number}       Total points earned
   */
  function calculateScore(results) {
    if (!Array.isArray(results)) return 0;
    return results.reduce((sum, r) => {
      if (!r.correct) return sum;
      const pts = (r.question && r.question.points) ? r.question.points : 1;
      return sum + pts;
    }, 0);
  }

  /**
   * Maximum possible score for a set of questions.
   * @param {Array} questions
   * @returns {number}
   */
  function maxScore(questions) {
    if (!Array.isArray(questions)) return 0;
    return questions.reduce((sum, q) => sum + (q.points || 1), 0);
  }

  /* ─────────────────────────────────────────
     PERSISTENCE  (weak spots / statistics)
     Uses a storage adapter so Node tests can
     inject a mock instead of real localStorage.
  ───────────────────────────────────────── */

  const LS_KEY = 'pdd_attempts';

  /** Default storage adapter — real localStorage in browser. */
  let _storage = (typeof localStorage !== 'undefined') ? localStorage : null;

  /**
   * Inject a custom storage adapter (for testing).
   * Must implement getItem(key) and setItem(key, value).
   * Pass null to reset to the default (real localStorage).
   * @param {object|null} adapter
   */
  function setStorage(adapter) {
    _storage = adapter;
  }

  /** Read attempt map from storage.  Returns {} on any error. */
  function _readAttempts() {
    try {
      if (!_storage) return {};
      const raw = _storage.getItem(LS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (_) {
      return {};
    }
  }

  /** Write attempt map to storage. */
  function _writeAttempts(map) {
    try {
      if (!_storage) return;
      _storage.setItem(LS_KEY, JSON.stringify(map));
    } catch (_) { /* quota exceeded — silently ignore */ }
  }

  /**
   * Record the result of answering a single question.
   * Increments attempt count and error count for the question's id.
   *
   * @param {string}  questionId  e.g. 't1_1_1'
   * @param {boolean} correct
   */
  function recordAttempt(questionId, correct) {
    const map = _readAttempts();
    if (!map[questionId]) map[questionId] = { attempts: 0, errors: 0 };
    map[questionId].attempts++;
    if (!correct) map[questionId].errors++;
    _writeAttempts(map);
  }

  /**
   * Return questions that have at least one recorded error,
   * sorted by error rate descending (most-failed first),
   * filtered to only questions present in the provided pool.
   *
   * @param {Array}  questions  Full question pool
   * @returns {Array}           Subset with weak questions first
   */
  function getWeakSpots(questions) {
    if (!Array.isArray(questions)) return [];
    const map = _readAttempts();

    return questions
      .filter(q => map[q.id] && map[q.id].errors > 0)
      .sort((a, b) => {
        const ra = map[a.id].errors / map[a.id].attempts;
        const rb = map[b.id].errors / map[b.id].attempts;
        if (rb !== ra) return rb - ra;           // higher error rate first
        return map[b.id].errors - map[a.id].errors; // then absolute error count
      });
  }

  /* ─────────────────────────────────────────
     PUBLIC API
  ───────────────────────────────────────── */
  return {
    filterByTopic,
    isAnswerImages,
    isMulti,
    checkAnswer,
    generateExam,
    calculateScore,
    maxScore,
    recordAttempt,
    getWeakSpots,
    getQuestionText,
    getAnswerText,
    setStorage,   // for testing
    shuffleArray, // randomisation utility
  };
}));
