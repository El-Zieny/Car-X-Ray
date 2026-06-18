#!/usr/bin/env python3
import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# Code to insert in head
auth_head_code = '''        <!-- Check auth immediately before page renders -->
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
    '''

print(f"Found {len(html_files)} HTML files\n")

updated_count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already updated
    if 'data-auth' in content:
        print(f"⏭  {file} - Already updated")
        continue
    
    # Find the </head> tag
    if '</head>' not in content:
        print(f"⚠  {file} - No </head> tag found")
        continue
    
    print(f"Updating {file}...")
    
    # Insert auth code before </head>
    new_content = content.replace('    </head>', auth_head_code)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Updated successfully\n")
    updated_count += 1

print(f"\n✓ Updated {updated_count} files")
