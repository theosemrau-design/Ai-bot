# AI-Bot

> [Caution]
> For this ai you need to install uv with:
```bash
[sudo] apt install uv
```
You need to purchase an openrouter api key and add a .env file with the format.
```python
OPENROUTER_API_KEY=<your key>
```
Activate the env with:
```bash
source .venv/bin/activate
```
Then run the file with uv and use --verbose to get a more detailed output:
```bash
uv run main.py <prompt> [--verbose]
```
> [Tip]
> When the ai doesn't do what you want go in the prompts file and edit the system prompt