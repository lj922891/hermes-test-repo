#!/usr/bin/env python3
"""
创建GitHub仓库的简单脚本
"""

import os
import sys
import json

def main():
    print("=== 测试GitHub API ===")
    
    # 直接使用提供的令牌
    token = "YOUR_GITHUB_TOKEN_HERE"
    
    if not token:
        print("错误: 未提供令牌")
        return 1
    
    print(f"使用令牌长度: {len(token)}")
    
    # 测试API连接
    import urllib.request
    import urllib.error
    
    # 首先测试用户API
    print("\n1. 测试用户API...")
    try:
        req = urllib.request.Request(
            'https://api.github.com/user',
            headers={
                'Authorization': f'token {token}',
                'User-Agent': 'Hermes-Agent'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode())
            print(f"✅ 用户API测试成功")
            print(f"   用户名: {user_data.get('login')}")
            print(f"   用户ID: {user_data.get('id')}")
            print(f"   仓库URL: {user_data.get('repos_url')}")
    except urllib.error.HTTPError as e:
        print(f"❌ 用户API测试失败: {e.code} {e.reason}")
        print(f"   响应: {e.read().decode()}")
        return 1
    
    # 检查现有仓库
    print("\n2. 检查现有仓库...")
    try:
        req = urllib.request.Request(
            'https://api.github.com/user/repos',
            headers={
                'Authorization': f'token {token}',
                'User-Agent': 'Hermes-Agent'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            repos = json.loads(response.read().decode())
            print(f"   找到 {len(repos)} 个仓库")
            for repo in repos[:3]:
                print(f"   - {repo.get('name')} ({'私有' if repo.get('private') else '公开'})")
    except Exception as e:
        print(f"   检查仓库时出错: {e}")
    
    print("\n3. 创建新仓库...")
    repo_name = "hermes-test-repo"
    repo_data = {
        'name': repo_name,
        'description': '测试Hermes Agent的GitHub技能',
        'private': False,
        'auto_init': True  # 自动初始化README
    }
    
    try:
        import urllib.parse
        data = json.dumps(repo_data).encode('utf-8')
        
        req = urllib.request.Request(
            'https://api.github.com/user/repos',
            data=data,
            headers={
                'Authorization': f'token {token}',
                'User-Agent': 'Hermes-Agent',
                'Content-Type': 'application/json'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✅ 仓库创建成功!")
            print(f"   仓库名: {result.get('name')}")
            print(f"   完整名: {result.get('full_name')}")
            print(f"   URL: {result.get('html_url')}")
            print(f"   克隆URL: {result.get('clone_url')}")
            
            # 保存信息
            with open('github_repo_info.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("   仓库信息已保存到 github_repo_info.json")
            
            return 0
            
    except urllib.error.HTTPError as e:
        print(f"❌ 仓库创建失败: {e.code} {e.reason}")
        error_body = e.read().decode()
        print(f"   错误详情: {error_body}")
        
        # 检查是否仓库已存在
        if 'name already exists' in error_body.lower():
            print("   仓库可能已存在，尝试推送现有代码...")
            return 2
        return 1
    except Exception as e:
        print(f"❌ 创建仓库时出错: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())