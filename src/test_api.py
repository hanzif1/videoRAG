#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from langchain_community.utilities import GoogleSerperAPIWrapper

def test_api():
    """测试API是否正常工作"""
    try:
        client = GoogleSerperAPIWrapper(
            serper_api_key='60702680d234a6f33ec41169acd2148ad497fa73',
            gl="cn",
            hhl="en",
            num=10
        )
        
        # 测试简单查询
        print("Testing simple query...")
        results = client.results("python programming")
        print(f"Results type: {type(results)}")
        print(f"Results keys: {results.keys() if isinstance(results, dict) else 'Not a dict'}")
        
        if 'organic' in results:
            print(f"Found {len(results['organic'])} organic results")
            for i, item in enumerate(results['organic'][:3]):
                print(f"  {i+1}. {item.get('title', 'No Title')}")
        
        return True
        
    except Exception as e:
        print(f"API Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Google Serper API...")
    success = test_api()
    if success:
        print("✓ API is working")
    else:
        print("✗ API has issues")


