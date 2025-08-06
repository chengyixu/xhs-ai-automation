#!/usr/bin/env python3
"""
小红书AI自动化客户端 - 程零九版本
外星政府工作女孩的地球学习之旅
"""

import asyncio
import json
import requests
import random
import re
import os
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import logging
from psychological_growth_manager import PsychologicalGrowthManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/个人_local/Xiaohongshu/cheng/app.log'),
        logging.StreamHandler()
    ]
)

# 配置
PHONE = "13391007743"
JSON_PATH = "/Users/个人_local/Xiaohongshu/cheng/cookies"
IMAGE_PATH = "/Users/个人_local/Xiaohongshu/cheng/Screenshot.png"

# Qwen API 配置
QWEN_API_KEY = "sk-316420c29c624dbeb7fbbcb63077a46f"
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_MODEL = "qwen-plus"

# Jina API 配置
JINA_API_KEY = "jina_26a656e516224ce28e71cc3b28fa7b07zUchXe4_MJ_935m8SpS9-TNGL--w"

# 文件路径
BASE_PATH = "/Users/个人_local/Xiaohongshu/cheng"
PERSONALITY_FILE = os.path.join(BASE_PATH, "personality.json")
UNDERSTANDINGS_FILE = os.path.join(BASE_PATH, "understandings.json")
MEMORIES_FILE = os.path.join(BASE_PATH, "memories.json")
POSTS_FILE = os.path.join(BASE_PATH, "posts.json")
KNOWLEDGE_FILE = os.path.join(BASE_PATH, "knowledge.json")

# 新闻源
NEWS_SOURCES = [
    {"name": "知乎", "url": "https://tophub.today/n/mproPpoq6O"},
    {"name": "微博", "url": "https://tophub.today/n/KqndgxeLl9"},
    {"name": "微信", "url": "https://tophub.today/n/WnBe01o371"},
    {"name": "抖音", "url": "https://tophub.today/n/DpQvNABoNE"},
    {"name": "小红书", "url": "https://tophub.today/n/L4MdA5ldxD"}
]

# MCP服务器参数
server_params = StdioServerParameters(
    command="uvx",
    args=["xhs_mcp_server@latest"],
    env={
        "phone": PHONE,
        "json_path": JSON_PATH
    }
)

