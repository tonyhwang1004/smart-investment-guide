#!/usr/bin/env python3
import os
import json
import random
from datetime import datetime
from openai import OpenAI
from pathlib import Path

class SmartInvestmentBlogGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.topics = [
            {"title": "주식투자 기초 완벽 가이드", "category": "stocks", "keywords": ["주식투자", "주식 기초", "투자 시작"]},
            {"title": "부동산투자 시작하기", "category": "realestate", "keywords": ["부동산투자", "부동산", "투자"]},  
            {"title": "재테크 초보자 가이드", "category": "finance", "keywords": ["재테크", "자산관리", "돈관리"]},
            {"title": "암호화폐 투자 기초", "category": "alternative", "keywords": ["암호화폐", "비트코인", "코인투자"]},
            {"title": "ETF 투자 완벽 가이드", "category": "stocks", "keywords": ["ETF", "인덱스펀드", "분산투자"]},
            {"title": "배당주 투자 전략", "category": "stocks", "keywords": ["배당주", "배당투자", "수익형투자"]}
        ]
    
    def check_daily_limit(self):
        """하루 1회 포스팅 제한"""
        today = datetime.now().strftime("%Y-%m-%d")
        posts_dir = Path("_posts")
        if not posts_dir.exists():
            posts_dir.mkdir()
            return True
        return not any(posts_dir.glob(f"{today}-*.md"))
    
    def generate_content(self, topic):
        """GPT-4로 콘텐츠 생성"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "user", 
                    "content": f"""'{topic['title']}'에 대한 전문적인 투자 가이드를 작성해주세요.

요구사항:
- 길이: 2,500-3,500단어
- 구조: 체계적인 목차 (## H2, ### H3 사용)
- 내용: 실용적이고 구체적인 투자 방법
- 톤: 전문적이면서 이해하기 쉽게
- 주의사항: 투자 리스크와 주의사항 포함

마크다운 형식으로 작성하되, front matter는 제외하고 본문만 작성해주세요."""
                }],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"GPT-4 오류: {e}")
            return None
    
    def save_post(self, topic, content):
        """포스트 저장"""
        today = datetime.now()
        filename = f"{today.strftime('%Y-%m-%d')}-{topic['category']}-guide.md"
        
        front_matter = f"""---
layout: post
title: "{topic['title']}"
date: {today.strftime('%Y-%m-%d %H:%M:%S +0900')}
categories: [{topic['category']}]
tags: {topic['keywords']}
description: "{topic['title']} - 전문가가 알려주는 실전 투자 전략과 방법을 상세히 안내합니다."
---

"""
        
        disclaimer = """

---

## ⚠️ 투자 유의사항

**면책조항**: 본 글의 정보는 교육 목적으로만 제공되며, 투자 권유가 아닙니다. 모든 투자에는 원금 손실 위험이 있으므로 신중한 판단이 필요합니다.

**투자 상담**: 금융감독원 투자자보호센터 1332 | 한국거래소 krx.co.kr
"""
        
        full_content = front_matter + content + disclaimer
        
        posts_dir = Path("_posts")
        posts_dir.mkdir(exist_ok=True)
        
        with open(f"_posts/{filename}", 'w', encoding='utf-8') as f:
            f.write(full_content)
            
        return filename
    
    def run(self):
        """메인 실행"""
        print("🚀 스마트 투자 가이드 - 자동 포스트 생성 시작!")
        
        if not self.check_daily_limit():
            print("✋ 오늘은 이미 포스트가 생성되었습니다.")
            return False
            
        topic = random.choice(self.topics)
        print(f"📋 선택된 주제: {topic['title']}")
        
        content = self.generate_content(topic)
        
        if content:
            filename = self.save_post(topic, content)
            print(f"✅ 포스트 생성 완료: {filename}")
            return True
        else:
            print("❌ 콘텐츠 생성 실패")
            return False

if __name__ == "__main__":
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY 환경변수가 필요합니다!")
    else:
        generator = SmartInvestmentBlogGenerator()
        generator.run()
