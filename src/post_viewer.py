# src/post_viewer.py

import json
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def generate_html_preview(posts_file: str = "generated_posts.json"):
    """Generate a beautiful HTML preview of all generated posts"""
    
    posts_path = Path(__file__).parent.parent / posts_file
    
    if not posts_path.exists():
        print(f"❌ {posts_file} not found!")
        return
    
    with open(posts_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Posts Preview</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }
        .post-card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .post-header {
            border-bottom: 2px solid #eee;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }
        .post-title {
            font-size: 20px;
            font-weight: 600;
            color: #1a1a1a;
        }
        .post-id {
            font-size: 12px;
            color: #999;
            margin-top: 4px;
        }
        .platform-content {
            margin-bottom: 20px;
            padding: 16px;
            border-left: 4px solid;
            border-radius: 4px;
        }
        .platform-content.linkedin {
            background: #f3f6ff;
            border-color: #0a66c2;
        }
        .platform-content.x {
            background: #f0f9ff;
            border-color: #1da1f2;
        }
        .platform-content.facebook {
            background: #f0f4ff;
            border-color: #1877f2;
        }
        .platform-content.instagram {
            background: #fff5f7;
            border-color: #e1306c;
        }
        .platform-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .platform-badge.linkedin { background: #0a66c2; color: white; }
        .platform-badge.x { background: #1da1f2; color: white; }
        .platform-badge.facebook { background: #1877f2; color: white; }
        .platform-badge.instagram { background: #e1306c; color: white; }
        
        .content-text {
            white-space: pre-wrap;
            color: #333;
            font-size: 14px;
        }
        .status-error {
            background: #fee;
            border-color: #d00;
            color: #900;
        }
        .char-count {
            font-size: 11px;
            color: #999;
            margin-top: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Social Media Posts Preview</h1>
"""
    
    for post in data['posts']:
        html += f"""
        <div class="post-card">
            <div class="post-header">
                <div class="post-title">{post['source_page']}</div>
                <div class="post-id">Proposal ID: {post['proposal_id']}</div>
            </div>
"""
        
        for platform, content_data in post['platforms'].items():
            status = content_data.get('status', 'unknown')
            
            if status == 'generated':
                content = content_data.get('content', 'No content')
                char_count = len(content)
                
                html += f"""
            <div class="platform-content {platform}">
                <span class="platform-badge {platform}">{platform}</span>
                <div class="content-text">{content}</div>
                <div class="char-count">{char_count} characters</div>
            </div>
"""
            elif status == 'error':
                error = content_data.get('error', 'Unknown error')
                html += f"""
            <div class="platform-content status-error">
                <span class="platform-badge {platform}">{platform}</span>
                <div class="content-text">❌ Error: {error}</div>
            </div>
"""
        
        html += """
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    # Save HTML
    output_path = Path(__file__).parent.parent / "posts_preview.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Preview generated: posts_preview.html")
    print(f"📂 Open in browser: file://{output_path.absolute()}")
    
    return output_path


if __name__ == "__main__":
    generate_html_preview()
