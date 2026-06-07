import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// INIT_CWD is the path where the user executed "npm install"
const projectRoot = process.env.INIT_CWD;

if (projectRoot) {
  const sourceDoc = path.resolve(__dirname, '../AGENT-doc.md');
  const targetDoc = path.join(projectRoot, 'AGENT-doc.md');

  // Avoid overwriting existing documentation if they already customized it
  if (!fs.existsSync(targetDoc)) {
    try {
      fs.copyFileSync(sourceDoc, targetDoc);
      console.log('SwifttAuth-Fire: Created AGENT-doc.md in your project root.');
    } catch (err) {
      console.warn('SwifttAuth-Fire: Failed to write AGENT-doc.md:', err.message);
    }
  }
}
