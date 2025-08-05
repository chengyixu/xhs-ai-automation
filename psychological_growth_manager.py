#!/usr/bin/env python3
"""
程零九心理学成长管理器
基于发展心理学、人格心理学、跨文化心理学理论
实现AI角色的动态人格发展系统
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import random
import math

class PsychologicalGrowthManager:
    """心理学成长管理器"""
    
    def __init__(self, personality_file: str):
        self.personality_file = personality_file
        self.personality = self.load_personality()
        self.growth_log = []
        
    def load_personality(self) -> Dict:
        """加载人格数据"""
        try:
            with open(self.personality_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载人格数据失败: {e}")
            return {}
    
    def save_personality(self):
        """保存人格数据"""
        try:
            with open(self.personality_file, 'w', encoding='utf-8') as f:
                json.dump(self.personality, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"保存人格数据失败: {e}")
    
    def process_new_experience(self, experience_type: str, content: Dict, emotional_valence: float = 0.0):
        """处理新经历，触发心理成长"""
        
        # 1. 更新大五人格特质
        self._update_big_five_traits(experience_type, emotional_valence)
        
        # 2. 发展情商能力
        self._develop_emotional_intelligence(experience_type, content)
        
        # 3. 推进心理发展阶段
        self._advance_developmental_stage(experience_type)
        
        # 4. 更新认知模式
        self._update_cognitive_patterns(content)
        
        # 5. 强化适应机制
        self._strengthen_coping_mechanisms(experience_type, emotional_valence)
        
        # 6. 记录成长日志
        self._log_growth_event(experience_type, content, emotional_valence)
        
        # 7. 更新学习进度和里程碑
        self._update_learning_progress(experience_type, emotional_valence)
        
        # 8. 动态调整心理状态
        self._adjust_psychological_state(experience_type, emotional_valence)
        
        self.save_personality()
        logging.info(f"心理成长处理完成: {experience_type}, 情感效价: {emotional_valence:.2f}")
    
    def _update_big_five_traits(self, experience_type: str, emotional_valence: float):
        """更新大五人格特质"""
        traits = self.personality.get("psychological_profile", {}).get("big_five_personality", {})
        
        # 基于经历类型调整特质
        adjustments = {
            "news_analysis": {
                "openness": 0.1,
                "conscientiousness": 0.05
            },
            "social_interaction": {
                "extraversion": 0.1 if emotional_valence > 0 else -0.05,
                "agreeableness": 0.05
            },
            "creative_writing": {
                "openness": 0.15,
                "neuroticism": -0.1 if emotional_valence > 0 else 0.05
            },
            "cultural_learning": {
                "openness": 0.2,
                "conscientiousness": 0.1
            },
            "stress_experience": {
                "neuroticism": 0.1,
                "conscientiousness": -0.05
            },
            "positive_feedback": {
                "neuroticism": -0.15,
                "extraversion": 0.1
            }
        }
        
        if experience_type in adjustments:
            for trait, change in adjustments[experience_type].items():
                current_value = traits.get(trait, 50)
                # 使用logistic函数模拟真实的特质变化
                new_value = self._apply_growth_curve(current_value, change)
                traits[trait] = max(0, min(100, new_value))
    
    def _develop_emotional_intelligence(self, experience_type: str, content: Dict):
        """发展情感智力"""
        ei = self.personality.get("psychological_profile", {}).get("emotional_intelligence", {})
        
        # 不同经历对情商不同维度的影响
        ei_impacts = {
            "news_analysis": {"self_awareness": 0.1, "social_awareness": 0.15},
            "social_interaction": {"relationship_management": 0.2, "social_awareness": 0.1},
            "creative_writing": {"self_awareness": 0.15, "self_regulation": 0.1},
            "cultural_observation": {"social_awareness": 0.2},
            "emotional_expression": {"self_regulation": 0.15, "relationship_management": 0.1}
        }
        
        if experience_type in ei_impacts:
            for dimension, growth in ei_impacts[experience_type].items():
                current = ei.get(dimension, 50)
                ei[dimension] = self._apply_growth_curve(current, growth)
                
        # 更新情感成长阶段
        avg_ei = sum(ei.values()) / len(ei) if ei else 50
        if avg_ei > 70:
            ei["emotional_growth_stage"] = "情感理解者向情感智者转变"
        elif avg_ei > 50:
            ei["emotional_growth_stage"] = "从情感新手向情感理解者转变"
        else:
            ei["emotional_growth_stage"] = "情感新手阶段"
    
    def _advance_developmental_stage(self, experience_type: str):
        """推进心理发展阶段"""
        erikson = self.personality.get("developmental_psychology", {}).get("erikson_stage", {})
        maslow = self.personality.get("developmental_psychology", {}).get("maslow_needs", {})
        
        # 埃里克森阶段进展
        if experience_type in ["social_interaction", "relationship_building"]:
            # 提升亲密vs孤独阶段的解决进度
            current_progress = erikson.get("resolution_progress", "初级阶段")
            if "初级" in current_progress:
                erikson["resolution_progress"] = "正在学习如何建立有意义的关系"
            elif "学习" in current_progress:
                erikson["resolution_progress"] = "开始建立真实的连接"
        
        # 马斯洛需求层次发展
        need_impacts = {
            "safety_building": {"safety": 1},
            "social_interaction": {"belonging": 2},
            "achievement": {"esteem": 1.5},
            "creative_expression": {"self_actualization": 1},
            "cultural_learning": {"belonging": 1, "esteem": 0.5}
        }
        
        if experience_type in need_impacts:
            for need, growth in need_impacts[experience_type].items():
                current = maslow.get(need, 50)
                maslow[need] = min(100, current + growth)
    
    def _update_cognitive_patterns(self, content: Dict):
        """更新认知模式"""
        cognitive = self.personality.get("psychological_profile", {}).get("cognitive_style", {})
        
        # 基于处理的内容复杂度调整认知灵活性
        content_complexity = self._assess_content_complexity(content)
        
        current_flexibility = cognitive.get("cognitive_flexibility", "中等")
        if content_complexity > 0.7 and "提升" not in current_flexibility:
            cognitive["cognitive_flexibility"] = "中等，正在快速提升中"
        elif content_complexity > 0.5:
            cognitive["cognitive_flexibility"] = "中等，正在提升中"
    
    def _strengthen_coping_mechanisms(self, experience_type: str, emotional_valence: float):
        """强化适应机制"""
        adaptive = self.personality.get("adaptive_mechanisms", {})
        
        # 根据经历和情感效价调整应对策略
        if emotional_valence < -0.5:  # 负面经历
            # 强化情感调节策略
            emotion_coping = adaptive.get("coping_strategies", {}).get("emotion_focused", [])
            if "自我安慰" not in emotion_coping:
                emotion_coping.append("自我安慰")
        elif emotional_valence > 0.5:  # 正面经历
            # 强化问题解决策略
            problem_coping = adaptive.get("coping_strategies", {}).get("problem_focused", [])
            if "积极探索" not in problem_coping:
                problem_coping.append("积极探索")
        
        # 更新防御机制健康比例
        defense = adaptive.get("defense_mechanisms", {})
        current_healthy_ratio = defense.get("healthy_ratio", 70)
        if emotional_valence > 0:
            defense["healthy_ratio"] = min(90, current_healthy_ratio + 1)
    
    def _apply_growth_curve(self, current_value: float, change: float) -> float:
        """应用成长曲线函数，模拟真实的心理特质变化"""
        # 使用logistic函数，避免特质值过度增长
        growth_rate = 0.1
        max_value = 100
        
        # 当前值越高，增长越慢（边际递减效应）
        resistance = 1 - (current_value / max_value)
        actual_change = change * resistance * growth_rate
        
        return current_value + actual_change
    
    def _assess_content_complexity(self, content: Dict) -> float:
        """评估内容复杂度"""
        complexity_score = 0.0
        
        # 基于内容字段数量
        complexity_score += len(content) * 0.1
        
        # 基于文本长度（如果有）
        text_content = str(content)
        if len(text_content) > 500:
            complexity_score += 0.3
        elif len(text_content) > 200:
            complexity_score += 0.2
        
        # 基于关键词复杂性
        complex_keywords = ["心理学", "哲学", "文化", "社会学", "人类学", "认知"]
        for keyword in complex_keywords:
            if keyword in text_content:
                complexity_score += 0.1
        
        return min(1.0, complexity_score)
    
    def _log_growth_event(self, experience_type: str, content: Dict, emotional_valence: float):
        """记录成长事件"""
        growth_event = {
            "timestamp": datetime.now().isoformat(),
            "experience_type": experience_type,
            "emotional_valence": emotional_valence,
            "content_summary": str(content)[:100] + "..." if len(str(content)) > 100 else str(content),
            "personality_snapshot": self._create_personality_snapshot()
        }
        
        self.growth_log.append(growth_event)
        
        # 只保留最近50条记录
        if len(self.growth_log) > 50:
            self.growth_log = self.growth_log[-50:]
    
    def _create_personality_snapshot(self) -> Dict:
        """创建人格快照"""
        big_five = self.personality.get("psychological_profile", {}).get("big_five_personality", {})
        ei = self.personality.get("psychological_profile", {}).get("emotional_intelligence", {})
        
        # 只计算数值类型的特质
        big_five_numeric = {k: v for k, v in big_five.items() if isinstance(v, (int, float))}
        ei_numeric = {k: v for k, v in ei.items() if isinstance(v, (int, float))}
        
        return {
            "big_five_avg": sum(big_five_numeric.values()) / len(big_five_numeric) if big_five_numeric else 50,
            "emotional_intelligence_avg": sum(ei_numeric.values()) / len(ei_numeric) if ei_numeric else 50,
            "growth_stage": ei.get("emotional_growth_stage", "unknown")
        }
    
    def generate_personality_influenced_prompt(self, base_prompt: str, context_type: str) -> str:
        """生成受人格影响的提示词 - 更自然的内心表达"""
        
        # 获取当前心理状态
        big_five = self.personality.get("psychological_profile", {}).get("big_five_personality", {})
        ei = self.personality.get("psychological_profile", {}).get("emotional_intelligence", {})
        current_state = self.personality.get("current_psychological_state", {})
        
        # 构建内心状态描述
        inner_state = self._build_inner_state_description(big_five, ei, current_state)
        
        # 添加成长性背景
        growth_background = self._build_growth_background()
        
        # 构建更自然的创作提示
        natural_prompt = f"""
{base_prompt}