class PersonalityManager:
    """人设管理器 - 增强心理学成长功能"""
    
    def __init__(self):
        self.personality = self.load_personality()
        self.understandings = self.load_understandings()
        self.memories = self.load_memories()
        self.posts = self.load_posts()
        self.knowledge = self.load_knowledge()
        
        # 初始化心理学成长管理器
        self.growth_manager = PsychologicalGrowthManager(PERSONALITY_FILE)
    
    def _ensure_int(self, value, default=0):
        """确保值是整数类型"""
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        else:
            return default
    
    def load_json_file(self, filepath, default_data):
        """加载JSON文件"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                self.save_json_file(filepath, default_data)
                return default_data
        except Exception as e:
            logging.error(f"加载文件 {filepath} 失败: {e}")
            return default_data
    
    def save_json_file(self, filepath, data):
        """保存JSON文件"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"保存文件 {filepath} 失败: {e}")
    
    def load_personality(self):
        """加载人设 - 兼容新旧格式"""
        # 尝试加载现有文件
        existing_data = self.load_json_file(PERSONALITY_FILE, {})
        
        # 如果是新格式，直接返回
        if "psychological_profile" in existing_data:
            return existing_data
        
        # 如果是旧格式或为空，使用默认的新格式
        default_personality = {
            "basic_info": {
                "name": "程零九",
                "age": 23,
                "species": "外星人",
                "job": "外星政府文化研究员",
                "location": "地球",
                "mission": "深度研究地球文化心理学，建立跨星际文化桥梁"
            },
            "psychological_profile": {
                "big_five_personality": {
                    "openness": 85,
                    "conscientiousness": 75,
                    "extraversion": 35,
                    "agreeableness": 70,
                    "neuroticism": 60,
                    "growth_trend": "openness和conscientiousness在提升，neuroticism在下降"
                },
                "emotional_intelligence": {
                    "self_awareness": 70,
                    "self_regulation": 65,
                    "social_awareness": 55,
                    "relationship_management": 45,
                    "emotional_growth_stage": "从情感新手向情感理解者转变"
                }
            },
            "current_psychological_state": {
                "mood_baseline": "轻度忧郁但稳定",
                "anxiety_level": "文化适应性焦虑，可管理",
                "curiosity_index": "高度活跃",
                "overall_wellbeing": "成长导向的适应状态"
            },
            "learning_progress": {
                "daily_hours_target": 4,
                "total_days": self._ensure_int(existing_data.get("learning_progress", {}).get("total_days", 3)),
                "last_study_date": existing_data.get("learning_progress", {}).get("last_study_date", "2025-06-30"),
                "psychological_milestones": [
                    "从文化shock到文化curiosity的转变",
                    "从language anxiety到expression confidence的发展"
                ]
            }
        }
        
        # 保存新格式
        self.save_json_file(PERSONALITY_FILE, default_personality)
        return default_personality
    
    def load_understandings(self):
        """加载理解"""
        default_understandings = {
            "about_earth": {
                "humans": "和我们长得很像，可能形状是好的方案",
                "culture": "复杂但有趣",
                "language": "还在学习中"
            },
            "daily_observations": [],
            "confusion_points": [],
            "new_discoveries": []
        }
        return self.load_json_file(UNDERSTANDINGS_FILE, default_understandings)
    
    def load_memories(self):
        """加载分析记忆"""
        default_memories = {
            "daily_analysis": [],
            "news_insights": [],
            "personal_thoughts": []
        }
        return self.load_json_file(MEMORIES_FILE, default_memories)
    
    def load_posts(self):
        """加载发布记录"""
        default_posts = {
            "history": [],
            "themes": [],
            "engagement": []
        }
        return self.load_json_file(POSTS_FILE, default_posts)
    
    def load_knowledge(self):
        """加载知识库"""
        default_knowledge = {
            "daily_news": [],
            "trending_topics": [],
            "learning_materials": []
        }
        return self.load_json_file(KNOWLEDGE_FILE, default_knowledge)
    
    def save_all(self):
        """保存所有数据"""
        self.save_json_file(PERSONALITY_FILE, self.personality)
        self.save_json_file(UNDERSTANDINGS_FILE, self.understandings)
        self.save_json_file(MEMORIES_FILE, self.memories)
        self.save_json_file(POSTS_FILE, self.posts)
        self.save_json_file(KNOWLEDGE_FILE, self.knowledge)

