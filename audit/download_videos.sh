#!/usr/bin/env bash
# Скачивание 58 официальных видео (кат. B). Запуск: bash audit/download_videos.sh
set -e
mkdir -p images/videos
BASE='https://public-eis.rta.government.bg/exam-questions/7_B_%D0%B1%D0%B5%D0%B7_%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D1%81%D0%BF%D0%BE%D1%81%D0%BE%D0%B1%D0%BD%D0%BE%D1%81%D1%82_%D0%B8%D0%BB%D0%B8_%D1%81_%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D1%81%D0%BF%D0%BE%D1%81%D0%BE%D0%B1%D0%BD%D0%BE%D1%81%D1%82_%D0%B7%D0%B0_%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F_%D0%90%D0%9C_01.06.2026/assets/'
ok=0; fail=0
if [ -s "images/videos/t3_60_1.mp4" ] || curl -fsS -o "images/videos/t3_60_1.mp4" "${BASE}5_video.mp4"; then echo "✓ t3_60_1.mp4"; ok=$((ok+1)); else echo "✗ t3_60_1 (5_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t3_59_1.mp4" ] || curl -fsS -o "images/videos/t3_59_1.mp4" "${BASE}2_video.mp4"; then echo "✓ t3_59_1.mp4"; ok=$((ok+1)); else echo "✗ t3_59_1 (2_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t3_61_1.mp4" ] || curl -fsS -o "images/videos/t3_61_1.mp4" "${BASE}6_video.mp4"; then echo "✓ t3_61_1.mp4"; ok=$((ok+1)); else echo "✗ t3_61_1 (6_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t3_62_1.mp4" ] || curl -fsS -o "images/videos/t3_62_1.mp4" "${BASE}10_video.mp4"; then echo "✓ t3_62_1.mp4"; ok=$((ok+1)); else echo "✗ t3_62_1 (10_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t3_63_1.mp4" ] || curl -fsS -o "images/videos/t3_63_1.mp4" "${BASE}7_video.mp4"; then echo "✓ t3_63_1.mp4"; ok=$((ok+1)); else echo "✗ t3_63_1 (7_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t3_64_1.mp4" ] || curl -fsS -o "images/videos/t3_64_1.mp4" "${BASE}8_video.mp4"; then echo "✓ t3_64_1.mp4"; ok=$((ok+1)); else echo "✗ t3_64_1 (8_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t3_65_1.mp4" ] || curl -fsS -o "images/videos/t3_65_1.mp4" "${BASE}9_video.mp4"; then echo "✓ t3_65_1.mp4"; ok=$((ok+1)); else echo "✗ t3_65_1 (9_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t6_55_1.mp4" ] || curl -fsS -o "images/videos/t6_55_1.mp4" "${BASE}12_video.mp4"; then echo "✓ t6_55_1.mp4"; ok=$((ok+1)); else echo "✗ t6_55_1 (12_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t6_54_1.mp4" ] || curl -fsS -o "images/videos/t6_54_1.mp4" "${BASE}11_video.mp4"; then echo "✓ t6_54_1.mp4"; ok=$((ok+1)); else echo "✗ t6_54_1 (11_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t6_56_1.mp4" ] || curl -fsS -o "images/videos/t6_56_1.mp4" "${BASE}13_video.mp4"; then echo "✓ t6_56_1.mp4"; ok=$((ok+1)); else echo "✗ t6_56_1 (13_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t6_57_1.mp4" ] || curl -fsS -o "images/videos/t6_57_1.mp4" "${BASE}14_video.mp4"; then echo "✓ t6_57_1.mp4"; ok=$((ok+1)); else echo "✗ t6_57_1 (14_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t6_58_1.mp4" ] || curl -fsS -o "images/videos/t6_58_1.mp4" "${BASE}15_video.mp4"; then echo "✓ t6_58_1.mp4"; ok=$((ok+1)); else echo "✗ t6_58_1 (15_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t6_59_1.mp4" ] || curl -fsS -o "images/videos/t6_59_1.mp4" "${BASE}16_video.mp4"; then echo "✓ t6_59_1.mp4"; ok=$((ok+1)); else echo "✗ t6_59_1 (16_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t6_60_1.mp4" ] || curl -fsS -o "images/videos/t6_60_1.mp4" "${BASE}17_video.mp4"; then echo "✓ t6_60_1.mp4"; ok=$((ok+1)); else echo "✗ t6_60_1 (17_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_131_1.mp4" ] || curl -fsS -o "images/videos/t7_131_1.mp4" "${BASE}29_video.mp4"; then echo "✓ t7_131_1.mp4"; ok=$((ok+1)); else echo "✗ t7_131_1 (29_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_145_1.mp4" ] || curl -fsS -o "images/videos/t7_145_1.mp4" "${BASE}42_video.mp4"; then echo "✓ t7_145_1.mp4"; ok=$((ok+1)); else echo "✗ t7_145_1 (42_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_126_1.mp4" ] || curl -fsS -o "images/videos/t7_126_1.mp4" "${BASE}24_video.mp4"; then echo "✓ t7_126_1.mp4"; ok=$((ok+1)); else echo "✗ t7_126_1 (24_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_130_1.mp4" ] || curl -fsS -o "images/videos/t7_130_1.mp4" "${BASE}28_video.mp4"; then echo "✓ t7_130_1.mp4"; ok=$((ok+1)); else echo "✗ t7_130_1 (28_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_132_1.mp4" ] || curl -fsS -o "images/videos/t7_132_1.mp4" "${BASE}30_video.mp4"; then echo "✓ t7_132_1.mp4"; ok=$((ok+1)); else echo "✗ t7_132_1 (30_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_127_1.mp4" ] || curl -fsS -o "images/videos/t7_127_1.mp4" "${BASE}25_video.mp4"; then echo "✓ t7_127_1.mp4"; ok=$((ok+1)); else echo "✗ t7_127_1 (25_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_125_1.mp4" ] || curl -fsS -o "images/videos/t7_125_1.mp4" "${BASE}23_video.mp4"; then echo "✓ t7_125_1.mp4"; ok=$((ok+1)); else echo "✗ t7_125_1 (23_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_120_1.mp4" ] || curl -fsS -o "images/videos/t7_120_1.mp4" "${BASE}18_video.mp4"; then echo "✓ t7_120_1.mp4"; ok=$((ok+1)); else echo "✗ t7_120_1 (18_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_121_1.mp4" ] || curl -fsS -o "images/videos/t7_121_1.mp4" "${BASE}19_video.mp4"; then echo "✓ t7_121_1.mp4"; ok=$((ok+1)); else echo "✗ t7_121_1 (19_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_122_1.mp4" ] || curl -fsS -o "images/videos/t7_122_1.mp4" "${BASE}20_video.mp4"; then echo "✓ t7_122_1.mp4"; ok=$((ok+1)); else echo "✗ t7_122_1 (20_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_123_1.mp4" ] || curl -fsS -o "images/videos/t7_123_1.mp4" "${BASE}21_video.mp4"; then echo "✓ t7_123_1.mp4"; ok=$((ok+1)); else echo "✗ t7_123_1 (21_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_124_1.mp4" ] || curl -fsS -o "images/videos/t7_124_1.mp4" "${BASE}22_video.mp4"; then echo "✓ t7_124_1.mp4"; ok=$((ok+1)); else echo "✗ t7_124_1 (22_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_128_1.mp4" ] || curl -fsS -o "images/videos/t7_128_1.mp4" "${BASE}26_video.mp4"; then echo "✓ t7_128_1.mp4"; ok=$((ok+1)); else echo "✗ t7_128_1 (26_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_129_1.mp4" ] || curl -fsS -o "images/videos/t7_129_1.mp4" "${BASE}27_video.mp4"; then echo "✓ t7_129_1.mp4"; ok=$((ok+1)); else echo "✗ t7_129_1 (27_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_133_1.mp4" ] || curl -fsS -o "images/videos/t7_133_1.mp4" "${BASE}31_video.mp4"; then echo "✓ t7_133_1.mp4"; ok=$((ok+1)); else echo "✗ t7_133_1 (31_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_134_1.mp4" ] || curl -fsS -o "images/videos/t7_134_1.mp4" "${BASE}32_video.mp4"; then echo "✓ t7_134_1.mp4"; ok=$((ok+1)); else echo "✗ t7_134_1 (32_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_135_1.mp4" ] || curl -fsS -o "images/videos/t7_135_1.mp4" "${BASE}33_video.mp4"; then echo "✓ t7_135_1.mp4"; ok=$((ok+1)); else echo "✗ t7_135_1 (33_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_136_1.mp4" ] || curl -fsS -o "images/videos/t7_136_1.mp4" "${BASE}34_video.mp4"; then echo "✓ t7_136_1.mp4"; ok=$((ok+1)); else echo "✗ t7_136_1 (34_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_137_1.mp4" ] || curl -fsS -o "images/videos/t7_137_1.mp4" "${BASE}35_video.mp4"; then echo "✓ t7_137_1.mp4"; ok=$((ok+1)); else echo "✗ t7_137_1 (35_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_138_1.mp4" ] || curl -fsS -o "images/videos/t7_138_1.mp4" "${BASE}36_video.mp4"; then echo "✓ t7_138_1.mp4"; ok=$((ok+1)); else echo "✗ t7_138_1 (36_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_139_1.mp4" ] || curl -fsS -o "images/videos/t7_139_1.mp4" "${BASE}37_video.mp4"; then echo "✓ t7_139_1.mp4"; ok=$((ok+1)); else echo "✗ t7_139_1 (37_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_140_1.mp4" ] || curl -fsS -o "images/videos/t7_140_1.mp4" "${BASE}38_video.mp4"; then echo "✓ t7_140_1.mp4"; ok=$((ok+1)); else echo "✗ t7_140_1 (38_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_141_1.mp4" ] || curl -fsS -o "images/videos/t7_141_1.mp4" "${BASE}39_video.mp4"; then echo "✓ t7_141_1.mp4"; ok=$((ok+1)); else echo "✗ t7_141_1 (39_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_142_1.mp4" ] || curl -fsS -o "images/videos/t7_142_1.mp4" "${BASE}40_video.mp4"; then echo "✓ t7_142_1.mp4"; ok=$((ok+1)); else echo "✗ t7_142_1 (40_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_143_1.mp4" ] || curl -fsS -o "images/videos/t7_143_1.mp4" "${BASE}41_video.mp4"; then echo "✓ t7_143_1.mp4"; ok=$((ok+1)); else echo "✗ t7_143_1 (41_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_144_1.mp4" ] || curl -fsS -o "images/videos/t7_144_1.mp4" "${BASE}30_video.mp4"; then echo "✓ t7_144_1.mp4"; ok=$((ok+1)); else echo "✗ t7_144_1 (30_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_146_1.mp4" ] || curl -fsS -o "images/videos/t7_146_1.mp4" "${BASE}43_video.mp4"; then echo "✓ t7_146_1.mp4"; ok=$((ok+1)); else echo "✗ t7_146_1 (43_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t7_147_1.mp4" ] || curl -fsS -o "images/videos/t7_147_1.mp4" "${BASE}44_video.mp4"; then echo "✓ t7_147_1.mp4"; ok=$((ok+1)); else echo "✗ t7_147_1 (44_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t8_137_1.mp4" ] || curl -fsS -o "images/videos/t8_137_1.mp4" "${BASE}45_video.mp4"; then echo "✓ t8_137_1.mp4"; ok=$((ok+1)); else echo "✗ t8_137_1 (45_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t8_138_1.mp4" ] || curl -fsS -o "images/videos/t8_138_1.mp4" "${BASE}46_video.mp4"; then echo "✓ t8_138_1.mp4"; ok=$((ok+1)); else echo "✗ t8_138_1 (46_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t8_139_1.mp4" ] || curl -fsS -o "images/videos/t8_139_1.mp4" "${BASE}47_video.mp4"; then echo "✓ t8_139_1.mp4"; ok=$((ok+1)); else echo "✗ t8_139_1 (47_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t8_140_1.mp4" ] || curl -fsS -o "images/videos/t8_140_1.mp4" "${BASE}48_video.mp4"; then echo "✓ t8_140_1.mp4"; ok=$((ok+1)); else echo "✗ t8_140_1 (48_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t8_141_1.mp4" ] || curl -fsS -o "images/videos/t8_141_1.mp4" "${BASE}49_video.mp4"; then echo "✓ t8_141_1.mp4"; ok=$((ok+1)); else echo "✗ t8_141_1 (49_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t8_142_1.mp4" ] || curl -fsS -o "images/videos/t8_142_1.mp4" "${BASE}50_video.mp4"; then echo "✓ t8_142_1.mp4"; ok=$((ok+1)); else echo "✗ t8_142_1 (50_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t8_143_1.mp4" ] || curl -fsS -o "images/videos/t8_143_1.mp4" "${BASE}51_video.mp4"; then echo "✓ t8_143_1.mp4"; ok=$((ok+1)); else echo "✗ t8_143_1 (51_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t8_144_1.mp4" ] || curl -fsS -o "images/videos/t8_144_1.mp4" "${BASE}52_video.mp4"; then echo "✓ t8_144_1.mp4"; ok=$((ok+1)); else echo "✗ t8_144_1 (52_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t8_145_1.mp4" ] || curl -fsS -o "images/videos/t8_145_1.mp4" "${BASE}53_video.mp4"; then echo "✓ t8_145_1.mp4"; ok=$((ok+1)); else echo "✗ t8_145_1 (53_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t10_32_1.mp4" ] || curl -fsS -o "images/videos/t10_32_1.mp4" "${BASE}55_video.mp4"; then echo "✓ t10_32_1.mp4"; ok=$((ok+1)); else echo "✗ t10_32_1 (55_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t10_33_1.mp4" ] || curl -fsS -o "images/videos/t10_33_1.mp4" "${BASE}56_video.mp4"; then echo "✓ t10_33_1.mp4"; ok=$((ok+1)); else echo "✗ t10_33_1 (56_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t10_34_1.mp4" ] || curl -fsS -o "images/videos/t10_34_1.mp4" "${BASE}57_video.mp4"; then echo "✓ t10_34_1.mp4"; ok=$((ok+1)); else echo "✗ t10_34_1 (57_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t11_45_1.mp4" ] || curl -fsS -o "images/videos/t11_45_1.mp4" "${BASE}58_video.mp4"; then echo "✓ t11_45_1.mp4"; ok=$((ok+1)); else echo "✗ t11_45_1 (58_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t13_30_1.mp4" ] || curl -fsS -o "images/videos/t13_30_1.mp4" "${BASE}59_video.mp4"; then echo "✓ t13_30_1.mp4"; ok=$((ok+1)); else echo "✗ t13_30_1 (59_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t13_31_1.mp4" ] || curl -fsS -o "images/videos/t13_31_1.mp4" "${BASE}62_video.mp4"; then echo "✓ t13_31_1.mp4"; ok=$((ok+1)); else echo "✗ t13_31_1 (62_video.mp4)"; fail=$((fail+1)); fi
if [ -s "images/videos/t18_31_1.mp4" ] || curl -fsS -o "images/videos/t18_31_1.mp4" "${BASE}61_video.mp4"; then echo "✓ t18_31_1.mp4"; ok=$((ok+1)); else echo "✗ t18_31_1 (61_video.mp4)"; fail=$((fail+1)); fi
echo; echo "Скачано/уже было: $ok, ошибок: $fail"
