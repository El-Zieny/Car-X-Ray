const fs = require('fs');
const path = require('path');

// Pattern to find the old desktop buttons
const oldPattern = /<div class="sign-buttons flex gap-2">\s*<a href="(src\/pages\/)?login\.html"[\s\S]*?<\/div>\s*<\/div>\s*<\/nav>/;

const newButtons = `<div id="guestButtonsDesktop" class="sign-buttons flex gap-2">
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
      </div>
    </nav>`;

// Get all HTML files
const files = fs.readdirSync('.');
const htmlFiles = files.filter(file => file.endsWith('.html'));

console.log(`Found ${htmlFiles.length} HTML files to update`);

htmlFiles.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  
  // Check if file has the old button pattern
  if (content.includes('Sign In') && content.includes('Sign Up') && !content.includes('userButtonsDesktop')) {
    console.log(`\nUpdating ${file}...`);
    
    // Replace the old desktop buttons with new ones
    // Find the section with the old buttons
    const desktopNavMatch = content.match(/<div class="right-nav flex gap-4">[\s\S]*?<div class="sign-buttons flex gap-2">[\s\S]*?<\/div>\s*<\/div>\s*<\/nav>/);
    
    if (desktopNavMatch) {
      console.log(`  - Found desktop nav section`);
      
      const oldSection = desktopNavMatch[0];
      // Extract the form part
      const formMatch = oldSection.match(/<form[\s\S]*?<\/form>/);
      const form = formMatch ? formMatch[0] : '';
      
      const newSection = `<div class="right-nav flex gap-4">
        ${form}
        ${newButtons}`;
      
      content = content.replace(oldSection, newSection);
      
      // Write back to file
      fs.writeFileSync(file, content, 'utf8');
      console.log(`  ✓ Updated successfully`);
    } else {
      console.log(`  ! Could not find exact pattern in ${file}`);
    }
  }
});

console.log('\n✓ Update complete!');
