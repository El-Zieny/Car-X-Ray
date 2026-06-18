#!/usr/bin/env python3
import os
import re

# Find all HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print(f"Found {len(html_files)} HTML files")

# Pattern to match old desktop button section
old_pattern = r'(<div class="right-nav flex gap-4">\s*<form[^>]*>[\s\S]*?</form>\s*)<div class="sign-buttons flex gap-2">\s*<a href="src/pages/login\.html"[\s\S]*?</div>\s*</div>'

new_replacement = r'''\1<div id="guestButtonsDesktop" class="sign-buttons flex gap-2">
          <a href="login.html"
            class="rounded-full border-white border px-6 py-2.25 
                            hover:bg-white hover:text-black">Sign In</a>
          <a href="signup.html"
            class="rounded-full bg-white text-black px-6 py-2.25 hover:bg-transparent hover:text-white hover:border-white border">Sign
            Up</a>
        </div>
        <div id="userButtonsDesktop" class="sign-buttons flex gap-2">
          <a href="#" id="userNameDesktop"
            class="rounded-full border-white border px-6 py-2.25 hover:bg-white hover:text-black">Hi, User</a>
          <a href="#" id="logoutBtnDesktop"
            class="rounded-full bg-white text-black px-6 py-2.25 hover:bg-transparent hover:text-white hover:border-white border">Logout</a>
        </div>
      </div>'''

updated_count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has the old pattern
    if 'sign-buttons flex gap-2' in content and 'userButtonsDesktop' not in content:
        print(f"\nUpdating {file}...")
        
        new_content = re.sub(old_pattern, new_replacement, content)
        
        if new_content != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✓ Updated successfully")
            updated_count += 1
        else:
            print(f"  ! Pattern not found in {file}")

print(f"\n✓ Updated {updated_count} files")
