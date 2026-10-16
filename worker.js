// CareSlot AI proxy — runs on Cloudflare Workers (free tier available).
// It keeps your Anthropic API key SECRET on the server so it never appears on your public website.
// Setup: see README.md → "Turn on AI answers".
export default {
  async fetch(req, env) {
    const cors = {
      'Access-Control-Allow-Origin': env.ALLOW_ORIGIN || '*',   // set to https://YOUR-USERNAME.github.io
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    };
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (req.method !== 'POST') return new Response('POST only', { status: 405, headers: cors });
    let body;
    try { body = await req.json(); } catch { return new Response('Bad JSON', { status: 400, headers: cors }); }
    const prompt = String(body.prompt || '').slice(0, 12000);
    if (!prompt) return new Response('Missing prompt', { status: 400, headers: cors });
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: env.MODEL || 'claude-haiku-5-5',   // check the model name in Anthropic's docs if this fails
        max_tokens: 400,
        messages: [{ role: 'user', content: prompt }]
      })
    });
    const d = await r.json();
    const text = (d.content || []).map(c => c.text || '').join('');
    return new Response(JSON.stringify({ result: text }), { status: r.ok ? 200 : 502, headers: { ...cors, 'content-type': 'application/json' } });
  }
};
