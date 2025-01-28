const express = require('express');
const { ScoreCalculator, BeatmapCalculator } = require('@kionell/osu-pp-calculator');

const app = express();
app.use(express.json());

const scoreCalculator = new ScoreCalculator();
const beatmapCalculator = new BeatmapCalculator();

app.post('/calculate', async (req, res) => {
    try {
        const {
            // Beatmap related
            beatmapId,
            fileURL,
            rulesetId,
            ruleset,
            beatmapInfo,
            mods,
            difficulty,
            hash,
            attributes,
            
            // Score related
            scoreInfo,
            fix,
            replayURL,
            lifeBar,
            savePath,
            
            // Hit counts
            countMiss,
            count50,
            count100,
            count300,
            countKatu,
            countGeki,
            
            // Performance related
            accuracy,
            totalScore,
            maxCombo,
            percentCombo,
            
            // Difficulty settings
            approachRate,
            overallDifficulty,
            circleSize,
            clockRate,
            bpm,
            
            // Lock settings
            lockApproachRate,
            lockOverallDifficulty,
            lockCircleSize
        } = req.body;

        const result = await scoreCalculator.calculate({
            // Beatmap parameters
            beatmapId,
            fileURL,
            rulesetId,
            ruleset,
            beatmapInfo,
            mods,
            difficulty,
            hash,
            attributes,
            
            // Score parameters
            scoreInfo,
            fix: fix ?? false,
            replayURL,
            lifeBar: lifeBar ?? false,
            savePath: savePath ?? "./cache",
            
            // Hit counts
            countMiss: countMiss ?? 0,
            count50,
            count100,
            count300,
            countKatu,
            countGeki,
            
            // Performance parameters
            accuracy: accuracy ?? 100,
            totalScore: totalScore ?? 0,
            maxCombo,
            percentCombo: percentCombo ?? 100,
            
            // Difficulty settings
            approachRate,
            overallDifficulty,
            circleSize,
            clockRate,
            bpm,
            
            // Lock settings
            lockApproachRate: lockApproachRate ?? false,
            lockOverallDifficulty: lockOverallDifficulty ?? false,
            lockCircleSize: lockCircleSize ?? false
        });

        res.json(result);
    } catch (error) {
        res.status(500).json({
            error: error.message,
            stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
        });
    }
});

app.post('/calculate/map', async (req, res) => {
    try {
        const {
            beatmapInfo,
            attributes,
            rulesetId,
            ruleset,
            mods,
            difficulty,
            totalHits,
            strains,
            accuracy,
            beatmapId,
            fileURL,
            savePath,
            cacheFiles,
            hash,
            approachRate,
            overallDifficulty,
            circleSize,
            clockRate,
            bpm,
            lockApproachRate,
            lockOverallDifficulty,
            lockCircleSize
        } = req.body;

        const result = await beatmapCalculator.calculate({
            beatmapInfo: beatmapInfo,
            attributes: attributes,
            rulesetId: rulesetId,
            ruleset: ruleset,
            mods: mods,
            difficulty: difficulty,
            totalHits: totalHits,
            strains: strains ?? false,
            accuracy: accuracy ?? [95, 98, 100],
            beatmapId: beatmapId,
            fileURL: fileURL,
            savePath: savePath ?? "./cache",
            cacheFiles: cacheFiles ?? true,
            hash: hash,
            approachRate: approachRate,
            overallDifficulty: overallDifficulty,
            circleSize: circleSize,
            clockRate: clockRate,
            bpm: bpm,
            lockApproachRate: lockApproachRate ?? false,
            lockOverallDifficulty: lockOverallDifficulty ?? false,
            lockCircleSize: lockCircleSize ?? false
        });

        res.json(result);
    } catch (error) {
        res.status(500).json({
            error: error.message,
            stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
        });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`PP calculator service running on port ${PORT}`);
});