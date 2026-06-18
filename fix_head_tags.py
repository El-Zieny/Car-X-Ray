#!/usr/bin/env python3
import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print(f"Found {len(html_files)} HTML files\n")

fixed_count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if </head> is missing (but has </style> before <body>)
    if '</head>' not in content and '</style>' in content and '<body' in content:
        print(f"Fixing {file}...")
        
        # Find </style> and add </head> after it
        new_content = content.replace('        </style>\n    \n    <body', '        </style>\n    </head>\n    <body')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✓ Fixed successfully\n")
        fixed_count += 1
    else:
        print(f"⏭  {file} - Already has closing </head>\n")

print(f"✓ Fixed {fixed_count} files")