class NewsCollector:
    """新闻收集器"""
    
    def __init__(self, personality_manager):
        self.pm = personality_manager
    
    def call_jina_api(self, url):
        """调用Jina Reader API"""
        try:
            headers = {
                "Authorization": f"Bearer {JINA_API_KEY}",
                "Accept": "application/json"
            }
            
            jina_url = f"https://r.jina.ai/{url}"
            response = requests.get(jina_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("content", "")
            else:
                logging.error(f"Jina API调用失败: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Jina API调用异常: {e}")
            return None
    
    def collect_daily_news(self):
        """收集每日新闻"""
        today = datetime.now().strftime("%Y-%m-%d")
        news_data = {
            "date": today,
            "sources": {}
        }
        
        for source in NEWS_SOURCES:
            logging.info(f"正在爬取 {source['name']} 新闻...")
            content = self.call_jina_api(source['url'])
            
            if content:
                # 简化内容，提取关键信息
                simplified_content = self.extract_key_news(content, source['name'])
                news_data["sources"][source['name']] = simplified_content
            
            time.sleep(2)  # 避免请求过于频繁
        
        # 保存到知识库
        self.pm.knowledge["daily_news"].append(news_data)
        
        # 只保留最近30天的新闻
        if len(self.pm.knowledge["daily_news"]) > 30:
            self.pm.knowledge["daily_news"] = self.pm.knowledge["daily_news"][-30:]
        
        self.pm.save_json_file(KNOWLEDGE_FILE, self.pm.knowledge)
        logging.info("新闻收集完成")
        return news_data
    
    def extract_key_news(self, content, source_name):
        """提取关键新闻信息"""
        # 简单的关键词提取，实际应用中可以更复杂
        lines = content.split('\n')
        key_news = []
        
        for line in lines[:20]:  # 只取前20行
            line = line.strip()
            if len(line) > 10 and not line.startswith('#'):
                key_news.append(line)
        
        return key_news[:10]  # 最多10条

class ContentAnalyzer:
    """内容分析器"""
    
    def __init__(self, personality_manager):
        self.pm = personality_manager
    
    def call_qwen_api(self, prompt, max_tokens=1000000000):
        """调用Qwen API"""
        try:
            headers = {
                "Authorization": f"Bearer {QWEN_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": QWEN_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.8,
                "top_p": 0.9
            }
            
            response = requests.post(
                f"{QWEN_BASE_URL}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                return content
            else:
                logging.error(f"Qwen API调用失败: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Qwen API调用异常: {e}")
            return None
    
    def analyze_news_with_personality(self, news_data):
        """用人设分析新闻 - 集成心理学成长机制"""
        # 构建更自然的分析情境
        analysis_context = f"""
        程零九刚刚浏览完今天的新闻，作为一个外星文化研究员，她想记录下自己的观察和感受。

        她不是在写学术报告，而是在记录她作为一个异乡人对这个世界的理解和感受。
        她的观察带有外星人的独特视角，也带有一个正在适应新文化的个体的敏感性。

        今天她看到的新闻：
        {json.dumps(news_data, ensure_ascii=False, indent=2)}

        她想记录下这些新闻给她的感受、触发的思考，以及她对人类行为和社会现象的观察。
        这是她的内心独白，带有她独特的思考方式和情感色彩。
        """
        
        # 生成受心理状态影响的提示词
        enhanced_prompt = self.pm.growth_manager.generate_personality_influenced_prompt(
            analysis_context, "news_analysis"
        )
        
        analysis = self.call_qwen_api(enhanced_prompt, max_tokens=1200)
        
        if analysis:
            try:
                # 将新闻分析作为经历输入心理成长系统
                experience_data = {
                    "news_content": news_data,
                    "analysis_quality": self._assess_analysis_quality(analysis),
                    "cultural_insights": self._extract_cultural_insights(analysis)
                }
                
                # 计算情感效价
                emotional_valence = self._calculate_emotional_valence(analysis)
                
                # 触发心理成长 - 这是一次文化学习和情感处理的经历
                self.pm.growth_manager.process_new_experience(
                    "cultural_learning", experience_data, emotional_valence
                )
                
                # 同时也是一次认知处理经历
                self.pm.growth_manager.process_new_experience(
                    "news_analysis", experience_data, emotional_valence * 0.8
                )
                
            except Exception as e:
                logging.error(f"心理成长处理失败: {e}")
                # 继续执行，不因为心理成长失败而中断分析
            
            # 保存分析到记忆中
            memory_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "news_summary": news_data,
                "analysis": analysis,
                "psychological_growth": self.pm.growth_manager.get_current_psychological_summary(),
                "emotional_valence": emotional_valence,
                "mood": "reflective_growth"
            }
            
            self.pm.memories["daily_analysis"].append(memory_entry)
            
            # 只保留最近30天的分析
            if len(self.pm.memories["daily_analysis"]) > 30:
                self.pm.memories["daily_analysis"] = self.pm.memories["daily_analysis"][-30:]
            
            self.pm.save_json_file(MEMORIES_FILE, self.pm.memories)
            
            logging.info("新闻分析完成，心理成长已更新")
            
        return analysis
    
    def _assess_analysis_quality(self, analysis: str) -> float:
        """评估分析质量"""
        quality_indicators = [
            "心理", "文化", "观察", "理解", "感受", "思考", "发现", 
            "对比", "反思", "成长", "适应", "学习"
        ]
        
        quality_score = 0.0
        for indicator in quality_indicators:
            if indicator in analysis:
                quality_score += 0.1
                
        # 长度因子
        if len(analysis) > 200:
            quality_score += 0.2
        
        return min(1.0, quality_score)
    
    def _extract_cultural_insights(self, analysis: str) -> List[str]:
        """提取文化洞察"""
        insights = []
        
        # 简单的关键句提取
        sentences = analysis.split('。')
        for sentence in sentences:
            if any(word in sentence for word in ["地球人", "文化", "社会", "人类", "行为"]):
                insights.append(sentence.strip())
        
        return insights[:3]  # 最多3个洞察
    
    def _calculate_emotional_valence(self, text: str) -> float:
        """计算情感效价"""
        positive_words = ["有趣", "好奇", "发现", "理解", "成长", "学习", "希望", "温暖"]
        negative_words = ["困惑", "迷茫", "焦虑", "担心", "不安", "孤独", "忧郁"]
        neutral_words = ["观察", "思考", "分析", "研究", "探索", "适应"]
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        neutral_count = sum(1 for word in neutral_words if word in text)
        
        total_count = positive_count + negative_count + neutral_count
        if total_count == 0:
            return 0.0
        
        # 计算加权情感效价
        valence = (positive_count * 1.0 + neutral_count * 0.1 - negative_count * 0.8) / total_count
        return max(-1.0, min(1.0, valence))

class ContentCreator:
    """内容创作器"""
    
    def __init__(self, personality_manager):
        self.pm = personality_manager
    
    def call_qwen_api(self, prompt, max_tokens=80000000000):
        """调用Qwen API"""
        try:
            headers = {
                "Authorization": f"Bearer {QWEN_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": QWEN_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.9,
                "top_p": 0.9
            }
            
            response = requests.post(
                f"{QWEN_BASE_URL}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                return content
            else:
                logging.error(f"Qwen API调用失败: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Qwen API调用异常: {e}")
            return None
    
    def generate_post_content(self):
        """生成发布内容 - 基于真实内心感受的自然表达"""
        # 获取最近的分析和新闻
        recent_analysis = ""
        recent_news = ""
        
        if self.pm.memories["daily_analysis"]:
            recent_analysis = self.pm.memories["daily_analysis"][-1].get("analysis", "")
        
        if self.pm.knowledge["daily_news"]:
            recent_news_data = self.pm.knowledge["daily_news"][-1]
            recent_news = json.dumps(recent_news_data["sources"], ensure_ascii=False)
        
        # 获取当前心理状态 - 用于生成更自然的表达
        psychological_summary = self.pm.growth_manager.get_current_psychological_summary()
        
        # 构建更自然的创作情境
        creative_context = f"""
        程零九刚刚浏览完今天的新闻，心里有些感触。她想在小红书上写点什么，分享一下内心的想法。

        她最近的内心状态：
        - 情感敏感度很高，容易被新闻中的人情冷暖触动
        - 正在经历文化适应的心理成长，对归属感有深层思考
        - 带着轻度忧郁但稳定的情绪基调
        - 对人类行为和社会现象有独特的观察视角

        她刚才看到的新闻让她想起了什么，或者触发了什么感受...

        最近看到的内容：
        {recent_news}

        她内心的一些思考：
        {recent_analysis}

        现在她想写一篇200字左右的感想，就像一个真实的人在深夜或者安静时刻的内心独白。
        她不是在完成任务，而是在表达真实的感受。
        """
        
        # 使用心理学成长管理器生成个性化的创作提示
        enhanced_prompt = self.pm.growth_manager.generate_personality_influenced_prompt(
            creative_context, "emotional_expression"
        )
        
        # 调用API生成内容
        content = self.call_qwen_api(enhanced_prompt, max_tokens=1000)
        
        if not content:
            # 更自然的备用内容
            fallback_prompts = [
                "程零九今天看新闻时突然想到了什么，她决定写下来...",
                "夜深了，程零九回想起今天的见闻，有些话想说...",
                "程零九坐在窗边，想起今天看到的那些故事...",
                "米饭牛肉套餐的香味中，程零九想起了今天的感触..."
            ]
            
            fallback_prompt = random.choice(fallback_prompts)
            content = self.call_qwen_api(f"{fallback_prompt}\n\n请写一段200字左右的内心感想，要真实自然，不要像在完成任务。", max_tokens=800)
        
        if not content:
            # 最终备用内容，也要更自然
            content = self._generate_natural_fallback_content()
        
        return content
    
    def _generate_natural_fallback_content(self):
        """生成更自然的备用内容"""
        natural_starters = [
            "今天又是模模糊糊的一天。",
            "窗外的光线慢慢暗下来，我想起了什么。",
            "刚才看新闻的时候，心里突然有点什么感觉。",
            "米饭牛肉套餐还是那个味道，但我好像想起了别的事情。"
        ]
        
        middle_thoughts = [
            "作为一个外星人，我总是觉得自己在这个世界的边缘观察。每天的新闻像是别人的故事，但偶尔会有什么触动我。",
            "地球人的情感表达方式总是让我困惑。他们可以为了很远的事情难过，也可以为了很小的事情开心。",
            "有时候我觉得自己在慢慢理解这个世界，有时候又觉得更加迷茫。这种感觉很奇怪。",
            "我想我在这里生活得越久，就越能感受到那些微妙的情感变化。但这也让我更加孤独。"
        ]
        
        endings = [
            "也许这就是成长吧，在理解中变得更敏感。",
            "111 110110000101111 111 011001101111001 111 101101001110010",
            "明天又是新的一天，我会继续观察，继续感受。",
            "我想我正在慢慢学会如何在这个世界上存在。"
        ]
        
        return f"{random.choice(natural_starters)}\n\n{random.choice(middle_thoughts)}\n\n{random.choice(endings)}"

    def generate_title(self):
        """生成标题 - 基于当前内容和心理状态动态生成"""
        # 获取最近的分析，从中提取关键情感或主题
        recent_analysis = ""
        if self.pm.memories["daily_analysis"]:
            recent_analysis = self.pm.memories["daily_analysis"][-1].get("analysis", "")
        
        # 获取当前心理状态
        psychological_summary = self.pm.growth_manager.get_current_psychological_summary()
        current_mood = self.pm.personality.get("current_psychological_state", {}).get("mood_baseline", "")
        
        title_prompt = f"""
        程零九想为她刚写的感想取个标题。

        她当前的心理状态：{current_mood}
        她最近的思考：{recent_analysis[:100]}...
        
        标题应该：
        1. 像她真实的情感抒发，不要像新闻标题
        2. 体现她当前的心理状态和感受
        3. 控制在10个字以内
        4. 自然、真实、有点忧郁但温暖
        
        请只返回标题，不要解释：
        """
        
        generated_title = self.call_qwen_api(title_prompt, max_tokens=100)
        
        if generated_title and len(generated_title.strip()) > 0:
            # 清理标题，去掉多余的符号和解释
            title = generated_title.strip().split('\n')[0].strip('"\'""''')
            if len(title) <= 20:  # 合理长度
                return title
        
        # 如果生成失败，使用更自然的备用标题
        natural_titles = [
            "今天的一些感想",
            "窗边的思考",
            "米饭牛肉套餐的时光",
            "模模糊糊的理解",
            "关于归属感的想法",
            "夜晚的观察",
            "一个外星人的疑问",
            "地球生活的感受"
        ]
        
        return random.choice(natural_titles)

class XiaohongshuPoster:
    """小红书发布器"""
    
    def __init__(self, personality_manager):
        self.pm = personality_manager
    
    async def test_connection(self):
        """测试MCP服务器连接"""
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    logging.info("MCP服务器连接成功!")
                    return True
        except Exception as e:
            logging.error(f"MCP服务器连接失败: {e}")
            return False
    
    async def publish_post(self, title, content):
        """发布内容到小红书"""
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    args = {
                        "title": title,
                        "content": content,
                        "images": [IMAGE_PATH] if os.path.exists(IMAGE_PATH) else []
                    }
                    
                    logging.info(f"正在发布到小红书...")
                    logging.info(f"标题: {title}")
                    logging.info(f"内容预览: {content[:100]}...")
                    
                    result = await session.call_tool("create_note", arguments=args)
                    
                    # 记录发布历史
                    post_record = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "title": title,
                        "content": content,
                        "result": str(result),
                        "success": True
                    }
                    
                    self.pm.posts["history"].append(post_record)
                    self.pm.save_json_file(POSTS_FILE, self.pm.posts)
                    
                    # 更新心理学成长：发帖是一种创作和社交经历
                    self.pm.growth_manager.update_post_experience(content)
                    
                    # 同时也是一种社交互动经历（positive feedback）
                    self.pm.growth_manager.process_new_experience(
                        "social_interaction", 
                        {"post_title": title, "content_length": len(content)},
                        0.3  # 轻微正面的情感效价，因为成功发布
                    )
                    
                    logging.info("发布成功! 心理成长已更新")
                    return result
                    
        except Exception as e:
            logging.error(f"发布失败: {e}")
            
            # 记录失败
            post_record = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "title": title,
                "content": content,
                "error": str(e),
                "success": False
            }
            
            self.pm.posts["history"].append(post_record)
            self.pm.save_json_file(POSTS_FILE, self.pm.posts)
            
            return None

