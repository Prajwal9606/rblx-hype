const { z } = require('zod');
const fs = require('fs');

const hex = z.string().regex(/^#[0-9a-fA-F]{6}$/, 'expected a #rrggbb colour');
const HAIR_STYLES = ["sidePart", "bob", "long", "ponytail", "tufts", "bun", "curly", "spikyTop", "hypeSpiky", "bald", "beanie", "rainHat"];
const BODY_TYPES = ["blocky", "boy", "girl", "man", "woman", "r20", "superhero"];

const torso = z.discriminatedUnion('kind', [
  z.object({ kind: z.literal('plain'), color: hex }).strict(),
  z.object({ kind: z.literal('varsity'), color: hex, strip: hex, trim: hex.optional() }).strict(),
  z.object({ kind: z.literal('stripes'), color: hex, color2: hex, bands: z.number().int().min(2).max(12).optional() }).strict(),
  z.object({ kind: z.literal('plaid'), color: hex, color2: hex }).strict(),
  z.object({ kind: z.literal('coat'), color: hex, trim: hex }).strict(),
  z.object({ kind: z.literal('cyberHoodie'), color: hex, accent: hex, trim: hex.optional() }).strict(),
]);

const characterDef = z.object({
  skin: hex,
  body: z.enum(BODY_TYPES).optional(),
  faceStyle: z.enum(["roblox", "drawn"]).optional(),
  faceFile: z.string().optional(),
  eyeColor: hex.optional(),
  hair: z.object({ style: z.enum(HAIR_STYLES), color: hex }).strict(),
  headphones: z.object({ color: hex, glow: hex }).strict().optional(),
  outfit: z.object({
    torso,
    sleeves: z.object({ color: hex, length: z.number().min(0).max(1).optional(), cuff: hex.optional(), accent: hex.optional(), gloves: hex.optional() }).strict().optional(),
    legs: z.object({ color: hex, length: z.number().min(0).max(1).optional(), shoes: hex.optional(), shoeAccent: hex.optional() }).strict(),
  }).strict(),
}).strict();

const castFile = z.record(z.string().regex(/^[a-z][a-zA-Z0-9_]*$/), characterDef);

const data = JSON.parse(fs.readFileSync('./data/cast.json','utf-8'));
const result = castFile.safeParse(data);
console.log(JSON.stringify(result, null, 2));
