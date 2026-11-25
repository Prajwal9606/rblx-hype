import { castFile } from '../blocky-studio/src/schema/cast';
import * as fs from 'fs';
const data = JSON.parse(fs.readFileSync('./data/cast.json', 'utf-8'));
console.log(JSON.stringify(castFile.safeParse(data), null, 2));