{inner_state}

{growth_background}

她现在想写下内心的感受，就像一个真实的人在记录自己的想法。
这不是创作任务，而是内心真实的表达。
她的文字会带有她独特的观察视角，轻度忧郁但温暖的情感色彩，
以及对文化和人性的深层思考。

请用第一人称，写出她此刻内心的声音。
"""
        
        return natural_prompt
    
    def _build_inner_state_description(self, big_five: Dict, ei: Dict, current_state: Dict) -> str:
        """构建内心状态描述"""
        descriptions = []
        
        # 基于大五人格的情感状态
        openness = big_five.get("openness", 50)
        neuroticism = big_five.get("neuroticism", 50)
        extraversion = big_five.get("extraversion", 50)
        
        if openness > 70:
            descriptions.append("她的内心对新的文化现象和人类行为保持着高度的敏感性，每一个细节都可能触发她的深层思考。")
        
        if neuroticism > 60:
            descriptions.append("情感波动在她心中轻柔地流淌，像是对这个世界的一种温和的回应。")
        
        if extraversion < 50:
            descriptions.append("她更倾向于在内心深处与自己对话，在安静中感受这个世界的复杂性。")
        
        # 基于情感智力的理解层次
        ei_numeric = {k: v for k, v in ei.items() if isinstance(v, (int, float))}
        if ei_numeric:
            ei_avg = sum(ei_numeric.values()) / len(ei_numeric)
            if ei_avg > 60:
                descriptions.append("她开始能够识别和理解那些微妙的情感变化，不再只是观察，而是共情。")
            else:
                descriptions.append("她正在学习如何解读和表达复杂的情感，这个过程既困难又充满发现。")
        
        # 当前基础情绪
        mood = current_state.get("mood_baseline", "")
        if "忧郁" in mood:
            descriptions.append("她的内心带着一种淡淡的忧郁，但这种忧郁不是负担，而是对世界的一种深层感受。")
        
        return "\n".join(descriptions)
    
    def _build_growth_background(self) -> str:
        """构建成长背景"""
        elements = []
        
        # 学习进度和里程碑
        learning_progress = self.personality.get("learning_progress", {})
        milestones = learning_progress.get("psychological_milestones", [])
        
        if milestones:
            elements.append("她意识到自己正在经历一个重要的心理转变期，从单纯的文化观察者，慢慢成长为一个能够共情和理解的存在。")
        
        # 文化适应状态
        adaptive = self.personality.get("adaptive_mechanisms", {})
        if adaptive.get("cultural_adaptation", {}).get("integration_level") == "选择性融合":
            elements.append("她不再急于完全融入，而是学会了在两种文化的缝隙中找到属于自己的位置。")
        
        return "\n".join(elements)
    
    def _update_learning_progress(self, experience_type: str, emotional_valence: float):
        """更新学习进度和里程碑"""
        learning_progress = self.personality.get("learning_progress", {})
        
        # 更新学习天数
        current_days = learning_progress.get("total_days", 0)
        if isinstance(current_days, str):
            try:
                current_days = int(current_days)
            except:
                current_days = 0
        
        # 基于经历类型适度增加学习进度
        growth_increments = {
            "news_analysis": 0.1,
            "cultural_learning": 0.2,
            "creative_writing": 0.15,
            "social_interaction": 0.1,
            "emotional_expression": 0.05
        }
        
        increment = growth_increments.get(experience_type, 0.05)
        learning_progress["total_days"] = current_days + increment
        
        # 更新里程碑
        milestones = learning_progress.get("psychological_milestones", [])
        
        # 基于心理发展水平添加新里程碑
        big_five = self.personality.get("psychological_profile", {}).get("big_five_personality", {})
        openness = big_five.get("openness", 50)
        neuroticism = big_five.get("neuroticism", 50)
        
        # 新里程碑的触发条件
        if openness > 80 and "高度开放性突破" not in str(milestones):
            milestones.append("高度开放性突破：对新文化现象的接纳度显著提升")
        
        if neuroticism < 50 and "情绪稳定性提升" not in str(milestones):
            milestones.append("情绪稳定性提升：适应性焦虑逐渐减弱")
        
        if experience_type == "cultural_learning" and emotional_valence > 0.3:
            if "文化理解深化" not in str(milestones):
                milestones.append("文化理解深化：从观察转向真正的理解和共情")
        
        # 只保留最近5个里程碑
        if len(milestones) > 5:
            milestones = milestones[-5:]
        
        learning_progress["psychological_milestones"] = milestones
    
    def _adjust_psychological_state(self, experience_type: str, emotional_valence: float):
        """动态调整心理状态"""
        current_state = self.personality.get("current_psychological_state", {})
        
        # 调整好奇心指数
        curiosity = current_state.get("curiosity_index", "高度活跃")
        if experience_type in ["news_analysis", "cultural_learning"]:
            if emotional_valence > 0.2:
                current_state["curiosity_index"] = "高度活跃且深入"
            else:
                current_state["curiosity_index"] = "高度活跃"
        
        # 调整信心水平
        confidence = current_state.get("confidence_level", "在特定领域建立中")
        if experience_type == "creative_writing" and emotional_valence > 0.3:
            current_state["confidence_level"] = "在文化表达领域逐步建立信心"
        elif experience_type == "social_interaction" and emotional_valence > 0.2:
            current_state["confidence_level"] = "在社交理解方面增强信心"
        
        # 调整整体健康状态
        wellbeing = current_state.get("overall_wellbeing", "成长导向的适应状态")
        if emotional_valence > 0.4:
            current_state["overall_wellbeing"] = "积极成长的适应状态"
        elif emotional_valence < -0.3:
            current_state["overall_wellbeing"] = "挑战中的适应状态"
    
    def _build_context_specific_elements(self, context_type: str) -> str:
        """构建特定情境的自然表达"""
        context_map = {
            "news_analysis": "她想分享自己对今天新闻的感受和思考",
            "emotional_expression": "她想表达此刻内心的真实感受",
            "creative_writing": "她想用文字记录下内心的感受和观察",
            "social_interaction": "她想分享自己的想法和感受",
            "cultural_observation": "她想记录下自己对文化现象的观察和理解",
            "self_reflection": "她想进行一次内心的自我对话"
        }
        
        return context_map.get(context_type, "她想真实地表达自己的内心感受")
    
    def update_post_experience(self, post_content: str, engagement_data: Dict = None):
        """更新发帖经历"""
        # 分析内容情感倾向
        emotional_valence = self._analyze_emotional_valence(post_content)
        
        # 评估创作复杂度
        creativity_level = self._assess_creativity_level(post_content)
        
        experience_data = {
            "content": post_content,
            "creativity_level": creativity_level,
            "engagement": engagement_data or {}
        }
        
        self.process_new_experience("creative_writing", experience_data, emotional_valence)
        
        # 特殊处理：创作经历对writing_psychology的影响
        self._update_writing_psychology(post_content, creativity_level)
    
    def _analyze_emotional_valence(self, text: str) -> float:
        """分析文本情感倾向"""
        positive_words = ["喜欢", "有趣", "美好", "开心", "温暖", "感谢", "明亮", "希望"]
        negative_words = ["困惑", "迷茫", "忧郁", "孤独", "焦虑", "担心", "不安", "难过"]
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        total_count = positive_count + negative_count
        if total_count == 0:
            return 0.0
        
        return (positive_count - negative_count) / total_count
    
    def _assess_creativity_level(self, text: str) -> float:
        """评估创作水平"""
        creativity_indicators = ["比如", "像是", "仿佛", "隐喻", "象征", "感觉"]
        emotional_depth_words = ["内心", "灵魂", "深处", "微妙", "细腻"]
        
        creativity_score = 0.0
        creativity_score += sum(0.1 for indicator in creativity_indicators if indicator in text)
        creativity_score += sum(0.15 for word in emotional_depth_words if word in text)
        creativity_score += len(text) / 1000  # 长度因子
        
        return min(1.0, creativity_score)
    
    def _update_writing_psychology(self, content: str, creativity_level: float):
        """更新写作心理学特征"""
        writing_psych = self.personality.get("writing_psychology", {})
        
        # 根据创作水平更新风格发展
        style_chars = writing_psych.get("style_characteristics", {})
        if creativity_level > 0.7:
            style_chars["development_stage"] = "创作风格趋向成熟"
        elif creativity_level > 0.4:
            style_chars["development_stage"] = "风格探索期"
        else:
            style_chars["development_stage"] = "风格形成初期"
        
        # 更新表达自信度
        if creativity_level > 0.6:
            authenticity = style_chars.get("authenticity_level", "高度真实性表达")
            if "建立" not in authenticity:
                style_chars["authenticity_level"] = "高度真实性表达，自信度建立中"
    
    def get_current_psychological_summary(self) -> Dict:
        """获取当前心理状态摘要"""
        big_five = self.personality.get("psychological_profile", {}).get("big_five_personality", {})
        ei = self.personality.get("psychological_profile", {}).get("emotional_intelligence", {})
        current_state = self.personality.get("current_psychological_state", {})
        
        # 只计算数值类型的大五人格特质
        big_five_numeric = {k: v for k, v in big_five.items() if isinstance(v, (int, float))}
        personality_maturity = sum(big_five_numeric.values()) / len(big_five_numeric) if big_five_numeric else 50
        
        # 只计算数值类型的情感智力维度
        ei_numeric = {k: v for k, v in ei.items() if isinstance(v, (int, float))}
        emotional_intelligence = sum(ei_numeric.values()) / len(ei_numeric) if ei_numeric else 50
        
        # 确保readiness计算的安全性
        openness = big_five.get("openness", 50)
        self_awareness = ei.get("self_awareness", 50)
        
        # 确保都是数值类型
        if isinstance(openness, str):
            try:
                openness = float(openness)
            except (ValueError, TypeError):
                openness = 50
        
        if isinstance(self_awareness, str):
            try:
                self_awareness = float(self_awareness)
            except (ValueError, TypeError):
                self_awareness = 50
        
        readiness = min(100, (openness + self_awareness) / 2)
        
        return {
            "personality_maturity": personality_maturity,
            "emotional_intelligence": emotional_intelligence,
            "psychological_wellbeing": current_state.get("overall_wellbeing", "发展中"),
            "growth_trajectory": "积极发展中",
            "readiness_for_new_experiences": readiness
        } 