#!/usr/bin/env python3
import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

auth_code = '''    <!-- Check auth immediately before page renders -->
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

print(f"Checking {len(html_files)} HTML files\n")

files_needing_fix = []
fixed_count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has auth code
    if 'data-auth' in content:
        print(f"✓ {file} - Has auth code")
        continue
    
    print(f"✗ {file} - MISSING AUTH CODE")
    files_needing_fix.append(file)

print(f"\nFound {len(files_needing_fix)} files needing fix:\n")

for file in files_needing_fix:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Fixing {file}...")
    
    # Replace any </head> tag with full auth code + closing head
    # This handles both inline (</head> on same line) and separate line cases
    new_content = re.sub(
        r'</head>',
        auth_code,
        content,
        count=1
    )
    
    # If the replacement didn't work, try a different pattern
    if new_content == content:
        # Look for the pattern where </head> is on the same line as other content
        new_content = re.sub(
            r'\s*</head>',
            '\n' + auth_code,
            content,
            count=1
        )
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ Fixed\n")
        fixed_count += 1
    else:
        print(f"  ⚠ Could not fix - no </head> tag found\n")

print(f"✓ Fixed {fixed_count} files")
