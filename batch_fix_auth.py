#!/usr/bin/env python3
import os

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])

auth_code = '''
    <!-- Check auth immediately before page renders -->
    <script>
        (function() {
            const token = localStorage.getItem("jwt");
            if (token) {
                document.documentElement.setAttribute("data-auth", "user");
            } else {
                document.documentElement.setAttribute("data-auth", "guest");
            }
        })();
    </script>
    
    <style>
        /* Hide guest buttons if authenticated */
        [data-auth="user"] #guestButtons,
        [data-auth="user"] #guestButtonsDesktop {
            display: none !important;
        }
        
        /* Hide user buttons if not authenticated */
        [data-auth="guest"] #userButtons,
        [data-auth="guest"] #userButtonsDesktop {
            display: none !important;
        }
    </style>
  </head>'''

print(f"Found {len(html_files)} HTML files\n")

files_with_auth = 0
files_needing_fix = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file already has auth code
    if 'data-auth' in content:
        print(f"✓ {file}")
        files_with_auth += 1
        continue
    
    # File needs fixing
    print(f"FIXING: {file}")
    files_needing_fix += 1
    
    # Replace closing </head> with auth code + closing head
    # Handle both inline and separate line cases
    if '  </head>' in content:
        new_content = content.replace('  </head>', auth_code)
    elif '</head>' in content:
        new_content = content.replace('</head>', auth_code)
    else:
        print(f"  ⚠ WARNING: No </head> tag found!")
        continue
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"\n✓ Already had auth: {files_with_auth}")
print(f"✓ Fixed: {files_needing_fix}")
print(f"✓ Total: {len(html_files)}")
