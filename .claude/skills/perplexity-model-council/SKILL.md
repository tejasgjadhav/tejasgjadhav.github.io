---
name: perplexity-model-council
description: Query a council of Perplexity Sonar models free via Puter.com. No Perplexity API key needed. Trigger phrases: "ask perplexity", "perplexity council", "model council", "/perplexity".
---

# Perplexity Model Council via Puter.com

Query perplexity/sonar, perplexity/sonar-pro, and perplexity/sonar-reasoning-pro in parallel using Puter's free OpenAI-compatible API, then synthesize a council verdict.

## Step 1 — Check token
Run: echo "${PUTER_TOKEN:0:8}..."
If empty, tell user PUTER_TOKEN is missing from environment variables.

## Step 2 — Query all 3 models in parallel

Set QUESTION to the user's question, then:

```bash
TMPDIR=$(mktemp -d)

for MODEL in "perplexity/sonar" "perplexity/sonar-pro" "perplexity/sonar-reasoning-pro"; do
  SLUG=$(echo $MODEL | tr '/' '_')
  PAYLOAD=$(python3 -c "
import json,sys
print(json.dumps({
  'model': sys.argv[1],
  'messages': [
    {'role':'system','content':'You are a factual research assistant. Be thorough and cite sources.'},
    {'role':'user','content':sys.argv[2]}
  ],
  'max_tokens': 1024,
  'temperature': 0.2
}))
" "$MODEL" "$QUESTION")
  
  curl -s https://api.puter.com/puterai/openai/v1/chat/completions \
    -H "Authorization: Bearer $PUTER_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" > "$TMPDIR/${SLUG}.json" &
done
wait
```

## Step 3 — Parse responses

```bash
for F in "$TMPDIR"/*.json; do
  MODEL=$(basename $F .json | tr '_' '/')
  echo "=== $MODEL ==="
  python3 -c "
import json,sys
d=json.load(sys.stdin)
if 'choices' in d:
    print(d['choices'][0]['message']['content'])
else:
    print('ERROR:', d.get('error', d))
" < "$F"
  echo
done
```

## Step 4 — Synthesize council verdict

After collecting all responses, present:

## Perplexity Model Council — [topic]

### Council Verdict
[2-3 paragraph synthesis of what all 3 models found]

### Where Models Agreed
- [key point 1]
- [key point 2]

### Nuances
- [any differences]

### Sources
[citations mentioned across responses]

---
*sonar · sonar-pro · sonar-reasoning-pro via Puter.com · free, no Perplexity key*
