from typing import Optional, Dict, Any, Union
import aiohttp

class PPCalculator:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def initialize(self) -> None:
        """Initialize the calculator service by creating an HTTP session"""
        self.session = aiohttp.ClientSession()
        
    async def calculate_score(self, 
        beatmap_id: Optional[int] = None,
        file_url: Optional[str] = None,
        ruleset_id: Optional[int] = None,
        mods: Optional[Union[str, int]] = None,
        accuracy: Optional[float] = None,
        count_miss: Optional[int] = None,
        count_50: Optional[int] = None,
        count_100: Optional[int] = None,
        count_300: Optional[int] = None,
        count_katu: Optional[int] = None,
        count_geki: Optional[int] = None,
        total_score: Optional[int] = None,
        max_combo: Optional[int] = None,
        percent_combo: Optional[float] = None,
        approach_rate: Optional[float] = None,
        overall_difficulty: Optional[float] = None,
        circle_size: Optional[float] = None,
        clock_rate: Optional[float] = None,
        bpm: Optional[float] = None,
        fix: bool = False,
        life_bar: bool = False,
        lock_ar: bool = False,
        lock_od: bool = False,
        lock_cs: bool = False,
        **additional_params: Dict[str, Any]
    ):
        """Calculate PP for a score with comprehensive parameters"""
        if not self.session:
            await self.initialize()
            
        payload = {
            "beatmapId": beatmap_id,
            "fileURL": file_url,
            "rulesetId": ruleset_id,
            "mods": mods,
            "accuracy": accuracy,
            "countMiss": count_miss,
            "count50": count_50,
            "count100": count_100,
            "count300": count_300,
            "countKatu": count_katu,
            "countGeki": count_geki,
            "totalScore": total_score,
            "maxCombo": max_combo,
            "percentCombo": percent_combo,
            "approachRate": approach_rate,
            "overallDifficulty": overall_difficulty,
            "circleSize": circle_size,
            "clockRate": clock_rate,
            "bpm": bpm,
            "fix": fix,
            "lifeBar": life_bar,
            "lockApproachRate": lock_ar,
            "lockOverallDifficulty": lock_od,
            "lockCircleSize": lock_cs,
            **additional_params
        }
        
        # Remove None values to use API defaults
        payload = {k: v for k, v in payload.items() if v is not None}
            
        async with self.session.post(f"{self.base_url}/calculate", json=payload) as response:
            return await response.json()
            
    async def calculate_map(self,
        beatmap_id: Optional[int] = None,
        file_url: Optional[str] = None,
        ruleset_id: Optional[int] = None,
        mods: Optional[Union[str, int]] = None,
        strains: bool = False,
        accuracy_list: Optional[list[float]] = None,
        approach_rate: Optional[float] = None,
        overall_difficulty: Optional[float] = None,
        circle_size: Optional[float] = None,
        clock_rate: Optional[float] = None,
        bpm: Optional[float] = None,
        total_hits: Optional[int] = None,
        lock_ar: bool = False,
        lock_od: bool = False,
        lock_cs: bool = False,
        **additional_params: Dict[str, Any]
    ):
        """Calculate beatmap difficulty and PP values for multiple accuracies"""
        if not self.session:
            await self.initialize()
            
        payload = {
            "beatmapId": beatmap_id,
            "fileURL": file_url,
            "rulesetId": ruleset_id,
            "mods": mods,
            "strains": strains,
            "accuracy": accuracy_list,
            "approachRate": approach_rate,
            "overallDifficulty": overall_difficulty,
            "circleSize": circle_size,
            "clockRate": clock_rate,
            "bpm": bpm,
            "totalHits": total_hits,
            "lockApproachRate": lock_ar,
            "lockOverallDifficulty": lock_od,
            "lockCircleSize": lock_cs,
            **additional_params
        }
        
        # Remove None values to use API defaults
        payload = {k: v for k, v in payload.items() if v is not None}
            
        async with self.session.post(f"{self.base_url}/calculate/map", json=payload) as response:
            return await response.json()
