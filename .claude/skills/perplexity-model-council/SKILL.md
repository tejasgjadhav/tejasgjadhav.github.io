---
name: perplexity-model-council
description: |
  Query a council of Perplexity AI models for web-grounded, multi-perspective synthesized answers.
  Use when the user wants real-time web search + AI reasoning, asks to "ask perplexity", wants a
  multi-model AI council opinion, or needs current information beyond your training cutoff.
  Trigger phrases: "ask perplexity", "perplexity council", "model council", "what does perplexity say",
  "search and reason", "web-grounded answer", "/perplexity".
---

# Perplexity Model Council Skill

Query multiple Perplexity models in parallel, then synthesize a unified "council" answer with source citations.

## What This Skill Does

1. Takes the user's question (from `args` or the conversation)
2. Queries 3 Perplexity models in parallel: `sonar`, `sonar-pro`, and `sonar-reasoning`
3. Synthesizes a structured council verdict with citations

## Setup Check

Before querying, check if `PERPLEXITY_API_KEY` is available:

```bash
echo "${PERPLEXITY_API_KEY:0:10}..."
```

If empty, tell the user:
> "PERPLEXITY_API_KEY is not set. Please add it to your environment. You can get a key at https://www.perplexity.ai/settings/api — then set it in your session or add it to your shell profile as `export PERPLEXITY_API_KEY=pplx-...`"

Then stop.

## Querying the Council

Run all three model calls in parallel using Bash. Use this exact curl pattern for each:

```bash
curl -s https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_NAME",
    "messages": [
      {
        "role": "system",
        "content": "You are a precise, factual research assistant. Provide a thorough, well-cited answer. Include specific facts, numbers, and dates where relevant."
      },
      {
        "role": "user",
        "content": "QUESTION_HERE"
      }
    ],
    "max_tokens": 1024,
    "temperature": 0.2,
    "return_citations": true,
    "search_recency_filter": "month"
  }'
```

**Models to query (run in parallel):**
- `sonar` — Fast web search baseline
- `sonar-pro` — Deep research with more sources
- `sonar-reasoning` — Step-by-step reasoning over web results

**Important:** Escape the question properly for JSON. Use `jq -Rs '.'` or Python to safely encode it:
```bash
QUESTION_JSON=$(echo "QUESTION" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))")
```

## Parsing Responses

Extract the answer content from each response:
```bash
echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
content = data['choices'][0]['message']['content']
citations = data.get('citations', [])
print(content)
print('---CITATIONS---')
for i, c in enumerate(citations, 1):
    print(f'[{i}] {c}')
"
```

## Synthesizing the Council Verdict

After collecting all 3 responses, synthesize them yourself into a structured output:

```
## Perplexity Model Council — [Question Summary]

### Council Verdict
[1-3 paragraph synthesis of what all 3 models agreed on, with the most important findings first]

### Where Models Agreed
- [Point 1]
- [Point 2]

### Notable Differences / Nuances
- [Any divergent perspectives or additional context from specific models]

### Sources
[Deduplicated list of all citations from all 3 models, numbered]

---
*Council queried: sonar (fast search) · sonar-pro (deep research) · sonar-reasoning (step-by-step)*
*Search recency: last month | Queried: [current date]*
```

## Full Workflow

1. Extract the question from `args` or the most recent user message
2. Run setup check for `PERPLEXITY_API_KEY`
3. Show: "Convening Perplexity Model Council for: [question]..."
4. Run 3 parallel curl calls (save outputs to temp files or variables)
5. Parse each response
6. Synthesize and present the council verdict
7. If any model call fails (non-200), note it in the verdict and proceed with available responses

## Error Handling

- If a model returns an error, note "sonar-X was unavailable" in the verdict but still synthesize from remaining models
- If ALL models fail, show the error response and suggest checking the API key or Perplexity status
- Rate limit (429): wait 5s and retry once

## Example Usage

User: `/perplexity What are the latest developments in AI agents as of 2026?`

Args would be: `What are the latest developments in AI agents as of 2026?`
