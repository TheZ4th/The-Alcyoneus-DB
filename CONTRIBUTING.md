# Contributing to The Alcyoneus DB

Thanks for your interest in making `Alcyoneus DB` the most comprehensive OSINT database! 🗿

We don't just collect data. We exceed every limit.

## How You Can Help

### 1. Add a New Platform

The easiest way to contribute is by adding a new platform to `data/platform.json`.

**Structure:**
```json
{
  "name": "platform_name",
  "display_name": "Platform Display Name",
  "url_pattern": "https://example.com/{}",
  "api_pattern": "https://example.com/{}" [Opsional],
  "category": "social_media",
  "subcategory": "social_network",
  "region": "global",
  "priority": 2,
  "method": "GET",
  "requires_auth": false,
  "verified": false,
  "confidence": 70,
  "notes": "Short description",
  "tags":  ["social", "meta", "network"]
}
```

Guidelines:

· name: use lowercase, underscores for spaces (my_platform)
· url_pattern: use {} as placeholder for username
· category: pick from existing (social_media, forum, coding, dark_web, etc.)
· region: global, asia_pacific, europe, north_america, dark
· verified: set false unless you've personally tested it
· confidence: 0-100 (start with 50-70 for unverified)

2. Update Existing Platform

Found a broken URL? A platform changed its domain? Open an issue or submit a PR.

3. Improve the Validator

core/validator.py is the brain. If you know how to reduce false positives, your help is gold.

4. Fix Bugs or Add Features

Check the Issues tab. Or propose a new feature.

Pull Request Process

1. Fork the repo.
2. Create a new branch (git checkout -b feature/amazing-feature).
3. Make your changes.
4. Test your changes.
5. Commit (git commit -m 'Add some amazing feature').
6. Push (git push origin feature/amazing-feature).
7. Open a Pull Request.

Style Guide

· Python: Follow PEP 8.
· JSON: Use 2-space indentation.
· Data: Keep alphabetical order when possible.

If you are interested to joining my community to just ask questions, develop Alcyoneus DB Or anything about Cyber,
you can copy this link https://discord.gg/cAhfsGxJJ to join my community

Disclaimer

This tool is for educational purposes. Use responsibly.