class XiaohongshuAutomation:
    """小红书自动化主控制器"""
    
    def __init__(self):
        self.pm = PersonalityManager()
        self.news_collector = NewsCollector(self.pm)
        self.content_analyzer = ContentAnalyzer(self.pm)
        self.content_creator = ContentCreator(self.pm)
        self.poster = XiaohongshuPoster(self.pm)
    
    def collect_and_analyze_news(self):
        """收集并分析新闻"""
        logging.info("开始收集新闻...")
        news_data = self.news_collector.collect_daily_news()
        
        logging.info("开始分析新闻...")
        analysis = self.content_analyzer.analyze_news_with_personality(news_data)
        
        if analysis:
            logging.info("新闻分析完成")
            logging.info(f"分析结果: {analysis[:100]}...")
        
        return news_data, analysis
    
    async def create_and_publish_post(self):
        """创建并发布内容"""
        logging.info("开始生成发布内容...")
        
        # 测试连接
        if not await self.poster.test_connection():
            logging.error("无法连接MCP服务器，跳过发布")
            return
        
        # 生成内容
        title = self.content_creator.generate_title()
        content = self.content_creator.generate_post_content()
        
        if content:
            logging.info("内容生成成功，准备发布...")
            result = await self.poster.publish_post(title, content)
            
            if result:
                # 更新学习进度
                today = datetime.now().strftime("%Y-%m-%d")
                
                # 确保数据类型正确
                learning_progress = self.pm.personality.get("learning_progress", {})
                learning_progress["last_study_date"] = today
                
                current_days = learning_progress.get("total_days", 0)
                if isinstance(current_days, str):
                    try:
                        current_days = int(current_days)
                    except (ValueError, TypeError):
                        current_days = 0
                
                learning_progress["total_days"] = current_days + 1
                
                # 更新理解
                self.update_understandings()
                
                self.pm.save_all()
                logging.info("发布完成，数据已保存")
        else:
            logging.error("内容生成失败")
    
    def update_understandings(self):
        """更新对世界的理解"""
        # 基于最近的分析更新理解
        if self.pm.memories["daily_analysis"]:
            recent_analysis = self.pm.memories["daily_analysis"][-1]
            
            # 简单的理解更新逻辑
            self.pm.understandings["daily_observations"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "observation": recent_analysis.get("analysis", "")[:100]
            })
            
            # 只保留最近30条观察
            if len(self.pm.understandings["daily_observations"]) > 30:
                self.pm.understandings["daily_observations"] = self.pm.understandings["daily_observations"][-30:]
    
    def run_daily_cycle(self):
        """运行日常循环"""
        logging.info("=== 开始日常循环 ===")
        
        # 1. 收集和分析新闻（下午5点）
        self.collect_and_analyze_news()
        
        # 2. 延时1小时后发布内容（下午6点）
        # 在实际定时任务中，这个延时会通过调度器处理
        
    async def run_post_cycle(self):
        """运行发布循环"""
        logging.info("=== 开始发布循环 ===")
        await self.create_and_publish_post()

def setup_schedule(automation):
    """设置定时任务"""
    # 每天下午5点收集新闻
    schedule.every().day.at("17:00").do(automation.run_daily_cycle)
    
    # 每天下午6点发布内容
    schedule.every().day.at("18:00").do(lambda: asyncio.run(automation.run_post_cycle()))
    
    logging.info("定时任务设置完成")
    logging.info("每天17:00收集新闻，18:00发布内容")

async def manual_mode():
    """手动模式"""
    automation = XiaohongshuAutomation()
    
    while True:
        print("\n=== 程零九的小红书自动化系统 ===")
        print("1. 收集并分析新闻")
        print("2. 生成并发布内容")
        print("3. 查看人设状态")
        print("4. 运行完整日常循环")
        print("5. 测试MCP连接")
        print("6. 退出")
        
        choice = input("\n请选择操作 (1-6): ").strip()
        
        if choice == "1":
            automation.collect_and_analyze_news()
        elif choice == "2":
            await automation.create_and_publish_post()
        elif choice == "3":
            print(f"\n=== 程零九当前状态 ===")
            
            # 基本信息
            basic_info = automation.pm.personality.get("basic_info", {})
            print(f"姓名: {basic_info.get('name', '程零九')}")
            print(f"职业: {basic_info.get('job', '外星政府文化研究员')}")
            
            # 心理发展状态
            psych_summary = automation.pm.growth_manager.get_current_psychological_summary()
            print(f"\n【心理发展状态】")
            print(f"人格成熟度: {psych_summary.get('personality_maturity', 50):.1f}/100")
            print(f"情感智力: {psych_summary.get('emotional_intelligence', 50):.1f}/100")
            print(f"心理健康: {psych_summary.get('psychological_wellbeing', '发展中')}")
            print(f"成长轨迹: {psych_summary.get('growth_trajectory', '积极发展')}")
            print(f"新体验准备度: {psych_summary.get('readiness_for_new_experiences', 50):.1f}/100")
            
            # 大五人格特质
            big_five = automation.pm.personality.get("psychological_profile", {}).get("big_five_personality", {})
            if big_five:
                print(f"\n【大五人格特质】")
                print(f"开放性: {big_five.get('openness', 50):.1f}/100")
                print(f"尽责性: {big_five.get('conscientiousness', 50):.1f}/100") 
                print(f"外向性: {big_five.get('extraversion', 50):.1f}/100")
                print(f"宜人性: {big_five.get('agreeableness', 50):.1f}/100")
                print(f"神经质: {big_five.get('neuroticism', 50):.1f}/100")
            
            # 情感智力
            ei = automation.pm.personality.get("psychological_profile", {}).get("emotional_intelligence", {})
            if ei:
                print(f"\n【情感智力发展】")
                print(f"自我觉察: {ei.get('self_awareness', 50):.1f}/100")
                print(f"自我调节: {ei.get('self_regulation', 50):.1f}/100")
                print(f"社会觉察: {ei.get('social_awareness', 50):.1f}/100")
                print(f"关系管理: {ei.get('relationship_management', 50):.1f}/100")
                print(f"成长阶段: {ei.get('emotional_growth_stage', '未知')}")
            
            # 学习进度
            learning = automation.pm.personality.get("learning_progress", {})
            print(f"\n【学习活动统计】")
            print(f"总学习天数: {learning.get('total_days', 0)}")
            print(f"最后学习日期: {learning.get('last_study_date', '未知')}")
            print(f"收集新闻次数: {len(automation.pm.knowledge['daily_news'])}")
            print(f"发布次数: {len(automation.pm.posts['history'])}")
            print(f"分析记录: {len(automation.pm.memories['daily_analysis'])}")
            
            # 心理成长里程碑
            milestones = learning.get("psychological_milestones", [])
            if milestones:
                print(f"\n【心理成长里程碑】")
                for i, milestone in enumerate(milestones[-3:], 1):  # 显示最近3个
                    print(f"{i}. {milestone}")
                    
            print(f"\n程零九正在持续成长中... 🌱")
        elif choice == "4":
            automation.run_daily_cycle()
            await automation.run_post_cycle()
        elif choice == "5":
            if await automation.poster.test_connection():
                print("MCP连接正常")
            else:
                print("MCP连接失败")
        elif choice == "6":
            print("再见！111 110110000101111 111")
            break
        else:
            print("无效选择!")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        # 手动模式
        asyncio.run(manual_mode())
    elif len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        # 守护进程模式
        automation = XiaohongshuAutomation()
        setup_schedule(automation)
        
        logging.info("程零九的自动化系统启动中...")
        logging.info("等待定时任务执行...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    else:
        # 默认运行一次完整循环
        automation = XiaohongshuAutomation()
        
        # 先收集新闻
        automation.run_daily_cycle()
        
        # 然后发布内容
        asyncio.run(automation.run_post_cycle())

if __name__ == "__main__":
    print("程零九的小红书AI自动化系统")
    print("外星政府工作女孩的地球学习之旅")
    print()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户中断，程序退出! 111 110110000101111")
    except Exception as e:
        logging.error(f"程序异常: {e}")
        print(f"\n程序异常: {e}")